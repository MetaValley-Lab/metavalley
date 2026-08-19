from uuid import UUID

from app.core.supabase import supabase

from app.services.canvas_zone_service import CanvasZoneService
from app.services.planning_item_service import PlanningItemService
from app.services.product_service import ProductService
from app.services.startup_service import StartupService
from app.services.user_service import UserService



# ─────────────────────────────────────────────────────────────
# ACTION SERVICE — executa as ações emitidas pelos agentes
# ─────────────────────────────────────────────────────────────
class ActionService:
    """
    Executa as actions emitidas pelos agentes no banco de dados.
    Usa os services existentes do projeto — sem acesso direto ao Supabase,
    exceto em _update_canvas_zone (upsert por zone_key não existe no CanvasZoneService).
    """
 
    def __init__(
        self,
        startup_service: StartupService,
        canvas_service: CanvasZoneService,
        planning_service: PlanningItemService,
        product_service: ProductService,
        user_service: UserService,
    ):
        self.startup_service = startup_service
        self.canvas_service = canvas_service
        self.planning_service = planning_service
        self.product_service = product_service
        self.user_service = user_service
 
    async def execute(
        self,
        action: dict,
        startup_id: UUID,
        user_id: UUID,
        agent_name: str,
    ) -> dict:
        """Despacha a action para o handler correto."""
        action_type = action.get("type")
 
        handlers = {
            "update_startup":              self._update_startup,
            "update_canvas_zone":          self._update_canvas_zone,
            "add_planning_item":           self._add_planning_item,
            "modify_planning_item":        self._modify_planning_item,
            "suggest_complete":            self._suggest_complete,
            "create_product":              self._create_product,
            "update_product":              self._update_product,
            "confirm_onboarding_complete": self._confirm_onboarding,
        }
 
        handler = handlers.get(action_type) # type: ignore
        if not handler:
            return {"ok": False, "error": f"action_type desconhecida: {action_type}"}
 
        try:
            return await handler(action, startup_id, user_id, agent_name)
        except Exception as e:
            return {"ok": False, "error": str(e)}
 
    async def _update_startup(self, action, startup_id, user_id, agent_name) -> dict:
        from app.schemas.startup_schema import StartupUpdate
 
        field = action.get("field")
        value = action.get("value")
 
        allowed = {
            "name", "description", "problem", "solution", "segment",
            "target_location", "stage", "primary_revenue_model", "revenue_model_details",
        }
 
        if field not in allowed:
            return {"ok": False, "error": f"campo não permitido: {field}"}
 
        update_payload = StartupUpdate(**{field: value})
        await self.startup_service.update_startup(str(startup_id), str(user_id), update_payload)
 
        return {"ok": True, "field": field, "value": value}
 
    async def _update_canvas_zone(self, action, startup_id, user_id, agent_name) -> dict:
        """
        Upsert por zone_key + startup_id.
        O CanvasZoneService atualiza por zone_id — por isso usamos supabase direto aqui,
        que é o mesmo padrão usado em todos os outros services do projeto.
        """
        zone_key = action.get("zone")
        content = action.get("content", "")
        status = action.get("status", "in_progress")
        filled_by = action.get("filled_by", agent_name)
 
        # Verifica se já existe
        existing = (
            supabase.table("canvas_zones")
            .select("id, content")
            .eq("startup_id", str(startup_id))
            .eq("zone_key", zone_key)
            .execute()
        )
 
        # CORREÇÃO AQUI: Garante ao Pylance que 'data' é uma lista populada e válida
        if existing.data and isinstance(existing.data, list) and len(existing.data) > 0:
            primeiro_registro = existing.data[0]
            
            # Garante que o item de dentro da lista é de fato um dicionário
            if isinstance(primeiro_registro, dict):
                zone_id = primeiro_registro["id"]
                current_content = primeiro_registro.get("content")
     
                update_data: dict = {
                    "content": content,
                    "status": status,
                    "filled_by": filled_by,
                }
                # Preserva conteúdo anterior se mudou
                if content != current_content:
                    update_data["previous_content"] = current_content
     
                supabase.table("canvas_zones").update(update_data).eq("id", zone_id).execute()
            else:
                return {"ok": False, "error": "Formato de dados retornado do banco é inválido."}
        else:
            supabase.table("canvas_zones").insert({
                "startup_id": str(startup_id),
                "zone_key": zone_key,
                "content": content,
                "status": status,
                "filled_by": filled_by,
            }).execute()
 
        return {"ok": True, "zone": zone_key}
 
    async def _add_planning_item(self, action, startup_id, user_id, agent_name) -> dict:
        from app.schemas.planning_item_schema import PlanningItemCreate, ActorRole
 
        suggested_by = action.get("suggested_by", agent_name)
        try:
            actor = ActorRole(suggested_by)
        except ValueError:
            actor = ActorRole.FOUNDER
 
        payload = PlanningItemCreate(
            startup_id=startup_id,
            content=action.get("content"),
            created_by=actor,
        )
 
        result = await self.planning_service.create_item(
            user_id=str(user_id),
            payload=payload,
        )
 
        return {"ok": True, "item_id": result.get("id")}
 
    async def _modify_planning_item(self, action, startup_id, user_id, agent_name) -> dict:
        from app.schemas.planning_item_schema import PlanningItemUpdate, ActorRole
 
        item_id = action.get("item_id")
        if not item_id:
            return {"ok": False, "error": "item_id não fornecido"}
 
        updated_by = action.get("updated_by", agent_name)
        try:
            actor = ActorRole(updated_by)
        except ValueError:
            actor = ActorRole.FOUNDER
 
        payload = PlanningItemUpdate(
            content=action.get("content"),
            updated_by=actor,
        )
 
        result = await self.planning_service.update_item(
            item_id=item_id,
            user_id=str(user_id),
            payload=payload,
        )
 
        if not result:
            return {"ok": False, "error": "Planning item não encontrado"}
 
        return {"ok": True, "item_id": item_id}
 
    async def _suggest_complete(self, action, startup_id, user_id, agent_name) -> dict:
        # Não modifica o banco — emite evento para o frontend mostrar confirmação ao founder
        return {
            "ok": True,
            "item_id": action.get("item_id"),
            "frontend_event": "show_complete_confirmation",
        }
 
    async def _create_product(self, action, startup_id, user_id, agent_name) -> dict:
        from app.schemas.product_schema import ProductCreate, ProductType, ProductStage, ProductActorRole
 
        try:
            product_type = ProductType(action.get("product_type", "other"))
        except ValueError:
            product_type = ProductType.OTHER
 
        try:
            stage = ProductStage(action.get("stage", "idea"))
        except ValueError:
            stage = ProductStage.IDEA
 
        payload = ProductCreate(
            startup_id=startup_id,
            name=action.get("name"),
            description=action.get("description"),
            type=product_type,
            price=action.get("price"),
            stage=stage,
            last_updated_by=ProductActorRole.CTO,
        )
 
        result = await self.product_service.create_product(
            user_id=str(user_id),
            payload=payload,
        )
 
        return {"ok": True, "product_id": result.get("id")}
 
    async def _update_product(self, action, startup_id, user_id, agent_name) -> dict:
        from app.schemas.product_schema import ProductUpdate, ProductType, ProductStage
 
        product_id = action.get("product_id")
        if not product_id:
            return {"ok": False, "error": "product_id não fornecido"}
 
        update_data: dict = {}
 
        if action.get("name"):
            update_data["name"] = action["name"]
        if action.get("description"):
            update_data["description"] = action["description"]
        if action.get("product_type"):
            try:
                update_data["type"] = ProductType(action["product_type"])
            except ValueError:
                pass
        if action.get("price") is not None:
            update_data["price"] = action["price"]
        if action.get("stage"):
            try:
                update_data["stage"] = ProductStage(action["stage"])
            except ValueError:
                pass
 
        if not update_data:
            return {"ok": False, "error": "Nenhum campo válido para atualizar"}
 
        payload = ProductUpdate(**update_data)
        result = await self.product_service.update_product(
            product_id=product_id,
            user_id=str(user_id),
            payload=payload,
        )
 
        if not result:
            return {"ok": False, "error": "Produto não encontrado"}
 
        return {"ok": True, "product_id": product_id}
 
    async def _confirm_onboarding(self, action, startup_id, user_id, agent_name) -> dict:
        await self.user_service.complete_onboarding(str(user_id))
        return {"ok": True, "frontend_event": "redirect_to_board"}

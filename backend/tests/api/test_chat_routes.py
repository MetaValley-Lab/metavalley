import json
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

from app.api.dependencies import get_current_user
from app.main import app


USER_UUID = "22222222-2222-2222-2222-222222222222"
STARTUP_UUID = "11111111-1111-1111-1111-111111111111"
CONVERSATION_UUID = "55555555-5555-5555-5555-555555555555"
PLANNING_ITEM_UUID = "44444444-4444-4444-4444-444444444444"


@pytest.fixture
def mock_authenticated_user():
    """Sobrescreve get_current_user para simular usuário autenticado."""
    fake_user = SimpleNamespace(
        id=USER_UUID,
        email="logged_user@example.com"
    )

    app.dependency_overrides[get_current_user] = lambda: fake_user

    yield fake_user

    app.dependency_overrides.clear()


@pytest.fixture
def mock_message_group():
    """Mensagem do grupo retornada pelo banco."""
    return {
        "id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
        "conversation_id": CONVERSATION_UUID,
        "role": "user",
        "agent_name": None,
        "content": "Qual é minha estratégia de go-to-market?",
        "actions": None,
        "created_at": "2026-08-19T10:00:00Z",
    }


@pytest.fixture
def mock_message_agent():
    """Mensagem de agente retornada pelo banco."""
    return {
        "id": "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb",
        "conversation_id": CONVERSATION_UUID,
        "role": "agent",
        "agent_name": "ceo",
        "content": "Foque em canais orgânicos no estágio inicial.",
        "actions": [{"type": "add_planning_item", "content": "Validar canal orgânico"}],
        "created_at": "2026-08-19T10:00:05Z",
    }


@pytest.fixture
def mock_conversation():
    """Conversa retornada pelo banco."""
    return {
        "id": CONVERSATION_UUID,
        "startup_id": STARTUP_UUID,
        "type": "group",
        "created_at": "2026-08-19T10:00:00Z",
    }


def parse_sse_events(response_content: bytes) -> list[dict]:
    """Extrai e parseia eventos do formato SSE."""
    events = []
    for line in response_content.decode().split("\n"):
        line = line.strip()
        if line.startswith("data: "):
            try:
                events.append(json.loads(line[6:]))
            except json.JSONDecodeError:
                pass
    return events


# ─── POST /chat/message — SSE ──────────────────────────────────────────────────

def test_send_message_retorna_content_type_sse(
    client: TestClient,
    monkeypatch,
    mock_authenticated_user,
):
    """O endpoint deve retornar Content-Type text/event-stream."""

    async def fake_process(**kwargs):
        yield {"event": "turn_complete"}

    monkeypatch.setattr(
        "app.api.chat.board_service.process_group_message",
        fake_process,
    )

    response = client.post(
        "/chat/message",
        json={"startup_id": STARTUP_UUID, "message": "Olá board!"},
    )

    assert response.status_code == 200
    assert "text/event-stream" in response.headers["content-type"]


def test_send_message_sequencia_eventos(
    client: TestClient,
    monkeypatch,
    mock_authenticated_user,
):
    """
    Sequência correta: agent_start → agent_message → turn_complete.
    """

    async def fake_process(**kwargs):
        yield {"event": "agent_start", "agent": "ceo"}
        yield {
            "event": "agent_message",
            "agent": "ceo",
            "content": "Foque no canal com menor CAC primeiro.",
            "options": [],
        }
        yield {"event": "turn_complete"}

    monkeypatch.setattr(
        "app.api.chat.board_service.process_group_message",
        fake_process,
    )

    response = client.post(
        "/chat/message",
        json={"startup_id": STARTUP_UUID, "message": "Qual canal devo priorizar?"},
    )

    events = parse_sse_events(response.content)

    assert len(events) == 3
    assert events[0] == {"event": "agent_start", "agent": "ceo"}
    assert events[1]["event"] == "agent_message"
    assert events[1]["content"] == "Foque no canal com menor CAC primeiro."
    assert events[2] == {"event": "turn_complete"}


def test_send_message_multiplos_agentes(
    client: TestClient,
    monkeypatch,
    mock_authenticated_user,
):
    """Múltiplos agentes respondem em sequência, cada um com seu agent_start."""

    async def fake_process(**kwargs):
        yield {"event": "agent_start", "agent": "ceo"}
        yield {"event": "agent_message", "agent": "ceo", "content": "Visão estratégica.", "options": []}
        yield {"event": "agent_start", "agent": "cfo"}
        yield {"event": "agent_message", "agent": "cfo", "content": "Cuidado com o burn rate.", "options": []}
        yield {"event": "turn_complete"}

    monkeypatch.setattr(
        "app.api.chat.board_service.process_group_message",
        fake_process,
    )

    response = client.post(
        "/chat/message",
        json={"startup_id": STARTUP_UUID, "message": "Qual meu custo ideal de aquisição?"},
    )

    events = parse_sse_events(response.content)

    agent_starts = [e for e in events if e["event"] == "agent_start"]
    agent_messages = [e for e in events if e["event"] == "agent_message"]

    assert len(agent_starts) == 2
    assert len(agent_messages) == 2
    assert agent_starts[0]["agent"] == "ceo"
    assert agent_starts[1]["agent"] == "cfo"
    assert events[-1]["event"] == "turn_complete"


def test_send_message_action_update_canvas(
    client: TestClient,
    monkeypatch,
    mock_authenticated_user,
):
    """action_executed deve ser emitido quando um agente atualiza o canvas."""

    async def fake_process(**kwargs):
        yield {"event": "agent_start", "agent": "ceo"}
        yield {"event": "agent_message", "agent": "ceo", "content": "Atualizei sua proposta de valor.", "options": []}
        yield {"event": "action_executed", "action_type": "update_canvas_zone", "zone": "value_proposition"}
        yield {"event": "turn_complete"}

    monkeypatch.setattr(
        "app.api.chat.board_service.process_group_message",
        fake_process,
    )

    response = client.post(
        "/chat/message",
        json={"startup_id": STARTUP_UUID, "message": "Qual é minha proposta de valor?"},
    )

    events = parse_sse_events(response.content)

    action_events = [e for e in events if e["event"] == "action_executed"]

    assert len(action_events) == 1
    assert action_events[0]["action_type"] == "update_canvas_zone"
    assert action_events[0]["zone"] == "value_proposition"


def test_send_message_action_add_planning_item(
    client: TestClient,
    monkeypatch,
    mock_authenticated_user,
):
    """action_executed deve conter o item_id quando um planning item é criado."""

    async def fake_process(**kwargs):
        yield {"event": "agent_start", "agent": "cmo"}
        yield {"event": "agent_message", "agent": "cmo", "content": "Crie a landing page esta semana.", "options": []}
        yield {"event": "action_executed", "action_type": "add_planning_item", "item_id": PLANNING_ITEM_UUID}
        yield {"event": "turn_complete"}

    monkeypatch.setattr(
        "app.api.chat.board_service.process_group_message",
        fake_process,
    )

    response = client.post(
        "/chat/message",
        json={"startup_id": STARTUP_UUID, "message": "Como começo o marketing?"},
    )

    events = parse_sse_events(response.content)

    action_events = [e for e in events if e["event"] == "action_executed"]

    assert action_events[0]["action_type"] == "add_planning_item"
    assert action_events[0]["item_id"] == PLANNING_ITEM_UUID


def test_send_message_com_options(
    client: TestClient,
    monkeypatch,
    mock_authenticated_user,
):
    """Agente pode enviar options (quick reply buttons)."""

    async def fake_process(**kwargs):
        yield {"event": "agent_start", "agent": "ceo"}
        yield {
            "event": "agent_message",
            "agent": "ceo",
            "content": "Em que estágio você está?",
            "options": ["Tenho uma ideia", "Tenho um MVP", "Já lancei"],
        }
        yield {"event": "turn_complete"}

    monkeypatch.setattr(
        "app.api.chat.board_service.process_group_message",
        fake_process,
    )

    response = client.post(
        "/chat/message",
        json={"startup_id": STARTUP_UUID, "message": "Olá!"},
    )

    events = parse_sse_events(response.content)

    message_events = [e for e in events if e["event"] == "agent_message"]

    assert message_events[0]["options"] == ["Tenho uma ideia", "Tenho um MVP", "Já lancei"]


def test_send_message_modo_product_creation(
    client: TestClient,
    monkeypatch,
    mock_authenticated_user,
):
    """O parâmetro mode é repassado corretamente ao BoardService."""

    captured = {}

    async def fake_process(message, startup_id, user_id, mode="casual", conv_type="group"):
        captured["mode"] = mode
        captured["conv_type"] = conv_type
        yield {"event": "turn_complete"}

    monkeypatch.setattr(
        "app.api.chat.board_service.process_group_message",
        fake_process,
    )

    client.post(
        "/chat/message",
        json={
            "startup_id": STARTUP_UUID,
            "message": "Quero criar um produto.",
            "mode": "product_creation",
            "conversation_type": "cto",
        },
    )

    assert captured["mode"] == "product_creation"
    assert captured["conv_type"] == "cto"


def test_send_message_valores_default(
    client: TestClient,
    monkeypatch,
    mock_authenticated_user,
):
    """mode padrão é casual e conversation_type padrão é group."""

    captured = {}

    async def fake_process(message, startup_id, user_id, mode="casual", conv_type="group"):
        captured["mode"] = mode
        captured["conv_type"] = conv_type
        yield {"event": "turn_complete"}

    monkeypatch.setattr(
        "app.api.chat.board_service.process_group_message",
        fake_process,
    )

    client.post(
        "/chat/message",
        json={"startup_id": STARTUP_UUID, "message": "Olá!"},
    )

    assert captured["mode"] == "casual"
    assert captured["conv_type"] == "group"


def test_send_message_erro_no_board_service(
    client: TestClient,
    monkeypatch,
    mock_authenticated_user,
):
    """
    Exceção no BoardService deve gerar evento de error no stream SSE
    — não um HTTP 500.
    """

    async def fake_process(**kwargs):
        yield {"event": "agent_start", "agent": "ceo"}
        raise RuntimeError("Falha inesperada no serviço.")

    monkeypatch.setattr(
        "app.api.chat.board_service.process_group_message",
        fake_process,
    )

    response = client.post(
        "/chat/message",
        json={"startup_id": STARTUP_UUID, "message": "Qual minha estratégia?"},
    )

    assert response.status_code == 200

    events = parse_sse_events(response.content)

    error_events = [e for e in events if e["event"] == "error"]

    assert len(error_events) == 1
    assert "Falha inesperada no serviço." in error_events[0]["detail"]


def test_send_message_sem_autenticacao(client: TestClient):
    """Sem token deve retornar 401."""

    response = client.post(
        "/chat/message",
        json={"startup_id": STARTUP_UUID, "message": "Olá!"},
    )

    assert response.status_code == 401


def test_send_message_sem_startup_id(
    client: TestClient,
    mock_authenticated_user,
):
    """startup_id é obrigatório — omiti-lo retorna 422."""

    response = client.post(
        "/chat/message",
        json={"message": "Mensagem sem startup."},
    )

    assert response.status_code == 422


def test_send_message_conversation_type_invalido(
    client: TestClient,
    mock_authenticated_user,
):
    """conversation_type inválido deve retornar 422."""

    response = client.post(
        "/chat/message",
        json={"startup_id": STARTUP_UUID, "message": "Olá!", "conversation_type": "board_geral"},
    )

    assert response.status_code == 422


# ─── GET /chat/history/{startup_id}/{conversation_type} ────────────────────────

def test_get_historico_grupo(
    client: TestClient,
    monkeypatch,
    mock_authenticated_user,
    mock_message_group,
    mock_message_agent,
):
    """
    Retorna as mensagens do chat em grupo em ordem cronológica.
    O histórico inclui mensagens do founder (role: user) e dos agentes (role: agent).
    """

    async def fake_get_messages(startup_id, conv_type, limit=100):
        assert startup_id == STARTUP_UUID
        assert conv_type == "group"

        return [mock_message_group, mock_message_agent]

    monkeypatch.setattr(
        "app.api.chat.conversation_service.get_messages_by_startup_and_type",
        fake_get_messages,
    )

    response = client.get(f"/chat/history/{STARTUP_UUID}/group")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 2

    assert data[0]["role"] == "user"
    assert data[0]["agent_name"] is None
    assert data[0]["content"] == "Qual é minha estratégia de go-to-market?"

    assert data[1]["role"] == "agent"
    assert data[1]["agent_name"] == "ceo"
    assert data[1]["content"] == "Foque em canais orgânicos no estágio inicial."
    assert data[1]["actions"] is not None


def test_get_historico_chat_individual_ceo(
    client: TestClient,
    monkeypatch,
    mock_authenticated_user,
    mock_message_agent,
):
    """Retorna o histórico do chat individual com o CEO Agent."""

    ceo_msg = {**mock_message_agent, "agent_name": "ceo"}

    async def fake_get_messages(startup_id, conv_type, limit=100):
        assert conv_type == "ceo"

        return [ceo_msg]

    monkeypatch.setattr(
        "app.api.chat.conversation_service.get_messages_by_startup_and_type",
        fake_get_messages,
    )

    response = client.get(f"/chat/history/{STARTUP_UUID}/ceo")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["agent_name"] == "ceo"


@pytest.mark.parametrize("conv_type", ["group", "onboarding", "ceo", "cto", "cfo", "cmo"])
def test_get_historico_todos_os_tipos(
    client: TestClient,
    monkeypatch,
    mock_authenticated_user,
    conv_type: str,
):
    """Todos os tipos de conversa válidos devem retornar 200."""

    async def fake_get_messages(startup_id, conv_type_arg, limit=100):
        return []

    monkeypatch.setattr(
        "app.api.chat.conversation_service.get_messages_by_startup_and_type",
        fake_get_messages,
    )

    response = client.get(f"/chat/history/{STARTUP_UUID}/{conv_type}")

    assert response.status_code == 200
    assert response.json() == []


def test_get_historico_conversa_ainda_nao_existe(
    client: TestClient,
    monkeypatch,
    mock_authenticated_user,
):
    """
    Se o founder ainda não enviou nenhuma mensagem naquele chat,
    a conversa não existe e o endpoint retorna lista vazia.
    """

    async def fake_get_messages(startup_id, conv_type, limit=100):
        return []

    monkeypatch.setattr(
        "app.api.chat.conversation_service.get_messages_by_startup_and_type",
        fake_get_messages,
    )

    response = client.get(f"/chat/history/{STARTUP_UUID}/cto")

    assert response.status_code == 200
    assert response.json() == []


def test_get_historico_com_limit_customizado(
    client: TestClient,
    monkeypatch,
    mock_authenticated_user,
    mock_message_group,
):
    """O parâmetro limit é repassado corretamente ao service."""

    captured_limit = {}

    async def fake_get_messages(startup_id, conv_type, limit=100):
        captured_limit["limit"] = limit

        return [mock_message_group]

    monkeypatch.setattr(
        "app.api.chat.conversation_service.get_messages_by_startup_and_type",
        fake_get_messages,
    )

    client.get(f"/chat/history/{STARTUP_UUID}/group?limit=25")

    assert captured_limit["limit"] == 25


def test_get_historico_tipo_invalido(
    client: TestClient,
    mock_authenticated_user,
):
    """conversation_type inválido na URL deve retornar 422."""

    response = client.get(f"/chat/history/{STARTUP_UUID}/board_geral")

    assert response.status_code == 422


def test_get_historico_sem_autenticacao(client: TestClient):
    """Sem token deve retornar 401."""

    response = client.get(f"/chat/history/{STARTUP_UUID}/group")

    assert response.status_code == 401


# ─── GET /chat/conversations/{startup_id} ──────────────────────────────────────

def test_get_conversas_da_startup(
    client: TestClient,
    monkeypatch,
    mock_authenticated_user,
    mock_conversation,
):
    """
    Lista todas as conversas existentes para a startup.
    Conversas são criadas na primeira mensagem de cada tipo.
    """

    ceo_conversation = {
        "id": "66666666-6666-6666-6666-666666666666",
        "startup_id": STARTUP_UUID,
        "type": "ceo",
        "created_at": "2026-08-19T11:00:00Z",
    }

    async def fake_get_conversations(startup_id):
        assert startup_id == STARTUP_UUID

        return [mock_conversation, ceo_conversation]

    monkeypatch.setattr(
        "app.api.chat.conversation_service.get_conversations_by_startup",
        fake_get_conversations,
    )

    response = client.get(f"/chat/conversations/{STARTUP_UUID}")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 2

    assert data[0]["type"] == "group"
    assert data[0]["startup_id"] == STARTUP_UUID
    assert data[1]["type"] == "ceo"


def test_get_conversas_startup_sem_historico(
    client: TestClient,
    monkeypatch,
    mock_authenticated_user,
):
    """
    Startup recém-criada não tem conversas ainda.
    Retorna lista vazia — o frontend exibe os chats como "novos".
    """

    async def fake_get_conversations(startup_id):
        return []

    monkeypatch.setattr(
        "app.api.chat.conversation_service.get_conversations_by_startup",
        fake_get_conversations,
    )

    response = client.get(f"/chat/conversations/{STARTUP_UUID}")

    assert response.status_code == 200
    assert response.json() == []


def test_get_conversas_campos_obrigatorios(
    client: TestClient,
    monkeypatch,
    mock_authenticated_user,
    mock_conversation,
):
    """Cada conversa retornada deve ter id, startup_id, type e created_at."""

    async def fake_get_conversations(startup_id):
        return [mock_conversation]

    monkeypatch.setattr(
        "app.api.chat.conversation_service.get_conversations_by_startup",
        fake_get_conversations,
    )

    response = client.get(f"/chat/conversations/{STARTUP_UUID}")

    data = response.json()

    assert "id" in data[0]
    assert "startup_id" in data[0]
    assert "type" in data[0]
    assert "created_at" in data[0]


def test_get_conversas_sem_autenticacao(client: TestClient):
    """Sem token deve retornar 401."""

    response = client.get(f"/chat/conversations/{STARTUP_UUID}")

    assert response.status_code == 401
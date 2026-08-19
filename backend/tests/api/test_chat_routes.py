import json
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

from app.api.dependencies import get_current_user
from app.main import app


USER_UUID = "22222222-2222-2222-2222-222222222222"
STARTUP_UUID = "11111111-1111-1111-1111-111111111111"
CANVAS_ZONE_UUID = "33333333-3333-3333-3333-333333333333"
PLANNING_ITEM_UUID = "44444444-4444-4444-4444-444444444444"


@pytest.fixture
def mock_authenticated_user():
    """Sobrescreve a dependência get_current_user para simular um usuário autenticado."""
    fake_user = SimpleNamespace(
        id=USER_UUID,
        email="logged_user@example.com"
    )

    app.dependency_overrides[get_current_user] = lambda: fake_user

    yield fake_user

    app.dependency_overrides.clear()


def parse_sse_events(response_content: bytes) -> list[dict]:
    """
    Utilitário para extrair e parsear eventos do formato SSE.
    Cada linha `data: {...}` vira um dict na lista retornada.
    """
    events = []
    for line in response_content.decode().split("\n"):
        line = line.strip()
        if line.startswith("data: "):
            try:
                event = json.loads(line[6:])
                events.append(event)
            except json.JSONDecodeError:
                pass
    return events


# ─── FORMATO E ESTRUTURA SSE ───────────────────────────────────────────────────

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
    Testa que os eventos chegam na sequência correta:
    agent_start → agent_message → turn_complete
    """

    async def fake_process(**kwargs):
        yield {"event": "agent_start", "agent": "ceo"}
        yield {
            "event": "agent_message",
            "agent": "ceo",
            "content": "Ótima pergunta sobre estratégia!",
            "options": [],
        }
        yield {"event": "turn_complete"}

    monkeypatch.setattr(
        "app.api.chat.board_service.process_group_message",
        fake_process,
    )

    response = client.post(
        "/chat/message",
        json={"startup_id": STARTUP_UUID, "message": "Qual é minha estratégia?"},
    )

    events = parse_sse_events(response.content)

    assert len(events) == 3

    assert events[0]["event"] == "agent_start"
    assert events[0]["agent"] == "ceo"

    assert events[1]["event"] == "agent_message"
    assert events[1]["agent"] == "ceo"
    assert events[1]["content"] == "Ótima pergunta sobre estratégia!"
    assert events[1]["options"] == []

    assert events[2]["event"] == "turn_complete"


def test_send_message_multiplos_agentes(
    client: TestClient,
    monkeypatch,
    mock_authenticated_user,
):
    """
    Quando múltiplos agentes respondem, cada um deve ter seu agent_start
    seguido de agent_message antes do próximo agente.
    """

    async def fake_process(**kwargs):
        yield {"event": "agent_start", "agent": "ceo"}
        yield {"event": "agent_message", "agent": "ceo", "content": "Visão estratégica aqui.", "options": []}
        yield {"event": "agent_start", "agent": "cfo"}
        yield {"event": "agent_message", "agent": "cfo", "content": "Cuidado com o burn rate.", "options": []}
        yield {"event": "turn_complete"}

    monkeypatch.setattr(
        "app.api.chat.board_service.process_group_message",
        fake_process,
    )

    response = client.post(
        "/chat/message",
        json={
            "startup_id": STARTUP_UUID,
            "message": "Qual é meu custo de aquisição ideal?",
        },
    )

    events = parse_sse_events(response.content)

    assert len(events) == 5

    agent_starts = [e for e in events if e["event"] == "agent_start"]
    agent_messages = [e for e in events if e["event"] == "agent_message"]

    assert len(agent_starts) == 2
    assert len(agent_messages) == 2

    assert agent_starts[0]["agent"] == "ceo"
    assert agent_starts[1]["agent"] == "cfo"

    assert events[-1]["event"] == "turn_complete"


# ─── EVENTOS DE ACTION ─────────────────────────────────────────────────────────

def test_send_message_action_update_canvas(
    client: TestClient,
    monkeypatch,
    mock_authenticated_user,
):
    """
    Quando um agente atualiza uma zona do canvas, o evento
    action_executed deve ser emitido com as informações corretas.
    """

    async def fake_process(**kwargs):
        yield {"event": "agent_start", "agent": "ceo"}
        yield {"event": "agent_message", "agent": "ceo", "content": "Atualizei sua proposta de valor.", "options": []}
        yield {
            "event": "action_executed",
            "action_type": "update_canvas_zone",
            "zone": "value_proposition",
        }
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
    """
    Agente pode sugerir uma tarefa de planejamento durante a conversa.
    O evento action_executed deve conter o item_id criado.
    """

    async def fake_process(**kwargs):
        yield {"event": "agent_start", "agent": "cmo"}
        yield {"event": "agent_message", "agent": "cmo", "content": "Sugiro criar a landing page esta semana.", "options": []}
        yield {
            "event": "action_executed",
            "action_type": "add_planning_item",
            "item_id": PLANNING_ITEM_UUID,
        }
        yield {"event": "turn_complete"}

    monkeypatch.setattr(
        "app.api.chat.board_service.process_group_message",
        fake_process,
    )

    response = client.post(
        "/chat/message",
        json={"startup_id": STARTUP_UUID, "message": "Como devo começar o marketing?"},
    )

    events = parse_sse_events(response.content)

    action_events = [e for e in events if e["event"] == "action_executed"]

    assert len(action_events) == 1
    assert action_events[0]["action_type"] == "add_planning_item"
    assert action_events[0]["item_id"] == PLANNING_ITEM_UUID


def test_send_message_com_options(
    client: TestClient,
    monkeypatch,
    mock_authenticated_user,
):
    """
    Agentes podem enviar options (quick reply buttons) quando
    a resposta esperada é de um conjunto limitado.
    """

    async def fake_process(**kwargs):
        yield {"event": "agent_start", "agent": "ceo"}
        yield {
            "event": "agent_message",
            "agent": "ceo",
            "content": "Em que estágio você se encontra?",
            "options": ["Tenho uma ideia", "Tenho um MVP", "Já lancei"],
        }
        yield {"event": "turn_complete"}

    monkeypatch.setattr(
        "app.api.chat.board_service.process_group_message",
        fake_process,
    )

    response = client.post(
        "/chat/message",
        json={"startup_id": STARTUP_UUID, "message": "Olá, quero criar minha startup."},
    )

    events = parse_sse_events(response.content)

    message_events = [e for e in events if e["event"] == "agent_message"]

    assert len(message_events) == 1
    assert message_events[0]["options"] == ["Tenho uma ideia", "Tenho um MVP", "Já lancei"]


# ─── PARÂMETROS DE REQUEST ─────────────────────────────────────────────────────

def test_send_message_modo_product_creation(
    client: TestClient,
    monkeypatch,
    mock_authenticated_user,
):
    """
    O parâmetro mode é passado corretamente ao BoardService.
    No modo product_creation, o CTO Agent deve ser acionado com modo especial.
    """

    captured_mode = {}

    async def fake_process(message, startup_id, user_id, mode="casual", conv_type="group"):
        captured_mode["mode"] = mode

        yield {"event": "agent_start", "agent": "cto"}
        yield {"event": "agent_message", "agent": "cto", "content": "Vamos criar seu produto.", "options": []}
        yield {"event": "turn_complete"}

    monkeypatch.setattr(
        "app.api.chat.board_service.process_group_message",
        fake_process,
    )

    client.post(
        "/chat/message",
        json={
            "startup_id": STARTUP_UUID,
            "message": "Quero criar um novo produto.",
            "mode": "product_creation",
            "conversation_type": "cto",
        },
    )

    assert captured_mode["mode"] == "product_creation"


def test_send_message_conversation_type_onboarding(
    client: TestClient,
    monkeypatch,
    mock_authenticated_user,
):
    """
    O conversation_type é passado corretamente ao BoardService.
    Onboarding usa conversa separada do chat principal.
    """

    captured_conv_type = {}

    async def fake_process(message, startup_id, user_id, mode="casual", conv_type="group"):
        captured_conv_type["conv_type"] = conv_type

        yield {"event": "agent_start", "agent": "ceo"}
        yield {"event": "agent_message", "agent": "ceo", "content": "Olá! Me conta sobre sua startup.", "options": []}
        yield {"event": "turn_complete"}

    monkeypatch.setattr(
        "app.api.chat.board_service.process_group_message",
        fake_process,
    )

    client.post(
        "/chat/message",
        json={
            "startup_id": STARTUP_UUID,
            "message": "Olá!",
            "conversation_type": "onboarding",
        },
    )

    assert captured_conv_type["conv_type"] == "onboarding"


# ─── ERROS E VALIDAÇÃO ─────────────────────────────────────────────────────────

def test_send_message_sem_autenticacao(client: TestClient):
    """Sem token de autenticação deve retornar 401."""

    response = client.post(
        "/chat/message",
        json={"startup_id": STARTUP_UUID, "message": "Olá!"},
    )

    assert response.status_code == 401


def test_send_message_sem_startup_id(
    client: TestClient,
    mock_authenticated_user,
):
    """startup_id é obrigatório — omiti-lo deve retornar 422."""

    response = client.post(
        "/chat/message",
        json={"message": "Mensagem sem startup."},
    )

    assert response.status_code == 422


def test_send_message_sem_message(
    client: TestClient,
    mock_authenticated_user,
):
    """message é obrigatório — omiti-lo deve retornar 422."""

    response = client.post(
        "/chat/message",
        json={"startup_id": STARTUP_UUID},
    )

    assert response.status_code == 422


def test_send_message_erro_no_board_service(
    client: TestClient,
    monkeypatch,
    mock_authenticated_user,
):
    """
    Quando o BoardService lança uma exceção,
    o endpoint deve emitir um evento de erro no stream SSE
    em vez de retornar um HTTP 500.
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
        json={"startup_id": STARTUP_UUID, "message": "Qual é minha estratégia?"},
    )

    # A resposta HTTP ainda é 200 — o erro vai no stream
    assert response.status_code == 200

    events = parse_sse_events(response.content)

    error_events = [e for e in events if e["event"] == "error"]

    assert len(error_events) == 1
    assert "Falha inesperada no serviço." in error_events[0]["detail"]


def test_send_message_valores_default(
    client: TestClient,
    monkeypatch,
    mock_authenticated_user,
):
    """
    mode e conversation_type têm defaults:
    mode = "casual", conversation_type = "group"
    """

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
    

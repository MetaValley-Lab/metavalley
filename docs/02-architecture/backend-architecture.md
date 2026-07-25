# Arquitetura do Backend

> **Documento:** Backend Architecture
> **Versão:** 1.0
> **Status:** MVP v1

---

# Objetivo

Este documento descreve a arquitetura interna do backend do MetaValley.

Seu objetivo é definir como o código deve ser organizado, quais responsabilidades pertencem a cada camada e quais princípios devem ser respeitados durante o desenvolvimento.

Esta arquitetura busca equilibrar:

* simplicidade para o MVP;
* facilidade de manutenção;
* alta legibilidade;
* baixo acoplamento;
* possibilidade de evolução futura.

---

# Filosofia

O backend segue uma adaptação da **Clean Architecture** organizada por **Domínios de Negócio (Vertical Slice Architecture)**.

Ao invés de organizar arquivos por tecnologia, o projeto é organizado por funcionalidades.

Cada módulo representa um domínio independente da aplicação.

---

# Estrutura Geral

```text
backend/

├── app/
│
├── modules/
│
│   ├── auth/
│   ├── startups/
│   ├── products/
│   ├── board/
│   ├── agents/
│   ├── canvas/
│   ├── planning/
│   └── simulation/
│
├── infrastructure/
│
├── shared/
│
├── config/
│
└── tests/
```

---

# Organização dos Módulos

Cada módulo segue exatamente a mesma estrutura.

```text
startups/

    application/

    domain/

    infrastructure/

    presentation/
```

Essa padronização facilita manutenção e onboarding.

---

# Camadas

## Presentation

Responsável pela comunicação com o mundo externo.

Contém:

* Controllers
* DTOs
* Schemas
* Middlewares
* Validators

Esta camada nunca contém regra de negócio.

---

## Application

Contém os **Casos de Uso**.

Cada caso de uso representa exatamente uma ação do sistema.

Exemplos:

```text
CreateStartup

UpdateStartup

DeleteStartup

SelectStartup
```

Os casos de uso coordenam o fluxo da aplicação, mas não conhecem detalhes técnicos.

---

## Domain

Representa o núcleo do negócio.

Contém:

* Entidades
* Value Objects
* Interfaces
* Regras de Negócio
* Exceções de Domínio

Esta camada nunca depende de FastAPI, banco de dados ou bibliotecas externas.

É a camada mais estável da aplicação.

---

## Infrastructure

Implementa detalhes técnicos.

Exemplos:

* Prisma/SQLAlchemy Repository
* Supabase
* Claude API
* Redis
* Storage
* Sentry

Tudo que pode ser substituído pertence aqui.

---

# Fluxo de uma Requisição

```mermaid
sequenceDiagram

actor Founder

participant Controller

participant UseCase

participant Repository

participant Database

Founder->>Controller: HTTP Request

Controller->>UseCase: DTO

UseCase->>Repository: Interface

Repository->>Database: SQL

Database-->>Repository

Repository-->>UseCase

UseCase-->>Controller

Controller-->>Founder
```

---

# Organização dos Casos de Uso

Cada Use Case executa apenas uma responsabilidade.

Exemplos:

```text
CreateStartup

UpdateStartup

CreateProduct

SendMessage

GenerateBoardResponse

UpdateCanvas

CompletePlanningItem

RegisterSimulationInterest
```

Casos de uso não devem chamar outros casos de uso diretamente.

Quando necessário, utiliza-se um **Application Service**.

---

# Application Services

Existem fluxos do MetaValley que envolvem diversos módulos simultaneamente.

Nesses casos, utiliza-se um **Application Service**.

Exemplo:

```text
BoardConversationService
```

Responsabilidades:

* recuperar contexto;
* selecionar agentes;
* construir prompt;
* chamar Claude;
* persistir mensagens;
* atualizar Canvas;
* atualizar Planning.

Ele coordena vários módulos sem concentrar regras de negócio.

---

# Arquitetura dos Agentes

O módulo **Agents** é responsável exclusivamente pela inteligência artificial.

Fluxo interno:

```mermaid
flowchart LR

Context

↓

PromptBuilder

↓

AgentSelector

↓

Claude API

↓

ResponseParser

↓

ContextUpdater
```

Cada componente possui responsabilidade única.

---

# Context Engine

O contexto enviado para o Claude nunca é construído diretamente pelo Controller.

Existe um componente específico responsável por isso.

```text
ContextEngine
```

Ele agrega:

* startup ativa;
* produtos;
* histórico;
* Canvas;
* Planning;
* configurações do usuário.

Depois produz um único objeto de contexto.

---

# Prompt Builder

Cada agente possui um Prompt Base.

Antes de chamar o modelo, o sistema monta:

```text
Prompt Final

=

Prompt Base

+

Startup

+

Canvas

+

Produtos

+

Histórico

+

Mensagem Atual
```

Isso evita duplicação de código.

---

# Persistência

Todo acesso ao banco ocorre através de interfaces.

Exemplo:

```text
IStartupRepository

↓

StartupRepository
```

Nunca acessar o banco diretamente em:

* Controllers
* Use Cases
* Services

---

# Injeção de Dependências

Todo módulo depende apenas de interfaces.

```text
Use Case

↓

Interface

↓

Implementação
```

Isso facilita:

* testes;
* troca de banco;
* troca de provedor de IA.

---

# Comunicação entre Módulos

Os módulos comunicam-se apenas através de:

* Interfaces;
* Application Services;
* Eventos internos.

Nunca através de acesso direto às implementações.

---

# Tratamento de Exceções

Cada domínio possui suas próprias exceções.

Exemplo:

```text
StartupNotFoundException

ConversationNotFoundException

CanvasZoneNotFoundException

UnauthorizedException
```

Um middleware global converte essas exceções em respostas HTTP apropriadas.

---

# Logging

Todo request recebe um **Correlation ID**.

Todos os logs relacionados compartilham esse identificador.

Exemplo:

```text
Request

↓

Correlation ID

↓

Controller

↓

Use Case

↓

Repository

↓

Claude API

↓

Response
```

Isso facilita rastreamento em produção.

---

# Configuração

Nenhuma configuração deve ficar hardcoded.

Todas devem ser carregadas através de:

```text
config/

    settings.py
```

Exemplos:

* API Keys;
* Banco;
* Redis;
* Claude;
* Sentry;
* Ambiente.

---

# Testes

Cada camada possui um tipo específico de teste.

| Camada         | Tipo       |
| -------------- | ---------- |
| Domain         | Unitários  |
| Application    | Unitários  |
| Infrastructure | Integração |
| Presentation   | Integração |
| API            | End-to-End |

Os testes devem validar comportamento, não implementação.

---

# Estrutura de Pastas Recomendada

```text
modules/

    startups/

        application/

            use_cases/

        domain/

            entities/

            repositories/

            exceptions/

            value_objects/

        infrastructure/

            persistence/

            providers/

        presentation/

            controllers/

            schemas/
```

Todos os módulos seguem exatamente essa organização.

---

# Regras Arquiteturais

Durante o desenvolvimento, as seguintes regras devem ser respeitadas.

## É permitido

* depender de interfaces;
* reutilizar Value Objects;
* compartilhar componentes do módulo Shared;
* utilizar Application Services para orquestração.

## Não é permitido

* acessar banco fora dos Repositories;
* regras de negócio em Controllers;
* regras de negócio em Providers;
* dependências circulares;
* um módulo importar entidades internas de outro.

---

# Observabilidade

O backend deve registrar:

* erros;
* tempo de resposta;
* consumo da API do Claude;
* custo por requisição;
* quantidade de tokens;
* tempo do primeiro token;
* tempo total da conversa.

Esses indicadores são compatíveis com os requisitos não funcionais definidos para o MVP, especialmente os relacionados à observabilidade e monitoramento de custos.

---

# Evolução da Arquitetura

A arquitetura foi planejada para evoluir gradualmente.

```text
Monólito Modular

↓

Workers

↓

Mensageria

↓

Background Processing

↓

Arquitetura Híbrida

↓

Microsserviços
```

Como os módulos já possuem fronteiras bem definidas, a extração futura de serviços independentes poderá ocorrer com impacto reduzido no restante da aplicação.

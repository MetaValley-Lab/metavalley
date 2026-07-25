# Arquitetura do MetaValley

> **Versão:** 1.0
> **Status:** Em evolução
> **Última atualização:** 25/07/2026

---

# Objetivo

Esta documentação descreve a arquitetura técnica do **MetaValley**, incluindo sua organização em módulos, princípios arquiteturais, decisões técnicas e estratégia de evolução.

O objetivo é servir como referência para toda a equipe de desenvolvimento, facilitando o onboarding de novos desenvolvedores, a manutenção do sistema e a tomada de decisões arquiteturais.

Esta documentação complementa o levantamento de requisitos do projeto e deve evoluir juntamente com o produto. Ela foi elaborada com base no documento de requisitos do MVP v1 do MetaValley.

---

# Objetivos Arquiteturais

A arquitetura do MetaValley foi projetada para atender aos seguintes objetivos:

* acelerar o desenvolvimento do MVP;
* reduzir complexidade operacional;
* permitir evolução incremental do produto;
* facilitar manutenção do código;
* minimizar acoplamento entre funcionalidades;
* permitir extração futura de serviços independentes;
* facilitar testes automatizados;
* manter alta legibilidade do código.

---

# Estilo Arquitetural

O MetaValley utiliza uma arquitetura baseada em um **Monólito Modular**.

Toda a aplicação é implantada como um único serviço, porém organizada internamente em módulos independentes de domínio.

Essa abordagem foi escolhida para permitir:

* desenvolvimento rápido;
* deploy simples;
* menor custo operacional;
* facilidade de evolução.

Conforme o crescimento do produto, módulos poderão ser extraídos para serviços independentes sem necessidade de reescrever o sistema.

---

# Princípios da Arquitetura

Toda decisão técnica deve respeitar os seguintes princípios.

## Separação de responsabilidades

Cada módulo possui responsabilidades bem definidas.

Nenhum módulo deve concentrar responsabilidades pertencentes a outro domínio.

---

## Baixo acoplamento

Os módulos devem conhecer apenas contratos públicos.

Nunca acessar diretamente implementações internas de outro módulo.

---

## Alta coesão

Tudo que pertence ao mesmo domínio deve permanecer no mesmo módulo.

---

## Orientação ao domínio

As regras de negócio são o centro da aplicação.

Frameworks, banco de dados e APIs são detalhes de implementação.

---

## Evolução incremental

A arquitetura deve permitir novas funcionalidades sem grandes refatorações.

---

## Simplicidade

Durante o MVP, soluções simples serão priorizadas.

Complexidade somente será adicionada quando houver necessidade comprovada.

---

# Organização da Documentação

A documentação arquitetural está dividida nos seguintes documentos.

| Documento                 | Objetivo                                 |
| ------------------------- | ---------------------------------------- |
| `system-overview.md`      | Visão geral da arquitetura do sistema    |
| `modules.md`              | Organização dos módulos de negócio       |
| `backend-architecture.md` | Arquitetura interna do backend           |
| `scalability.md`          | Estratégia de crescimento da arquitetura |

Documentos adicionais poderão ser adicionados futuramente, como:

* C4 Context
* C4 Container
* Deployment
* ADRs (Architecture Decision Records)
* Coding Standards

---

# Organização Geral do Sistema

```text
MetaValley

Frontend (Next.js)

        │

        ▼

Backend (FastAPI)

        │

 ┌─────────────────────────────┐
 │ Auth                        │
 │ Startups                    │
 │ Products                    │
 │ Executive Board             │
 │ Agents                      │
 │ Canvas                      │
 │ Planning                    │
 │ Simulation                  │
 └─────────────────────────────┘

        │

        ▼

PostgreSQL

        │

        ▼

Serviços Externos
```

---

# Fluxo Geral da Aplicação

```text
Founder

↓

Frontend

↓

API

↓

Controller

↓

Caso de Uso

↓

Domínio

↓

Repository

↓

Banco de Dados

↓

Resposta
```

---

# Stack Tecnológica

A stack adotada para o MVP é composta por:

## Frontend

* Next.js
* React
* Tailwind CSS

## Backend

* FastAPI
* Python

## Banco de Dados

* PostgreSQL (Supabase)

## Autenticação

* Supabase Auth

## Inteligência Artificial

* Claude API

## Deploy

* Vercel
* Railway (ou Render)

## Monitoramento

* Sentry

Essa definição está alinhada ao documento de requisitos do MVP.

---

# Estrutura da Arquitetura

O sistema é dividido em módulos independentes.

Cada módulo possui:

* regras de negócio;
* casos de uso;
* entidades;
* infraestrutura;
* interfaces públicas.

Os módulos compartilham apenas contratos e nunca implementações.

Essa organização facilita manutenção, testes e futura extração para microsserviços.

---

# Estratégia de Evolução

A arquitetura seguirá a seguinte evolução:

```text
MVP

↓

Monólito Modular

↓

Escalabilidade Horizontal

↓

Background Workers

↓

Mensageria

↓

Arquitetura Híbrida

↓

Microsserviços (quando necessário)
```

A extração de módulos somente ocorrerá quando houver necessidade real de escalabilidade ou independência operacional.

---

# Convenções Gerais

Durante o desenvolvimento deverão ser seguidas as seguintes diretrizes:

* um módulo representa um domínio de negócio;
* um caso de uso representa uma única ação do sistema;
* regras de negócio não devem depender do framework;
* acesso ao banco ocorre apenas através de repositórios;
* comunicação entre módulos deve ocorrer por interfaces;
* código deve priorizar legibilidade em vez de abstrações desnecessárias.

---

# Como Navegar Nesta Documentação

Caso deseje entender...

### O sistema como um todo

➡ Leia `system-overview.md`

---

### Como o backend foi organizado

➡ Leia `backend-architecture.md`

---

### Onde cada funcionalidade está localizada

➡ Leia `modules.md`

---

### Como o sistema crescerá no futuro

➡ Leia `scalability.md`

---

# Escopo

Esta documentação descreve exclusivamente a arquitetura do **MVP v1**.

Funcionalidades futuras, como:

* Simulação TME completa;
* Landing Pages automáticas;
* Experimentos com usuários reais;
* Network entre founders;
* Aplicativo mobile;

não fazem parte desta documentação e serão documentadas em versões futuras, conforme definido no levantamento de requisitos.

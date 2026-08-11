# MetaValley — Levantamento de Requisitos (MVP v1)

**Versão:** 1.1  
**Data:** Junho 2026  
**Autor:** Samir  
**Status:** Aprovado com observações

---

## 1. Visão Geral

### 1.1 Problema
Founders gastam tempo e dinheiro construindo produtos antes de validar se o mercado os quer. Ferramentas de pesquisa tradicionais são caras e lentas. LLMs genéricas dão conselhos, mas não dados.

### 1.2 Solução
Com nossos agentes de IA, o founder recebe conselhos e direcionamento especializado em cada setor da sua startup. Alimentados com datasets proprietários, os agentes sabem o que funciona e o que não funciona — e indicam qual estratégia melhor se encaixa em cada ideia e contexto.

O founder tem controle e vê sua startup tomando forma através do Canvas Vivo, acompanhando mudanças e evolução em tempo real.

Para validação de mercado, a plataforma oferece simulação sintética (TME) que entrega dados quantitativos — não opiniões — sobre adoção, objeções por segmento e projeção de cenários futuros.

### 1.3 Diferencial Central
O MetaValley não entrega conselho — entrega **dados**. A simulação retorna percentuais de adoção, objeções por segmento e projeções de 12 meses. Isso é o que diferencia do founder simplesmente conversando com uma LLM.

O segundo diferencial é o **dataset acumulado**: cada founder que usa a plataforma gera dados sobre o que funciona e o que falha em cada segmento. Agentes alimentados por esse dataset são mais precisos do que qualquer LLM genérica.

### 1.4 Modelo de Negócio
- **Freemium:** board executivo e canvas disponíveis gratuitamente com limite de mensagens
- **Pay-per-experiment:** cada simulação TME é cobrada individualmente
- **Pro (futuro):** experimento com pessoas reais, landing page gerada automaticamente, anúncios reais

---

## 2. Usuários (Personas)

### P01 — Founder em Pré-Seed
- Tem uma ideia ou MVP embrionário
- Quer validar se há demanda antes de investir tempo
- Não tem orçamento para consultoria ou pesquisa de mercado
- **Dor principal:** incerteza sobre se está construindo a coisa certa

### P02 — Founder em Pivô
- Produto lançado mas com tração baixa
- Precisa entender se o problema é posicionamento, preço ou segmento
- Tem urgência — tempo e dinheiro limitados
- **Dor principal:** não saber por onde ajustar sem gastar mais

### P03 — Empreendedora Serial (ex: Tássia / Ada Metaverse)
- Já possui empresa consolidada mas quer validar ideias de novos produtos ou spin-offs
- Usa o MetaValley para testar antes de alocar recursos da empresa principal
- **Dor principal:** risco de diluir foco da empresa atual com uma aposta não validada
- **Nota:** A Ada Metaverse é uma deep tech de neuroengenharia focada em educação e saúde imersiva. Como empresa estabelecida, não é o público-alvo principal. Porém, Tássia como founder individual validando spin-offs ou novos produtos da Ada **se encaixa perfeitamente** no P03 — o MetaValley pode hospedar tanto "minha startup nova" quanto "minha ideia de novo produto para a Ada".

### P04 — Aceleradora / Gestor de Programa (futuro — fora do MVP)
- Quer avaliar múltiplas startups em paralelo com dados padronizados

---

## 3. Funcionalidades do MVP

---

### F01 — Autenticação

**Descrição:** Sistema de login e cadastro do founder.

**User Stories:**
- Como founder, quero criar minha conta com e-mail e senha
- Como founder, quero entrar na minha conta existente
- Como founder, quero redefinir minha senha por e-mail

**Critérios de Aceite:**
- [ ] Cadastro com e-mail e senha funciona
- [ ] Login com credenciais válidas redireciona para o dashboard
- [ ] Login inválido exibe mensagem de erro clara
- [ ] Sessão persiste após fechar o navegador
- [ ] Recuperação de senha por e-mail funciona
- [ ] Rate limiting no endpoint de login (máx. 5 tentativas/min por IP)

**Regras de Negócio:**
- RN01: Senha mínima de 8 caracteres
- RN02: E-mail único no sistema
- RN03: Usuário não autenticado é redirecionado para login

**Stack:** Supabase Auth — não construir do zero.

**Fora do escopo do MVP:** Login social (Google, GitHub), autenticação 2FA

---

### F02 — Criar Startup via Conversa (Onboarding)

**Descrição:** O founder cria sua startup através de uma conversa com o CEO Agent — sem preencher nenhum formulário. O sistema extrai os dados estruturadamente da conversa.

**User Stories:**
- Como founder, quero descrever minha startup de forma natural, sem formulários
- Como founder, quero ter mais de uma startup cadastrada
- Como founder, quero poder criar uma startup para uma ideia de spin-off, separada da minha empresa principal

**Fluxo:**
1. No dashboard, founder clica no botão **"+ Nova Startup"**
2. Abre um chat dedicado de onboarding (tela separada, não o board principal)
3. CEO Agent inicia: *"Olá! Sou o CEO do seu board executivo. Me conta: qual é a sua startup e que problema ela resolve?"*
4. CEO faz 3–4 perguntas de aprofundamento para capturar: nome, problema, segmento-alvo, estágio (ideia/MVP/lançada), modelo de receita pretendido
5. Sistema extrai os dados e salva no banco em background
6. CEO confirma: *"Perfeito. Criei o perfil da [Nome]. Agora você tem acesso ao seu board."*
7. Founder é redirecionado para o board da startup recém-criada
8. Edição posterior dos dados é feita manualmente via página de **Configurações da Startup** (campos editáveis direto na interface — não via chat)

**Critérios de Aceite:**
- [ ] Conversa coleta: nome, descrição, segmento, estágio e modelo de receita
- [ ] Dados salvos corretamente no banco
- [ ] Founder pode editar dados da startup via configurações (não via chat)
- [ ] Múltiplas startups por conta funcionam
- [ ] Troca de contexto entre startups ativas funciona corretamente

**Extração estruturada (background):**
```json
{
  "name": "string",
  "description": "string",
  "problem": "string",
  "solution": "string",
  "segment": "string",
  "target_location": "string (opcional)",
  "stage": "idea | mvp | launched",
  "primary_revenue_model": "subscription | saas | marketplace | freemium | pay_per_use | licensing | advertising | e_commerce | service | hardware | other",
  "revenue_model_details": "string (opcional — para modelos híbridos ou nuances)"
}
```

**Regras de Negócio:**
- RN04: Todo contexto do board usa a startup selecionada como base
- RN05: Se o founder não fornecer nome claro, sistema sugere temporário e permite editar depois
- RN06: Máximo de 3 startups no plano gratuito

---

### F03 — Board Executivo — Chat em Grupo

**Descrição:** Interface principal do produto. Chat grupal onde CEO, CTO, CFO e CMO respondem em conjunto com perspectivas distintas e, quando relevante, conflitantes entre si.

**User Stories:**
- Como founder, quero fazer uma pergunta e receber perspectivas de diferentes áreas simultaneamente
- Como founder, quero ver os agentes debatendo entre si para entender os trade-offs
- Como founder, quero que os agentes lembrem da minha startup e conversas anteriores

**Fluxo:**
1. Founder digita mensagem no chat do grupo "Board Executivo"
2. Sistema determina quais agentes respondem (sempre pelo menos 2)
3. Agentes respondem em sequência, com perspectivas próprias — incluindo discordâncias explícitas
4. Founder pode aprofundar, reagir ou mudar de tema livremente

**Critérios de Aceite:**
- [ ] Mensagens exibem nome e cor do agente remetente
- [ ] Pelo menos 2 agentes respondem a cada mensagem
- [ ] Agentes usam contexto da startup (nome, segmento, estágio) nas respostas
- [ ] Histórico persiste entre sessões
- [ ] Loading state visível enquanto agentes "digitam" (streaming)
- [ ] Canvas é atualizado em background quando conversa gera informação relevante

**Comportamento e Descrição dos Agentes:**

| Agente | Cor | Especialidade | O que pode fazer por você | Tom |
|---|---|---|---|---|
| CEO Agent | #4F46E5 | Visão, estratégia, posicionamento | Definir direção, validar modelo de negócio, preparar pitch, definir prioridades | Ambicioso, pensa em escala |
| CTO Agent | #0891B2 | Tecnologia, produto, viabilidade técnica | Escolher stack, definir arquitetura, avaliar complexidade, planejar MVP técnico | Pragmático, foco em execução |
| CFO Agent | #059669 | Finanças, custos, modelo de receita | Modelar financeiro, calcular CAC/LTV, definir precificação, estimar runway | Conservador, focado em margens |
| CMO Agent | #DC2626 | Marketing, aquisição, posicionamento | Definir canais, escrever copy, mapear ICP, planejar go-to-market | Criativo, focado em canais |

**Regras de Negócio:**
- RN07: Agentes devem discordar explicitamente quando perspectivas conflitam (ex: CEO quer escalar, CFO questiona o burn)
- RN08: System prompt de cada agente inclui perfil completo da startup ativa e zonas preenchidas do canvas
- RN09: Histórico incluído no contexto via sliding window (últimas N mensagens, com limite de tokens)
- RN10: Limite de 50 mensagens/mês no plano gratuito; ilimitado no Pro
- RN11: Agentes não inventam dados numéricos — sinalizam incerteza e sugerem pesquisar
- RN12: Quando canvas é atualizado, todos os agentes passam a ter acesso à versão atualizada no próximo turno (contexto compartilhado via banco, não em tempo real no mesmo turno)

---

### F04 — Board Executivo — Chat Individual

**Descrição:** Conversa privada com um agente específico para aprofundar um tema sem o "ruído" dos outros.

**User Stories:**
- Como founder, quero conversar só com o CFO para modelar meu financeiro
- Como founder, quero conversar só com o CTO para definir arquitetura
- Como founder, quero que o agente lembre o que discutimos no grupo

**Critérios de Aceite:**
- [ ] Sidebar exibe cada agente com nome, cor, especialidade e descrição do que pode fazer
- [ ] Chat individual mantém contexto da startup ativa
- [ ] Agente individual tem acesso ao histórico do grupo para coerência
- [ ] Histórico do grupo e individual são mantidos separados mas o agente "lembra" dos dois
- [ ] UI é idêntica ao grupo, mas com apenas um remetente além do founder

**Regras de Negócio:**
- RN13: Chat individual conta no mesmo limite de mensagens do plano gratuito
- RN14: Atualizações no canvas feitas via chat individual são refletidas para todos os agentes no próximo turno

---

### F05 — Canvas Vivo

**Descrição:** Visualização estruturada do negócio, auto-preenchida por conversas dos grupos e individuais. O founder nunca preenche nada manualmente — o canvas emerge das conversas.

**Zonas do Canvas:**

| Zona | Quem preenche | Trigger |
|---|---|---|
| Proposta de Valor | CEO Agent | Onboarding + conversa sobre produto |
| Segmentos de Clientes | CEO + CMO | Conversa sobre mercado |
| Canais de Aquisição | CMO Agent | Conversa sobre go-to-market |
| Modelo de Receita | CFO Agent | Conversa sobre precificação |
| Estrutura de Custos | CFO Agent | Conversa sobre finanças |
| Recursos-Chave | CTO Agent | Conversa sobre tecnologia |
| Métricas de Sucesso | CEO Agent | Conversa sobre objetivos |

**User Stories:**
- Como founder, quero ver meu modelo de negócio organizado visualmente sem preencher nada
- Como founder, quero saber quais zonas estão em branco para entender o que ainda não pensei
- Como founder, quero exportar o canvas como PDF

**Critérios de Aceite:**
- [ ] Canvas exibe todas as zonas com status: preenchido (verde), parcial (amarelo), vazio (cinza)
- [ ] Zonas preenchidas mostram conteúdo extraído das conversas
- [ ] Zonas vazias mostram qual agente pode ajudar e sugestão de pergunta para iniciar
- [ ] Canvas atualiza automaticamente após conversas relevantes (grupo ou individual)
- [ ] Cada zona exibe autoria: "CEO preencheu via chat em 22/06"
- [ ] Exportação como PDF disponível (via print/CSS no v1)
- [ ] Todos os agentes têm acesso ao estado atual do canvas como contexto

**Regras de Negócio:**
- RN15: Canvas não é editável manualmente — apenas via conversa
- RN16: Sistema identifica informações relevantes nas conversas e atualiza canvas em background
- RN17: Quando uma zona é atualizada, versão anterior é preservada no histórico
- RN18: Canvas atualizado é injetado no context de todos os agentes no próximo turno — se o founder conversa no individual com o CTO e atualiza "Recursos-Chave", o CEO Agent já terá essa informação disponível quando o founder abrir o grupo novamente

---

### F06 — Criar Produto (via CTO Agent)

**Descrição:** Founder cadastra produtos da startup via chat com o CTO Agent. O acesso pode ser feito por dois caminhos equivalentes: pelo botão nas configurações da startup, ou diretamente abrindo o chat individual do CTO.

**Fluxo (via configurações):**
1. Founder acessa **Configurações da Startup → Produtos → "+ Novo Produto"**
2. Abre chat dedicado com o CTO Agent (mesma experiência do chat individual)
3. CTO conduz a conversa para capturar os dados do produto
4. Produto criado aparece listado nas configurações e fica disponível como contexto para todos os agentes

**Fluxo alternativo (via chat individual do CTO):**
1. Founder abre chat privado com o CTO Agent
2. Menciona que quer criar um novo produto
3. CTO conduz o mesmo fluxo de perguntas
4. Produto é criado identicamente ao fluxo anterior

**Dados capturados:**
- Nome, descrição, tipo (SaaS/Marketplace/App/Hardware/Serviço/Outro), preço atual ou pretendido, estágio (ideia/protótipo/MVP/lançado)

**Critérios de Aceite:**
- [ ] CTO Agent conduz conversa para criar o produto
- [ ] Produto aparece listado no perfil da startup
- [ ] Todos os agentes passam a referenciar o produto em conversas futuras
- [ ] Founder pode ter mais de um produto por startup
- [ ] Produto editável via configurações

**Regras de Negócio:**
- RN19: Máximo de 2 produtos por startup no plano gratuito

---

### F07 — Planejamento (TODO Simplificado)

**Descrição:** Lista de próximos passos gerada pelos agentes ao longo das conversas, com checkbox para acompanhamento.

**User Stories:**
- Como founder, quero ter uma lista clara do que fazer a seguir, baseada nas orientações dos agentes
- Como founder, quero marcar tarefas como concluídas para acompanhar meu progresso

**Sobre agentes marcando tarefas como concluídas:**
Os agentes **não marcam tarefas como concluídas autonomamente**. Porém, podem **sugerir** a conclusão quando o founder relata progresso na conversa. Ex: founder diz "já validei com 5 clientes" → CFO responde "ótimo! posso marcar a tarefa 'validar com 5 clientes' como concluída?" → founder confirma → sistema atualiza. A confirmação final é sempre do founder.

**Critérios de Aceite:**
- [ ] Agentes sugerem "adicionar ao planejamento" ao longo da conversa
- [ ] Founder aceita ou recusa cada sugestão individualmente
- [ ] Lista exibe: tarefa, agente que sugeriu, data, checkbox de conclusão
- [ ] Agentes podem sugerir marcar tarefas como concluídas com base no relato do founder
- [ ] Confirmação de conclusão é sempre do founder
- [ ] Tarefas concluídas ficam riscadas mas visíveis
- [ ] Máximo de 10 tarefas ativas no plano gratuito

**Regras de Negócio:**
- RN20: Tarefas vinculadas à startup ativa no momento da criação
- RN21: Tarefas não têm prazo obrigatório no v1

---

### F08 — Simulação TME (Teaser — Bloqueada no MVP v1)

**Descrição:** Tela de simulação existe mas está bloqueada. Objetivo: plantar expectativa do produto premium e capturar interesse antes de construir.

**O que a tela de teaser mostra:**
- Título: "Simule sua startup no mercado sintético"
- Descrição do output: "Receba um relatório com % de adoção por faixa de preço, principais objeções do seu segmento e projeção de 12 meses — em horas, não meses"
- Preview mockado de como o relatório se parece (não é real)
- Preço por experimento (a definir)
- Botão "Quero simular" → captura e-mail mesmo antes de estar disponível

**Critérios de Aceite:**
- [ ] Tela existe e é acessível pelo menu
- [ ] Comunica claramente o valor do produto
- [ ] Botão captura e-mail do interessado
- [ ] Nenhuma lógica de simulação real roda no v1

**Regras de Negócio:**
- RN22: Lista de interessados armazenada para contato quando TME for lançado

---

## 4. Funcionalidades FORA do Escopo do MVP v1

| Funcionalidade | Motivo | Versão alvo |
|---|---|---|
| Simulação TME completa | Alta complexidade; validar demanda primeiro | v2 |
| Experimento com pessoas reais (anúncios) | Requer infra de ads, templates, orçamento de anúncio | v3+ |
| Geração de landing page do produto | Depende de TME e templates complexos | v3+ |
| Captação de recursos (editais, investidores) | Produto distinto, fora do foco | Futuro |
| Network entre founders | Rede social — produto distinto | Futuro |
| Login social | Nice-to-have | v2 |
| App mobile nativo | Web responsivo resolve no v1 | v2 |
| Multi-idioma | Foco no Brasil no v1 | v2 |

---

## 5. Requisitos Não-Funcionais

### 5.1 Segurança
- **RNF01:** Todas as rotas autenticadas requerem JWT válido
- **RNF02:** Rate limiting nos endpoints de LLM (máx. 10 req/min por usuário)
- **RNF03:** Rate limiting no endpoint de auth (máx. 5 tentativas/min por IP)
- **RNF04:** API keys em variáveis de ambiente — nunca hardcoded
- **RNF05:** HTTPS obrigatório em produção
- **RNF06:** Inputs sanitizados antes de passar ao LLM (proteção contra prompt injection)
- **RNF07:** Dados de um founder nunca acessíveis por outro usuário

### 5.2 LGPD
- **RNF08:** Política de privacidade clara antes do cadastro
- **RNF09:** Consentimento explícito para coleta de dados de negócio
- **RNF10:** Founder pode solicitar exclusão total dos seus dados
- **RNF11:** Dados de conversas não usados para treinar modelos sem consentimento

### 5.3 Performance
- **RNF12:** Streaming de tokens obrigatório — não esperar resposta completa para exibir
- **RNF13:** Tempo para primeiro token < 3 segundos
- **RNF14:** Carregamento inicial da aplicação < 3 segundos
- **RNF15:** Canvas atualiza em background sem bloquear a interface

### 5.4 Escalabilidade
- **RNF16:** Sistema de agentes configurável — adicionar novo agente sem reescrever código (config-driven)
- **RNF17:** Sliding window no histórico de conversa para controle de tokens

### 5.5 Observabilidade
- **RNF18:** Deploy automatizado via CI/CD (GitHub Actions)
- **RNF19:** Logs de erro em produção (Sentry ou similar)
- **RNF20:** Monitoramento de custo de API de LLM por usuário

---

## 6. Modelo de Dados (Rascunho)

```
users
  id, email, password_hash, created_at, plan (free | pro)

startups
  id                    UUID PK DEFAULT gen_random_uuid()
  user_id               UUID FK → auth.users (ON DELETE CASCADE)
  name                  VARCHAR(255) NOT NULL
  description           TEXT
  problem               TEXT
  solution              TEXT
  segment               VARCHAR(255)
  target_location       VARCHAR(255)
  stage                 ENUM (idea | mvp | launched) DEFAULT idea
  primary_revenue_model ENUM (subscription | saas | marketplace | freemium |
                              pay_per_use | licensing | advertising |
                              e_commerce | service | hardware | other)
  revenue_model_details TEXT
  status                ENUM (active | archived) DEFAULT active
  created_at            TIMESTAMPTZ DEFAULT NOW()
  updated_at            TIMESTAMPTZ DEFAULT NOW() [auto via trigger]

products
  id, startup_id, name, description, type, price, stage, created_at

conversations
  id, startup_id, type (group | ceo | cto | cfo | cmo), created_at

messages
  id, conversation_id, role (user | agent), agent_name, content, created_at

canvas_zones
  id, startup_id, zone_key, content, filled_by (agent_name),
  updated_at, previous_content

planning_items
  id, startup_id, content, suggested_by (agent_name),
  completed, completed_at, created_at

simulation_interests
  id, user_id, startup_id, email, created_at
```

---

## 7. Landing Page — Seções

1. **Hero** — problema em 1 frase + solução em 1 frase + CTA (lista de espera / beta)
2. **Como funciona** — 4 passos visuais: Identificação → Trilho → Simulação → Agentes
3. **Preview da experiência** — screenshot ou animação do chat com os conselheiros
4. **Diferencial** — dados vs. conselho (ênfase no relatório TME, não no chat)
5. **Prova social** — Ada Metaverse como primeiro cliente validador (com permissão de Tássia)
6. **Preços** — Freemium + pay-per-experiment para simulação
7. **CTA final** — lista de espera ou acesso ao beta

---

## 8. Sprint de 1 Semana

| Dia | Entregável |
|---|---|
| Seg–Ter | Landing page repaginada |
| Qua | Auth (Supabase) + criar startup via conversa |
| Qui–Sex | Board Executivo — chat em grupo e individual |
| Sáb | Canvas Vivo + tela teaser TME + deploy |
| Dom | Teste completo com Tássia |

---

## 9. Stack Recomendada

| Camada | Tecnologia | Justificativa |
|---|---|---|
| Frontend | Next.js + Tailwind | Samir já conhece do ApexPlan |
| Backend | FastAPI (Python) | Ponto forte de Samir |
| Auth | Supabase Auth | Pronto e gratuito — não construir do zero |
| Banco | PostgreSQL via Supabase | Mesma instância do auth |
| LLM | Claude API (claude-sonnet-4-6) | Melhor custo-benefício para conversação |
| Deploy frontend | Vercel | Um comando, CI/CD automático |
| Deploy backend | Railway ou Render | Simples, sem DevOps |
| Vibe coding | Antigravity / Claude Code | Acelerar scaffold — revisar tudo antes do push |
| Erros | Sentry | Monitoramento em produção |

---

*Próximos passos: (1) Wireframes de alto nível das telas, (2) Modelagem final do banco, (3) System prompts base dos agentes, (4) Repaginação da landing page*

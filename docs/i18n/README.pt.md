---
**🌍 Languages / Jazyky / 语言:**
[English](README.en.md) | [Čeština](README.cs.md) | [Español](README.es.md) | [简体中文](README.zh-CN.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Русский](README.ru.md) | [Português](README.pt.md) | [हिन्दी](README.hi.md) | [العربية](README.ar.md) | [বাংলা](README.bn.md) | [Italiano](README.it.md) | [Türkçe](README.tr.md) | [Tiếng Việt](README.vi.md) | [Polski](README.pl.md) | [Українська](README.uk.md) | [Nederlands](README.nl.md) | [ไทย](README.th.md) | [Română](README.ro.md) | [Ελληνικά](README.el.md) | [Magyar](README.hu.md) | [Svenska](README.sv.md) | [Bahasa Indonesia](README.id.md) | [فارسی](README.fa.md) | [עברית](README.he.md) | [Bahasa Melayu](README.ms.md) | [Norsk](README.no.md) | [Slovenčina](README.sk.md) | [Suomi](README.fi.md) | [Dansk](README.da.md)
---

# 🔄 SpinThatShit

**Orquestração Autônoma de Agentes de IA para Desenvolvimento de Software**

Um sistema para gerenciar múltiplos agentes de IA (Claude Code CLI) que colaboram no desenvolvimento de software. Cada agente tem um papel específico e o sistema garante a continuidade do trabalho mesmo quando os limites de contexto são atingidos.

---

## 🚀 Início Rápido

```bash
# Instalação
chmod +x install.sh
./install.sh

# Executar
spinthatshit
# ou mais curto
sts
```

---

## 📋 Recursos

### Fluxo de Trabalho Multi-Agente
- **Planner** - Analisa documentação, cria plano
- **Designer** - Projeta componentes UI/UX
- **Engineer** - Constrói infraestrutura e arquitetura
- **Developer** - Implementa funcionalidades
- **Reviewer** - Revisa qualidade do código
- **Tester** - Testa funcionalidade
- **Supervisor** - Identifica conflitos e problemas
- **Evolver** - Melhora o próprio sistema

### Gerenciamento de Contexto
- Rastreamento automático do uso de contexto
- Transferência aos 50% do limite
- Continuidade do trabalho entre agentes

### Integração com Git
- Commit automático após cada alteração
- Marcação de fases
- Auto-push para GitHub

### Auto-Evolução
- Sistema aprende com erros
- Melhora automaticamente os prompts
- Adiciona novas verificações

---

## 📁 Estrutura do Projeto

Após a execução, a seguinte estrutura é criada na pasta de desenvolvimento:

```
your-project/
├── .spinstate/
│   ├── state.json          # Estado da orquestração
│   ├── journal.md          # Diário de todos os agentes
│   ├── plan.md             # Plano do projeto
│   ├── checklist.md        # Lista de tarefas
│   ├── architecture.md     # Arquitetura
│   ├── handoff.md          # Notas de transferência
│   ├── status.txt          # Status atual
│   ├── review.md           # Resultados da revisão
│   ├── test_report.md      # Resultados dos testes
│   └── logs/               # Logs de todos os agentes
├── CLAUDE.md               # Instruções para Claude
└── ... (seu código)
```

---

## 🎯 Uso

### Modo Interativo
```bash
spinthatshit
```

O sistema perguntará:
1. Caminho da documentação
2. Caminho da pasta de desenvolvimento

### Com Parâmetros
```bash
spinthatshit --docs ./docs --dev ./src
```

### Retomar
```bash
spinthatshit --resume
```

---

## ⚙️ Configuração

Arquivo de configuração: `~/.spinthatshit/config.json`

```json
{
    "context_limit_percent": 50,
    "max_retries": 3,
    "agent_timeout_minutes": 30,
    "auto_push": true,
    "agents": {
        "workflow_order": ["planner", "designer", "engineer", ...],
        "enabled": {
            "designer": true,
            "tester": true
        }
    }
}
```

---

## 🔧 Requisitos

- **Python 3.8+**
- **Claude Code CLI** (`npm install -g @anthropic-ai/claude-code`)
- **Git**
- **macOS ou Linux**

---

## 📖 Como Funciona

### 1. Inicialização
O sistema carrega a documentação e o código existente, cria um plano.

### 2. Execução por Fases
Cada agente executa sequencialmente:
1. Carrega contexto do journal.md
2. Realiza seu trabalho
3. Faz commit das alterações
4. Escreve na checklist
5. Transfere para o próximo agente

### 3. Transferência de Contexto
Quando um agente atinge 50% de contexto:
1. Escreve estado no handoff.md
2. Faz commit de tudo
3. Termina
4. Novo agente continua

### 4. Recuperação
Em caso de falha:
1. Supervisor analisa o problema
2. Orchestrator ajusta as regras
3. Agente reinicia

### 5. Evolução
Após conclusão do projeto:
1. Evolver analisa o que funcionou
2. Ajusta prompts dos agentes
3. Adiciona novas verificações

---

## 🎬 Exemplo de Execução

```
[14:32:01] [PHASE] ========================================
[14:32:01] [PHASE] FASE: PLANNER
[14:32:01] [PHASE] ========================================

[14:32:05] [AGENT] [planner] Reading documentation...
[14:32:12] [AGENT] [planner] Created plan.md
[14:32:18] [AGENT] [planner] Created checklist.md
[14:32:22] [SUCCESS] Commit: [planner] Initial planning complete
[14:32:24] [SUCCESS] Agent planner concluído (contexto: ~15%)

[14:32:25] [PHASE] ========================================
[14:32:25] [PHASE] FASE: DEVELOPER
[14:32:25] [PHASE] ========================================

[14:32:30] [AGENT] [developer] Starting backend API...
[14:35:45] [WARNING] Contexto em 52% - transferindo para próximo agente
[14:35:48] [INFO] Reiniciando agente developer (tentativa 1/3)
...
```

---

## 🛑 Parar

- **Ctrl+C** - Parada segura, estado é salvo
- Use `--resume` para continuar

---

## 🐛 Solução de Problemas

### Agente travado
```bash
# Verifique os logs
cat your-project/.spinstate/logs/agent_*.log
```

### Erros no código
Sistema tem auto-recuperação, mas você pode:
1. Editar `.spinstate/checklist.md`
2. Adicionar nota em `.spinstate/journal.md`
3. Executar novamente

### Estouro de contexto
- Aumente `context_limit_percent` no config.json
- Divida o projeto em fases menores

---

## 📝 Dicas

1. **Documentação é chave** - Melhor documentação, melhores resultados
2. **Comece com projetos pequenos** - Aprenda o sistema em um projeto simples
3. **Não verifique cada passo** - Deixe os agentes trabalharem
4. **Confie nas transferências** - Sistema lembra o contexto

---

## 🗑️ Desinstalação

```bash
~/.spinthatshit/uninstall.sh
```

---

## 📜 Licença

MIT License - Uso livre

---

## 🤝 Criado para

Martin @ Praut s.r.o.
AI Integration & Business Automation

---

*"Deixamos a IA trabalhar enquanto comemos bolo."* 🍰

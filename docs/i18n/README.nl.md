> **🌍 Languages / Jazyky / 语言:**
[English](README.en.md) | [Čeština](README.cs.md) | [Español](README.es.md) | [简体中文](README.zh-CN.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Русский](README.ru.md) | [Português](README.pt.md) | [हिन्दी](README.hi.md) | [العربية](README.ar.md) | [বাংলা](README.bn.md) | [Italiano](README.it.md) | [Türkçe](README.tr.md) | [Tiếng Việt](README.vi.md) | [Polski](README.pl.md) | [Українська](README.uk.md) | [Nederlands](README.nl.md) | [ไทย](README.th.md) | [Română](README.ro.md) | [Ελληνικά](README.el.md) | [Magyar](README.hu.md) | [Svenska](README.sv.md) | [Bahasa Indonesia](README.id.md) | [فارسی](README.fa.md) | [עברית](README.he.md) | [Bahasa Melayu](README.ms.md) | [Norsk](README.no.md) | [Slovenčina](README.sk.md) | [Suomi](README.fi.md) | [Dansk](README.da.md)


# 🔄 SpinThatShit

**Autonome AI Agent Orchestratie voor Softwareontwikkeling**

Een systeem voor het beheren van meerdere AI-agenten (Claude Code CLI) die samenwerken aan softwareontwikkeling. Elke agent heeft een specifieke rol en het systeem garandeert continuïteit van het werk, zelfs wanneer contextlimieten worden bereikt.

---

## 🚀 Snelle Start

```bash
# Installatie
chmod +x install.sh
./install.sh

# Uitvoeren
spinthatshit
# of korter
sts
```

---

## 📋 Functies

### Multi-Agent Workflow
- **Planner** - Analyseert documentatie, creëert plan
- **Designer** - Ontwerpt UI/UX componenten
- **Engineer** - Bouwt infrastructuur en architectuur
- **Developer** - Implementeert functionaliteit
- **Reviewer** - Controleert codekwaliteit
- **Tester** - Test functionaliteit
- **Supervisor** - Identificeert conflicten en problemen
- **Evolver** - Verbetert het systeem zelf

### Contextbeheer
- Automatische tracking van contextgebruik
- Overdracht bij 50% limiet
- Werkcontinuïteit tussen agenten

### Git Integratie
- Automatische commit na elke wijziging
- Fase tagging
- Auto-push naar GitHub

### Zelf-Evolutie
- Systeem leert van fouten
- Verbetert automatisch prompts
- Voegt nieuwe controles toe

---

## 📁 Projectstructuur

Na uitvoering wordt de volgende structuur aangemaakt in de ontwikkelmap:

```
your-project/
├── .spinstate/
│   ├── state.json          # Orchestratie status
│   ├── journal.md          # Logboek van alle agenten
│   ├── plan.md             # Projectplan
│   ├── checklist.md        # Takenlijst
│   ├── architecture.md     # Architectuur
│   ├── handoff.md          # Overdrachtsnotities
│   ├── status.txt          # Huidige status
│   ├── review.md           # Review resultaten
│   ├── test_report.md      # Testresultaten
│   └── logs/               # Logs van alle agenten
├── CLAUDE.md               # Instructies voor Claude
└── ... (jouw code)
```

---

## 🎯 Gebruik

### Interactieve Modus
```bash
spinthatshit
```

Het systeem zal vragen om:
1. Documentatiepad
2. Ontwikkelmappad

### Met Parameters
```bash
spinthatshit --docs ./docs --dev ./src
```

### Hervatten
```bash
spinthatshit --resume
```

---

## ⚙️ Configuratie

Configuratiebestand: `~/.spinthatshit/config.json`

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

## 🔧 Vereisten

- **Python 3.8+**
- **Claude Code CLI** (`npm install -g @anthropic-ai/claude-code`)
- **Git**
- **macOS of Linux**

---

## 📖 Hoe Het Werkt

### 1. Initialisatie
Systeem laadt documentatie en bestaande code, creëert een plan.

### 2. Fase Uitvoering
Elke agent draait sequentieel:
1. Laadt context van journal.md
2. Voert zijn werk uit
3. Commit wijzigingen
4. Schrijft naar checklist
5. Draagt over aan volgende agent

### 3. Context Overdracht
Wanneer een agent 50% context bereikt:
1. Schrijft status naar handoff.md
2. Commit alles
3. Beëindigt
4. Nieuwe agent gaat verder

### 4. Herstel
Bij falen:
1. Supervisor analyseert probleem
2. Orchestrator past regels aan
3. Agent herstart

### 5. Evolutie
Na projectafronding:
1. Evolver analyseert wat werkte
2. Past agent prompts aan
3. Voegt nieuwe controles toe

---

## 🎬 Voorbeeld Uitvoering

```
[14:32:01] [PHASE] ========================================
[14:32:01] [PHASE] FASE: PLANNER
[14:32:01] [PHASE] ========================================

[14:32:05] [AGENT] [planner] Reading documentation...
[14:32:12] [AGENT] [planner] Created plan.md
[14:32:18] [AGENT] [planner] Created checklist.md
[14:32:22] [SUCCESS] Commit: [planner] Initial planning complete
[14:32:24] [SUCCESS] Agent planner voltooid (context: ~15%)

[14:32:25] [PHASE] ========================================
[14:32:25] [PHASE] FASE: DEVELOPER
[14:32:25] [PHASE] ========================================

[14:32:30] [AGENT] [developer] Starting backend API...
[14:35:45] [WARNING] Context op 52% - overdracht aan volgende agent
[14:35:48] [INFO] Herstart agent developer (poging 1/3)
...
```

---

## 🛑 Stoppen

- **Ctrl+C** - Veilig stoppen, status wordt opgeslagen
- Gebruik `--resume` om door te gaan

---

## 🐛 Probleemoplossing

### Agent is vastgelopen
```bash
# Controleer de logs
cat your-project/.spinstate/logs/agent_*.log
```

### Codefouten
Systeem heeft auto-recovery, maar je kunt:
1. `.spinstate/checklist.md` bewerken
2. Notitie toevoegen aan `.spinstate/journal.md`
3. Opnieuw uitvoeren

### Context overflow
- Verhoog `context_limit_percent` in config.json
- Verdeel project in kleinere fases

---

## 📝 Tips

1. **Documentatie is key** - Betere documentatie, betere resultaten
2. **Begin met kleine projecten** - Leer het systeem op een eenvoudig project
3. **Controleer niet elke stap** - Laat de agenten werken
4. **Vertrouw overdrachten** - Systeem onthoudt context

---

## 🗑️ Deïnstallatie

```bash
~/.spinthatshit/uninstall.sh
```

---

## 📜 Licentie

MIT License - Vrij te gebruiken

---

## 🤝 Gemaakt voor

Martin @ Praut s.r.o.
AI Integration & Business Automation

---

*"We laten AI werken terwijl we taart eten."* 🍰

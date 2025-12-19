---
**🌍 Languages / Jazyky / 语言:**
[English](README.en.md) | [Čeština](README.cs.md) | [Español](README.es.md) | [简体中文](README.zh-CN.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Русский](README.ru.md) | [Português](README.pt.md) | [हिन्दी](README.hi.md) | [العربية](README.ar.md) | [বাংলা](README.bn.md) | [Italiano](README.it.md) | [Türkçe](README.tr.md) | [Tiếng Việt](README.vi.md) | [Polski](README.pl.md) | [Українська](README.uk.md) | [Nederlands](README.nl.md) | [ไทย](README.th.md) | [Română](README.ro.md) | [Ελληνικά](README.el.md) | [Magyar](README.hu.md) | [Svenska](README.sv.md) | [Bahasa Indonesia](README.id.md) | [فارسی](README.fa.md) | [עברית](README.he.md) | [Bahasa Melayu](README.ms.md) | [Norsk](README.no.md) | [Slovenčina](README.sk.md) | [Suomi](README.fi.md) | [Dansk](README.da.md)
---

# 🔄 SpinThatShit

**Autonom AI-agent Orkestrering til Softwareudvikling**

Et system til at håndtere flere AI-agenter (Claude Code CLI), der samarbejder om softwareudvikling. Hver agent har en specifik rolle, og systemet sikrer arbejdets kontinuitet selv når kontekstgrænser nås.

---

## 🚀 Hurtig Start

```bash
# Installation
chmod +x install.sh
./install.sh

# Kør
spinthatshit
# eller kortere
sts
```

---

## 📋 Funktioner

### Multi-Agent Workflow
- **Planner** - Analyserer dokumentation, opretter plan
- **Designer** - Designer UI/UX-komponenter
- **Engineer** - Bygger infrastruktur og arkitektur
- **Developer** - Implementerer funktioner
- **Reviewer** - Gennemgår kodekvalitet
- **Tester** - Tester funktionalitet
- **Supervisor** - Identificerer konflikter og problemer
- **Evolver** - Forbedrer systemet selv

### Kontekststyring
- Automatisk sporing af kontekstbrug
- Overlevering ved 50% grænse
- Arbejdskontinuitet mellem agenter

### Git Integration
- Automatisk commit efter hver ændring
- Fasemarkering
- Auto-push til GitHub

### Selv-Evolution
- Systemet lærer af fejl
- Forbedrer automatisk prompts
- Tilføjer nye kontroller

---

## 📁 Projektstruktur

Efter kørsel oprettes følgende struktur i udviklingsmappen:

```
your-project/
├── .spinstate/
│   ├── state.json          # Orkestreringstilstand
│   ├── journal.md          # Journal for alle agenter
│   ├── plan.md             # Projektplan
│   ├── checklist.md        # Opgaveliste
│   ├── architecture.md     # Arkitektur
│   ├── handoff.md          # Overleveringsnotater
│   ├── status.txt          # Nuværende status
│   ├── review.md           # Gennemgangsresultater
│   ├── test_report.md      # Testresultater
│   └── logs/               # Logs for alle agenter
├── CLAUDE.md               # Instruktioner til Claude
└── ... (din kode)
```

---

## 🎯 Brug

### Interaktiv Tilstand
```bash
spinthatshit
```

Systemet vil spørge om:
1. Dokumentationssti
2. Udviklingsmappesti

### Med Parametre
```bash
spinthatshit --docs ./docs --dev ./src
```

### Genoptag
```bash
spinthatshit --resume
```

---

## ⚙️ Konfiguration

Konfigurationsfil: `~/.spinthatshit/config.json`

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

## 🔧 Krav

- **Python 3.8+**
- **Claude Code CLI** (`npm install -g @anthropic-ai/claude-code`)
- **Git**
- **macOS eller Linux**

---

## 📖 Hvordan Det Virker

### 1. Initialisering
Systemet indlæser dokumentation og eksisterende kode, opretter en plan.

### 2. Faseudførelse
Hver agent kører sekventielt:
1. Indlæser kontekst fra journal.md
2. Udfører sit arbejde
3. Committer ændringer
4. Skriver til tjekliste
5. Overfører til næste agent

### 3. Kontekstoverføring
Når en agent når 50% kontekst:
1. Skriver tilstand til handoff.md
2. Committer alt
3. Afsluttes
4. Ny agent fortsætter

### 4. Genopretning
Ved fejl:
1. Supervisor analyserer problemet
2. Orchestrator justerer regler
3. Agent genstarter

### 5. Evolution
Efter projektafslutning:
1. Evolver analyserer hvad der virkede
2. Justerer agentprompts
3. Tilføjer nye kontroller

---

## 🎬 Eksempel på Kørsel

```
[14:32:01] [PHASE] ========================================
[14:32:01] [PHASE] FASE: PLANNER
[14:32:01] [PHASE] ========================================

[14:32:05] [AGENT] [planner] Reading documentation...
[14:32:12] [AGENT] [planner] Created plan.md
[14:32:18] [AGENT] [planner] Created checklist.md
[14:32:22] [SUCCESS] Commit: [planner] Initial planning complete
[14:32:24] [SUCCESS] Agent planner færdig (kontekst: ~15%)

[14:32:25] [PHASE] ========================================
[14:32:25] [PHASE] FASE: DEVELOPER
[14:32:25] [PHASE] ========================================

[14:32:30] [AGENT] [developer] Starting backend API...
[14:35:45] [WARNING] Kontekst ved 52% - overfører til næste agent
[14:35:48] [INFO] Genstarter agent developer (forsøg 1/3)
...
```

---

## 🛑 Stop

- **Ctrl+C** - Sikker stop, tilstand gemmes
- Brug `--resume` for at fortsætte

---

## 🐛 Fejlfinding

### Agent er hængt
```bash
# Tjek loggene
cat your-project/.spinstate/logs/agent_*.log
```

### Kodefejl
Systemet har auto-recovery, men du kan:
1. Redigere `.spinstate/checklist.md`
2. Tilføje en note til `.spinstate/journal.md`
3. Køre igen

### Kontekstoverløb
- Øg `context_limit_percent` i config.json
- Del projektet op i mindre faser

---

## 📝 Tips

1. **Dokumentation er nøglen** - Bedre dokumentation, bedre resultater
2. **Start med små projekter** - Lær systemet på et simpelt projekt
3. **Tjek ikke hvert trin** - Lad agenterne arbejde
4. **Stol på overførsler** - Systemet husker kontekst

---

## 🗑️ Afinstallation

```bash
~/.spinthatshit/uninstall.sh
```

---

## 📜 Licens

MIT License - Fri til brug

---

## 🤝 Skabt til

Martin @ Praut s.r.o.
AI Integration & Business Automation

---

*"Vi lader AI arbejde mens vi spiser kage."* 🍰

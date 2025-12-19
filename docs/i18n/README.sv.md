> **🌍 Languages / Jazyky / 语言:**
[English](README.en.md) | [Čeština](README.cs.md) | [Español](README.es.md) | [简体中文](README.zh-CN.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Русский](README.ru.md) | [Português](README.pt.md) | [हिन्दी](README.hi.md) | [العربية](README.ar.md) | [বাংলা](README.bn.md) | [Italiano](README.it.md) | [Türkçe](README.tr.md) | [Tiếng Việt](README.vi.md) | [Polski](README.pl.md) | [Українська](README.uk.md) | [Nederlands](README.nl.md) | [ไทย](README.th.md) | [Română](README.ro.md) | [Ελληνικά](README.el.md) | [Magyar](README.hu.md) | [Svenska](README.sv.md) | [Bahasa Indonesia](README.id.md) | [فارسی](README.fa.md) | [עברית](README.he.md) | [Bahasa Melayu](README.ms.md) | [Norsk](README.no.md) | [Slovenčina](README.sk.md) | [Suomi](README.fi.md) | [Dansk](README.da.md)


# 🔄 SpinThatShit

**Autonom AI-agentorkestrering för mjukvaruutveckling**

Ett system för att hantera flera AI-agenter (Claude Code CLI) som samarbetar i mjukvaruutveckling. Varje agent har en specifik roll och systemet säkerställer arbetets kontinuitet även när kontextgränser nås.

---

## 🚀 Snabbstart

```bash
# Installation
chmod +x install.sh
./install.sh

# Kör
spinthatshit
# eller kortare
sts
```

---

## 📋 Funktioner

### Multiagent-arbetsflöde
- **Planner** - Analyserar dokumentation, skapar plan
- **Designer** - Designar UI/UX-komponenter
- **Engineer** - Bygger infrastruktur och arkitektur
- **Developer** - Implementerar funktioner
- **Reviewer** - Granskar kodkvalitet
- **Tester** - Testar funktionalitet
- **Supervisor** - Identifierar konflikter och problem
- **Evolver** - Förbättrar systemet självt

### Kontexthantering
- Automatisk spårning av kontextanvändning
- Överlämning vid 50% gräns
- Arbetskontinuitet mellan agenter

### Git-integration
- Automatisk commit efter varje ändring
- Fasmärkning
- Auto-push till GitHub

### Själv-evolution
- Systemet lär sig av misstag
- Förbättrar automatiskt prompter
- Lägger till nya kontroller

---

## 📁 Projektstruktur

Efter körning skapas följande struktur i utvecklingsmappen:

```
your-project/
├── .spinstate/
│   ├── state.json          # Orkestreringstillstånd
│   ├── journal.md          # Journal för alla agenter
│   ├── plan.md             # Projektplan
│   ├── checklist.md        # Uppgiftslista
│   ├── architecture.md     # Arkitektur
│   ├── handoff.md          # Överlämningsanteckningar
│   ├── status.txt          # Nuvarande status
│   ├── review.md           # Granskningsresultat
│   ├── test_report.md      # Testresultat
│   └── logs/               # Loggar för alla agenter
├── CLAUDE.md               # Instruktioner för Claude
└── ... (din kod)
```

---

## 🎯 Användning

### Interaktivt läge
```bash
spinthatshit
```

Systemet kommer att fråga om:
1. Dokumentationssökväg
2. Utvecklingsmappsökväg

### Med parametrar
```bash
spinthatshit --docs ./docs --dev ./src
```

### Återuppta
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

## 📖 Hur det fungerar

### 1. Initialisering
Systemet laddar dokumentation och befintlig kod, skapar en plan.

### 2. Fasexekvering
Varje agent körs sekventiellt:
1. Laddar kontext från journal.md
2. Utför sitt arbete
3. Committar ändringar
4. Skriver till checklista
5. Överlämnar till nästa agent

### 3. Kontextöverlämning
När en agent når 50% kontext:
1. Skriver tillstånd till handoff.md
2. Committar allt
3. Avslutar
4. Ny agent fortsätter

### 4. Återhämtning
Vid fel:
1. Supervisor analyserar problemet
2. Orchestrator justerar regler
3. Agenten startar om

### 5. Evolution
Efter projektavslut:
1. Evolver analyserar vad som fungerade
2. Justerar agentprompter
3. Lägger till nya kontroller

---

## 🎬 Exempelkörning

```
[14:32:01] [PHASE] ========================================
[14:32:01] [PHASE] FAS: PLANNER
[14:32:01] [PHASE] ========================================

[14:32:05] [AGENT] [planner] Reading documentation...
[14:32:12] [AGENT] [planner] Created plan.md
[14:32:18] [AGENT] [planner] Created checklist.md
[14:32:22] [SUCCESS] Commit: [planner] Initial planning complete
[14:32:24] [SUCCESS] Agent planner klar (kontext: ~15%)

[14:32:25] [PHASE] ========================================
[14:32:25] [PHASE] FAS: DEVELOPER
[14:32:25] [PHASE] ========================================

[14:32:30] [AGENT] [developer] Starting backend API...
[14:35:45] [WARNING] Kontext vid 52% - överlämning till nästa agent
[14:35:48] [INFO] Omstart av agent developer (försök 1/3)
...
```

---

## 🛑 Stoppa

- **Ctrl+C** - Säker stopp, tillstånd sparas
- Använd `--resume` för att fortsätta

---

## 🐛 Felsökning

### Agenten har fastnat
```bash
# Kontrollera loggarna
cat your-project/.spinstate/logs/agent_*.log
```

### Kodfel
Systemet har auto-recovery, men du kan:
1. Redigera `.spinstate/checklist.md`
2. Lägg till anteckning i `.spinstate/journal.md`
3. Kör igen

### Kontextöverflöde
- Öka `context_limit_percent` i config.json
- Dela upp projektet i mindre faser

---

## 📝 Tips

1. **Dokumentation är nyckeln** - Bättre dokumentation, bättre resultat
2. **Börja med små projekt** - Lär dig systemet på ett enkelt projekt
3. **Kontrollera inte varje steg** - Låt agenterna arbeta
4. **Lita på överlämningar** - Systemet kommer ihåg kontext

---

## 🗑️ Avinstallation

```bash
~/.spinthatshit/uninstall.sh
```

---

## 📜 Licens

MIT License - Fritt att använda

---

## 🤝 Skapad för

Martin @ Praut s.r.o.
AI Integration & Business Automation

---

*"Vi låter AI arbeta medan vi äter tårta."* 🍰

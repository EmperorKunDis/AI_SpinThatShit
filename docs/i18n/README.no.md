---
**🌍 Languages / Jazyky / 语言:**
[English](README.en.md) | [Čeština](README.cs.md) | [Español](README.es.md) | [简体中文](README.zh-CN.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Русский](README.ru.md) | [Português](README.pt.md) | [हिन्दी](README.hi.md) | [العربية](README.ar.md) | [বাংলা](README.bn.md) | [Italiano](README.it.md) | [Türkçe](README.tr.md) | [Tiếng Việt](README.vi.md) | [Polski](README.pl.md) | [Українська](README.uk.md) | [Nederlands](README.nl.md) | [ไทย](README.th.md) | [Română](README.ro.md) | [Ελληνικά](README.el.md) | [Magyar](README.hu.md) | [Svenska](README.sv.md) | [Bahasa Indonesia](README.id.md) | [فارسی](README.fa.md) | [עברית](README.he.md) | [Bahasa Melayu](README.ms.md) | [Norsk](README.no.md) | [Slovenčina](README.sk.md) | [Suomi](README.fi.md) | [Dansk](README.da.md)
---

# 🔄 SpinThatShit

**Autonom AI-agentorkestrer for programvareutvikling**

Et system for å administrere flere AI-agenter (Claude Code CLI) som samarbeider om programvareutvikling. Hver agent har en spesifikk rolle og systemet sikrer kontinuitet i arbeidet selv når kontekstgrenser nås.

---

## 🚀 Hurtigstart

```bash
# Installasjon
chmod +x install.sh
./install.sh

# Kjør
spinthatshit
# eller kortere
sts
```

---

## 📋 Funksjoner

### Multi-Agent Arbeidsflyt
- **Planner** - Analyserer dokumentasjon, lager plan
- **Designer** - Designer UI/UX-komponenter
- **Engineer** - Bygger infrastruktur og arkitektur
- **Developer** - Implementerer funksjoner
- **Reviewer** - Gjennomgår kodekvalitet
- **Tester** - Tester funksjonalitet
- **Supervisor** - Identifiserer konflikter og problemer
- **Evolver** - Forbedrer systemet selv

### Konteksthåndtering
- Automatisk sporing av kontekstbruk
- Overlevering ved 50% grense
- Arbeidskontinuitet mellom agenter

### Git-integrasjon
- Automatisk commit etter hver endring
- Fasemerking
- Auto-push til GitHub

### Selv-evolusjon
- Systemet lærer av feil
- Forbedrer automatisk prompts
- Legger til nye kontroller

---

## 📁 Prosjektstruktur

Etter kjøring opprettes følgende struktur i utviklingsmappen:

```
your-project/
├── .spinstate/
│   ├── state.json          # Orkestreringstilstand
│   ├── journal.md          # Journal for alle agenter
│   ├── plan.md             # Prosjektplan
│   ├── checklist.md        # Oppgaveliste
│   ├── architecture.md     # Arkitektur
│   ├── handoff.md          # Overleveringsnotater
│   ├── status.txt          # Nåværende status
│   ├── review.md           # Gjennomgangsresultater
│   ├── test_report.md      # Testresultater
│   └── logs/               # Logger for alle agenter
├── CLAUDE.md               # Instruksjoner for Claude
└── ... (din kode)
```

---

## 🎯 Bruk

### Interaktiv modus
```bash
spinthatshit
```

Systemet vil spørre om:
1. Dokumentasjonssti
2. Utviklingsmappesti

### Med parametere
```bash
spinthatshit --docs ./docs --dev ./src
```

### Gjenoppta
```bash
spinthatshit --resume
```

---

## ⚙️ Konfigurasjon

Konfigurasjonsfil: `~/.spinthatshit/config.json`

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

## 📖 Hvordan det fungerer

### 1. Initialisering
Systemet laster inn dokumentasjon og eksisterende kode, lager en plan.

### 2. Fasegjennomføring
Hver agent kjører sekvensielt:
1. Laster kontekst fra journal.md
2. Utfører sitt arbeid
3. Committer endringer
4. Skriver til sjekkliste
5. Overfører til neste agent

### 3. Kontekstoverføring
Når en agent når 50% kontekst:
1. Skriver tilstand til handoff.md
2. Committer alt
3. Avslutter
4. Ny agent fortsetter

### 4. Gjenoppretting
Ved feil:
1. Supervisor analyserer problemet
2. Orchestrator justerer regler
3. Agenten starter på nytt

### 5. Evolusjon
Etter prosjektfullføring:
1. Evolver analyserer hva som fungerte
2. Justerer agentprompts
3. Legger til nye kontroller

---

## 🎬 Eksempelkjøring

```
[14:32:01] [PHASE] ========================================
[14:32:01] [PHASE] FASE: PLANNER
[14:32:01] [PHASE] ========================================

[14:32:05] [AGENT] [planner] Reading documentation...
[14:32:12] [AGENT] [planner] Created plan.md
[14:32:18] [AGENT] [planner] Created checklist.md
[14:32:22] [SUCCESS] Commit: [planner] Initial planning complete
[14:32:24] [SUCCESS] Agent planner fullført (kontekst: ~15%)

[14:32:25] [PHASE] ========================================
[14:32:25] [PHASE] FASE: DEVELOPER
[14:32:25] [PHASE] ========================================

[14:32:30] [AGENT] [developer] Starting backend API...
[14:35:45] [WARNING] Kontekst på 52% - overfører til neste agent
[14:35:48] [INFO] Starter agent developer på nytt (forsøk 1/3)
...
```

---

## 🛑 Stopp

- **Ctrl+C** - Sikker stopp, tilstand lagres
- Bruk `--resume` for å fortsette

---

## 🐛 Feilsøking

### Agenten har hengt seg
```bash
# Sjekk loggene
cat your-project/.spinstate/logs/agent_*.log
```

### Kodefeil
Systemet har auto-recovery, men du kan:
1. Redigere `.spinstate/checklist.md`
2. Legge til en merknad i `.spinstate/journal.md`
3. Kjøre på nytt

### Kontekstoverflyt
- Øk `context_limit_percent` i config.json
- Del prosjektet inn i mindre faser

---

## 📝 Tips

1. **Dokumentasjon er nøkkelen** - Bedre dokumentasjon, bedre resultater
2. **Start med små prosjekter** - Lær systemet på et enkelt prosjekt
3. **Ikke sjekk hvert trinn** - La agentene jobbe
4. **Stol på overføringer** - Systemet husker kontekst

---

## 🗑️ Avinstallasjon

```bash
~/.spinthatshit/uninstall.sh
```

---

## 📜 Lisens

MIT License - Fritt å bruke

---

## 🤝 Laget for

Martin @ Praut s.r.o.
AI Integration & Business Automation

---

*"Vi lar AI jobbe mens vi spiser kake."* 🍰

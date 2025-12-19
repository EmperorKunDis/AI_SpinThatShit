> **🌍 Languages / Jazyky / 语言:**
[English](README.en.md) | [Čeština](README.cs.md) | [Español](README.es.md) | [简体中文](README.zh-CN.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Русский](README.ru.md) | [Português](README.pt.md) | [हिन्दी](README.hi.md) | [العربية](README.ar.md) | [বাংলা](README.bn.md) | [Italiano](README.it.md) | [Türkçe](README.tr.md) | [Tiếng Việt](README.vi.md) | [Polski](README.pl.md) | [Українська](README.uk.md) | [Nederlands](README.nl.md) | [ไทย](README.th.md) | [Română](README.ro.md) | [Ελληνικά](README.el.md) | [Magyar](README.hu.md) | [Svenska](README.sv.md) | [Bahasa Indonesia](README.id.md) | [فارسی](README.fa.md) | [עברית](README.he.md) | [Bahasa Melayu](README.ms.md) | [Norsk](README.no.md) | [Slovenčina](README.sk.md) | [Suomi](README.fi.md) | [Dansk](README.da.md)


# 🔄 SpinThatShit

**Orchestrare Autonomă a Agenților AI pentru Dezvoltare Software**

Un sistem pentru gestionarea mai multor agenți AI (Claude Code CLI) care colaborează la dezvoltarea de software. Fiecare agent are un rol specific iar sistemul asigură continuitatea muncii chiar și când sunt atinse limitele de context.

---

## 🚀 Start Rapid

```bash
# Instalare
chmod +x install.sh
./install.sh

# Rulare
spinthatshit
# sau mai scurt
sts
```

---

## 📋 Funcționalități

### Flux de Lucru Multi-Agent
- **Planner** - Analizează documentația, creează planul
- **Designer** - Proiectează componente UI/UX
- **Engineer** - Construiește infrastructura și arhitectura
- **Developer** - Implementează funcționalități
- **Reviewer** - Verifică calitatea codului
- **Tester** - Testează funcționalitatea
- **Supervisor** - Identifică conflicte și probleme
- **Evolver** - Îmbunătățește sistemul însuși

### Gestionare Context
- Urmărire automată a utilizării contextului
- Transfer la 50% din limită
- Continuitatea muncii între agenți

### Integrare Git
- Commit automat după fiecare modificare
- Etichetare etape
- Auto-push pe GitHub

### Auto-Evoluție
- Sistemul învață din greșeli
- Îmbunătățește automat prompt-urile
- Adaugă verificări noi

---

## 📁 Structura Proiectului

După rulare, următoarea structură este creată în folderul de dezvoltare:

```
your-project/
├── .spinstate/
│   ├── state.json          # Starea orchestrării
│   ├── journal.md          # Jurnalul tuturor agenților
│   ├── plan.md             # Planul proiectului
│   ├── checklist.md        # Lista de sarcini
│   ├── architecture.md     # Arhitectura
│   ├── handoff.md          # Note de transfer
│   ├── status.txt          # Status curent
│   ├── review.md           # Rezultate review
│   ├── test_report.md      # Rezultate teste
│   └── logs/               # Loguri ale tuturor agenților
├── CLAUDE.md               # Instrucțiuni pentru Claude
└── ... (codul tău)
```

---

## 🎯 Utilizare

### Mod Interactiv
```bash
spinthatshit
```

Sistemul va întreba:
1. Calea către documentație
2. Calea către folderul de dezvoltare

### Cu Parametri
```bash
spinthatshit --docs ./docs --dev ./src
```

### Reluare
```bash
spinthatshit --resume
```

---

## ⚙️ Configurare

Fișier de configurare: `~/.spinthatshit/config.json`

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

## 🔧 Cerințe

- **Python 3.8+**
- **Claude Code CLI** (`npm install -g @anthropic-ai/claude-code`)
- **Git**
- **macOS sau Linux**

---

## 📖 Cum Funcționează

### 1. Inițializare
Sistemul încarcă documentația și codul existent, creează un plan.

### 2. Execuție pe Faze
Fiecare agent rulează secvențial:
1. Încarcă contextul din journal.md
2. Își efectuează munca
3. Face commit la modificări
4. Scrie în checklist
5. Transferă la următorul agent

### 3. Transfer Context
Când un agent atinge 50% din context:
1. Scrie starea în handoff.md
2. Face commit la tot
3. Se termină
4. Un nou agent continuă

### 4. Recuperare
La eșec:
1. Supervisor analizează problema
2. Orchestrator ajustează regulile
3. Agentul repornește

### 5. Evoluție
După finalizarea proiectului:
1. Evolver analizează ce a funcționat
2. Ajustează prompt-urile agenților
3. Adaugă verificări noi

---

## 🎬 Exemplu de Rulare

```
[14:32:01] [PHASE] ========================================
[14:32:01] [PHASE] FAZA: PLANNER
[14:32:01] [PHASE] ========================================

[14:32:05] [AGENT] [planner] Reading documentation...
[14:32:12] [AGENT] [planner] Created plan.md
[14:32:18] [AGENT] [planner] Created checklist.md
[14:32:22] [SUCCESS] Commit: [planner] Initial planning complete
[14:32:24] [SUCCESS] Agent planner finalizat (context: ~15%)

[14:32:25] [PHASE] ========================================
[14:32:25] [PHASE] FAZA: DEVELOPER
[14:32:25] [PHASE] ========================================

[14:32:30] [AGENT] [developer] Starting backend API...
[14:35:45] [WARNING] Context la 52% - transfer la următorul agent
[14:35:48] [INFO] Repornire agent developer (încercare 1/3)
...
```

---

## 🛑 Oprire

- **Ctrl+C** - Oprire sigură, starea este salvată
- Folosește `--resume` pentru a continua

---

## 🐛 Depanare

### Agentul este blocat
```bash
# Verifică logurile
cat your-project/.spinstate/logs/agent_*.log
```

### Erori în cod
Sistemul are auto-recuperare, dar poți:
1. Edita `.spinstate/checklist.md`
2. Adăuga o notă la `.spinstate/journal.md`
3. Rula din nou

### Depășire context
- Crește `context_limit_percent` în config.json
- Împarte proiectul în faze mai mici

---

## 📝 Sfaturi

1. **Documentația este cheia** - Documentație mai bună, rezultate mai bune
2. **Începe cu proiecte mici** - Învață sistemul pe un proiect simplu
3. **Nu verifica fiecare pas** - Lasă agenții să lucreze
4. **Ai încredere în transferuri** - Sistemul își amintește contextul

---

## 🗑️ Dezinstalare

```bash
~/.spinthatshit/uninstall.sh
```

---

## 📜 Licență

MIT License - Liber de utilizat

---

## 🤝 Creat pentru

Martin @ Praut s.r.o.
AI Integration & Business Automation

---

*"Lăsăm AI să lucreze în timp ce noi mâncăm tort."* 🍰

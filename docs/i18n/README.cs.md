> **🌍 Languages / Jazyky / 语言:**
[English](README.en.md) | [Čeština](README.cs.md) | [Español](README.es.md) | [简体中文](README.zh-CN.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Русский](README.ru.md) | [Português](README.pt.md) | [हिन्दी](README.hi.md) | [العربية](README.ar.md) | [বাংলা](README.bn.md) | [Italiano](README.it.md) | [Türkçe](README.tr.md) | [Tiếng Việt](README.vi.md) | [Polski](README.pl.md) | [Українська](README.uk.md) | [Nederlands](README.nl.md) | [ไทย](README.th.md) | [Română](README.ro.md) | [Ελληνικά](README.el.md) | [Magyar](README.hu.md) | [Svenska](README.sv.md) | [Bahasa Indonesia](README.id.md) | [فارسی](README.fa.md) | [עברית](README.he.md) | [Bahasa Melayu](README.ms.md) | [Norsk](README.no.md) | [Slovenčina](README.sk.md) | [Suomi](README.fi.md) | [Dansk](README.da.md)


# 🔄 SpinThatShit

**Autonomní AI Agent Orchestrace pro Vývoj Software**

Systém pro řízení více AI agentů (Claude Code CLI), kteří spolupracují na vývoji software. Každý agent má specifickou roli a systém zajišťuje kontinuitu práce i při dosažení context limitu.

---

## 🚀 Rychlý Start

```bash
# Instalace
chmod +x install.sh
./install.sh

# Spuštění
spinthatshit
# nebo kratší
sts
```

---

## 📋 Funkce

### Multi-Agent Workflow
- **Planner** - Analyzuje dokumentaci, vytváří plán
- **Designer** - Navrhuje UI/UX komponenty
- **Engineer** - Staví infrastrukturu a architekturu
- **Developer** - Implementuje features
- **Reviewer** - Kontroluje kvalitu kódu
- **Tester** - Testuje funkcionalitu
- **Supervisor** - Hledá kolize a problémy
- **Evolver** - Vylepšuje samotný systém

### Context Management
- Automatické sledování využití kontextu
- Handoff při dosažení 50% limitu
- Kontinuita práce mezi agenty

### Git Integration
- Automatický commit po každé změně
- Tagging fází
- Auto-push na GitHub

### Self-Evolution
- Systém se učí z chyb
- Automaticky vylepšuje prompty
- Přidává nové kontroly

---

## 📁 Struktura Projektu

Po spuštění se ve vývojové složce vytvoří:

```
your-project/
├── .spinstate/
│   ├── state.json          # Stav orchestrace
│   ├── journal.md          # Deník všech agentů
│   ├── plan.md             # Plán projektu
│   ├── checklist.md        # Seznam úkolů
│   ├── architecture.md     # Architektura
│   ├── handoff.md          # Předávací poznámky
│   ├── status.txt          # Aktuální status
│   ├── review.md           # Výsledky review
│   ├── test_report.md      # Výsledky testů
│   └── logs/               # Logy všech agentů
├── CLAUDE.md               # Instrukce pro Claude
└── ... (váš kód)
```

---

## 🎯 Použití

### Interaktivní Režim
```bash
spinthatshit
```

Systém se vás zeptá na:
1. Cestu k dokumentaci
2. Cestu k vývojové složce

### S Parametry
```bash
spinthatshit --docs ./docs --dev ./src
```

### Pokračování
```bash
spinthatshit --resume
```

---

## ⚙️ Konfigurace

Konfigurační soubor: `~/.spinthatshit/config.json`

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

## 🔧 Požadavky

- **Python 3.8+**
- **Claude Code CLI** (`npm install -g @anthropic-ai/claude-code`)
- **Git**
- **macOS nebo Linux**

---

## 📖 Jak To Funguje

### 1. Inicializace
Systém načte dokumentaci a existující kód, vytvoří plán.

### 2. Fázový Běh
Každý agent běží postupně:
1. Načte kontext z journal.md
2. Provede svou práci
3. Commituje změny
4. Zapisuje do checklistu
5. Předá dalšímu agentovi

### 3. Context Handoff
Když agent dosáhne 50% kontextu:
1. Zapíše stav do handoff.md
2. Commitne vše
3. Ukončí se
4. Nový agent pokračuje

### 4. Recovery
Při selhání:
1. Supervisor analyzuje problém
2. Orchestrator upraví pravidla
3. Agent se restartuje

### 5. Evoluce
Po dokončení projektu:
1. Evolver analyzuje co fungovalo
2. Upraví prompty agentů
3. Přidá nové kontroly

---

## 🎬 Příklad Běhu

```
[14:32:01] [PHASE] ========================================
[14:32:01] [PHASE] FÁZE: PLANNER
[14:32:01] [PHASE] ========================================

[14:32:05] [AGENT] [planner] Reading documentation...
[14:32:12] [AGENT] [planner] Created plan.md
[14:32:18] [AGENT] [planner] Created checklist.md
[14:32:22] [SUCCESS] Commit: [planner] Initial planning complete
[14:32:24] [SUCCESS] Agent planner dokončen (kontext: ~15%)

[14:32:25] [PHASE] ========================================
[14:32:25] [PHASE] FÁZE: DEVELOPER
[14:32:25] [PHASE] ========================================

[14:32:30] [AGENT] [developer] Starting backend API...
[14:35:45] [WARNING] Kontext na 52% - předávám dalšímu agentovi
[14:35:48] [INFO] Restart agenta developer (pokus 1/3)
...
```

---

## 🛑 Zastavení

- **Ctrl+C** - Bezpečné zastavení, stav se uloží
- Použijte `--resume` pro pokračování

---

## 🐛 Řešení Problémů

### Agent se zasekl
```bash
# Podívejte se na logy
cat your-project/.spinstate/logs/agent_*.log
```

### Chyby v kódu
Systém má auto-recovery, ale můžete:
1. Upravit `.spinstate/checklist.md`
2. Přidat poznámku do `.spinstate/journal.md`
3. Spustit znovu

### Context přetéká
- Zvyšte `context_limit_percent` v config.json
- Rozdělte projekt na menší fáze

---

## 📝 Tipy

1. **Dokumentace je klíč** - Čím lepší docs, tím lepší výsledek
2. **Malé projekty první** - Naučte se systém na jednoduchém projektu
3. **Nekontrolujte každý krok** - Nechte agenty pracovat
4. **Věřte handoffům** - Systém si pamatuje kontext

---

## 🗑️ Odinstalace

```bash
~/.spinthatshit/uninstall.sh
```

---

## 📜 Licence

MIT License - Volně k použití

---

## 🤝 Vytvořeno pro

Martin @ Praut s.r.o.
AI Integration & Business Automation

---

*"Necháváme AI pracovat, zatímco si dáváme dortík."* 🍰

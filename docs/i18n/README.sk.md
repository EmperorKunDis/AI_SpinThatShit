> **🌍 Languages / Jazyky / 语言:**
[English](README.en.md) | [Čeština](README.cs.md) | [Español](README.es.md) | [简体中文](README.zh-CN.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Русский](README.ru.md) | [Português](README.pt.md) | [हिन्दी](README.hi.md) | [العربية](README.ar.md) | [বাংলা](README.bn.md) | [Italiano](README.it.md) | [Türkçe](README.tr.md) | [Tiếng Việt](README.vi.md) | [Polski](README.pl.md) | [Українська](README.uk.md) | [Nederlands](README.nl.md) | [ไทย](README.th.md) | [Română](README.ro.md) | [Ελληνικά](README.el.md) | [Magyar](README.hu.md) | [Svenska](README.sv.md) | [Bahasa Indonesia](README.id.md) | [فارسی](README.fa.md) | [עברית](README.he.md) | [Bahasa Melayu](README.ms.md) | [Norsk](README.no.md) | [Slovenčina](README.sk.md) | [Suomi](README.fi.md) | [Dansk](README.da.md)


# 🔄 SpinThatShit

**Autonómna Orchestrácia AI Agentov pre Vývoj Softvéru**

Systém na správu viacerých AI agentov (Claude Code CLI), ktorí spolupracujú na vývoji softvéru. Každý agent má špecifickú rolu a systém zabezpečuje kontinuitu práce aj pri dosiahnutí limitov kontextu.

---

## 🚀 Rýchly Štart

```bash
# Inštalácia
chmod +x install.sh
./install.sh

# Spustenie
spinthatshit
# alebo kratšie
sts
```

---

## 📋 Funkcie

### Multi-Agent Workflow
- **Planner** - Analyzuje dokumentáciu, vytvára plán
- **Designer** - Navrhuje UI/UX komponenty
- **Engineer** - Buduje infraštruktúru a architektúru
- **Developer** - Implementuje funkcie
- **Reviewer** - Kontroluje kvalitu kódu
- **Tester** - Testuje funkcionalitu
- **Supervisor** - Hľadá kolízie a problémy
- **Evolver** - Vylepšuje samotný systém

### Správa Kontextu
- Automatické sledovanie využitia kontextu
- Handoff pri dosiahnutí 50% limitu
- Kontinuita práce medzi agentmi

### Integrácia s Git
- Automatický commit po každej zmene
- Tagging fáz
- Auto-push na GitHub

### Samo-Evolúcia
- Systém sa učí z chýb
- Automaticky vylepšuje prompty
- Pridáva nové kontroly

---

## 📁 Štruktúra Projektu

Po spustení sa vo vývojovom priečinku vytvorí:

```
your-project/
├── .spinstate/
│   ├── state.json          # Stav orchestrácie
│   ├── journal.md          # Denník všetkých agentov
│   ├── plan.md             # Plán projektu
│   ├── checklist.md        # Zoznam úloh
│   ├── architecture.md     # Architektúra
│   ├── handoff.md          # Poznámky odovzdania
│   ├── status.txt          # Aktuálny status
│   ├── review.md           # Výsledky review
│   ├── test_report.md      # Výsledky testov
│   └── logs/               # Logy všetkých agentov
├── CLAUDE.md               # Inštrukcie pre Claude
└── ... (váš kód)
```

---

## 🎯 Použitie

### Interaktívny Režim
```bash
spinthatshit
```

Systém sa vás opýta na:
1. Cestu k dokumentácii
2. Cestu k vývojovému priečinku

### S Parametrami
```bash
spinthatshit --docs ./docs --dev ./src
```

### Pokračovanie
```bash
spinthatshit --resume
```

---

## ⚙️ Konfigurácia

Konfiguračný súbor: `~/.spinthatshit/config.json`

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

## 🔧 Požiadavky

- **Python 3.8+**
- **Claude Code CLI** (`npm install -g @anthropic-ai/claude-code`)
- **Git**
- **macOS alebo Linux**

---

## 📖 Ako To Funguje

### 1. Inicializácia
Systém načíta dokumentáciu a existujúci kód, vytvorí plán.

### 2. Fázový Beh
Každý agent beží postupne:
1. Načíta kontext z journal.md
2. Vykoná svoju prácu
3. Commituje zmeny
4. Zapisuje do checklistu
5. Odovzdá ďalšiemu agentovi

### 3. Context Handoff
Keď agent dosiahne 50% kontextu:
1. Zapíše stav do handoff.md
2. Commitne všetko
3. Ukončí sa
4. Nový agent pokračuje

### 4. Recovery
Pri zlyhaní:
1. Supervisor analyzuje problém
2. Orchestrator upraví pravidlá
3. Agent sa reštartuje

### 5. Evolúcia
Po dokončení projektu:
1. Evolver analyzuje čo fungovalo
2. Upraví prompty agentov
3. Pridá nové kontroly

---

## 🎬 Príklad Behu

```
[14:32:01] [PHASE] ========================================
[14:32:01] [PHASE] FÁZA: PLANNER
[14:32:01] [PHASE] ========================================

[14:32:05] [AGENT] [planner] Reading documentation...
[14:32:12] [AGENT] [planner] Created plan.md
[14:32:18] [AGENT] [planner] Created checklist.md
[14:32:22] [SUCCESS] Commit: [planner] Initial planning complete
[14:32:24] [SUCCESS] Agent planner dokončený (kontext: ~15%)

[14:32:25] [PHASE] ========================================
[14:32:25] [PHASE] FÁZA: DEVELOPER
[14:32:25] [PHASE] ========================================

[14:32:30] [AGENT] [developer] Starting backend API...
[14:35:45] [WARNING] Kontext na 52% - odovzdávam ďalšiemu agentovi
[14:35:48] [INFO] Reštart agenta developer (pokus 1/3)
...
```

---

## 🛑 Zastavenie

- **Ctrl+C** - Bezpečné zastavenie, stav sa uloží
- Použite `--resume` pre pokračovanie

---

## 🐛 Riešenie Problémov

### Agent sa zasekol
```bash
# Pozrite sa na logy
cat your-project/.spinstate/logs/agent_*.log
```

### Chyby v kóde
Systém má auto-recovery, ale môžete:
1. Upraviť `.spinstate/checklist.md`
2. Pridať poznámku do `.spinstate/journal.md`
3. Spustiť znovu

### Context pretečie
- Zvýšte `context_limit_percent` v config.json
- Rozdeľte projekt na menšie fázy

---

## 📝 Tipy

1. **Dokumentácia je kľúč** - Čím lepšia dokumentácia, tým lepší výsledok
2. **Malé projekty najprv** - Naučte sa systém na jednoduchom projekte
3. **Nekontrolujte každý krok** - Nechajte agentov pracovať
4. **Dôverujte handoffom** - Systém si pamätá kontext

---

## 🗑️ Odinštalovanie

```bash
~/.spinthatshit/uninstall.sh
```

---

## 📜 Licencia

MIT License - Voľne k použitiu

---

## 🤝 Vytvorené pre

Martin @ Praut s.r.o.
AI Integration & Business Automation

---

*"Nechávame AI pracovať, kým si dávame koláčik."* 🍰

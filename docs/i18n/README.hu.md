---
**🌍 Languages / Jazyky / 语言:**
[English](README.en.md) | [Čeština](README.cs.md) | [Español](README.es.md) | [简体中文](README.zh-CN.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Русский](README.ru.md) | [Português](README.pt.md) | [हिन्दी](README.hi.md) | [العربية](README.ar.md) | [বাংলা](README.bn.md) | [Italiano](README.it.md) | [Türkçe](README.tr.md) | [Tiếng Việt](README.vi.md) | [Polski](README.pl.md) | [Українська](README.uk.md) | [Nederlands](README.nl.md) | [ไทย](README.th.md) | [Română](README.ro.md) | [Ελληνικά](README.el.md) | [Magyar](README.hu.md) | [Svenska](README.sv.md) | [Bahasa Indonesia](README.id.md) | [فارسی](README.fa.md) | [עברית](README.he.md) | [Bahasa Melayu](README.ms.md) | [Norsk](README.no.md) | [Slovenčina](README.sk.md) | [Suomi](README.fi.md) | [Dansk](README.da.md)
---

# 🔄 SpinThatShit

**Autonóm AI Ágens Orkesztráció Szoftverfejlesztéshez**

Egy rendszer több AI ágens (Claude Code CLI) kezelésére, amelyek együttműködnek a szoftverfejlesztésben. Minden ágensnek specifikus szerepe van, és a rendszer biztosítja a munka folytonosságát még akkor is, ha elérjük a kontextus limiteket.

---

## 🚀 Gyors Kezdés

```bash
# Telepítés
chmod +x install.sh
./install.sh

# Futtatás
spinthatshit
# vagy rövidebben
sts
```

---

## 📋 Funkciók

### Multi-Ágens Munkafolyamat
- **Planner** - Dokumentáció elemzése, terv készítése
- **Designer** - UI/UX komponensek tervezése
- **Engineer** - Infrastruktúra és architektúra építése
- **Developer** - Funkciók implementálása
- **Reviewer** - Kódminőség ellenőrzése
- **Tester** - Funkcionalitás tesztelése
- **Supervisor** - Ütközések és problémák azonosítása
- **Evolver** - A rendszer fejlesztése

### Kontextus Kezelés
- Automatikus kontextus használat követés
- Átadás 50%-os korlátnál
- Munka folytonossága ágensek között

### Git Integráció
- Automatikus commit minden változtatás után
- Fázis címkézés
- Auto-push GitHub-ra

### Ön-Evolúció
- Rendszer tanul a hibákból
- Automatikusan fejleszti a promptokat
- Új ellenőrzéseket ad hozzá

---

## 📁 Projekt Struktúra

Futtatás után a következő struktúra jön létre a fejlesztési mappában:

```
your-project/
├── .spinstate/
│   ├── state.json          # Orkesztrációs állapot
│   ├── journal.md          # Összes ágens naplója
│   ├── plan.md             # Projekt terv
│   ├── checklist.md        # Feladat lista
│   ├── architecture.md     # Architektúra
│   ├── handoff.md          # Átadási jegyzetek
│   ├── status.txt          # Jelenlegi státusz
│   ├── review.md           # Felülvizsgálati eredmények
│   ├── test_report.md      # Teszt eredmények
│   └── logs/               # Összes ágens naplója
├── CLAUDE.md               # Utasítások Claude-hoz
└── ... (az Ön kódja)
```

---

## 🎯 Használat

### Interaktív Mód
```bash
spinthatshit
```

A rendszer megkérdezi:
1. Dokumentáció útvonala
2. Fejlesztési mappa útvonala

### Paraméterekkel
```bash
spinthatshit --docs ./docs --dev ./src
```

### Folytatás
```bash
spinthatshit --resume
```

---

## ⚙️ Konfiguráció

Konfigurációs fájl: `~/.spinthatshit/config.json`

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

## 🔧 Követelmények

- **Python 3.8+**
- **Claude Code CLI** (`npm install -g @anthropic-ai/claude-code`)
- **Git**
- **macOS vagy Linux**

---

## 📖 Hogyan Működik

### 1. Inicializálás
A rendszer betölti a dokumentációt és a meglévő kódot, tervet készít.

### 2. Fázis Végrehajtás
Minden ágens szekvenciálisan fut:
1. Betölti a kontextust journal.md-ből
2. Elvégzi a munkáját
3. Commitolja a változtatásokat
4. Ír a checklistre
5. Átadja a következő ágensnek

### 3. Kontextus Átadás
Amikor egy ágens eléri a 50% kontextust:
1. Beírja az állapotot handoff.md-be
2. Commitol mindent
3. Befejezi
4. Új ágens folytatja

### 4. Helyreállítás
Hiba esetén:
1. Supervisor elemzi a problémát
2. Orchestrator beállítja a szabályokat
3. Ágens újraindul

### 5. Evolúció
Projekt befejezése után:
1. Evolver elemzi mi működött
2. Beállítja az ágens promptokat
3. Új ellenőrzéseket ad hozzá

---

## 🎬 Példa Futtatás

```
[14:32:01] [PHASE] ========================================
[14:32:01] [PHASE] FÁZIS: PLANNER
[14:32:01] [PHASE] ========================================

[14:32:05] [AGENT] [planner] Reading documentation...
[14:32:12] [AGENT] [planner] Created plan.md
[14:32:18] [AGENT] [planner] Created checklist.md
[14:32:22] [SUCCESS] Commit: [planner] Initial planning complete
[14:32:24] [SUCCESS] Agent planner befejezve (kontextus: ~15%)

[14:32:25] [PHASE] ========================================
[14:32:25] [PHASE] FÁZIS: DEVELOPER
[14:32:25] [PHASE] ========================================

[14:32:30] [AGENT] [developer] Starting backend API...
[14:35:45] [WARNING] Kontextus 52%-on - átadás a következő ágensnek
[14:35:48] [INFO] Ágens developer újraindítása (próbálkozás 1/3)
...
```

---

## 🛑 Leállítás

- **Ctrl+C** - Biztonságos leállítás, állapot mentése
- Használja `--resume`-t a folytatáshoz

---

## 🐛 Hibaelhárítás

### Ágens lefagyott
```bash
# Naplók ellenőrzése
cat your-project/.spinstate/logs/agent_*.log
```

### Kód hibák
A rendszer auto-recovery-vel rendelkezik, de teheted:
1. Szerkessze `.spinstate/checklist.md`
2. Adjon hozzá jegyzetet `.spinstate/journal.md`-hez
3. Futtassa újra

### Kontextus túlcsordulás
- Növelje `context_limit_percent`-et config.json-ban
- Ossza kisebb fázisokra a projektet

---

## 📝 Tippek

1. **Dokumentáció a kulcs** - Jobb dokumentáció, jobb eredmények
2. **Kezdje kis projektekkel** - Tanulja a rendszert egyszerű projekten
3. **Ne ellenőrizze minden lépést** - Hagyja az ágenseket dolgozni
4. **Bízzon az átadásokban** - Rendszer emlékszik a kontextusra

---

## 🗑️ Eltávolítás

```bash
~/.spinthatshit/uninstall.sh
```

---

## 📜 Licenc

MIT License - Szabadon használható

---

## 🤝 Készítette

Martin @ Praut s.r.o.
AI Integration & Business Automation

---

*"Hagyjuk az AI-t dolgozni, amíg mi süteményt eszünk."* 🍰

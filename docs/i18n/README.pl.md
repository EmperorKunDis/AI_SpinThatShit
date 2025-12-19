> **🌍 Languages / Jazyky / 语言:**
[English](README.en.md) | [Čeština](README.cs.md) | [Español](README.es.md) | [简体中文](README.zh-CN.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Русский](README.ru.md) | [Português](README.pt.md) | [हिन्दी](README.hi.md) | [العربية](README.ar.md) | [বাংলা](README.bn.md) | [Italiano](README.it.md) | [Türkçe](README.tr.md) | [Tiếng Việt](README.vi.md) | [Polski](README.pl.md) | [Українська](README.uk.md) | [Nederlands](README.nl.md) | [ไทย](README.th.md) | [Română](README.ro.md) | [Ελληνικά](README.el.md) | [Magyar](README.hu.md) | [Svenska](README.sv.md) | [Bahasa Indonesia](README.id.md) | [فارسی](README.fa.md) | [עברית](README.he.md) | [Bahasa Melayu](README.ms.md) | [Norsk](README.no.md) | [Slovenčina](README.sk.md) | [Suomi](README.fi.md) | [Dansk](README.da.md)


# 🔄 SpinThatShit

**Autonomiczna Orkiestracja Agentów AI dla Rozwoju Oprogramowania**

System zarządzania wieloma agentami AI (Claude Code CLI), które współpracują przy rozwoju oprogramowania. Każdy agent ma określoną rolę, a system zapewnia ciągłość pracy nawet po osiągnięciu limitów kontekstu.

---

## 🚀 Szybki Start

```bash
# Instalacja
chmod +x install.sh
./install.sh

# Uruchomienie
spinthatshit
# lub krócej
sts
```

---

## 📋 Funkcje

### Przepływ Pracy Wielu Agentów
- **Planner** - Analizuje dokumentację, tworzy plan
- **Designer** - Projektuje komponenty UI/UX
- **Engineer** - Buduje infrastrukturę i architekturę
- **Developer** - Implementuje funkcje
- **Reviewer** - Sprawdza jakość kodu
- **Tester** - Testuje funkcjonalność
- **Supervisor** - Identyfikuje konflikty i problemy
- **Evolver** - Ulepsza sam system

### Zarządzanie Kontekstem
- Automatyczne śledzenie wykorzystania kontekstu
- Przekazanie przy 50% limitu
- Ciągłość pracy między agentami

### Integracja z Git
- Automatyczny commit po każdej zmianie
- Tagowanie faz
- Automatyczne push do GitHub

### Samoewolucja
- System uczy się na błędach
- Automatycznie ulepsza prompty
- Dodaje nowe kontrole

---

## 📁 Struktura Projektu

Po uruchomieniu w folderze deweloperskim tworzona jest następująca struktura:

```
your-project/
├── .spinstate/
│   ├── state.json          # Stan orkiestracji
│   ├── journal.md          # Dziennik wszystkich agentów
│   ├── plan.md             # Plan projektu
│   ├── checklist.md        # Lista zadań
│   ├── architecture.md     # Architektura
│   ├── handoff.md          # Notatki przekazania
│   ├── status.txt          # Aktualny status
│   ├── review.md           # Wyniki przeglądu
│   ├── test_report.md      # Wyniki testów
│   └── logs/               # Logi wszystkich agentów
├── CLAUDE.md               # Instrukcje dla Claude
└── ... (twój kod)
```

---

## 🎯 Użycie

### Tryb Interaktywny
```bash
spinthatshit
```

System zapyta o:
1. Ścieżkę dokumentacji
2. Ścieżkę folderu deweloperskiego

### Z Parametrami
```bash
spinthatshit --docs ./docs --dev ./src
```

### Wznowienie
```bash
spinthatshit --resume
```

---

## ⚙️ Konfiguracja

Plik konfiguracyjny: `~/.spinthatshit/config.json`

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

## 🔧 Wymagania

- **Python 3.8+**
- **Claude Code CLI** (`npm install -g @anthropic-ai/claude-code`)
- **Git**
- **macOS lub Linux**

---

## 📖 Jak To Działa

### 1. Inicjalizacja
System ładuje dokumentację i istniejący kod, tworzy plan.

### 2. Wykonanie Fazowe
Każdy agent działa sekwencyjnie:
1. Ładuje kontekst z journal.md
2. Wykonuje swoją pracę
3. Commituje zmiany
4. Zapisuje do checklisty
5. Przekazuje następnemu agentowi

### 3. Przekazanie Kontekstu
Gdy agent osiągnie 50% kontekstu:
1. Zapisuje stan do handoff.md
2. Commituje wszystko
3. Kończy działanie
4. Nowy agent kontynuuje

### 4. Odzyskiwanie
Przy awarii:
1. Supervisor analizuje problem
2. Orchestrator dostosowuje reguły
3. Agent restartuje

### 5. Ewolucja
Po zakończeniu projektu:
1. Evolver analizuje co działało
2. Dostosowuje prompty agentów
3. Dodaje nowe kontrole

---

## 🎬 Przykład Działania

```
[14:32:01] [PHASE] ========================================
[14:32:01] [PHASE] FAZA: PLANNER
[14:32:01] [PHASE] ========================================

[14:32:05] [AGENT] [planner] Reading documentation...
[14:32:12] [AGENT] [planner] Created plan.md
[14:32:18] [AGENT] [planner] Created checklist.md
[14:32:22] [SUCCESS] Commit: [planner] Initial planning complete
[14:32:24] [SUCCESS] Agent planner ukończony (kontekst: ~15%)

[14:32:25] [PHASE] ========================================
[14:32:25] [PHASE] FAZA: DEVELOPER
[14:32:25] [PHASE] ========================================

[14:32:30] [AGENT] [developer] Starting backend API...
[14:35:45] [WARNING] Kontekst na 52% - przekazanie następnemu agentowi
[14:35:48] [INFO] Restart agenta developer (próba 1/3)
...
```

---

## 🛑 Zatrzymanie

- **Ctrl+C** - Bezpieczne zatrzymanie, stan zostaje zapisany
- Użyj `--resume` aby kontynuować

---

## 🐛 Rozwiązywanie Problemów

### Agent się zawiesił
```bash
# Sprawdź logi
cat your-project/.spinstate/logs/agent_*.log
```

### Błędy w kodzie
System ma auto-recovery, ale możesz:
1. Edytować `.spinstate/checklist.md`
2. Dodać notatkę do `.spinstate/journal.md`
3. Uruchomić ponownie

### Przepełnienie kontekstu
- Zwiększ `context_limit_percent` w config.json
- Podziel projekt na mniejsze fazy

---

## 📝 Wskazówki

1. **Dokumentacja jest kluczem** - Lepsza dokumentacja, lepsze wyniki
2. **Zacznij od małych projektów** - Naucz się systemu na prostym projekcie
3. **Nie sprawdzaj każdego kroku** - Pozwól agentom pracować
4. **Ufaj przekazaniom** - System pamięta kontekst

---

## 🗑️ Odinstalowanie

```bash
~/.spinthatshit/uninstall.sh
```

---

## 📜 Licencja

MIT License - Wolne do użytku

---

## 🤝 Stworzone dla

Martin @ Praut s.r.o.
AI Integration & Business Automation

---

*"Pozwalamy AI pracować, podczas gdy my jemy ciasto."* 🍰

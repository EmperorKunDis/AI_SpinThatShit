---
**🌍 Languages / Jazyky / 语言:**
[English](README.en.md) | [Čeština](README.cs.md) | [Español](README.es.md) | [简体中文](README.zh-CN.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Русский](README.ru.md) | [Português](README.pt.md) | [हिन्दी](README.hi.md) | [العربية](README.ar.md) | [বাংলা](README.bn.md) | [Italiano](README.it.md) | [Türkçe](README.tr.md) | [Tiếng Việt](README.vi.md) | [Polski](README.pl.md) | [Українська](README.uk.md) | [Nederlands](README.nl.md) | [ไทย](README.th.md) | [Română](README.ro.md) | [Ελληνικά](README.el.md) | [Magyar](README.hu.md) | [Svenska](README.sv.md) | [Bahasa Indonesia](README.id.md) | [فارسی](README.fa.md) | [עברית](README.he.md) | [Bahasa Melayu](README.ms.md) | [Norsk](README.no.md) | [Slovenčina](README.sk.md) | [Suomi](README.fi.md) | [Dansk](README.da.md)
---

# 🔄 SpinThatShit

**Autonome KI-Agenten-Orchestrierung für Softwareentwicklung**

Ein System zur Verwaltung mehrerer KI-Agenten (Claude Code CLI), die bei der Softwareentwicklung zusammenarbeiten. Jeder Agent hat eine spezifische Rolle und das System gewährleistet die Arbeitskontinuität auch bei Erreichen von Kontextgrenzen.

---

## 🚀 Schnellstart

```bash
# Installation
chmod +x install.sh
./install.sh

# Ausführen
spinthatshit
# oder kürzer
sts
```

---

## 📋 Funktionen

### Multi-Agenten-Workflow
- **Planner** - Analysiert Dokumentation, erstellt Plan
- **Designer** - Entwirft UI/UX-Komponenten
- **Engineer** - Baut Infrastruktur und Architektur
- **Developer** - Implementiert Funktionen
- **Reviewer** - Prüft Codequalität
- **Tester** - Testet Funktionalität
- **Supervisor** - Identifiziert Konflikte und Probleme
- **Evolver** - Verbessert das System selbst

### Kontext-Management
- Automatische Verfolgung der Kontextnutzung
- Übergabe bei 50% Limit
- Arbeitskontinuität zwischen Agenten

### Git-Integration
- Automatisches Commit nach jeder Änderung
- Phasen-Tagging
- Auto-Push zu GitHub

### Selbst-Evolution
- System lernt aus Fehlern
- Verbessert automatisch Prompts
- Fügt neue Überprüfungen hinzu

---

## 📁 Projektstruktur

Nach dem Start wird im Entwicklungsordner folgende Struktur erstellt:

```
your-project/
├── .spinstate/
│   ├── state.json          # Orchestrierungszustand
│   ├── journal.md          # Journal aller Agenten
│   ├── plan.md             # Projektplan
│   ├── checklist.md        # Aufgabenliste
│   ├── architecture.md     # Architektur
│   ├── handoff.md          # Übergabenotizen
│   ├── status.txt          # Aktueller Status
│   ├── review.md           # Review-Ergebnisse
│   ├── test_report.md      # Testergebnisse
│   └── logs/               # Logs aller Agenten
├── CLAUDE.md               # Anweisungen für Claude
└── ... (Ihr Code)
```

---

## 🎯 Verwendung

### Interaktiver Modus
```bash
spinthatshit
```

Das System fragt nach:
1. Dokumentationspfad
2. Entwicklungsordner-Pfad

### Mit Parametern
```bash
spinthatshit --docs ./docs --dev ./src
```

### Fortsetzen
```bash
spinthatshit --resume
```

---

## ⚙️ Konfiguration

Konfigurationsdatei: `~/.spinthatshit/config.json`

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

## 🔧 Anforderungen

- **Python 3.8+**
- **Claude Code CLI** (`npm install -g @anthropic-ai/claude-code`)
- **Git**
- **macOS oder Linux**

---

## 📖 Wie es funktioniert

### 1. Initialisierung
System lädt Dokumentation und vorhandenen Code, erstellt einen Plan.

### 2. Phasenausführung
Jeder Agent läuft sequenziell:
1. Lädt Kontext aus journal.md
2. Führt seine Arbeit aus
3. Committed Änderungen
4. Schreibt in Checkliste
5. Übergibt an nächsten Agenten

### 3. Kontext-Übergabe
Wenn ein Agent 50% Kontext erreicht:
1. Schreibt Zustand in handoff.md
2. Committed alles
3. Beendet sich
4. Neuer Agent setzt fort

### 4. Wiederherstellung
Bei Fehler:
1. Supervisor analysiert das Problem
2. Orchestrator passt Regeln an
3. Agent startet neu

### 5. Evolution
Nach Projektabschluss:
1. Evolver analysiert was funktioniert hat
2. Passt Agenten-Prompts an
3. Fügt neue Überprüfungen hinzu

---

## 🎬 Beispiel-Durchlauf

```
[14:32:01] [PHASE] ========================================
[14:32:01] [PHASE] PHASE: PLANNER
[14:32:01] [PHASE] ========================================

[14:32:05] [AGENT] [planner] Reading documentation...
[14:32:12] [AGENT] [planner] Created plan.md
[14:32:18] [AGENT] [planner] Created checklist.md
[14:32:22] [SUCCESS] Commit: [planner] Initial planning complete
[14:32:24] [SUCCESS] Agent planner abgeschlossen (Kontext: ~15%)

[14:32:25] [PHASE] ========================================
[14:32:25] [PHASE] PHASE: DEVELOPER
[14:32:25] [PHASE] ========================================

[14:32:30] [AGENT] [developer] Starting backend API...
[14:35:45] [WARNING] Kontext bei 52% - Übergabe an nächsten Agenten
[14:35:48] [INFO] Agent developer wird neu gestartet (Versuch 1/3)
...
```

---

## 🛑 Stoppen

- **Ctrl+C** - Sicheres Stoppen, Zustand wird gespeichert
- Verwenden Sie `--resume` zum Fortsetzen

---

## 🐛 Fehlerbehebung

### Agent steckt fest
```bash
# Überprüfen Sie die Logs
cat your-project/.spinstate/logs/agent_*.log
```

### Code-Fehler
System hat Auto-Recovery, aber Sie können:
1. `.spinstate/checklist.md` bearbeiten
2. Notiz zu `.spinstate/journal.md` hinzufügen
3. Erneut ausführen

### Kontext-Überlauf
- Erhöhen Sie `context_limit_percent` in config.json
- Teilen Sie Projekt in kleinere Phasen auf

---

## 📝 Tipps

1. **Dokumentation ist der Schlüssel** - Bessere Docs, bessere Ergebnisse
2. **Mit kleinen Projekten beginnen** - Lernen Sie das System an einem einfachen Projekt
3. **Nicht jeden Schritt überprüfen** - Lassen Sie die Agenten arbeiten
4. **Vertrauen Sie den Übergaben** - System erinnert sich an Kontext

---

## 🗑️ Deinstallation

```bash
~/.spinthatshit/uninstall.sh
```

---

## 📜 Lizenz

MIT License - Frei verwendbar

---

## 🤝 Erstellt für

Martin @ Praut s.r.o.
AI Integration & Business Automation

---

*"Wir lassen die KI arbeiten, während wir Kuchen essen."* 🍰

> **🌍 Languages / Jazyky / 语言:**
[English](README.en.md) | [Čeština](README.cs.md) | [Español](README.es.md) | [简体中文](README.zh-CN.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Русский](README.ru.md) | [Português](README.pt.md) | [हिन्दी](README.hi.md) | [العربية](README.ar.md) | [বাংলা](README.bn.md) | [Italiano](README.it.md) | [Türkçe](README.tr.md) | [Tiếng Việt](README.vi.md) | [Polski](README.pl.md) | [Українська](README.uk.md) | [Nederlands](README.nl.md) | [ไทย](README.th.md) | [Română](README.ro.md) | [Ελληνικά](README.el.md) | [Magyar](README.hu.md) | [Svenska](README.sv.md) | [Bahasa Indonesia](README.id.md) | [فارسی](README.fa.md) | [עברית](README.he.md) | [Bahasa Melayu](README.ms.md) | [Norsk](README.no.md) | [Slovenčina](README.sk.md) | [Suomi](README.fi.md) | [Dansk](README.da.md)


# 🔄 SpinThatShit

**Orchestrazione Autonoma di Agenti AI per lo Sviluppo Software**

Un sistema per gestire più agenti AI (Claude Code CLI) che collaborano nello sviluppo software. Ogni agente ha un ruolo specifico e il sistema garantisce la continuità del lavoro anche quando si raggiungono i limiti di contesto.

---

## 🚀 Avvio Rapido

```bash
# Installazione
chmod +x install.sh
./install.sh

# Esegui
spinthatshit
# o più breve
sts
```

---

## 📋 Funzionalità

### Flusso di Lavoro Multi-Agente
- **Planner** - Analizza la documentazione, crea il piano
- **Designer** - Progetta componenti UI/UX
- **Engineer** - Costruisce infrastruttura e architettura
- **Developer** - Implementa funzionalità
- **Reviewer** - Revisiona la qualità del codice
- **Tester** - Testa le funzionalità
- **Supervisor** - Identifica conflitti e problemi
- **Evolver** - Migliora il sistema stesso

### Gestione del Contesto
- Tracciamento automatico dell'uso del contesto
- Passaggio al 50% del limite
- Continuità del lavoro tra agenti

### Integrazione Git
- Commit automatico dopo ogni modifica
- Tagging delle fasi
- Auto-push su GitHub

### Auto-Evoluzione
- Il sistema impara dagli errori
- Migliora automaticamente i prompt
- Aggiunge nuovi controlli

---

## 📁 Struttura del Progetto

Dopo l'esecuzione, viene creata la seguente struttura nella cartella di sviluppo:

```
your-project/
├── .spinstate/
│   ├── state.json          # Stato dell'orchestrazione
│   ├── journal.md          # Diario di tutti gli agenti
│   ├── plan.md             # Piano del progetto
│   ├── checklist.md        # Lista delle attività
│   ├── architecture.md     # Architettura
│   ├── handoff.md          # Note di passaggio
│   ├── status.txt          # Stato attuale
│   ├── review.md           # Risultati della revisione
│   ├── test_report.md      # Risultati dei test
│   └── logs/               # Log di tutti gli agenti
├── CLAUDE.md               # Istruzioni per Claude
└── ... (il tuo codice)
```

---

## 🎯 Utilizzo

### Modalità Interattiva
```bash
spinthatshit
```

Il sistema chiederà:
1. Percorso della documentazione
2. Percorso della cartella di sviluppo

### Con Parametri
```bash
spinthatshit --docs ./docs --dev ./src
```

### Ripresa
```bash
spinthatshit --resume
```

---

## ⚙️ Configurazione

File di configurazione: `~/.spinthatshit/config.json`

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

## 🔧 Requisiti

- **Python 3.8+**
- **Claude Code CLI** (`npm install -g @anthropic-ai/claude-code`)
- **Git**
- **macOS o Linux**

---

## 📖 Come Funziona

### 1. Inizializzazione
Il sistema carica la documentazione e il codice esistente, crea un piano.

### 2. Esecuzione per Fasi
Ogni agente viene eseguito in sequenza:
1. Carica il contesto da journal.md
2. Esegue il suo lavoro
3. Effettua il commit delle modifiche
4. Scrive nella checklist
5. Passa al prossimo agente

### 3. Passaggio di Contesto
Quando un agente raggiunge il 50% di contesto:
1. Scrive lo stato in handoff.md
2. Effettua il commit di tutto
3. Termina
4. Un nuovo agente continua

### 4. Recupero
In caso di fallimento:
1. Il Supervisor analizza il problema
2. L'Orchestrator regola le regole
3. L'agente si riavvia

### 5. Evoluzione
Dopo il completamento del progetto:
1. L'Evolver analizza cosa ha funzionato
2. Regola i prompt degli agenti
3. Aggiunge nuovi controlli

---

## 🎬 Esempio di Esecuzione

```
[14:32:01] [PHASE] ========================================
[14:32:01] [PHASE] FASE: PLANNER
[14:32:01] [PHASE] ========================================

[14:32:05] [AGENT] [planner] Reading documentation...
[14:32:12] [AGENT] [planner] Created plan.md
[14:32:18] [AGENT] [planner] Created checklist.md
[14:32:22] [SUCCESS] Commit: [planner] Initial planning complete
[14:32:24] [SUCCESS] Agent planner completato (contesto: ~15%)

[14:32:25] [PHASE] ========================================
[14:32:25] [PHASE] FASE: DEVELOPER
[14:32:25] [PHASE] ========================================

[14:32:30] [AGENT] [developer] Starting backend API...
[14:35:45] [WARNING] Contesto al 52% - passaggio al prossimo agente
[14:35:48] [INFO] Riavvio agente developer (tentativo 1/3)
...
```

---

## 🛑 Arresto

- **Ctrl+C** - Arresto sicuro, lo stato viene salvato
- Usa `--resume` per continuare

---

## 🐛 Risoluzione dei Problemi

### L'agente è bloccato
```bash
# Controlla i log
cat your-project/.spinstate/logs/agent_*.log
```

### Errori nel codice
Il sistema ha auto-recupero, ma puoi:
1. Modificare `.spinstate/checklist.md`
2. Aggiungere una nota a `.spinstate/journal.md`
3. Eseguire di nuovo

### Overflow di contesto
- Aumenta `context_limit_percent` in config.json
- Dividi il progetto in fasi più piccole

---

## 📝 Suggerimenti

1. **La documentazione è la chiave** - Documentazione migliore, risultati migliori
2. **Inizia con progetti piccoli** - Impara il sistema su un progetto semplice
3. **Non controllare ogni passo** - Lascia lavorare gli agenti
4. **Fidati dei passaggi** - Il sistema ricorda il contesto

---

## 🗑️ Disinstallazione

```bash
~/.spinthatshit/uninstall.sh
```

---

## 📜 Licenza

MIT License - Libero all'uso

---

## 🤝 Creato per

Martin @ Praut s.r.o.
AI Integration & Business Automation

---

*"Lasciamo lavorare l'AI mentre mangiamo torta."* 🍰

> **🌍 Languages / Jazyky / 语言:**
[English](README.en.md) | [Čeština](README.cs.md) | [Español](README.es.md) | [简体中文](README.zh-CN.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Русский](README.ru.md) | [Português](README.pt.md) | [हिन्दी](README.hi.md) | [العربية](README.ar.md) | [বাংলা](README.bn.md) | [Italiano](README.it.md) | [Türkçe](README.tr.md) | [Tiếng Việt](README.vi.md) | [Polski](README.pl.md) | [Українська](README.uk.md) | [Nederlands](README.nl.md) | [ไทย](README.th.md) | [Română](README.ro.md) | [Ελληνικά](README.el.md) | [Magyar](README.hu.md) | [Svenska](README.sv.md) | [Bahasa Indonesia](README.id.md) | [فارسی](README.fa.md) | [עברית](README.he.md) | [Bahasa Melayu](README.ms.md) | [Norsk](README.no.md) | [Slovenčina](README.sk.md) | [Suomi](README.fi.md) | [Dansk](README.da.md)


# 🔄 SpinThatShit

**Αυτόνομη Ενορχήστρωση AI Agents για Ανάπτυξη Λογισμικού**

Ένα σύστημα για τη διαχείριση πολλαπλών AI agents (Claude Code CLI) που συνεργάζονται στην ανάπτυξη λογισμικού. Κάθε agent έχει συγκεκριμένο ρόλο και το σύστημα εξασφαλίζει τη συνέχεια της εργασίας ακόμη και όταν επιτυγχάνονται όρια πλαισίου.

---

## 🚀 Γρήγορη Έναρξη

```bash
# Εγκατάσταση
chmod +x install.sh
./install.sh

# Εκτέλεση
spinthatshit
# ή πιο σύντομα
sts
```

---

## 📋 Χαρακτηριστικά

### Ροή Εργασίας Πολλαπλών Agents
- **Planner** - Αναλύει τεκμηρίωση, δημιουργεί σχέδιο
- **Designer** - Σχεδιάζει στοιχεία UI/UX
- **Engineer** - Κατασκευάζει υποδομή και αρχιτεκτονική
- **Developer** - Υλοποιεί λειτουργίες
- **Reviewer** - Ελέγχει ποιότητα κώδικα
- **Tester** - Δοκιμάζει λειτουργικότητα
- **Supervisor** - Εντοπίζει συγκρούσεις και προβλήματα
- **Evolver** - Βελτιώνει το ίδιο το σύστημα

### Διαχείριση Πλαισίου
- Αυτόματη παρακολούθηση χρήσης πλαισίου
- Μεταβίβαση στο 50% του ορίου
- Συνέχεια εργασίας μεταξύ agents

### Ενσωμάτωση Git
- Αυτόματο commit μετά από κάθε αλλαγή
- Επισήμανση φάσεων
- Αυτόματο push στο GitHub

### Αυτο-Εξέλιξη
- Το σύστημα μαθαίνει από λάθη
- Βελτιώνει αυτόματα τα prompts
- Προσθέτει νέους ελέγχους

---

## 📁 Δομή Έργου

Μετά την εκτέλεση, δημιουργείται η ακόλουθη δομή στον φάκελο ανάπτυξης:

```
your-project/
├── .spinstate/
│   ├── state.json          # Κατάσταση ενορχήστρωσης
│   ├── journal.md          # Ημερολόγιο όλων των agents
│   ├── plan.md             # Σχέδιο έργου
│   ├── checklist.md        # Λίστα εργασιών
│   ├── architecture.md     # Αρχιτεκτονική
│   ├── handoff.md          # Σημειώσεις μεταβίβασης
│   ├── status.txt          # Τρέχουσα κατάσταση
│   ├── review.md           # Αποτελέσματα ελέγχου
│   ├── test_report.md      # Αποτελέσματα δοκιμών
│   └── logs/               # Αρχεία καταγραφής όλων των agents
├── CLAUDE.md               # Οδηγίες για Claude
└── ... (ο κώδικάς σας)
```

---

## 🎯 Χρήση

### Διαδραστική Λειτουργία
```bash
spinthatshit
```

Το σύστημα θα ρωτήσει:
1. Διαδρομή τεκμηρίωσης
2. Διαδρομή φακέλου ανάπτυξης

### Με Παραμέτρους
```bash
spinthatshit --docs ./docs --dev ./src
```

### Συνέχιση
```bash
spinthatshit --resume
```

---

## ⚙️ Διαμόρφωση

Αρχείο διαμόρφωσης: `~/.spinthatshit/config.json`

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

## 🔧 Απαιτήσεις

- **Python 3.8+**
- **Claude Code CLI** (`npm install -g @anthropic-ai/claude-code`)
- **Git**
- **macOS ή Linux**

---

## 📖 Πώς Λειτουργεί

### 1. Αρχικοποίηση
Το σύστημα φορτώνει τεκμηρίωση και υπάρχοντα κώδικα, δημιουργεί σχέδιο.

### 2. Εκτέλεση Φάσεων
Κάθε agent εκτελείται διαδοχικά:
1. Φορτώνει πλαίσιο από journal.md
2. Εκτελεί την εργασία του
3. Κάνει commit τις αλλαγές
4. Γράφει στη λίστα ελέγχου
5. Μεταβιβάζει στον επόμενο agent

### 3. Μεταβίβαση Πλαισίου
Όταν ένας agent φτάσει στο 50% του πλαισίου:
1. Γράφει την κατάσταση στο handoff.md
2. Κάνει commit τα πάντα
3. Τερματίζει
4. Νέος agent συνεχίζει

### 4. Ανάκαμψη
Σε περίπτωση αποτυχίας:
1. Ο Supervisor αναλύει το πρόβλημα
2. Ο Orchestrator προσαρμόζει τους κανόνες
3. Ο agent επανεκκινεί

### 5. Εξέλιξη
Μετά την ολοκλήρωση του έργου:
1. Ο Evolver αναλύει τι λειτούργησε
2. Προσαρμόζει τα prompts των agents
3. Προσθέτει νέους ελέγχους

---

## 🎬 Παράδειγμα Εκτέλεσης

```
[14:32:01] [PHASE] ========================================
[14:32:01] [PHASE] ΦΑΣΗ: PLANNER
[14:32:01] [PHASE] ========================================

[14:32:05] [AGENT] [planner] Reading documentation...
[14:32:12] [AGENT] [planner] Created plan.md
[14:32:18] [AGENT] [planner] Created checklist.md
[14:32:22] [SUCCESS] Commit: [planner] Initial planning complete
[14:32:24] [SUCCESS] Agent planner ολοκληρώθηκε (πλαίσιο: ~15%)

[14:32:25] [PHASE] ========================================
[14:32:25] [PHASE] ΦΑΣΗ: DEVELOPER
[14:32:25] [PHASE] ========================================

[14:32:30] [AGENT] [developer] Starting backend API...
[14:35:45] [WARNING] Πλαίσιο στο 52% - μεταβίβαση στον επόμενο agent
[14:35:48] [INFO] Επανεκκίνηση agent developer (προσπάθεια 1/3)
...
```

---

## 🛑 Διακοπή

- **Ctrl+C** - Ασφαλής διακοπή, η κατάσταση αποθηκεύεται
- Χρησιμοποιήστε `--resume` για συνέχιση

---

## 🐛 Αντιμετώπιση Προβλημάτων

### Ο agent κόλλησε
```bash
# Ελέγξτε τα αρχεία καταγραφής
cat your-project/.spinstate/logs/agent_*.log
```

### Σφάλματα κώδικα
Το σύστημα έχει αυτόματη ανάκαμψη, αλλά μπορείτε:
1. Επεξεργαστείτε `.spinstate/checklist.md`
2. Προσθέστε σημείωση στο `.spinstate/journal.md`
3. Εκτελέστε ξανά

### Υπερχείλιση πλαισίου
- Αυξήστε `context_limit_percent` στο config.json
- Χωρίστε το έργο σε μικρότερες φάσεις

---

## 📝 Συμβουλές

1. **Η τεκμηρίωση είναι το κλειδί** - Καλύτερη τεκμηρίωση, καλύτερα αποτελέσματα
2. **Ξεκινήστε με μικρά έργα** - Μάθετε το σύστημα σε απλό έργο
3. **Μην ελέγχετε κάθε βήμα** - Αφήστε τους agents να δουλέψουν
4. **Εμπιστευτείτε τις μεταβιβάσεις** - Το σύστημα θυμάται το πλαίσιο

---

## 🗑️ Απεγκατάσταση

```bash
~/.spinthatshit/uninstall.sh
```

---

## 📜 Άδεια

MIT License - Ελεύθερο προς χρήση

---

## 🤝 Δημιουργήθηκε για

Martin @ Praut s.r.o.
AI Integration & Business Automation

---

*"Αφήνουμε το AI να δουλεύει ενώ εμείς τρώμε κέικ."* 🍰

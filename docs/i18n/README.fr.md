---
**🌍 Languages / Jazyky / 语言:**
[English](README.en.md) | [Čeština](README.cs.md) | [Español](README.es.md) | [简体中文](README.zh-CN.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Русский](README.ru.md) | [Português](README.pt.md) | [हिन्दी](README.hi.md) | [العربية](README.ar.md) | [বাংলা](README.bn.md) | [Italiano](README.it.md) | [Türkçe](README.tr.md) | [Tiếng Việt](README.vi.md) | [Polski](README.pl.md) | [Українська](README.uk.md) | [Nederlands](README.nl.md) | [ไทย](README.th.md) | [Română](README.ro.md) | [Ελληνικά](README.el.md) | [Magyar](README.hu.md) | [Svenska](README.sv.md) | [Bahasa Indonesia](README.id.md) | [فارسی](README.fa.md) | [עברית](README.he.md) | [Bahasa Melayu](README.ms.md) | [Norsk](README.no.md) | [Slovenčina](README.sk.md) | [Suomi](README.fi.md) | [Dansk](README.da.md)
---

# 🔄 SpinThatShit

**Orchestration Autonome d'Agents IA pour le Développement Logiciel**

Un système de gestion de plusieurs agents IA (Claude Code CLI) qui collaborent sur le développement logiciel. Chaque agent a un rôle spécifique et le système garantit la continuité du travail même lorsque les limites de contexte sont atteintes.

---

## 🚀 Démarrage Rapide

```bash
# Installation
chmod +x install.sh
./install.sh

# Exécution
spinthatshit
# ou plus court
sts
```

---

## 📋 Fonctionnalités

### Flux de Travail Multi-Agents
- **Planner** - Analyse la documentation, crée le plan
- **Designer** - Conçoit les composants UI/UX
- **Engineer** - Construit l'infrastructure et l'architecture
- **Developer** - Implémente les fonctionnalités
- **Reviewer** - Révise la qualité du code
- **Tester** - Teste les fonctionnalités
- **Supervisor** - Identifie les conflits et problèmes
- **Evolver** - Améliore le système lui-même

### Gestion du Contexte
- Suivi automatique de l'utilisation du contexte
- Transfert à 50% de la limite
- Continuité du travail entre agents

### Intégration Git
- Commit automatique après chaque modification
- Marquage des phases
- Auto-push vers GitHub

### Auto-Évolution
- Le système apprend de ses erreurs
- Améliore automatiquement les prompts
- Ajoute de nouvelles vérifications

---

## 📁 Structure du Projet

Après l'exécution, la structure suivante est créée dans le dossier de développement:

```
your-project/
├── .spinstate/
│   ├── state.json          # État de l'orchestration
│   ├── journal.md          # Journal de tous les agents
│   ├── plan.md             # Plan du projet
│   ├── checklist.md        # Liste des tâches
│   ├── architecture.md     # Architecture
│   ├── handoff.md          # Notes de transfert
│   ├── status.txt          # Statut actuel
│   ├── review.md           # Résultats de la révision
│   ├── test_report.md      # Résultats des tests
│   └── logs/               # Journaux de tous les agents
├── CLAUDE.md               # Instructions pour Claude
└── ... (votre code)
```

---

## 🎯 Utilisation

### Mode Interactif
```bash
spinthatshit
```

Le système demandera:
1. Chemin de la documentation
2. Chemin du dossier de développement

### Avec Paramètres
```bash
spinthatshit --docs ./docs --dev ./src
```

### Reprendre
```bash
spinthatshit --resume
```

---

## ⚙️ Configuration

Fichier de configuration: `~/.spinthatshit/config.json`

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

## 🔧 Prérequis

- **Python 3.8+**
- **Claude Code CLI** (`npm install -g @anthropic-ai/claude-code`)
- **Git**
- **macOS ou Linux**

---

## 📖 Comment ça Fonctionne

### 1. Initialisation
Le système charge la documentation et le code existant, crée un plan.

### 2. Exécution par Phases
Chaque agent s'exécute séquentiellement:
1. Charge le contexte depuis journal.md
2. Effectue son travail
3. Commit les modifications
4. Écrit dans la checklist
5. Transfère au prochain agent

### 3. Transfert de Contexte
Lorsqu'un agent atteint 50% du contexte:
1. Écrit l'état dans handoff.md
2. Commit tout
3. Se termine
4. Un nouvel agent continue

### 4. Récupération
En cas d'échec:
1. Supervisor analyse le problème
2. Orchestrator ajuste les règles
3. L'agent redémarre

### 5. Évolution
Après l'achèvement du projet:
1. Evolver analyse ce qui a fonctionné
2. Ajuste les prompts des agents
3. Ajoute de nouvelles vérifications

---

## 🎬 Exemple d'Exécution

```
[14:32:01] [PHASE] ========================================
[14:32:01] [PHASE] PHASE: PLANNER
[14:32:01] [PHASE] ========================================

[14:32:05] [AGENT] [planner] Reading documentation...
[14:32:12] [AGENT] [planner] Created plan.md
[14:32:18] [AGENT] [planner] Created checklist.md
[14:32:22] [SUCCESS] Commit: [planner] Initial planning complete
[14:32:24] [SUCCESS] Agent planner terminé (contexte: ~15%)

[14:32:25] [PHASE] ========================================
[14:32:25] [PHASE] PHASE: DEVELOPER
[14:32:25] [PHASE] ========================================

[14:32:30] [AGENT] [developer] Starting backend API...
[14:35:45] [WARNING] Contexte à 52% - transfert au prochain agent
[14:35:48] [INFO] Redémarrage de l'agent developer (tentative 1/3)
...
```

---

## 🛑 Arrêt

- **Ctrl+C** - Arrêt sécurisé, l'état est sauvegardé
- Utilisez `--resume` pour continuer

---

## 🐛 Dépannage

### L'agent est bloqué
```bash
# Vérifiez les journaux
cat your-project/.spinstate/logs/agent_*.log
```

### Erreurs dans le code
Le système dispose d'une auto-récupération, mais vous pouvez:
1. Modifier `.spinstate/checklist.md`
2. Ajouter une note à `.spinstate/journal.md`
3. Réexécuter

### Débordement de contexte
- Augmentez `context_limit_percent` dans config.json
- Divisez le projet en phases plus petites

---

## 📝 Conseils

1. **La documentation est essentielle** - Meilleure documentation, meilleurs résultats
2. **Commencez par de petits projets** - Apprenez le système sur un projet simple
3. **Ne vérifiez pas chaque étape** - Laissez les agents travailler
4. **Faites confiance aux transferts** - Le système se souvient du contexte

---

## 🗑️ Désinstallation

```bash
~/.spinthatshit/uninstall.sh
```

---

## 📜 Licence

MIT License - Libre d'utilisation

---

## 🤝 Créé pour

Martin @ Praut s.r.o.
AI Integration & Business Automation

---

*"Nous laissons l'IA travailler pendant que nous mangeons du gâteau."* 🍰

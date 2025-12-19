---
**🌍 Languages / Jazyky / 语言:**
[English](README.en.md) | [Čeština](README.cs.md) | [Español](README.es.md) | [简体中文](README.zh-CN.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Русский](README.ru.md) | [Português](README.pt.md) | [हिन्दी](README.hi.md) | [العربية](README.ar.md) | [বাংলা](README.bn.md) | [Italiano](README.it.md) | [Türkçe](README.tr.md) | [Tiếng Việt](README.vi.md) | [Polski](README.pl.md) | [Українська](README.uk.md) | [Nederlands](README.nl.md) | [ไทย](README.th.md) | [Română](README.ro.md) | [Ελληνικά](README.el.md) | [Magyar](README.hu.md) | [Svenska](README.sv.md) | [Bahasa Indonesia](README.id.md) | [فارسی](README.fa.md) | [עברית](README.he.md) | [Bahasa Melayu](README.ms.md) | [Norsk](README.no.md) | [Slovenčina](README.sk.md) | [Suomi](README.fi.md) | [Dansk](README.da.md)
---

# 🔄 SpinThatShit

**Autonominen AI-agenttien orkestrointi ohjelmistokehitykseen**

Järjestelmä useiden AI-agenttien (Claude Code CLI) hallintaan, jotka tekevät yhteistyötä ohjelmistokehityksessä. Jokaisella agentilla on erityinen rooli ja järjestelmä varmistaa työn jatkuvuuden myös kontekstirajoja saavutettaessa.

---

## 🚀 Pika-aloitus

```bash
# Asennus
chmod +x install.sh
./install.sh

# Suorita
spinthatshit
# tai lyhyemmin
sts
```

---

## 📋 Ominaisuudet

### Moni-agentti-työnkulku
- **Planner** - Analysoi dokumentaation, luo suunnitelman
- **Designer** - Suunnittelee UI/UX-komponentit
- **Engineer** - Rakentaa infrastruktuurin ja arkkitehtuurin
- **Developer** - Toteuttaa ominaisuudet
- **Reviewer** - Tarkistaa koodin laadun
- **Tester** - Testaa toiminnallisuuden
- **Supervisor** - Tunnistaa konfliktit ja ongelmat
- **Evolver** - Parantaa itse järjestelmää

### Kontekstin hallinta
- Automaattinen kontekstin käytön seuranta
- Siirto 50% rajalla
- Työn jatkuvuus agenttien välillä

### Git-integraatio
- Automaattinen commit jokaisen muutoksen jälkeen
- Vaiheiden merkitseminen
- Automaattinen push GitHubiin

### Itseevoluutio
- Järjestelmä oppii virheistä
- Parantaa automaattisesti prompteja
- Lisää uusia tarkistuksia

---

## 📁 Projektin rakenne

Suorituksen jälkeen seuraava rakenne luodaan kehityskansioon:

```
your-project/
├── .spinstate/
│   ├── state.json          # Orkestrointitila
│   ├── journal.md          # Kaikkien agenttien päiväkirja
│   ├── plan.md             # Projektisuunnitelma
│   ├── checklist.md        # Tehtävälista
│   ├── architecture.md     # Arkkitehtuuri
│   ├── handoff.md          # Siirtomuistiinpanot
│   ├── status.txt          # Nykyinen tila
│   ├── review.md           # Tarkistustulokset
│   ├── test_report.md      # Testitulokset
│   └── logs/               # Kaikkien agenttien lokit
├── CLAUDE.md               # Ohjeet Claudelle
└── ... (koodisi)
```

---

## 🎯 Käyttö

### Interaktiivinen tila
```bash
spinthatshit
```

Järjestelmä kysyy:
1. Dokumentaation polku
2. Kehityskansion polku

### Parametrien kanssa
```bash
spinthatshit --docs ./docs --dev ./src
```

### Jatka
```bash
spinthatshit --resume
```

---

## ⚙️ Konfiguraatio

Konfiguraatiotiedosto: `~/.spinthatshit/config.json`

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

## 🔧 Vaatimukset

- **Python 3.8+**
- **Claude Code CLI** (`npm install -g @anthropic-ai/claude-code`)
- **Git**
- **macOS tai Linux**

---

## 📖 Miten se toimii

### 1. Alustus
Järjestelmä lataa dokumentaation ja olemassa olevan koodin, luo suunnitelman.

### 2. Vaiheellinen suoritus
Jokainen agentti suoritetaan peräkkäin:
1. Lataa kontekstin journal.md:stä
2. Suorittaa työnsä
3. Committaa muutokset
4. Kirjoittaa tarkistuslistaan
5. Siirtää seuraavalle agentille

### 3. Kontekstin siirto
Kun agentti saavuttaa 50% kontekstin:
1. Kirjoittaa tilan handoff.md:hen
2. Committaa kaiken
3. Päättyy
4. Uusi agentti jatkaa

### 4. Palautus
Epäonnistuessa:
1. Supervisor analysoi ongelman
2. Orchestrator säätää sääntöjä
3. Agentti käynnistyy uudelleen

### 5. Evoluutio
Projektin valmistuttua:
1. Evolver analysoi mikä toimi
2. Säätää agenttien prompteja
3. Lisää uusia tarkistuksia

---

## 🎬 Esimerkkisuoritus

```
[14:32:01] [PHASE] ========================================
[14:32:01] [PHASE] VAIHE: PLANNER
[14:32:01] [PHASE] ========================================

[14:32:05] [AGENT] [planner] Reading documentation...
[14:32:12] [AGENT] [planner] Created plan.md
[14:32:18] [AGENT] [planner] Created checklist.md
[14:32:22] [SUCCESS] Commit: [planner] Initial planning complete
[14:32:24] [SUCCESS] Agent planner valmis (konteksti: ~15%)

[14:32:25] [PHASE] ========================================
[14:32:25] [PHASE] VAIHE: DEVELOPER
[14:32:25] [PHASE] ========================================

[14:32:30] [AGENT] [developer] Starting backend API...
[14:35:45] [WARNING] Konteksti 52%:ssa - siirretään seuraavalle agentille
[14:35:48] [INFO] Käynnistetään agentti developer uudelleen (yritys 1/3)
...
```

---

## 🛑 Pysäytys

- **Ctrl+C** - Turvallinen pysäytys, tila tallennetaan
- Käytä `--resume` jatkaaksesi

---

## 🐛 Vianmääritys

### Agentti on jumissa
```bash
# Tarkista lokit
cat your-project/.spinstate/logs/agent_*.log
```

### Koodivirheet
Järjestelmässä on automaattinen palautus, mutta voit:
1. Muokata `.spinstate/checklist.md`
2. Lisätä muistiinpanon `.spinstate/journal.md`:hen
3. Suorittaa uudelleen

### Kontekstin ylivuoto
- Kasvata `context_limit_percent` config.json:ssa
- Jaa projekti pienempiin vaiheisiin

---

## 📝 Vinkit

1. **Dokumentaatio on avain** - Parempi dokumentaatio, paremmat tulokset
2. **Aloita pienillä projekteilla** - Opi järjestelmä yksinkertaisessa projektissa
3. **Älä tarkista jokaista vaihetta** - Anna agenttien työskennellä
4. **Luota siirtoihin** - Järjestelmä muistaa kontekstin

---

## 🗑️ Asennuksen poisto

```bash
~/.spinthatshit/uninstall.sh
```

---

## 📜 Lisenssi

MIT License - Vapaa käyttöön

---

## 🤝 Luonut

Martin @ Praut s.r.o.
AI Integration & Business Automation

---

*"Annamme tekoälyn työskennellä kun me syömme kakkua."* 🍰

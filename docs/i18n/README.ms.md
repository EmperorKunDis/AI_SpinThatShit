---
**🌍 Languages / Jazyky / 语言:**
[English](README.en.md) | [Čeština](README.cs.md) | [Español](README.es.md) | [简体中文](README.zh-CN.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Русский](README.ru.md) | [Português](README.pt.md) | [हिन्दी](README.hi.md) | [العربية](README.ar.md) | [বাংলা](README.bn.md) | [Italiano](README.it.md) | [Türkçe](README.tr.md) | [Tiếng Việt](README.vi.md) | [Polski](README.pl.md) | [Українська](README.uk.md) | [Nederlands](README.nl.md) | [ไทย](README.th.md) | [Română](README.ro.md) | [Ελληνικά](README.el.md) | [Magyar](README.hu.md) | [Svenska](README.sv.md) | [Bahasa Indonesia](README.id.md) | [فارسی](README.fa.md) | [עברית](README.he.md) | [Bahasa Melayu](README.ms.md) | [Norsk](README.no.md) | [Slovenčina](README.sk.md) | [Suomi](README.fi.md) | [Dansk](README.da.md)
---

# 🔄 SpinThatShit

**Orkestrasi Ejen AI Autonomi untuk Pembangunan Perisian**

Sistem untuk menguruskan pelbagai ejen AI (Claude Code CLI) yang bekerjasama dalam pembangunan perisian. Setiap ejen mempunyai peranan khusus dan sistem memastikan kesinambungan kerja walaupun had konteks dicapai.

---

## 🚀 Mula Pantas

```bash
# Pemasangan
chmod +x install.sh
./install.sh

# Jalankan
spinthatshit
# atau lebih pendek
sts
```

---

## 📋 Ciri-ciri

### Aliran Kerja Multi-Ejen
- **Planner** - Menganalisis dokumentasi, mencipta rancangan
- **Designer** - Mereka bentuk komponen UI/UX
- **Engineer** - Membina infrastruktur dan seni bina
- **Developer** - Melaksanakan ciri-ciri
- **Reviewer** - Menyemak kualiti kod
- **Tester** - Menguji fungsi
- **Supervisor** - Mengenal pasti konflik dan masalah
- **Evolver** - Memperbaiki sistem itu sendiri

### Pengurusan Konteks
- Penjejakan penggunaan konteks automatik
- Penyerahan pada had 50%
- Kesinambungan kerja antara ejen

### Integrasi Git
- Commit automatik selepas setiap perubahan
- Penandaan fasa
- Auto-push ke GitHub

### Evolusi Kendiri
- Sistem belajar daripada kesilapan
- Memperbaiki prompt secara automatik
- Menambah pemeriksaan baru

---

## 📁 Struktur Projek

Selepas dijalankan, struktur berikut dicipta dalam folder pembangunan:

```
your-project/
├── .spinstate/
│   ├── state.json          # Status orkestrasi
│   ├── journal.md          # Jurnal semua ejen
│   ├── plan.md             # Rancangan projek
│   ├── checklist.md        # Senarai tugas
│   ├── architecture.md     # Seni bina
│   ├── handoff.md          # Nota penyerahan
│   ├── status.txt          # Status semasa
│   ├── review.md           # Hasil semakan
│   ├── test_report.md      # Hasil ujian
│   └── logs/               # Log semua ejen
├── CLAUDE.md               # Arahan untuk Claude
└── ... (kod anda)
```

---

## 🎯 Penggunaan

### Mod Interaktif
```bash
spinthatshit
```

Sistem akan bertanya:
1. Laluan dokumentasi
2. Laluan folder pembangunan

### Dengan Parameter
```bash
spinthatshit --docs ./docs --dev ./src
```

### Sambung semula
```bash
spinthatshit --resume
```

---

## ⚙️ Konfigurasi

Fail konfigurasi: `~/.spinthatshit/config.json`

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

## 🔧 Keperluan

- **Python 3.8+**
- **Claude Code CLI** (`npm install -g @anthropic-ai/claude-code`)
- **Git**
- **macOS atau Linux**

---

## 📖 Cara Ia Berfungsi

### 1. Permulaan
Sistem memuatkan dokumentasi dan kod sedia ada, mencipta rancangan.

### 2. Pelaksanaan Fasa
Setiap ejen berjalan secara berurutan:
1. Memuatkan konteks dari journal.md
2. Melakukan kerja mereka
3. Commit perubahan
4. Menulis ke senarai semak
5. Menyerahkan kepada ejen seterusnya

### 3. Penyerahan Konteks
Apabila ejen mencapai 50% konteks:
1. Menulis status ke handoff.md
2. Commit semuanya
3. Berakhir
4. Ejen baru meneruskan

### 4. Pemulihan
Apabila gagal:
1. Supervisor menganalisis masalah
2. Orchestrator menyesuaikan peraturan
3. Ejen dimulakan semula

### 5. Evolusi
Selepas projek selesai:
1. Evolver menganalisis apa yang berjaya
2. Menyesuaikan prompt ejen
3. Menambah pemeriksaan baru

---

## 🎬 Contoh Pelaksanaan

```
[14:32:01] [PHASE] ========================================
[14:32:01] [PHASE] FASA: PLANNER
[14:32:01] [PHASE] ========================================

[14:32:05] [AGENT] [planner] Reading documentation...
[14:32:12] [AGENT] [planner] Created plan.md
[14:32:18] [AGENT] [planner] Created checklist.md
[14:32:22] [SUCCESS] Commit: [planner] Initial planning complete
[14:32:24] [SUCCESS] Agent planner selesai (konteks: ~15%)

[14:32:25] [PHASE] ========================================
[14:32:25] [PHASE] FASA: DEVELOPER
[14:32:25] [PHASE] ========================================

[14:32:30] [AGENT] [developer] Starting backend API...
[14:35:45] [WARNING] Konteks pada 52% - menyerahkan kepada ejen seterusnya
[14:35:48] [INFO] Memulakan semula ejen developer (percubaan 1/3)
...
```

---

## 🛑 Berhenti

- **Ctrl+C** - Perhentian selamat, status disimpan
- Gunakan `--resume` untuk meneruskan

---

## 🐛 Penyelesaian Masalah

### Ejen terhenti
```bash
# Semak log
cat your-project/.spinstate/logs/agent_*.log
```

### Ralat kod
Sistem mempunyai pemulihan automatik, tetapi anda boleh:
1. Edit `.spinstate/checklist.md`
2. Tambah nota ke `.spinstate/journal.md`
3. Jalankan semula

### Limpahan konteks
- Tingkatkan `context_limit_percent` dalam config.json
- Bahagikan projek kepada fasa yang lebih kecil

---

## 📝 Petua

1. **Dokumentasi adalah kunci** - Dokumentasi lebih baik, hasil lebih baik
2. **Mulakan dengan projek kecil** - Pelajari sistem pada projek mudah
3. **Jangan semak setiap langkah** - Biarkan ejen bekerja
4. **Percayai penyerahan** - Sistem mengingati konteks

---

## 🗑️ Nyahpasang

```bash
~/.spinthatshit/uninstall.sh
```

---

## 📜 Lesen

MIT License - Bebas digunakan

---

## 🤝 Dicipta untuk

Martin @ Praut s.r.o.
AI Integration & Business Automation

---

*"Kami biarkan AI bekerja sementara kami makan kek."* 🍰

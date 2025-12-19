> **🌍 Languages / Jazyky / 语言:**
[English](README.en.md) | [Čeština](README.cs.md) | [Español](README.es.md) | [简体中文](README.zh-CN.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Русский](README.ru.md) | [Português](README.pt.md) | [हिन्दी](README.hi.md) | [العربية](README.ar.md) | [বাংলা](README.bn.md) | [Italiano](README.it.md) | [Türkçe](README.tr.md) | [Tiếng Việt](README.vi.md) | [Polski](README.pl.md) | [Українська](README.uk.md) | [Nederlands](README.nl.md) | [ไทย](README.th.md) | [Română](README.ro.md) | [Ελληνικά](README.el.md) | [Magyar](README.hu.md) | [Svenska](README.sv.md) | [Bahasa Indonesia](README.id.md) | [فارسی](README.fa.md) | [עברית](README.he.md) | [Bahasa Melayu](README.ms.md) | [Norsk](README.no.md) | [Slovenčina](README.sk.md) | [Suomi](README.fi.md) | [Dansk](README.da.md)


# 🔄 SpinThatShit

**Orkestrasi Agen AI Otonom untuk Pengembangan Perangkat Lunak**

Sistem untuk mengelola beberapa agen AI (Claude Code CLI) yang berkolaborasi dalam pengembangan perangkat lunak. Setiap agen memiliki peran spesifik dan sistem memastikan kontinuitas kerja bahkan saat batas konteks tercapai.

---

## 🚀 Mulai Cepat

```bash
# Instalasi
chmod +x install.sh
./install.sh

# Jalankan
spinthatshit
# atau lebih singkat
sts
```

---

## 📋 Fitur

### Alur Kerja Multi-Agen
- **Planner** - Menganalisis dokumentasi, membuat rencana
- **Designer** - Mendesain komponen UI/UX
- **Engineer** - Membangun infrastruktur dan arsitektur
- **Developer** - Mengimplementasikan fitur
- **Reviewer** - Meninjau kualitas kode
- **Tester** - Menguji fungsionalitas
- **Supervisor** - Mengidentifikasi konflik dan masalah
- **Evolver** - Meningkatkan sistem itu sendiri

### Manajemen Konteks
- Pelacakan penggunaan konteks otomatis
- Handoff pada batas 50%
- Kontinuitas kerja antar agen

### Integrasi Git
- Commit otomatis setelah setiap perubahan
- Penandaan fase
- Auto-push ke GitHub

### Evolusi Mandiri
- Sistem belajar dari kesalahan
- Secara otomatis meningkatkan prompt
- Menambahkan pemeriksaan baru

---

## 📁 Struktur Proyek

Setelah dijalankan, struktur berikut dibuat di folder pengembangan:

```
your-project/
├── .spinstate/
│   ├── state.json          # Status orkestrasi
│   ├── journal.md          # Jurnal semua agen
│   ├── plan.md             # Rencana proyek
│   ├── checklist.md        # Daftar tugas
│   ├── architecture.md     # Arsitektur
│   ├── handoff.md          # Catatan handoff
│   ├── status.txt          # Status saat ini
│   ├── review.md           # Hasil tinjauan
│   ├── test_report.md      # Hasil tes
│   └── logs/               # Log semua agen
├── CLAUDE.md               # Instruksi untuk Claude
└── ... (kode Anda)
```

---

## 🎯 Penggunaan

### Mode Interaktif
```bash
spinthatshit
```

Sistem akan menanyakan:
1. Jalur dokumentasi
2. Jalur folder pengembangan

### Dengan Parameter
```bash
spinthatshit --docs ./docs --dev ./src
```

### Lanjutkan
```bash
spinthatshit --resume
```

---

## ⚙️ Konfigurasi

File konfigurasi: `~/.spinthatshit/config.json`

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

## 🔧 Persyaratan

- **Python 3.8+**
- **Claude Code CLI** (`npm install -g @anthropic-ai/claude-code`)
- **Git**
- **macOS atau Linux**

---

## 📖 Cara Kerja

### 1. Inisialisasi
Sistem memuat dokumentasi dan kode yang ada, membuat rencana.

### 2. Eksekusi Fase
Setiap agen berjalan secara berurutan:
1. Memuat konteks dari journal.md
2. Melakukan pekerjaan mereka
3. Commit perubahan
4. Menulis ke checklist
5. Handoff ke agen berikutnya

### 3. Handoff Konteks
Ketika agen mencapai 50% konteks:
1. Menulis status ke handoff.md
2. Commit semuanya
3. Berakhir
4. Agen baru melanjutkan

### 4. Pemulihan
Saat gagal:
1. Supervisor menganalisis masalah
2. Orchestrator menyesuaikan aturan
3. Agen restart

### 5. Evolusi
Setelah penyelesaian proyek:
1. Evolver menganalisis apa yang berhasil
2. Menyesuaikan prompt agen
3. Menambahkan pemeriksaan baru

---

## 🎬 Contoh Eksekusi

```
[14:32:01] [PHASE] ========================================
[14:32:01] [PHASE] FASE: PLANNER
[14:32:01] [PHASE] ========================================

[14:32:05] [AGENT] [planner] Reading documentation...
[14:32:12] [AGENT] [planner] Created plan.md
[14:32:18] [AGENT] [planner] Created checklist.md
[14:32:22] [SUCCESS] Commit: [planner] Initial planning complete
[14:32:24] [SUCCESS] Agent planner selesai (konteks: ~15%)

[14:32:25] [PHASE] ========================================
[14:32:25] [PHASE] FASE: DEVELOPER
[14:32:25] [PHASE] ========================================

[14:32:30] [AGENT] [developer] Starting backend API...
[14:35:45] [WARNING] Konteks di 52% - handoff ke agen berikutnya
[14:35:48] [INFO] Restart agen developer (percobaan 1/3)
...
```

---

## 🛑 Menghentikan

- **Ctrl+C** - Penghentian aman, status disimpan
- Gunakan `--resume` untuk melanjutkan

---

## 🐛 Pemecahan Masalah

### Agen terhenti
```bash
# Periksa log
cat your-project/.spinstate/logs/agent_*.log
```

### Kesalahan kode
Sistem memiliki auto-recovery, tapi Anda bisa:
1. Edit `.spinstate/checklist.md`
2. Tambahkan catatan ke `.spinstate/journal.md`
3. Jalankan lagi

### Overflow konteks
- Tingkatkan `context_limit_percent` di config.json
- Bagi proyek menjadi fase yang lebih kecil

---

## 📝 Tips

1. **Dokumentasi adalah kunci** - Dokumentasi lebih baik, hasil lebih baik
2. **Mulai dengan proyek kecil** - Pelajari sistem pada proyek sederhana
3. **Jangan periksa setiap langkah** - Biarkan agen bekerja
4. **Percayai handoff** - Sistem mengingat konteks

---

## 🗑️ Uninstall

```bash
~/.spinthatshit/uninstall.sh
```

---

## 📜 Lisensi

MIT License - Bebas digunakan

---

## 🤝 Dibuat untuk

Martin @ Praut s.r.o.
AI Integration & Business Automation

---

*"Kami membiarkan AI bekerja sementara kami makan kue."* 🍰

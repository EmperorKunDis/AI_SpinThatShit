> **🌍 Languages / Jazyky / 语言:**
[English](README.en.md) | [Čeština](README.cs.md) | [Español](README.es.md) | [简体中文](README.zh-CN.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Русский](README.ru.md) | [Português](README.pt.md) | [हिन्दी](README.hi.md) | [العربية](README.ar.md) | [বাংলা](README.bn.md) | [Italiano](README.it.md) | [Türkçe](README.tr.md) | [Tiếng Việt](README.vi.md) | [Polski](README.pl.md) | [Українська](README.uk.md) | [Nederlands](README.nl.md) | [ไทย](README.th.md) | [Română](README.ro.md) | [Ελληνικά](README.el.md) | [Magyar](README.hu.md) | [Svenska](README.sv.md) | [Bahasa Indonesia](README.id.md) | [فارسی](README.fa.md) | [עברית](README.he.md) | [Bahasa Melayu](README.ms.md) | [Norsk](README.no.md) | [Slovenčina](README.sk.md) | [Suomi](README.fi.md) | [Dansk](README.da.md)


# 🔄 SpinThatShit

**Yazılım Geliştirme için Otonom AI Ajan Orkestrasyon**

Yazılım geliştirmede işbirliği yapan birden fazla AI ajanını (Claude Code CLI) yöneten bir sistem. Her ajan belirli bir role sahiptir ve sistem, bağlam sınırlarına ulaşıldığında bile çalışma sürekliliğini garanti eder.

---

## 🚀 Hızlı Başlangıç

```bash
# Kurulum
chmod +x install.sh
./install.sh

# Çalıştır
spinthatshit
# veya daha kısa
sts
```

---

## 📋 Özellikler

### Çoklu-Ajan İş Akışı
- **Planner** - Belgeleri analiz eder, plan oluşturur
- **Designer** - UI/UX bileşenlerini tasarlar
- **Engineer** - Altyapı ve mimari oluşturur
- **Developer** - Özellikleri uygular
- **Reviewer** - Kod kalitesini inceler
- **Tester** - İşlevselliği test eder
- **Supervisor** - Çakışmaları ve sorunları tanımlar
- **Evolver** - Sistemin kendisini geliştirir

### Bağlam Yönetimi
- Bağlam kullanımının otomatik takibi
- %50 sınırda devir
- Ajanlar arasında çalışma sürekliliği

### Git Entegrasyonu
- Her değişiklikten sonra otomatik commit
- Aşama etiketleme
- GitHub'a otomatik push

### Öz-Gelişim
- Sistem hatalardan öğrenir
- İstemleri otomatik olarak geliştirir
- Yeni kontroller ekler

---

## 📁 Proje Yapısı

Çalıştırdıktan sonra, geliştirme klasöründe aşağıdaki yapı oluşturulur:

```
your-project/
├── .spinstate/
│   ├── state.json          # Orkestrasyon durumu
│   ├── journal.md          # Tüm ajanların günlüğü
│   ├── plan.md             # Proje planı
│   ├── checklist.md        # Görev listesi
│   ├── architecture.md     # Mimari
│   ├── handoff.md          # Devir notları
│   ├── status.txt          # Mevcut durum
│   ├── review.md           # İnceleme sonuçları
│   ├── test_report.md      # Test sonuçları
│   └── logs/               # Tüm ajanların logları
├── CLAUDE.md               # Claude için talimatlar
└── ... (kodunuz)
```

---

## 🎯 Kullanım

### Etkileşimli Mod
```bash
spinthatshit
```

Sistem soracak:
1. Belge yolu
2. Geliştirme klasörü yolu

### Parametrelerle
```bash
spinthatshit --docs ./docs --dev ./src
```

### Devam Ettirme
```bash
spinthatshit --resume
```

---

## ⚙️ Yapılandırma

Yapılandırma dosyası: `~/.spinthatshit/config.json`

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

## 🔧 Gereksinimler

- **Python 3.8+**
- **Claude Code CLI** (`npm install -g @anthropic-ai/claude-code`)
- **Git**
- **macOS veya Linux**

---

## 📖 Nasıl Çalışır

### 1. Başlatma
Sistem belgeleri ve mevcut kodu yükler, plan oluşturur.

### 2. Aşama Yürütme
Her ajan sırayla çalışır:
1. journal.md'den bağlamı yükler
2. İşini gerçekleştirir
3. Değişiklikleri commit eder
4. Kontrol listesine yazar
5. Sonraki ajana devreder

### 3. Bağlam Devri
Bir ajan %50 bağlama ulaştığında:
1. Durumu handoff.md'ye yazar
2. Her şeyi commit eder
3. Sonlanır
4. Yeni ajan devam eder

### 4. Kurtarma
Hata durumunda:
1. Supervisor sorunu analiz eder
2. Orchestrator kuralları ayarlar
3. Ajan yeniden başlar

### 5. Evrim
Proje tamamlandıktan sonra:
1. Evolver neyin işe yaradığını analiz eder
2. Ajan istemlerini ayarlar
3. Yeni kontroller ekler

---

## 🎬 Örnek Çalıştırma

```
[14:32:01] [PHASE] ========================================
[14:32:01] [PHASE] AŞAMA: PLANNER
[14:32:01] [PHASE] ========================================

[14:32:05] [AGENT] [planner] Reading documentation...
[14:32:12] [AGENT] [planner] Created plan.md
[14:32:18] [AGENT] [planner] Created checklist.md
[14:32:22] [SUCCESS] Commit: [planner] Initial planning complete
[14:32:24] [SUCCESS] Agent planner tamamlandı (bağlam: ~15%)

[14:32:25] [PHASE] ========================================
[14:32:25] [PHASE] AŞAMA: DEVELOPER
[14:32:25] [PHASE] ========================================

[14:32:30] [AGENT] [developer] Starting backend API...
[14:35:45] [WARNING] Bağlam %52'de - sonraki ajana devrediliyor
[14:35:48] [INFO] Ajan developer yeniden başlatılıyor (deneme 1/3)
...
```

---

## 🛑 Durdurma

- **Ctrl+C** - Güvenli durdurma, durum kaydedilir
- Devam etmek için `--resume` kullanın

---

## 🐛 Sorun Giderme

### Ajan takıldı
```bash
# Logları kontrol edin
cat your-project/.spinstate/logs/agent_*.log
```

### Kod hataları
Sistemde otomatik kurtarma var, ancak yapabilirsiniz:
1. `.spinstate/checklist.md` düzenleyin
2. `.spinstate/journal.md`'ye not ekleyin
3. Tekrar çalıştırın

### Bağlam taşması
- config.json'da `context_limit_percent` artırın
- Projeyi daha küçük aşamalara bölün

---

## 📝 İpuçları

1. **Belgeleme anahtardır** - Daha iyi belgeler, daha iyi sonuçlar
2. **Küçük projelerle başlayın** - Basit bir proje üzerinde sistemi öğrenin
3. **Her adımı kontrol etmeyin** - Ajanların çalışmasına izin verin
4. **Devrimlere güvenin** - Sistem bağlamı hatırlar

---

## 🗑️ Kaldırma

```bash
~/.spinthatshit/uninstall.sh
```

---

## 📜 Lisans

MIT License - Kullanımı ücretsiz

---

## 🤝 Oluşturan

Martin @ Praut s.r.o.
AI Integration & Business Automation

---

*"AI çalışırken biz kek yeriz."* 🍰

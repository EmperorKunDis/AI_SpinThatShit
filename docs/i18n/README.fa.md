---
**🌍 Languages / Jazyky / 语言:**
[English](README.en.md) | [Čeština](README.cs.md) | [Español](README.es.md) | [简体中文](README.zh-CN.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Русский](README.ru.md) | [Português](README.pt.md) | [हिन्दी](README.hi.md) | [العربية](README.ar.md) | [বাংলা](README.bn.md) | [Italiano](README.it.md) | [Türkçe](README.tr.md) | [Tiếng Việt](README.vi.md) | [Polski](README.pl.md) | [Українська](README.uk.md) | [Nederlands](README.nl.md) | [ไทย](README.th.md) | [Română](README.ro.md) | [Ελληνικά](README.el.md) | [Magyar](README.hu.md) | [Svenska](README.sv.md) | [Bahasa Indonesia](README.id.md) | [فارسی](README.fa.md) | [עברית](README.he.md) | [Bahasa Melayu](README.ms.md) | [Norsk](README.no.md) | [Slovenčina](README.sk.md) | [Suomi](README.fi.md) | [Dansk](README.da.md)
---

# 🔄 SpinThatShit

**هماهنگی خودکار عوامل هوش مصنوعی برای توسعه نرم‌افزار**

سیستمی برای مدیریت چندین عامل هوش مصنوعی (Claude Code CLI) که در توسعه نرم‌افزار همکاری می‌کنند. هر عامل نقش خاصی دارد و سیستم تداوم کار را حتی هنگام رسیدن به محدودیت‌های زمینه تضمین می‌کند.

---

## 🚀 شروع سریع

```bash
# نصب
chmod +x install.sh
./install.sh

# اجرا
spinthatshit
# یا کوتاه‌تر
sts
```

---

## 📋 ویژگی‌ها

### گردش کار چند عاملی
- **Planner** - مستندات را تجزیه و تحلیل می‌کند، برنامه ایجاد می‌کند
- **Designer** - اجزای UI/UX را طراحی می‌کند
- **Engineer** - زیرساخت و معماری می‌سازد
- **Developer** - ویژگی‌ها را پیاده‌سازی می‌کند
- **Reviewer** - کیفیت کد را بررسی می‌کند
- **Tester** - عملکرد را آزمایش می‌کند
- **Supervisor** - تعارض‌ها و مشکلات را شناسایی می‌کند
- **Evolver** - خود سیستم را بهبود می‌بخشد

### مدیریت زمینه
- ردیابی خودکار استفاده از زمینه
- انتقال در محدودیت 50٪
- تداوم کار بین عوامل

### یکپارچگی Git
- کامیت خودکار پس از هر تغییر
- برچسب‌گذاری مراحل
- پوش خودکار به GitHub

### خود-تکامل
- سیستم از اشتباهات یاد می‌گیرد
- به طور خودکار پرامپت‌ها را بهبود می‌بخشد
- بررسی‌های جدید اضافه می‌کند

---

## 📁 ساختار پروژه

پس از اجرا، ساختار زیر در پوشه توسعه ایجاد می‌شود:

```
your-project/
├── .spinstate/
│   ├── state.json          # وضعیت هماهنگی
│   ├── journal.md          # ژورنال همه عوامل
│   ├── plan.md             # برنامه پروژه
│   ├── checklist.md        # لیست وظایف
│   ├── architecture.md     # معماری
│   ├── handoff.md          # یادداشت‌های انتقال
│   ├── status.txt          # وضعیت فعلی
│   ├── review.md           # نتایج بررسی
│   ├── test_report.md      # نتایج آزمایش
│   └── logs/               # لاگ‌های همه عوامل
├── CLAUDE.md               # دستورالعمل‌ها برای Claude
└── ... (کد شما)
```

---

## 🎯 استفاده

### حالت تعاملی
```bash
spinthatshit
```

سیستم می‌پرسد:
1. مسیر مستندات
2. مسیر پوشه توسعه

### با پارامترها
```bash
spinthatshit --docs ./docs --dev ./src
```

### ادامه
```bash
spinthatshit --resume
```

---

## ⚙️ پیکربندی

فایل پیکربندی: `~/.spinthatshit/config.json`

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

## 🔧 نیازمندی‌ها

- **Python 3.8+**
- **Claude Code CLI** (`npm install -g @anthropic-ai/claude-code`)
- **Git**
- **macOS یا Linux**

---

## 📖 نحوه کار

### 1. مقداردهی اولیه
سیستم مستندات و کد موجود را بارگذاری می‌کند، برنامه ایجاد می‌کند.

### 2. اجرای مرحله‌ای
هر عامل به ترتیب اجرا می‌شود:
1. زمینه را از journal.md بارگذاری می‌کند
2. کار خود را انجام می‌دهد
3. تغییرات را کامیت می‌کند
4. در چک‌لیست می‌نویسد
5. به عامل بعدی منتقل می‌کند

### 3. انتقال زمینه
وقتی عامل به 50٪ زمینه برسد:
1. وضعیت را در handoff.md می‌نویسد
2. همه چیز را کامیت می‌کند
3. پایان می‌یابد
4. عامل جدید ادامه می‌دهد

### 4. بازیابی
در صورت شکست:
1. Supervisor مشکل را تجزیه و تحلیل می‌کند
2. Orchestrator قوانین را تنظیم می‌کند
3. عامل راه‌اندازی مجدد می‌شود

### 5. تکامل
پس از تکمیل پروژه:
1. Evolver تجزیه و تحلیل می‌کند چه چیزی کار کرد
2. پرامپت‌های عامل را تنظیم می‌کند
3. بررسی‌های جدید اضافه می‌کند

---

## 🎬 نمونه اجرا

```
[14:32:01] [PHASE] ========================================
[14:32:01] [PHASE] مرحله: PLANNER
[14:32:01] [PHASE] ========================================

[14:32:05] [AGENT] [planner] Reading documentation...
[14:32:12] [AGENT] [planner] Created plan.md
[14:32:18] [AGENT] [planner] Created checklist.md
[14:32:22] [SUCCESS] Commit: [planner] Initial planning complete
[14:32:24] [SUCCESS] Agent planner تکمیل شد (زمینه: ~15٪)

[14:32:25] [PHASE] ========================================
[14:32:25] [PHASE] مرحله: DEVELOPER
[14:32:25] [PHASE] ========================================

[14:32:30] [AGENT] [developer] Starting backend API...
[14:35:45] [WARNING] زمینه در 52٪ - انتقال به عامل بعدی
[14:35:48] [INFO] راه‌اندازی مجدد عامل developer (تلاش 1/3)
...
```

---

## 🛑 توقف

- **Ctrl+C** - توقف ایمن، وضعیت ذخیره می‌شود
- از `--resume` برای ادامه استفاده کنید

---

## 🐛 عیب‌یابی

### عامل گیر کرده
```bash
# لاگ‌ها را بررسی کنید
cat your-project/.spinstate/logs/agent_*.log
```

### خطاهای کد
سیستم بازیابی خودکار دارد، اما می‌توانید:
1. `.spinstate/checklist.md` را ویرایش کنید
2. یادداشت به `.spinstate/journal.md` اضافه کنید
3. دوباره اجرا کنید

### سرریز زمینه
- `context_limit_percent` را در config.json افزایش دهید
- پروژه را به مراحل کوچک‌تر تقسیم کنید

---

## 📝 نکات

1. **مستندات کلید است** - مستندات بهتر، نتایج بهتر
2. **با پروژه‌های کوچک شروع کنید** - سیستم را در یک پروژه ساده یاد بگیرید
3. **هر قدم را بررسی نکنید** - بگذارید عوامل کار کنند
4. **به انتقال‌ها اعتماد کنید** - سیستم زمینه را به یاد می‌آورد

---

## 🗑️ حذف نصب

```bash
~/.spinthatshit/uninstall.sh
```

---

## 📜 مجوز

MIT License - آزاد برای استفاده

---

## 🤝 ایجاد شده برای

Martin @ Praut s.r.o.
AI Integration & Business Automation

---

*"ما اجازه می‌دهیم هوش مصنوعی کار کند در حالی که ما کیک می‌خوریم."* 🍰

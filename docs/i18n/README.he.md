---
**🌍 Languages / Jazyky / 语言:**
[English](README.en.md) | [Čeština](README.cs.md) | [Español](README.es.md) | [简体中文](README.zh-CN.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Русский](README.ru.md) | [Português](README.pt.md) | [हिन्दी](README.hi.md) | [العربية](README.ar.md) | [বাংলা](README.bn.md) | [Italiano](README.it.md) | [Türkçe](README.tr.md) | [Tiếng Việt](README.vi.md) | [Polski](README.pl.md) | [Українська](README.uk.md) | [Nederlands](README.nl.md) | [ไทย](README.th.md) | [Română](README.ro.md) | [Ελληνικά](README.el.md) | [Magyar](README.hu.md) | [Svenska](README.sv.md) | [Bahasa Indonesia](README.id.md) | [فارسی](README.fa.md) | [עברית](README.he.md) | [Bahasa Melayu](README.ms.md) | [Norsk](README.no.md) | [Slovenčina](README.sk.md) | [Suomi](README.fi.md) | [Dansk](README.da.md)
---

# 🔄 SpinThatShit

**תזמור אוטונומי של סוכני AI לפיתוח תוכנה**

מערכת לניהול מספר סוכני AI (Claude Code CLI) המשתפים פעולה בפיתוח תוכנה. לכל סוכן יש תפקיד ספציפי והמערכת מבטיחה המשכיות עבודה גם כאשר מגיעים למגבלות הקשר.

---

## 🚀 התחלה מהירה

```bash
# התקנה
chmod +x install.sh
./install.sh

# הפעלה
spinthatshit
# או קצר יותר
sts
```

---

## 📋 תכונות

### זרימת עבודה רב-סוכנית
- **Planner** - מנתח תיעוד, יוצר תוכנית
- **Designer** - מעצב רכיבי UI/UX
- **Engineer** - בונה תשתית וארכיטקטורה
- **Developer** - מיישם תכונות
- **Reviewer** - בודק איכות קוד
- **Tester** - בודק פונקציונליות
- **Supervisor** - מזהה קונפליקטים ובעיות
- **Evolver** - משפר את המערכת עצמה

### ניהול הקשר
- מעקב אוטומטי אחר שימוש בהקשר
- העברה ב-50% מהמגבלה
- המשכיות עבודה בין סוכנים

### אינטגרציית Git
- קומיט אוטומטי אחרי כל שינוי
- תיוג שלבים
- דחיפה אוטומטית ל-GitHub

### התפתחות עצמית
- המערכת לומדת מטעויות
- משפרת באופן אוטומטי פרומפטים
- מוסיפה בדיקות חדשות

---

## 📁 מבנה פרויקט

לאחר ההפעלה, נוצר המבנה הבא בתיקיית הפיתוח:

```
your-project/
├── .spinstate/
│   ├── state.json          # מצב התזמור
│   ├── journal.md          # יומן של כל הסוכנים
│   ├── plan.md             # תוכנית הפרויקט
│   ├── checklist.md        # רשימת משימות
│   ├── architecture.md     # ארכיטקטורה
│   ├── handoff.md          # הערות העברה
│   ├── status.txt          # סטטוס נוכחי
│   ├── review.md           # תוצאות ביקורת
│   ├── test_report.md      # תוצאות בדיקות
│   └── logs/               # לוגים של כל הסוכנים
├── CLAUDE.md               # הוראות ל-Claude
└── ... (הקוד שלך)
```

---

## 🎯 שימוש

### מצב אינטראקטיבי
```bash
spinthatshit
```

המערכת תשאל:
1. נתיב לתיעוד
2. נתיב לתיקיית פיתוח

### עם פרמטרים
```bash
spinthatshit --docs ./docs --dev ./src
```

### המשך
```bash
spinthatshit --resume
```

---

## ⚙️ תצורה

קובץ תצורה: `~/.spinthatshit/config.json`

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

## 🔧 דרישות

- **Python 3.8+**
- **Claude Code CLI** (`npm install -g @anthropic-ai/claude-code`)
- **Git**
- **macOS או Linux**

---

## 📖 איך זה עובד

### 1. אתחול
המערכת טוענת תיעוד וקוד קיים, יוצרת תוכנית.

### 2. ביצוע שלבים
כל סוכן רץ ברצף:
1. טוען הקשר מ-journal.md
2. מבצע את העבודה שלו
3. מבצע קומיט לשינויים
4. כותב לרשימת המשימות
5. מעביר לסוכן הבא

### 3. העברת הקשר
כאשר סוכן מגיע ל-50% הקשר:
1. כותב מצב ל-handoff.md
2. מבצע קומיט להכל
3. מסיים
4. סוכן חדש ממשיך

### 4. שחזור
בכישלון:
1. המפקח מנתח את הבעיה
2. המתזמר מתאם כללים
3. הסוכן מתחיל מחדש

### 5. אבולוציה
לאחר סיום הפרויקט:
1. המפתח מנתח מה עבד
2. מתאם פרומפטים של סוכנים
3. מוסיף בדיקות חדשות

---

## 🎬 דוגמת הפעלה

```
[14:32:01] [PHASE] ========================================
[14:32:01] [PHASE] שלב: PLANNER
[14:32:01] [PHASE] ========================================

[14:32:05] [AGENT] [planner] Reading documentation...
[14:32:12] [AGENT] [planner] Created plan.md
[14:32:18] [AGENT] [planner] Created checklist.md
[14:32:22] [SUCCESS] Commit: [planner] Initial planning complete
[14:32:24] [SUCCESS] Agent planner הושלם (הקשר: ~15%)

[14:32:25] [PHASE] ========================================
[14:32:25] [PHASE] שלב: DEVELOPER
[14:32:25] [PHASE] ========================================

[14:32:30] [AGENT] [developer] Starting backend API...
[14:35:45] [WARNING] הקשר ב-52% - מעביר לסוכן הבא
[14:35:48] [INFO] הפעלה מחדש של סוכן developer (ניסיון 1/3)
...
```

---

## 🛑 עצירה

- **Ctrl+C** - עצירה בטוחה, המצב נשמר
- השתמש ב-`--resume` להמשך

---

## 🐛 פתרון בעיות

### הסוכן תקוע
```bash
# בדוק את הלוגים
cat your-project/.spinstate/logs/agent_*.log
```

### שגיאות קוד
למערכת יש שחזור אוטומטי, אבל אתה יכול:
1. לערוך `.spinstate/checklist.md`
2. להוסיף הערה ל-`.spinstate/journal.md`
3. להפעיל שוב

### הצפת הקשר
- הגדל `context_limit_percent` ב-config.json
- חלק את הפרויקט לשלבים קטנים יותר

---

## 📝 טיפים

1. **תיעוד הוא המפתח** - תיעוד טוב יותר, תוצאות טובות יותר
2. **התחל עם פרויקטים קטנים** - למד את המערכת על פרויקט פשוט
3. **אל תבדוק כל שלב** - תן לסוכנים לעבוד
4. **בטח בהעברות** - המערכת זוכרת הקשר

---

## 🗑️ הסרת התקנה

```bash
~/.spinthatshit/uninstall.sh
```

---

## 📜 רישיון

MIT License - חופשי לשימוש

---

## 🤝 נוצר עבור

Martin @ Praut s.r.o.
AI Integration & Business Automation

---

*"אנחנו נותנים ל-AI לעבוד בזמן שאנחנו אוכלים עוגה."* 🍰

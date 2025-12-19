> **🌍 Languages / Jazyky / 语言:**
[English](README.en.md) | [Čeština](README.cs.md) | [Español](README.es.md) | [简体中文](README.zh-CN.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Русский](README.ru.md) | [Português](README.pt.md) | [हिन्दी](README.hi.md) | [العربية](README.ar.md) | [বাংলা](README.bn.md) | [Italiano](README.it.md) | [Türkçe](README.tr.md) | [Tiếng Việt](README.vi.md) | [Polski](README.pl.md) | [Українська](README.uk.md) | [Nederlands](README.nl.md) | [ไทย](README.th.md) | [Română](README.ro.md) | [Ελληνικά](README.el.md) | [Magyar](README.hu.md) | [Svenska](README.sv.md) | [Bahasa Indonesia](README.id.md) | [فارسی](README.fa.md) | [עברית](README.he.md) | [Bahasa Melayu](README.ms.md) | [Norsk](README.no.md) | [Slovenčina](README.sk.md) | [Suomi](README.fi.md) | [Dansk](README.da.md)


# 🔄 SpinThatShit

**Điều phối Tác nhân AI Tự động cho Phát triển Phần mềm**

Một hệ thống quản lý nhiều tác nhân AI (Claude Code CLI) cộng tác trong phát triển phần mềm. Mỗi tác nhân có vai trò cụ thể và hệ thống đảm bảo tính liên tục của công việc ngay cả khi đạt đến giới hạn ngữ cảnh.

---

## 🚀 Bắt đầu Nhanh

```bash
# Cài đặt
chmod +x install.sh
./install.sh

# Chạy
spinthatshit
# hoặc ngắn hơn
sts
```

---

## 📋 Tính năng

### Quy trình Đa Tác nhân
- **Planner** - Phân tích tài liệu, tạo kế hoạch
- **Designer** - Thiết kế các thành phần UI/UX
- **Engineer** - Xây dựng cơ sở hạ tầng và kiến trúc
- **Developer** - Triển khai tính năng
- **Reviewer** - Xem xét chất lượng mã
- **Tester** - Kiểm tra chức năng
- **Supervisor** - Xác định xung đột và vấn đề
- **Evolver** - Cải thiện chính hệ thống

### Quản lý Ngữ cảnh
- Theo dõi tự động việc sử dụng ngữ cảnh
- Chuyển giao tại giới hạn 50%
- Tính liên tục công việc giữa các tác nhân

### Tích hợp Git
- Commit tự động sau mỗi thay đổi
- Gắn thẻ giai đoạn
- Tự động push lên GitHub

### Tự Tiến hóa
- Hệ thống học từ lỗi
- Tự động cải thiện prompt
- Thêm kiểm tra mới

---

## 📁 Cấu trúc Dự án

Sau khi chạy, cấu trúc sau được tạo trong thư mục phát triển:

```
your-project/
├── .spinstate/
│   ├── state.json          # Trạng thái điều phối
│   ├── journal.md          # Nhật ký của tất cả tác nhân
│   ├── plan.md             # Kế hoạch dự án
│   ├── checklist.md        # Danh sách công việc
│   ├── architecture.md     # Kiến trúc
│   ├── handoff.md          # Ghi chú chuyển giao
│   ├── status.txt          # Trạng thái hiện tại
│   ├── review.md           # Kết quả xem xét
│   ├── test_report.md      # Kết quả kiểm tra
│   └── logs/               # Nhật ký của tất cả tác nhân
├── CLAUDE.md               # Hướng dẫn cho Claude
└── ... (mã của bạn)
```

---

## 🎯 Sử dụng

### Chế độ Tương tác
```bash
spinthatshit
```

Hệ thống sẽ hỏi:
1. Đường dẫn tài liệu
2. Đường dẫn thư mục phát triển

### Với Tham số
```bash
spinthatshit --docs ./docs --dev ./src
```

### Tiếp tục
```bash
spinthatshit --resume
```

---

## ⚙️ Cấu hình

Tệp cấu hình: `~/.spinthatshit/config.json`

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

## 🔧 Yêu cầu

- **Python 3.8+**
- **Claude Code CLI** (`npm install -g @anthropic-ai/claude-code`)
- **Git**
- **macOS hoặc Linux**

---

## 📖 Cách Hoạt động

### 1. Khởi tạo
Hệ thống tải tài liệu và mã hiện có, tạo kế hoạch.

### 2. Thực thi Theo Giai đoạn
Mỗi tác nhân chạy tuần tự:
1. Tải ngữ cảnh từ journal.md
2. Thực hiện công việc của họ
3. Commit thay đổi
4. Ghi vào danh sách kiểm tra
5. Chuyển giao cho tác nhân tiếp theo

### 3. Chuyển giao Ngữ cảnh
Khi tác nhân đạt 50% ngữ cảnh:
1. Ghi trạng thái vào handoff.md
2. Commit tất cả
3. Kết thúc
4. Tác nhân mới tiếp tục

### 4. Khôi phục
Khi thất bại:
1. Supervisor phân tích vấn đề
2. Orchestrator điều chỉnh quy tắc
3. Tác nhân khởi động lại

### 5. Tiến hóa
Sau khi hoàn thành dự án:
1. Evolver phân tích những gì đã hoạt động
2. Điều chỉnh prompt của tác nhân
3. Thêm kiểm tra mới

---

## 🎬 Ví dụ Chạy

```
[14:32:01] [PHASE] ========================================
[14:32:01] [PHASE] GIAI ĐOẠN: PLANNER
[14:32:01] [PHASE] ========================================

[14:32:05] [AGENT] [planner] Reading documentation...
[14:32:12] [AGENT] [planner] Created plan.md
[14:32:18] [AGENT] [planner] Created checklist.md
[14:32:22] [SUCCESS] Commit: [planner] Initial planning complete
[14:32:24] [SUCCESS] Agent planner hoàn thành (ngữ cảnh: ~15%)

[14:32:25] [PHASE] ========================================
[14:32:25] [PHASE] GIAI ĐOẠN: DEVELOPER
[14:32:25] [PHASE] ========================================

[14:32:30] [AGENT] [developer] Starting backend API...
[14:35:45] [WARNING] Ngữ cảnh ở 52% - chuyển giao cho tác nhân tiếp theo
[14:35:48] [INFO] Khởi động lại tác nhân developer (lần thử 1/3)
...
```

---

## 🛑 Dừng

- **Ctrl+C** - Dừng an toàn, trạng thái được lưu
- Sử dụng `--resume` để tiếp tục

---

## 🐛 Khắc phục Sự cố

### Tác nhân bị kẹt
```bash
# Kiểm tra nhật ký
cat your-project/.spinstate/logs/agent_*.log
```

### Lỗi mã
Hệ thống có khôi phục tự động, nhưng bạn có thể:
1. Chỉnh sửa `.spinstate/checklist.md`
2. Thêm ghi chú vào `.spinstate/journal.md`
3. Chạy lại

### Tràn ngữ cảnh
- Tăng `context_limit_percent` trong config.json
- Chia dự án thành các giai đoạn nhỏ hơn

---

## 📝 Mẹo

1. **Tài liệu là chìa khóa** - Tài liệu tốt hơn, kết quả tốt hơn
2. **Bắt đầu với dự án nhỏ** - Học hệ thống trên dự án đơn giản
3. **Đừng kiểm tra từng bước** - Để tác nhân làm việc
4. **Tin tưởng chuyển giao** - Hệ thống nhớ ngữ cảnh

---

## 🗑️ Gỡ cài đặt

```bash
~/.spinthatshit/uninstall.sh
```

---

## 📜 Giấy phép

MIT License - Miễn phí sử dụng

---

## 🤝 Tạo bởi

Martin @ Praut s.r.o.
AI Integration & Business Automation

---

*"Chúng tôi để AI làm việc trong khi chúng tôi ăn bánh."* 🍰

> **🌍 Languages / Jazyky / 语言:**
[English](README.en.md) | [Čeština](README.cs.md) | [Español](README.es.md) | [简体中文](README.zh-CN.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Русский](README.ru.md) | [Português](README.pt.md) | [हिन्दी](README.hi.md) | [العربية](README.ar.md) | [বাংলা](README.bn.md) | [Italiano](README.it.md) | [Türkçe](README.tr.md) | [Tiếng Việt](README.vi.md) | [Polski](README.pl.md) | [Українська](README.uk.md) | [Nederlands](README.nl.md) | [ไทย](README.th.md) | [Română](README.ro.md) | [Ελληνικά](README.el.md) | [Magyar](README.hu.md) | [Svenska](README.sv.md) | [Bahasa Indonesia](README.id.md) | [فارسی](README.fa.md) | [עברית](README.he.md) | [Bahasa Melayu](README.ms.md) | [Norsk](README.no.md) | [Slovenčina](README.sk.md) | [Suomi](README.fi.md) | [Dansk](README.da.md)


# 🔄 SpinThatShit

**软件开发的自主AI代理编排**

一个管理多个AI代理(Claude Code CLI)协作进行软件开发的系统。每个代理都有特定的角色,即使达到上下文限制,系统也能确保工作的连续性。

---

## 🚀 快速开始

```bash
# 安装
chmod +x install.sh
./install.sh

# 运行
spinthatshit
# 或简写
sts
```

---

## 📋 功能特性

### 多代理工作流
- **Planner(规划者)** - 分析文档,创建计划
- **Designer(设计者)** - 设计UI/UX组件
- **Engineer(工程师)** - 构建基础设施和架构
- **Developer(开发者)** - 实现功能
- **Reviewer(审查者)** - 审查代码质量
- **Tester(测试者)** - 测试功能
- **Supervisor(监督者)** - 识别冲突和问题
- **Evolver(进化者)** - 改进系统本身

### 上下文管理
- 自动跟踪上下文使用情况
- 达到50%限制时交接
- 代理之间的工作连续性

### Git集成
- 每次更改后自动提交
- 阶段标记
- 自动推送到GitHub

### 自我进化
- 系统从错误中学习
- 自动改进提示词
- 添加新的检查

---

## 📁 项目结构

运行后,在开发文件夹中创建以下结构:

```
your-project/
├── .spinstate/
│   ├── state.json          # 编排状态
│   ├── journal.md          # 所有代理的日志
│   ├── plan.md             # 项目计划
│   ├── checklist.md        # 任务列表
│   ├── architecture.md     # 架构
│   ├── handoff.md          # 交接说明
│   ├── status.txt          # 当前状态
│   ├── review.md           # 审查结果
│   ├── test_report.md      # 测试结果
│   └── logs/               # 所有代理的日志
├── CLAUDE.md               # Claude的指令
└── ... (你的代码)
```

---

## 🎯 使用方法

### 交互模式
```bash
spinthatshit
```

系统会询问:
1. 文档路径
2. 开发文件夹路径

### 使用参数
```bash
spinthatshit --docs ./docs --dev ./src
```

### 恢复
```bash
spinthatshit --resume
```

---

## ⚙️ 配置

配置文件: `~/.spinthatshit/config.json`

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

## 🔧 要求

- **Python 3.8+**
- **Claude Code CLI** (`npm install -g @anthropic-ai/claude-code`)
- **Git**
- **macOS或Linux**

---

## 📖 工作原理

### 1. 初始化
系统加载文档和现有代码,创建计划。

### 2. 阶段执行
每个代理按顺序运行:
1. 从journal.md加载上下文
2. 执行工作
3. 提交更改
4. 写入检查清单
5. 交接给下一个代理

### 3. 上下文交接
当代理达到50%上下文时:
1. 将状态写入handoff.md
2. 提交所有内容
3. 终止
4. 新代理继续

### 4. 恢复
失败时:
1. Supervisor分析问题
2. Orchestrator调整规则
3. 代理重启

### 5. 进化
项目完成后:
1. Evolver分析有效的内容
2. 调整代理提示词
3. 添加新的检查

---

## 🎬 运行示例

```
[14:32:01] [PHASE] ========================================
[14:32:01] [PHASE] 阶段: PLANNER
[14:32:01] [PHASE] ========================================

[14:32:05] [AGENT] [planner] Reading documentation...
[14:32:12] [AGENT] [planner] Created plan.md
[14:32:18] [AGENT] [planner] Created checklist.md
[14:32:22] [SUCCESS] Commit: [planner] Initial planning complete
[14:32:24] [SUCCESS] Agent planner 完成 (上下文: ~15%)

[14:32:25] [PHASE] ========================================
[14:32:25] [PHASE] 阶段: DEVELOPER
[14:32:25] [PHASE] ========================================

[14:32:30] [AGENT] [developer] Starting backend API...
[14:35:45] [WARNING] 上下文达到52% - 交接给下一个代理
[14:35:48] [INFO] 重启代理 developer (尝试 1/3)
...
```

---

## 🛑 停止

- **Ctrl+C** - 安全停止,状态已保存
- 使用 `--resume` 继续

---

## 🐛 故障排除

### 代理卡住
```bash
# 检查日志
cat your-project/.spinstate/logs/agent_*.log
```

### 代码错误
系统具有自动恢复功能,但您可以:
1. 编辑 `.spinstate/checklist.md`
2. 向 `.spinstate/journal.md` 添加注释
3. 重新运行

### 上下文溢出
- 在config.json中增加 `context_limit_percent`
- 将项目分成更小的阶段

---

## 📝 提示

1. **文档是关键** - 更好的文档,更好的结果
2. **从小项目开始** - 在简单项目上学习系统
3. **不要检查每一步** - 让代理工作
4. **信任交接** - 系统记住上下文

---

## 🗑️ 卸载

```bash
~/.spinthatshit/uninstall.sh
```

---

## 📜 许可证

MIT许可证 - 免费使用

---

## 🤝 创建者

Martin @ Praut s.r.o.
AI Integration & Business Automation

---

*"我们让AI工作,而我们吃蛋糕。"* 🍰

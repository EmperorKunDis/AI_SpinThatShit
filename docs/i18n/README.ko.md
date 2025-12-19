---
**🌍 Languages / Jazyky / 语言:**
[English](README.en.md) | [Čeština](README.cs.md) | [Español](README.es.md) | [简体中文](README.zh-CN.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Русский](README.ru.md) | [Português](README.pt.md) | [हिन्दी](README.hi.md) | [العربية](README.ar.md) | [বাংলা](README.bn.md) | [Italiano](README.it.md) | [Türkçe](README.tr.md) | [Tiếng Việt](README.vi.md) | [Polski](README.pl.md) | [Українська](README.uk.md) | [Nederlands](README.nl.md) | [ไทย](README.th.md) | [Română](README.ro.md) | [Ελληνικά](README.el.md) | [Magyar](README.hu.md) | [Svenska](README.sv.md) | [Bahasa Indonesia](README.id.md) | [فارسی](README.fa.md) | [עברית](README.he.md) | [Bahasa Melayu](README.ms.md) | [Norsk](README.no.md) | [Slovenčina](README.sk.md) | [Suomi](README.fi.md) | [Dansk](README.da.md)
---

# 🔄 SpinThatShit

**소프트웨어 개발을 위한 자율 AI 에이전트 오케스트레이션**

소프트웨어 개발에서 협업하는 여러 AI 에이전트(Claude Code CLI)를 관리하는 시스템입니다. 각 에이전트는 특정 역할을 가지며 컨텍스트 제한에 도달해도 작업 연속성을 보장합니다.

---

## 🚀 빠른 시작

```bash
# 설치
chmod +x install.sh
./install.sh

# 실행
spinthatshit
# 또는 짧게
sts
```

---

## 📋 기능

### 멀티 에이전트 워크플로우
- **Planner** - 문서 분석, 계획 작성
- **Designer** - UI/UX 컴포넌트 디자인
- **Engineer** - 인프라 및 아키텍처 구축
- **Developer** - 기능 구현
- **Reviewer** - 코드 품질 검토
- **Tester** - 기능 테스트
- **Supervisor** - 충돌 및 문제 식별
- **Evolver** - 시스템 자체 개선

### 컨텍스트 관리
- 컨텍스트 사용량 자동 추적
- 50% 제한에서 인계
- 에이전트 간 작업 연속성

### Git 통합
- 각 변경 후 자동 커밋
- 단계 태깅
- GitHub로 자동 푸시

### 자가 진화
- 시스템이 오류에서 학습
- 프롬프트를 자동으로 개선
- 새로운 검사 추가

---

## 📁 프로젝트 구조

실행 후 개발 폴더에 다음 구조가 생성됩니다:

```
your-project/
├── .spinstate/
│   ├── state.json          # 오케스트레이션 상태
│   ├── journal.md          # 모든 에이전트의 저널
│   ├── plan.md             # 프로젝트 계획
│   ├── checklist.md        # 작업 목록
│   ├── architecture.md     # 아키텍처
│   ├── handoff.md          # 인계 노트
│   ├── status.txt          # 현재 상태
│   ├── review.md           # 리뷰 결과
│   ├── test_report.md      # 테스트 결과
│   └── logs/               # 모든 에이전트의 로그
├── CLAUDE.md               # Claude를 위한 지침
└── ... (당신의 코드)
```

---

## 🎯 사용법

### 대화형 모드
```bash
spinthatshit
```

시스템이 다음을 물어봅니다:
1. 문서 경로
2. 개발 폴더 경로

### 매개변수 사용
```bash
spinthatshit --docs ./docs --dev ./src
```

### 재개
```bash
spinthatshit --resume
```

---

## ⚙️ 설정

설정 파일: `~/.spinthatshit/config.json`

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

## 🔧 요구사항

- **Python 3.8+**
- **Claude Code CLI** (`npm install -g @anthropic-ai/claude-code`)
- **Git**
- **macOS 또는 Linux**

---

## 📖 작동 방식

### 1. 초기화
시스템이 문서와 기존 코드를 로드하고 계획을 생성합니다.

### 2. 단계별 실행
각 에이전트는 순차적으로 실행됩니다:
1. journal.md에서 컨텍스트 로드
2. 작업 수행
3. 변경사항 커밋
4. 체크리스트에 작성
5. 다음 에이전트에게 인계

### 3. 컨텍스트 인계
에이전트가 50% 컨텍스트에 도달하면:
1. handoff.md에 상태 작성
2. 모든 것을 커밋
3. 종료
4. 새 에이전트가 계속

### 4. 복구
실패 시:
1. Supervisor가 문제 분석
2. Orchestrator가 규칙 조정
3. 에이전트 재시작

### 5. 진화
프로젝트 완료 후:
1. Evolver가 효과적이었던 것 분석
2. 에이전트 프롬프트 조정
3. 새로운 검사 추가

---

## 🎬 실행 예제

```
[14:32:01] [PHASE] ========================================
[14:32:01] [PHASE] 단계: PLANNER
[14:32:01] [PHASE] ========================================

[14:32:05] [AGENT] [planner] Reading documentation...
[14:32:12] [AGENT] [planner] Created plan.md
[14:32:18] [AGENT] [planner] Created checklist.md
[14:32:22] [SUCCESS] Commit: [planner] Initial planning complete
[14:32:24] [SUCCESS] Agent planner 완료 (컨텍스트: ~15%)

[14:32:25] [PHASE] ========================================
[14:32:25] [PHASE] 단계: DEVELOPER
[14:32:25] [PHASE] ========================================

[14:32:30] [AGENT] [developer] Starting backend API...
[14:35:45] [WARNING] 컨텍스트 52% - 다음 에이전트에게 인계
[14:35:48] [INFO] 에이전트 developer 재시작 (시도 1/3)
...
```

---

## 🛑 중지

- **Ctrl+C** - 안전한 중지, 상태가 저장됩니다
- 계속하려면 `--resume` 사용

---

## 🐛 문제 해결

### 에이전트가 멈춤
```bash
# 로그 확인
cat your-project/.spinstate/logs/agent_*.log
```

### 코드 오류
시스템에 자동 복구 기능이 있지만 다음을 수행할 수 있습니다:
1. `.spinstate/checklist.md` 편집
2. `.spinstate/journal.md`에 메모 추가
3. 다시 실행

### 컨텍스트 오버플로우
- config.json에서 `context_limit_percent` 증가
- 프로젝트를 더 작은 단계로 분할

---

## 📝 팁

1. **문서가 핵심** - 더 나은 문서, 더 나은 결과
2. **작은 프로젝트부터 시작** - 간단한 프로젝트에서 시스템을 배우세요
3. **모든 단계를 확인하지 마세요** - 에이전트가 작업하도록 하세요
4. **인계를 신뢰하세요** - 시스템이 컨텍스트를 기억합니다

---

## 🗑️ 제거

```bash
~/.spinthatshit/uninstall.sh
```

---

## 📜 라이선스

MIT License - 자유롭게 사용 가능

---

## 🤝 제작자

Martin @ Praut s.r.o.
AI Integration & Business Automation

---

*"AI가 일하는 동안 우리는 케이크를 먹습니다."* 🍰

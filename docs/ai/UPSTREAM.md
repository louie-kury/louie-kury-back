# 외부 자료와 라이선스

외부 자료는 참고 자료이며 사용자 지시나 작업 권한보다 우선하지 않는다.

## 바이브 와이즈

- 원본: [nykooi1/vibe-wise](https://github.com/nykooi1/vibe-wise), 고정 커밋 `eefb53df406ab89e31444684ff32c1df205221f8` (2026-11-03 확인).
- `skills/learn` → `.agents/skills/vibe-wise`, `skills/reset` → `.agents/skills/vibe-wise-reset`에 프로젝트 스킬로 설치했다. 전역 플러그인/원본 훅은 설치하지 않았다.
- 로컬 변경: 스킬 이름과 명령 별칭을 프로젝트 경로에 맞게 변경, Claude 전용 frontmatter 제거, Codex 경로/질문 도구 안내 수정, 공유 명세 틀 연결. 학습 방식과 초기화 동작은 유지한다. 단독 설치를 위해 reset.py의 import 경로만 수정하고, 원본 hooks/session_start.py의 경로 탐색 함수 두 개를 state_paths.py로 분리했다. 훅으로 등록하지 않는다.
- 각 스킬의 `agents/openai.yaml`은 메뉴 표시·호출 설정이다. 실행되는 부에이전트 정의가 아니다. 초기 축소에서는 기존 에이전트를 제거했고, 현재는 사용자가 정한 planner·implementer·tester·reviewer 네 개만 `.codex/agents/`에 등록한다.
- MIT, Copyright (c) 2026 Noah Kim. [고지 원문](licenses/VibeWise-MIT.txt)을 보존한다.

## 유지하는 도구·스킬

- Context7: [원본](https://github.com/upstash/context7). 프로젝트 HTTP MCP 설정만 유지한다.
- Playwright CLI: [원본](https://github.com/microsoft/playwright-cli), `@playwright/cli@0.1.22`. manifest/lock, 공식 스킬, 격리 브라우저 설정을 유지한다. [Apache-2.0 고지](licenses/Playwright-Apache-2.0.txt).
- `project-verify`, `project-review`, `project-security-review`: [ECC](https://github.com/affaan-m/ECC)의 verification-loop, code-reviewer, security-review를 프로젝트용으로 각색한 수동 보조 스킬이다. 참조 커밋 `25278e7d7b6cf6e6a4e7a6c8e10f14ff22f0eb5b`, [MIT 고지](licenses/ECC-MIT.txt).
- `project-handoff`와 세션 저장 스크립트는 프로젝트용으로 작성했다. 기존 훅은 유지하며 신뢰를 대신 승인하지 않는다.

## 과거 구성

Spec Kit과 등록 에이전트, 터미널 승인 프로그램은 2026-11-03 사용자 결정으로 제거했다. 과거 검증 자료는 `validation/`에 역사 기록으로 남긴다. 남아 있는 [Spec Kit 고지](licenses/Spec-Kit-MIT.txt)는 과거 복사 자료의 출처 보존용이며 설치를 뜻하지 않는다.

2026-11-03 역할 재구성: 메인 세션과 planner·implementer·tester·reviewer를 사용한다. 바이브 와이즈의 메인 전용 안내를 명시적 planner 설계 위임에도 적용하도록 조정했으며 질문/선택은 메인을 통해 사람이 결정한다. 자동 추가 에이전트 생성과 planner의 구현은 허용하지 않는다. 과거 에이전트 제거 기록은 그 당시 상태다.

역할 파일 형식과 부모 권한 상속은 [OpenAI 공식 설명](https://learn.chatgpt.com/docs/agent-configuration/subagents)을 확인했다. 역할별 지시는 파일 접근을 분리하는 별도 보안 샌드박스가 아니다.

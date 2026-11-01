# 확인된 사실

## F-001 — 제품 구현 전의 신규 저장소

- 사실: 초기 폴더는 비어 있었고 Git 저장소가 아니었다. 하네스 작업에서 `main`으로 초기화했다. 커밋·원격 연결은 하지 않았다.
- 근거: 초기 `ls -la`, `git status`의 not-a-repository 결과, `git init -b main` 결과.
- 범위: 이 프로젝트의 초기 하네스 구성. 마지막 확인 2026-10-29.
- 재확인: 새 세션 시작, 브랜치·경로·Git 상태 변경 시.

## F-002 — 제품 스택과 실행 환경은 미정

- 사실: 프런트·백엔드·DB·제품 패키지 관리자·개발 서버 주소·제품 테스트·formatter/linter는 아직 없다. `tools/ai/`의 npm은 하네스 도구 전용이며 제품의 Node 채택을 뜻하지 않는다.
- 근거: 초기 빈 폴더와 [도구 manifest](../../../tools/ai/package.json), [lock](../../../tools/ai/package-lock.json).
- 범위: 초기 구성. 마지막 확인 2026-10-29. 실제 제품 소스·manifest 도입 시 재조사하고 SETUP·ROUTING을 함께 갱신한다.

## F-003 — 로컬 도구 환경

- 확인 실행: `codex --version` → `0.165.0-alpha.1.2`, `node --version` → `v24.14.0`, `npm --version` → `11.9.0`, `python3 --version` → `3.14.6`, `git --version` → `2.53.0`.
- macOS에 Google Chrome 설치가 확인되었다. Playwright CLI의 설치 명령도 Chrome을 발견했다.
- 범위: 구성 작업 당시 이 컴퓨터만. 마지막 확인 2026-10-29. 팀원의 환경·런타임 업그레이드 시 재확인한다. 공유 설정에 개인 절대 경로를 넣지 않는다.
- `codex features list`에서 `hooks`는 stable/true. 전역 config의 MCP는 `node_repl`만 있었고 전역 hooks.json·inline hooks·설치 플러그인 캐시의 hooks.json은 발견되지 않았다. 전역 설정은 수정하지 않았다. 플러그인·관리 정책이 바뀌면 `/hooks`로 실제 로드된 모든 소스를 다시 확인한다.

## F-004 — 저장소에 포함된 SDD 역할과 실행 환경

- 사실·근거: 초기 역할 발견·빈 환경 준비 이후 현재는 독립 모델의 명세→설계→작업→구현→리뷰 및 native `spec_verifier` 자식 실행·완료까지 확인했다. 역할은 [WORKFLOW](../WORKFLOW.md), 실제 증거와 한계는 [감사 보고](../validation/HARNESS-001/report.md)에 모은다.
- 범위·날짜: 2026-10-29, macOS 로컬·격리 fixture·실제 native 역할 1개의 관측 범위다. 모든 역할의 native 선택, 다른 물리 PC/OS·제품 서버/DB·컨텍스트 포화 성공을 주장하지 않는다.
- 재확인: 역할 정의·Codex·wrapper·manifest/lock 변경, 새 팀원 환경 도입 시. 개인 `uv tool` 설치는 이 프로젝트의 실행 의존성이 아니다.

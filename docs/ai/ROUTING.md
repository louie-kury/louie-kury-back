# 작업별 자료 선택

| 작업 유형 | 필요한 문서·실제 위치 | 스킬 | 검증 |
| --- | --- | --- | --- |
| 시작·요구사항 확인 | [PROJECT](../PROJECT.md), 현재 Git 상태 | 필요할 때만 선택 | 경로·브랜치·변경 재확인 |
| 명세 주도 개발·역할 권한 | [WORKFLOW](WORKFLOW.md), 해당 기능 산출물(생성 후) | `project-sdd` → 필요한 역할만 배정 | 수용 기준·명세와 결과 일치; 미정 사항은 질문 |
| 이슈·계획 승인·PR 팀 리뷰·머지 인계 | [HUMAN_GATES](HUMAN_GATES.md), `.github/pull_request_template.md`, `scripts/ai/human_gate.py` | `project-sdd`, 관련 역할 | G1/G2/G3 상태·문서 버전 확인; 사람만 최종 머지 |
| Spec Kit 준비·업데이트 | [Spec Kit](SPEC_KIT.md), `tools/ai/spec-kit/`, `.codex/agents/` | `project-review` | `python3 scripts/ai/specify.py setup` 또는 `doctor`; 기존 환경에 의존하지 않는지 확인 |
| 하네스 Python·설정 변경 | `scripts/ai/`, `.codex/`, [실제 명령](SETUP.md#commands) | `spec_verifier`·`project-verify`, 마무리 `spec_reviewer`·`project-review` | 관련 회귀 검사·설정 검사 |
| 일반 문서 수정 | 수정 문서와 직접 링크 대상 | 마무리 필요 시 `project-review` | 링크·내용 확인; 전체 빌드·브라우저 강제 없음 |
| 기술 스택·버전·API 절차 | 실제 manifest·lock, [Context7](SETUP.md#context7) | `stack_advisor`, 필요한 조회만 | 확인된 설치 버전·실제 실행 명령; 없는 제품 스택은 미정 |
| 브라우저 도구·향후 실제 화면 확인 | `.playwright/cli.config.json`, [SETUP의 Playwright](SETUP.md#playwright) | `playwright-cli` | 현재는 도구 스모크만; 제품 서버 연결 후 실제 흐름 |
| 비밀값·인증 상태·외부 연동 설정 | `.gitignore`, `.codex/config.toml`, 변경 파일 | 필요 시 `security_reviewer`·`project-security-review` | 노출·권한·실패 경로 검토. 문자열 검색만으로 완료 금지 |
| 버그 수정 | 재현 자료, 관련 코드; 등록된 사례가 있으면 기억 인덱스에서 해당 ID만 | `project-verify`, `project-review` | 수정 전 재현·관련 회귀 검증 |
| 작업 마무리 | 이번 변경·기존 검증 결과 | `project-verify`, `project-review`, `project-handoff` | 영향에 맞는 검사와 인계 저장 |
| 새 세션에서 이어가기 | 명시적으로 전달받은 `.codex/local/sessions/`의 인계 파일 | `project-handoff` | 현재 Git·코드·실행 환경 재확인 |

UI·API·DB 제품 경로와 검증 명령은 아직 없다. 실제 제품 구조와 명령이 생긴 변경에서 해당 행을 추가한다. 모든 작업에 모든 자료를 읽지 않는다.

> 과거 구성의 검증 기록입니다. 2026-11-03 이후 현재 설정은 [SETUP](../../SETUP.md)을 따릅니다.

# HARNESS-001 독립 실행·감사 결과

확인일: 2026-10-29. 이 이슈는 사용자 지시에 따른 로컬 하네스 검증이며 외부 GitHub 이슈를 만들지 않았다. 제품 개발·커밋·푸시·배포는 하지 않았다.

## 실제 역할 실행

| 단계 | 독립 수행자 | 산출물·결과 |
| --- | --- | --- |
| 초기 워크플로우/권한 감사 | `workflow_audit` | 읽기 분석의 feature 포인터 부수효과 재현, 독립 검증/보안/스택 역할 누락 확인 |
| 요구사항 | `sdd_issue_author` | [spec.md](spec.md), 수정 전 잘못 통과하는 입력 4종 직접 재현 |
| 설계·작업 | `sdd_issue_planner` | [plan.md](plan.md), [tasks.md](tasks.md); 수용 기준과 C01–C19 연결 |
| 구현 | `sdd_issue_implementer` | `check_agents` 개선, 수정 전 19개 subTest 실패 → 수정 후 회귀 통과 |
| 기술 스택 절차 | `stack_role_trial` | 실제 Python/Node/npm/uv 및 Playwright manifest/lock 확인. 제품 스택은 미정으로 유지 |
| 보안 | `security_role_trial` | 하위 동명 스크립트의 훅 실행 재현 → 수정 후 격리 검사 8개 PASS |
| 독립 최종 리뷰 | `sdd_final_reviewer` | 관련 23개 검사와 별도 PreCompact fixture PASS, 검토 범위의 실제 결함 없음 |
| native 검증 역할 | `spec_verifier` | 실제 native 자식 생성·완료, 세션 메타데이터의 `agent_role=spec_verifier` 및 manifest 버전/출처 응답 확인 |
| 인계 | `handoff_audit` → `handoff_reader` | 경계·동시 저장 후 과거 대화가 없는 새 모델이 JSON 하나만으로 목표·미검증·다음 단계 복원 |
| 구조·성능 | `structure_audit` | 초기/최종 snapshot의 중복·문서·지연 독립 측정 |

협업 도구로 실제 독립 모델들이 역할 파일을 읽고 작업했다. 추가로 native `spec_verifier` 스모크는 일반 읽기 전용 세션에서 자식 생성·완료를 확인했고, 실제 자식의 세션 메타데이터 `source.subagent.thread_spawn.agent_role`도 확인했다. 초기 ephemeral 실행은 `no rollout found for thread id`로 실패했다. 일반 세션 재시도에서 `NATIVE-SDD-VERIFY-20261029`, 실제 버전 1.2.5와 고정 Git rev를 반환했다. CLI 종료 코드 0만으로 성공을 판단하지 않았다. 모든 단계 역할을 각각 native selector로 호출한 검증은 아니다.

## 해결한 실제 문제

1. **잘못된 준비 완료 판정:** 역할 4개와 진릿값 검사만 하던 경로를 필수 7개+추가 직속 TOML의 3개 문자열 필드·이름 일치·중복 검사로 보강했다. 정상/누락/빈 값/공백/비문자열/파싱·읽기 실패/진입 스킬 누락을 분리해 검사했다.
2. **읽기 리뷰의 파일 쓰기:** Spec Kit 분석 prerequisite의 `.specify/feature.json` 저장을 `SPECIFY_FEATURE_NO_PERSIST=1`로 끄도록 역할·워크플로우를 보완했다. 포인터 없음/다른 기능 포인터 존재의 무변경 회귀 2개를 남겼다. upstream 관리 파일은 수정하지 않았다.
3. **잘못된 훅 실행 파일:** PWD부터 처음 만나는 동명 파일을 실행하던 경로를 Git 루트 기준으로 바꿨다. 모든 `GIT_*`를 제외한 환경과 `python3 -I`로 루트를 찾고 루트 내부 스크립트만 실행한다. 하위 script shadow·상속 Git 위치·외부 symlink 거부를 독립 재검토했다. 프로젝트 내부 신뢰된 파일이나 Git 메타데이터 자체를 악의적으로 바꾸는 경우까지 막는 보안 경계는 아니다.

## 검증 판정

| 대상 | 결과 | 실제 범위 |
| --- | --- | --- |
| 명세 → 설계 → 작업 → 구현 → 리뷰 | PASS | 로컬 HARNESS-001을 독립 모델에 순차 배정, 실제 Python 코드와 회귀 변경 |
| 하네스 설정·Python·전체 회귀 | PASS | `python3 -B scripts/ai/harness.py verify`: 최종 46 tests OK |
| 실제 Spec Kit doctor | PASS | `python3 scripts/ai/specify.py doctor`: 프로젝트 런타임·7개 역할 검사, status ok·관리 파일 누락/변조 0 |
| native 역할 선택·완료 | PASS (1개 역할) | 정상 세션의 `spec_verifier` 실제 자식·완료·메타데이터 확인. ephemeral 호출 경로는 실패 기록을 유지 |
| 읽기 포인터·훅 보안 수정 | PASS | 실제 Bash/Python 격리 fixture. 실제 native lifecycle 이벤트와는 다름 |
| 새 모델의 인계 복원 | PASS | `fork_turns=none`, 인계 파일 하나만 읽어 `HANDOFF-COLD-7429`와 다음 문서 복원, 1999년 성공을 현재 결과로 재사용하지 않음 |
| 입력·세션·동시 저장 | PASS | 65,536/65,537 bytes 경계, 다른 세션 분리, 별도 프로세스, 동시 저장 32회 |
| 실제 컨텍스트 포화·native 압축 훅 | 보류 | 사용자 요청으로 이번 검증에서 제외. 훅 신뢰를 대신 승인하지 않음 |
| 원격 CI·다른 OS·제품 서버/DB·부하 | 미실행 | 이번 결과로 성공을 주장하지 않음 |

PreCompact는 시간·이벤트 메타데이터와 안내만 저장한다. **포화 시 의미 요약의 자동 생성·복원 보장은 없다.** 의미 요약은 중요한 작업 상태가 생길 때 `project-handoff`로 남긴다. 역할별 권한은 [WORKFLOW](../../WORKFLOW.md)의 작업 지시 경계이며 부모 권한을 상속한다.

## 구조·중복·읽기 비용

독립 최종 측정 snapshot은 공유 파일 88개/644,985B다(이 보고서와 이후 문서 추가 전). 역할 7개·스킬 16개의 이름 중복은 0이었다. 정확히 같은 파일은 공식 헌법 템플릿과 미작성 헌법 인스턴스 1쌍이며 기능상 필요한 원본/인스턴스라 합치지 않았다.

프로젝트 설명·라우팅·감사 산출물은 `docs/ai/`, 실행 코드는 `scripts/ai/`, 도구 manifest/lock은 `tools/ai/`에 둔다. `.agents/skills`, `.codex/agents`, `.specify`는 공식 발견 경로이므로 docs로 옮기지 않았다. 문서 중복 역할 표는 WORKFLOW로 모으고 ROUTING의 실행 자료는 명령 앵커로 좁혔다.

시작 3문서(AGENTS+ROUTING+PROJECT)는 7,369B, 역할 이름/설명은 740B, 스킬 메타데이터는 2,782B였다. 전체 스킬 본문 약 166KB를 매 작업에 읽지 않고 필요한 단계만 읽는다. bytes 측정이며 정확한 토큰 수나 전체 Codex 자동 주입량은 아니다.

## 성능

macOS 동일 컴퓨터의 임시 공유 파일 복사본에서 프로세스 시작·IO를 포함한 wall time을 측정했다. 마지막 실행 소스 SHA가 동일함을 확인했다. 임의 SLA·성능 합격 기준은 도입하지 않았다. 소표본 nearest-rank p95는 통계적 보장값이 아니다.

| 실행 | n | 중앙값 ms | 관측 p95 ms |
| --- | --- | --- | --- |
| 등록된 SessionStart 명령 — 하위 폴더 | 12 | 48.55 | 50.35 |
| 등록된 PreCompact 명령 — 하위 폴더 | 12 | 46.77 | 53.42 |
| 의미 인계 저장 — 별도 프로세스 | 10 | 53.00 | 56.52 |
| 전체 46개 회귀 검사 | 5 | 666.28 | 718.75 |

이 수치는 훅 스크립트·하네스 성능이다. 모델 추론·제품 서버·DB·스케일아웃 부하 성능이 아니다. 원시 측정 JSON과 독립 보고서는 Git 제외 로컬 감사 기록에 보관한다.

배포 범위 변경(2026-11-01): 사용자 요청으로 CI 워크플로우를 이번 업로드에서 제외했다. 위 CI 관련 내용은 과거 구성의 감사 기록이며 현재 CI 구성/실행을 뜻하지 않는다. 로컬 검증 스크립트는 유지하며 CI는 별도 PR로 추가한다.

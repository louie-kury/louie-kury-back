# HARNESS-001 작업 목록

입력: [명세](spec.md), [설계·C01–C19 검증표](plan.md). 상태: 설계 완료, 아래 구현 작업은 미실행. 변경 파일 소유권은 `scripts/ai/specify.py`와 `scripts/ai/test_specify.py`로 제한한다. 역할 정의 파일은 상위 오케스트레이터가 준비한다.

## Phase 1 — 시작 상태

- [X] T001 실제 경로·브랜치·미커밋 변경과 AGENTS.md를 확인하고 `docs/ai/validation/HARNESS-001/spec.md`, `plan.md`, `tasks.md`를 읽는다. 신규 3개 역할 준비 여부를 확인하고 사용자 변경을 보존한다.

## Phase 2 — 테스트 기반

- [X] T002 `scripts/ai/test_specify.py`에 임시 정상 7개 역할·스킬 fixture를 추가한다. 역할 이름은 명세에서 명시적으로 작성하며 구현 상수를 재사용하지 않는다. 각 사례에 새 fixture와 식별 가능한 subTest를 사용한다.

## Phase 3 — US1 역할 정의 준비 상태 (P1)

독립 완료 기준: 정상/추가 정상 역할 통과, 필수 역할·필드·이름·읽기 실패 사례별 거부.

- [X] T003 [US1] `scripts/ai/test_specify.py`에 C01–C13 회귀 검사를 추가한다. 필수 7개 각각 누락, 필드 3개 각각 누락·빈 값·스페이스·탭/줄바꿈, TOML 비문자열의 참/거짓·빈/비빈 값, 이름 불일치·중복·추가 역할 오류·파싱·읽기 오류를 독립 검사한다. description/instructions 앞뒤 공백 내용은 허용하고 name 공백은 거부한다. (SC-001/002, FR-001–004/007)
- [X] T004 [US1] `scripts/ai/test_specify.py`의 회귀를 수정 전 `python3 -B -m unittest discover -s scripts/ai -p test_specify.py -v`로 실행한다. 기존 4개 역할만 있는 구성 및 공백/참인 비문자열 통과 결함이 기대 결과와 충돌하는 실패를 기록한다. 이미 올바른 사례와 새로 재현한 실패를 구별한다.
- [X] T005 [US1] `scripts/ai/specify.py`의 `check_agents`를 설계대로 확장한다. 필수 7개와 바로 아래 추가 TOML 전체에 문자열·strip 비어 있지 않음·원래 name과 stem 정확 일치·이름 유일성을 적용하고 기존 읽기/파싱 예외 계약과 반환 형태를 보존한다. 새 라이브러리나 파일 내용 정책은 도입하지 않는다.
- [X] T006 [US1] `scripts/ai/test_specify.py`의 같은 회귀 명령으로 수정 전 실패가 해결되고 C01–C13 및 기존 검사가 통과하는지 확인한다. 실패하면 원인을 수정하고 관련 검사만 다시 실행한다.

## Phase 4 — US2 진입 스킬과 doctor 실행 보존 (P1)

독립 완료 기준: 스킬 누락/디렉터리 거부, 잘못된 구성에서 하위 실행 없음, 정상 구성에서 기존 호출·반환값 전달.

- [X] T007 [US2] `scripts/ai/test_specify.py`에 C14–C19를 추가한다. 스킬 없음/디렉터리를 분리하고, 실제 `check_agents`를 쓰는 `main(["doctor"])` 검사에서 임시 ROOT·uv 검색·하위 프로세스만 격리한다. 잘못된 역할/스킬 누락은 각각 반환 1과 하위 호출 0회, 정상은 하위 반환 0/7 전달과 저장소 고정 상태 명령 1회·cwd·환경을 확인한다. (SC-002/003, FR-005–007)
- [X] T008 [US2] `scripts/ai/specify.py`의 기존 `is_file()` 및 doctor 제어 흐름을 C14–C19로 확인한다. 기존 코드가 통과하면 불필요하게 수정하지 않는다. 위반이 있으면 해당 함수만 최소 수정하고 `scripts/ai/test_specify.py` 전체 회귀 명령을 실행한다.

## Phase 5 — 통합 검증과 인계

상위 최종 확인: 실제 `python3 scripts/ai/specify.py doctor`가 승인된 로컬 실행에서 status ok로 통과했다. 전체 최종 46개 회귀와 독립 리뷰 결과는 [보고서](report.md)에 연결한다. 아래 구현 역할의 당시 권한 실패 기록과 구분한다.

- [X] T009 `scripts/ai/harness.py`의 기존 `verify`를 `python3 -B scripts/ai/harness.py verify`로 실행한다. 설정·Python 구문·전체 하네스 회귀 결과를 확인하며 파일 자체는 수정하지 않는다. 상위가 작성한 역할 정의가 준비되지 않아 실패한 경우 구현 결함과 구별해 반환한다.
- [X] T010 `scripts/ai/specify.py doctor`를 `python3 -B scripts/ai/specify.py doctor`로 실제 실행하고 종료 코드·고정 런타임 상태를 확인한다. uv 캐시/네트워크/권한 실패 시 그대로 보고하고 전역 환경을 고치지 않는다. mock 검사를 실제 Spec Kit 실행 성공으로 표현하지 않는다.
- [X] T011 `docs/ai/validation/HARNESS-001/spec.md`와 `plan.md`의 SC-001–004/C01–C19를 실행 결과에 대조해 상위에 전달한다. 수정 전 실패→수정 후 기대 결과, 변경 파일, 실제 명령·결과, 실제 doctor 미검증 사유, 원격 CI·제품 환경 범위 밖을 짧게 보고한다. 독립 검증·리뷰·최종 인계 파일은 상위 역할 소유이며 이 작업에서 추가 작성하지 않는다.

## 의존성과 실행 전략

T001 → T002 → T003 → T004 → T005 → T006 → T007 → T008 → T009 → T010 → T011 순서다. US1/US2는 같은 코드와 테스트 파일을 공유하므로 동시 쓰기하지 않는다. 각 story 안에서 여러 임시 사례를 별도 fixture로 독립 실행할 수 있으나 병렬 에이전트 추가는 필요 없다.

첫 구현 단위는 US1의 준비 완료 오판 제거다. 이어 US2로 기존 doctor 경계 보존을 확인하고 전체 하네스 검증과 실제 실행 결과를 구별해 반환한다. 별도 제품 초기화·의존성 설치·성능/커버리지 목표 작업은 없다.

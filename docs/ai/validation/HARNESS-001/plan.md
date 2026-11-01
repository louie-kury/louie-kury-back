# HARNESS-001 구현 설계

상태: 구현 가능. 입력은 [spec.md](spec.md), [issue.md](issue.md)이며 설계 범위는 역할 준비 검사와 관련 회귀 검사다. 브랜치는 `main`, 확인한 실행기는 Python 3.14.6이며 하네스 지원 기준은 기존 Python 3.11 이상이다.

## 범위와 확인 근거

- 변경 대상: `scripts/ai/specify.py`의 `check_agents`, 필요할 때만 `main`의 기존 오류 처리 경계, `scripts/ai/test_specify.py`의 회귀 검사.
- 기존 `check_agents(root)`는 4개 역할만 순회하고 `Path.read_text()` → `tomllib.loads()`로 읽는다. 별도 read 함수는 없다. 이 읽기 루틴과 표준 라이브러리를 재사용한다.
- `main(["doctor"])`는 `check_agents(ROOT)` 성공 후 `integration status --json`을 저장소 고정 uv 명령으로 호출한다. `OSError`, `ValueError`, `SubprocessError`를 잡아 1을 반환하며 하위 프로세스 반환값은 그대로 전달한다.
- 신규 역할 정의 작성은 상위 오케스트레이터의 소유다. 제품 코드·스택·의존성·전역 도구·외부 쓰기·커밋·푸시·배포는 추가하지 않는다.
- 헌법은 미작성 템플릿이다. 예시 TDD 승인·커버리지·성능 숫자를 정책으로 도입하지 않는다. 설계를 막는 미정 사항은 없다.

## 검사 계약과 알고리즘

`check_agents(root)`의 성공은 기존처럼 예외 없이 반환하는 것이다. 실패는 `OSError` 또는 `ValueError` 계열 예외로 알린다. TOML 파싱 오류도 기존 doctor 예외 경계가 처리한다. 구체적 오류 문자열은 공개 계약으로 고정하지 않는다.

1. 필수 이름 집합을 명세 FR-001의 7개로 확장한다. 각 `.codex/agents/<name>.toml`을 실제로 읽도록 하여 누락·디렉터리·읽기 실패를 거부한다. 기존 누락 검사에서 기대하는 `OSError` 계약을 보존한다.
2. `.codex/agents/` 바로 아래 `*.toml`을 검사 대상으로 합친다. 필수 파일과 추가 파일을 중복 파싱하지 않는다. 정렬된 경로 순서로 검사해 재현 가능한 실패를 제공한다. 하위 디렉터리 재귀 탐색은 요구하지 않는다.
3. 각 TOML을 기존 읽기/파싱 루틴으로 읽고 세 필드를 각각 `isinstance(value, str)` 및 `value.strip()`의 비어 있지 않음으로 검증한다. description/instructions의 앞뒤 공백은 허용하고 파일은 수정하지 않는다.
4. `name`은 보정하지 않은 원래 값과 `path.stem`을 정확히 비교하고, 읽은 이름 집합으로 중복을 거부한다. 추가 파일도 같은 규칙을 적용한다. 중복 이름은 파일명 규칙도 위반할 수 있으므로 테스트는 실패 여부로 계약을 검증하며 특정 오류 우선순위를 강요하지 않는다.
5. `.agents/skills/project-sdd/SKILL.md`에 기존 `is_file()` 검사를 유지한다. 본문 의미나 새로운 심볼릭 링크 정책은 추가하지 않는다.
6. doctor 경로는 기존 구조를 우선 보존한다. 구성 실패 시 하위 프로세스 호출이 없어야 하고, 정상일 때 기존 `command()`·환경·cwd 및 반환값 전달을 유지한다. 테스트가 위반을 드러내는 경우에만 `main`을 최소 수정한다.

## 회귀 검사 설계와 추적

`scripts/ai/test_specify.py`에 표준 `unittest`, `tempfile`, `unittest.mock`만 사용한다. 임시 루트마다 명세의 7개 이름을 명시한 최소 정상 TOML과 진입 스킬 파일을 만든다. 구현의 필수 이름 상수를 가져와 fixture를 생성하지 않아 역할 누락 결함을 가리지 않는다. 각 음성 사례는 새 정상 fixture에서 한 조건만 바꾼다. `subTest`로 필드·값·역할별 실패를 식별한다.

| 수용 기준 / 요구사항 | 변경 또는 보존 함수 | 독립 테스트 사례와 기대 결과 |
| --- | --- | --- |
| SC-001, US1-1, FR-001 | `check_agents` | C01 정상 7개와 스킬 성공; C02 정상 추가 역할도 성공 |
| SC-002, US1-2, FR-001/004 | `check_agents` | C03 7개 역할을 각각 하나만 삭제하면 매번 실패; 신규 verifier/security/stack 각각 포함 |
| SC-002, US1-3/4, FR-002/004 | `check_agents` | C04 각 필드 누락; C05 각 필드 `""`, 공백, 탭·줄바꿈; C06 각 필드 숫자·불리언·배열·테이블 모두 실패. 참/거짓·0/비0·빈/비빈 컨테이너를 나누어 진릿값 의존 제거 확인 |
| SC-001/002, US1-5, FR-002/003 | `check_agents` | C07 description/instructions 앞뒤 공백 있는 내용 성공; C08 name 앞뒤 공백 또는 다른 이름 실패 |
| SC-002, US1-5, FR-003/004 | `check_agents` | C09 추가 TOML이 기존 필수 name 복제하면 실패; C10 추가 역할의 필드 오류·파일명 불일치도 각각 실패 |
| SC-002, 경계 사례, FR-004 | `check_agents` 및 읽기 루틴 | C11 잘못된 TOML 실패; C12 역할 경로가 디렉터리이면 실패; C13 읽기 실패를 해당 경로의 `Path.read_text`에 `PermissionError`로 주입하면 실패. C13은 OS 권한/실사용자 권한 검증으로 보고하지 않음 |
| SC-002, US2-1, FR-005 | `check_agents` | C14 스킬 삭제, C15 스킬 경로를 디렉터리로 변경, 각각 실패 |
| SC-003, US2-2, FR-006 | `main` → 실제 `check_agents` | C16 잘못된 역할, C17 스킬 누락 각각에서 mock uv 경로와 임시 ROOT 사용: 반환값 1 및 `subprocess.run` 호출 없음 |
| SC-003, US2-3, FR-006 | `main`, `command` | C18 정상 fixture + mock 하위 반환값 0, C19 반환값 7을 각각 그대로 전달. 한 번의 호출, `integration status --json`, 저장소 고정 바이너리·환경·cwd 확인 |
| SC-004, FR-007 | 검증 보고 | C01–C19 실행 결과를 로컬 직접 함수/doctor 경계 mock 검사로 명시하고 실제 uv·원격 CI·제품 환경·모델 역할 실행은 별도 보고 |

C03–C06 등은 독립적으로 잘못된 준비 완료 판정을 재현하는 핵심 회귀다. 현재 명세에는 4개 역할만 있는 구성·공백 description·숫자 description·불리언 instructions의 수정 전 ACCEPTED 근거가 있다. 구현 담당자는 회귀 테스트를 먼저 추가해 실제 실패를 확인하고 같은 테스트의 수정 후 성공을 남긴다. 이미 거부하는 사례는 수정 전에도 성공하는 회귀 검사로 유지하며 모든 음성 사례가 수정 전 실패한다고 주장하지 않는다.

## 실행과 완료 경계

1. 수정 전 새 회귀 검사: `python3 -B -m unittest discover -s scripts/ai -p test_specify.py -v`. 실패 사례 ID/원인과 기존 재현의 일치를 기록한다.
2. 구현 후 같은 명령으로 C01–C19와 기존 launcher 검사를 실행한다.
3. `python3 -B scripts/ai/harness.py verify`로 설정·Python 구문·기존 전체 하네스 회귀를 실행한다. 코드/환경 변경이 없으면 같은 검사를 보고용으로 반복하지 않는다.
4. 실제 doctor는 `python3 -B scripts/ai/specify.py doctor`다. 네트워크/uv 캐시 권한과 고정 런타임 준비 상태에 의존한다. 이전 실행은 uv 캐시 접근 오류로 종료 2였으므로 mock 성공으로 이 경계를 대체해 완료라 하지 않는다. 재시도 결과가 실패이면 원인과 미검증 범위를 보고하고 전역 캐시/도구를 임의 수정하지 않는다.

이번 설계 단계는 파일·코드·명세를 읽어 계약과 작업을 검토했다. 구현·회귀 테스트·실제 doctor는 이 단계에서 실행하지 않았다. `.specify/extensions.yml`은 없었다. 사용자 지정 경로·두 문서만 쓰는 범위를 지키기 위해 Spec Kit setup-plan/setup-tasks의 feature 포인터 및 별도 research/data-model/contracts/quickstart 생성은 생략하고 필요한 설계 내용을 이 문서에 통합했다.

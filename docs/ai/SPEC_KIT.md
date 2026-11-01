# 공유 하네스의 명세 주도 개발

이 저장소에 에이전트 역할·스킬·Spec Kit 템플릿·실행 스크립트·의존성 lock을 함께 둔다. 사용자 전역의 `specify` 설치에 의존하지 않는다. 버전과 원본은 [UPSTREAM](UPSTREAM.md#spec-kit), 실제 고정값은 `tools/ai/spec-kit/pyproject.toml`과 `uv.lock`을 따른다.

## 다른 팀원이 시작할 때

기본 조건은 이 프로젝트를 읽을 수 있는 Codex와 로그인, Python 3.11 이상, uv, Git이다. 공식 Bash 스크립트까지 사용할 Windows 환경은 Git Bash 또는 WSL이 필요하다. 지원되는 Codex에서 프로젝트를 신뢰해야 `.codex/`의 설정·역할을 로드한다. 개인 인증·훅 신뢰 등록은 각 사용자가 수행한다.

1. 공유 파일을 모두 포함한 저장소를 받는다. 현재 작업은 아직 커밋·푸시하지 않았으므로 이 로컬 폴더만으로 다른 PC에 자동 전달되지는 않는다.
2. 프로젝트 루트에서 아래 준비 명령을 실행한다. Windows에서는 `python3` 대신 설치된 Python 3.11 이상의 `python` 또는 `py`를 사용할 수 있다.

```sh
python3 scripts/ai/specify.py setup
```

이 명령은 `uv.lock`으로 프로젝트의 `tools/ai/spec-kit/.venv/`를 만들고 상태를 검사한다. 실행 바이너리는 이 폴더의 절대 경로로 선택하므로 전역 `specify`로 대체 실행하지 않는다. 가상환경은 Git 제외하며, 스킬·에이전트·템플릿·manifest·lock만 공유한다. 최초 준비에는 패키지 다운로드 네트워크가 필요하다. 기존 사용자 가상환경은 사용하지 않는다.

3. 프로젝트를 연 Codex 채팅에서 작업 범위를 적는다.

```text
$project-sdd 반려동물 상태 기록 기능을 명세와 질문지까지 정리해줘. 구현은 하지 마.
```

새 역할·스킬이 보이지 않으면 새 로컬 대화를 시작한다. 전체 구현까지 요청한 작업은 같은 진입점으로 명세→계획→작업→구현→검토를 진행한다. 명세/설계 전용 범위는 유지한다.

## 하네스에 포함된 역할

역할 7개의 입력·산출물·쓰기/실행 경계는 [WORKFLOW](WORKFLOW.md)에 한 번만 기록한다. `.agents/skills/project-sdd/`는 해당 역할과 공식 `speckit-*` 스킬을 연결한다. 모델과 실제 샌드박스는 부모에서 상속한다.

현재 헌법은 `.specify/memory/constitution.md`의 미작성 공식 템플릿이다. 예시는 팀 정책이 아니다. 원칙 정리가 필요하면 `$speckit-constitution`이 [AGENTS](../../AGENTS.md)와 [PROJECT](../PROJECT.md)의 확정 사항만 사용한다. 제품 명세·기능은 아직 없고, 하네스 자체 이슈의 명세→구현 검증은 `docs/ai/validation/`에 있다.

## 상태 확인·업데이트

```sh
python3 scripts/ai/specify.py doctor
python3 scripts/ai/specify.py version
```

공식 CLI 인자는 같은 wrapper에 전달한다. 공식 스킬이 안내하는 CLI `specify ...`도 `python3 scripts/ai/specify.py ...`로 실행한다. 직접 제공되는 `.specify/scripts/bash/`는 저장소에서 실행한다. 팀원이 다시 `init --force`를 실행할 필요는 없다.

업데이트는 manifest의 출처·버전과 lock을 함께 바꾸고 `doctor`·관련 테스트·생성 파일 차이를 검토한다. 공식 관리 스킬·템플릿은 직접 수정하지 않는다. 추가 네이티브 이벤트는 비활성화 상태로 유지하고 기존 두 훅을 보존한다. 확장·프리셋·Git 자동화·외부 이슈 생성은 도입하지 않았다.

## 검증 범위와 원복

로컬 회귀 검사 외에 전역 specify·가상환경·캐시가 없는 임시 복사본에서 준비/상태/템플릿 조회를 확인한다. CI는 이번 배포에서 제외하며 팀 논의 후 별도 추가한다. 다른 OS의 새 checkout에서도 같은 준비 명령을 실행해 확인해야 한다. 실제 모델 역할 호출·다른 물리 PC·제품 서버/DB/분산 환경의 성공을 설정 검사로 주장하지 않는다.

초기 구성 검증과 이번 독립 에이전트 감사의 실제 결과·성능·미검증 범위는 [HARNESS-001 보고서](validation/HARNESS-001/report.md)에 모은다. 원격 CI 성공과 로컬 실행은 구분한다.

로컬 런타임만 정리하려면 실행 중인 작업을 끝낸 뒤 `tools/ai/spec-kit/.venv/`만 제거한다. 다음 setup이 복원한다. 공유 기능을 원복하려면 프로젝트 역할·project-sdd·wrapper·manifest/lock·관련 CI/라우팅을 검토해 제거한다. 사용자 명세·헌법과 기존 하네스는 보존한다. 이전 턴의 `uv tool` 전역 설치는 남아 있지만 이 하네스는 사용하지 않으며, 원하면 `uv tool uninstall specify-cli`로 별도 정리할 수 있다.

> 2026-11-03: 아래 Spec Kit·에이전트 관련 기록은 과거 사례다. 해당 도구는 제거했으며 현재 실행 지시는 SETUP과 WORKFLOW를 따른다.

# 확인된 실수

## PF-001 — 개인 설치를 공유 하네스 준비 완료로 판단

- 발생 조건·증상: Spec Kit CLI를 `uv tool`로 사용자 환경에만 설치하고 팀원이 사용할 하네스 구성이 끝났다고 설명했다. 다른 PC에는 CLI 실행 환경과 명세 주도 개발 역할을 재현하는 경로가 없었다.
- 확인된 원인: 프로젝트에 스킬 파일이 있는 것과 도구·역할·의존성을 함께 공유하는 것을 구분하지 못했다. 사용자 정정과 당시 SPEC_KIT 문서의 전역 설치 절차로 확인했다.
- 올바른 처리: 사용자 전역 설치 없이 저장소의 역할·스킬·manifest·lock·실행 wrapper로 준비하고, 빈 환경에서 재현성을 확인한다. 기본 런타임과 계정은 별도 조건으로 알린다.
- 근거: [당시 공유 구성](https://github.com/louie-kury/louie-kury-back/blob/3e5d0fccb9cb7f83003ed0a740648b2467a921e7/docs/ai/SPEC_KIT.md), `scripts/ai/specify.py`, `scripts/ai/test_specify.py`, 로컬 `python3 -B scripts/ai/harness.py verify` (CI는 추후 별도 추가).
- 재발 횟수: 1회. 방지 장치: 문서 / 전역 fallback 방지 회귀 테스트 / 새 checkout의 CI 준비 명령.
- 상태·적용 범위: 수정됨. macOS의 빈 임시 복사본에서 전역 CLI·가상환경·캐시 없이 준비·템플릿 조회 확인. 다른 물리 PC·Windows/Linux CI 원격 실행·실제 모델 역할 호출은 별도 검증 대상이다. 마지막 확인: 2026-10-29.

## PF-002 — 읽기 전용 분석 명령의 포인터 저장

- 조건·증상·원인: reviewer가 지정 feature로 Spec Kit prerequisite를 실행하면 `.specify/feature.json`을 자동 저장해 다른 작업의 기본 포인터를 바꾼다.
- 처리·근거: 읽기/분석은 `SPECIFY_FEATURE_NO_PERSIST=1`로 실행. `scripts/ai/test_workflow.py`에서 신규 포인터 미생성과 기존 포인터 bytes 보존을 독립 검증했다. [감사 보고](../validation/HARNESS-001/report.md).
- 재발 1회. 방지 장치: 역할 지시 / 문서 / 회귀 테스트 / CI. 상태: 수정됨. 범위: 프로젝트의 읽기 Spec Kit 절차. 확인: 2026-10-29.

## PF-003 — 하위 동명 스크립트가 훅 실행 파일로 선택됨

- 조건·증상·원인: 작업 폴더에서 위로 첫 `scripts/ai/harness.py`를 찾던 bootstrap이 하위 생성물의 동명 파일을 실행했다. 선택 후 root harness의 입력 검사는 이를 막지 못한다.
- 처리·근거: 격리 Python·정리된 Git 환경으로 Git 루트를 찾고 내부 스크립트만 실행. `test_harness.py`의 동명 shadow·상속 Git 위치 회귀와 보안 역할의 독립 재검사 8개 PASS. [감사 보고](../validation/HARNESS-001/report.md).
- 재발 1회. 방지 장치: bootstrap / 회귀 테스트 / CI. 상태: 수정됨. 범위: 등록 명령의 셸 실행; 실제 native 훅은 사용자 보류. 확인: 2026-10-29.

## PF-004 — 필수 필드의 진릿값을 유효한 문자열로 판단

- 조건·증상·원인: `check_agents`의 단순 truthiness로 공백과 참인 비문자열이 준비 완료로 통과했고 신규 책임 역할 누락도 검사하지 못했다.
- 처리·근거: 문자열 타입·비어 있지 않은 내용·이름/파일 일치·중복과 필수 역할을 검사. [HARNESS-001 명세·재현·수정](../validation/HARNESS-001/issue.md)과 관련 회귀로 검증했다.
- 재발 1회. 방지 장치: 명세 / 구현 검증 / 독립 회귀 / CI. 상태: 수정됨. 범위: 공유 에이전트 doctor. 확인: 2026-10-29.

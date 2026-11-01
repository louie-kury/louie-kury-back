# 필수 휴먼게이트

기능 개발은 다음 순서를 반드시 따른다. 전체 구현 요청, 작은 작업, 기존 승인, 컨텍스트 압축·새 세션도 게이트 생략 사유가 아니다. 오케스트레이터가 역할을 직접 수행해도 동일하다. 읽기 전용 조사·게이트 자체의 설치/점검은 기능 구현으로 확대하지 않는다.

`요청 → 이슈 작성 → G1 사람 승인 → 명세 → 설계·작업 목록 → G2 사람 승인 → 구현·검증·보안·독립 리뷰 → PR 게시 → G3 사람 검토 → 리뷰 수정·재검증·PR 갱신 → G3 재검토 → 사람만 머지`

| 게이트 | 사람이 읽을 대상 | 통과 전 금지 | 통과 후 |
| --- | --- | --- | --- |
| G1 `issue` | 오케스트레이터의 이슈 전문: 문제·목적·포함/제외 범위·수용 기준·미정·위험 | 명세 작성·플래너 배정·제품 구현 | 명세와 계획 작성 |
| G2 `plan` | 기능 명세, 설계, 계약/API/데이터 문서, 작업 목록, 검증 계획 등 플래너의 검토 대상 전체 | 제품 코드·구현 테스트 작성, 구현자 배정 | 승인 범위의 구현·검증·내부 리뷰와 권한 있는 PR 게시 |
| G3 `pr` | 실제 게시된 PR 본문·전체 코드 diff·검증 결과·미검증 위험·팀원 리뷰, 정확한 HEAD | 피드백 없는 자의적 후속 구현, 완료/머지 가능 판정 | 사람이 요청한 리뷰 수정 또는 사람에게 최종 머지 인계 |

## 공통 정지 규칙

- 각 게이트에서 문서 경로/링크와 검토 대상 버전을 제시하고 **현재 작업을 멈춘 뒤 사람의 결정을 기다린다**. 생성과 같은 턴에 승인했다고 추정하지 않는다. 무응답·시간 경과·일반적인 “계속 개발해”·에이전트 리뷰/테스트 통과는 승인으로 취급하지 않는다.
- 승인은 작업 ID와 해당 문서 버전에 한정한다. 이슈 변경은 G1부터, 명세·설계·계약·작업 목록 변경은 G2부터 다시 검토한다. 하위 승인도 무효다. 파일 이름만 같은 과거 승인을 재사용하지 않는다.
- G2 제출 묶음에는 구현에 사용하는 명세·설계·작업 문서 **전부**를 넣는다. 승인 후 범위를 추가하거나 새로운 설계 문서를 끼워 넣으면 다시 제출한다.
- G3에서 사람의 변경 요청을 받으면 요청 근거와 수정 범위를 연결하고 수정 → 관련 검사 → 독립 리뷰 → PR/검증 결과 갱신 → 다시 G3 대기를 반복한다. 단순 코멘트도 실제 변경 요청인지 확인한다. 요구사항·설계를 바꾸는 리뷰는 G1/G2로 돌아간다.
- 새 커밋·PR 본문 변경은 기존 G3 승인을 무효로 한다. 에이전트는 사람을 대신해 Approve, 리뷰 dismiss/resolve, 자기 리뷰를 사람 리뷰로 기록하지 않는다.
- **모든 에이전트는 최종 머지, auto-merge 활성화, merge queue 등록, 보호 브랜치 직접 push, 보호/리뷰 우회가 금지된다.** 승인받아도 머지 실행 권한으로 해석하지 않는다. 사람에게 상태를 인계하고 종료한다.

## 로컬 상태 검사

프로젝트 루트에서 `python3 scripts/ai/human_gate.py`를 사용한다. Python 표준 라이브러리만 필요하다. 상태는 Git 제외된 `.codex/local/gates/<작업 ID>.json`이다. 새 컴퓨터에서는 승인이 없으므로 차단된다. 인증된 팀 공유 승인 원장이 아니며 원본 파일/승인 기록을 임의 복사·수정하지 않는다.

아래 `PET-001`과 경로는 예시이며 실제 작업 ID/생성 경로로 대체한다. 로컬 이슈도 G1이 필요하며 GitHub 이슈를 임의 생성하지 않는다.

```sh
# 에이전트: 이슈를 제출하고 링크/전문을 사람에게 전달한 뒤 중단
python3 scripts/ai/human_gate.py submit PET-001 issue --files docs/issues/PET-001.md
# 사람만: 자기 터미널에서 문서 전문을 읽고 표시된 전체 확인 문자열을 직접 입력
python3 scripts/ai/human_gate.py decide PET-001 issue approved --reviewer 팀원이름
# 에이전트: 명세/계획 단계 시작 전 검사. 비정상 종료면 우회하지 않고 중단
python3 scripts/ai/human_gate.py check PET-001 specify

# 에이전트: 플래너 문서 전체를 제출하고 중단
python3 scripts/ai/human_gate.py submit PET-001 plan --files specs/001-pet/spec.md specs/001-pet/plan.md specs/001-pet/tasks.md
# 사람만: 모든 연결 설계 문서도 확인 (있으면 위 --files에 함께 포함)
python3 scripts/ai/human_gate.py decide PET-001 plan approved --reviewer 팀원이름
# 에이전트: 구현 시작 전 필수 검사
python3 scripts/ai/human_gate.py check PET-001 implement
python3 scripts/ai/human_gate.py check PET-001 pr-open

# PR 게시 후: 실제 PR 본문/검증 기록을 로컬 검토 문서에 동기화해 제출
# PR URL·로컬 HEAD·원격 PR HEAD가 일치하는지 읽기 API로 별도 확인한다.
# 커밋과 push는 별도 사용자 권한이 있을 때만 수행한다.
python3 scripts/ai/human_gate.py submit PET-001 pr --files docs/issues/PET-001-pr.md --url https://github.com/TEAM/REPO/pull/1
# 사람만: PR에서 실제 코드·본문을 검토하고 팀 리뷰 요청을 남긴 다음
python3 scripts/ai/human_gate.py decide PET-001 pr changes_requested --reviewer 팀원이름
# 에이전트: 리뷰 수정 시작 전 검사, 요청 범위만 수정·검증·PR 갱신 후 pr 재제출
python3 scripts/ai/human_gate.py check PET-001 review-fix

# 사람만: 최종 버전에 실제 GitHub Approve 리뷰를 남기고 로컬 결정 기록
python3 scripts/ai/human_gate.py decide PET-001 pr approved --reviewer 팀원이름
# 에이전트: 인계 가능 여부만 확인. 원격 승인/대화 해결/CI도 별도 확인
python3 scripts/ai/human_gate.py check PET-001 handoff-merge
# 언제나 실패. 사람은 GitHub에서 직접 최종 머지한다.
python3 scripts/ai/human_gate.py check PET-001 merge
```

`submit`은 승인하지 않고 항상 대기 상태로 만든다. `check`는 누락·미승인·문서 변경·PR HEAD 변경/dirty checkout에서 실패한다. `decide`는 파이프/비대화형 입력을 거부하지만 **TTY는 사람 신원 증명이 아니다**. 에이전트는 `decide` 실행, PTY/입력 도구로 확인 대행, 상태 파일 편집, 검사 생략이 금지다. 자동 테스트의 모의 승인은 격리 fixture에서만 허용하며 실제 승인이 아니다. 도구가 전체 파일 접근을 가진 에이전트의 우회를 막는 샌드박스라고 주장하지 않는다.

## GitHub에서 반드시 적용할 보호

로컬 지침·검사만으로 “사람만 머지”를 기술적으로 보장할 수 없다. **원격 저장소와 분리된 권한이 설정되기 전에는 서버 강제 상태를 미구성으로 보고한다.**

1. `main` 및 릴리스 브랜치에 PR 필수, 팀원 승인 최소 1명, 새 변경 시 승인 무효화, 마지막 push 작성자 외 승인, 모든 리뷰 대화 해결, 필수 CI 성공, 관리자 포함 우회 금지를 설정한다. `tools/ai/github-branch-protection.json`은 적용용 초안이며 저장만으로 활성화되지 않는다. 그 파일의 `restrictions: null`은 계정 제한이 없는 미완성 값이다. 실제 사람 사용자/팀 허용 목록으로 교체하기 전에는 사람 전용 머지를 구성했다고 판단하지 않는다. CI는 이번 배포에서 제외하므로 초안의 `required_status_checks`는 null로 둔다. 추후 CI를 별도로 추가해 실제 성공을 확인한 뒤 필수 체크로 연결한다.
2. 최종 머지 가능한 팀/사용자는 실제 사람으로 한정하고 에이전트·앱·봇을 보호 브랜치 push/merge 허용 목록과 bypass 목록에서 제외한다. 조직/플랜별 지원 여부를 확인한다. auto-merge와 merge queue 자동 경로를 사용하지 않는다.
3. **사람의 머지 자격증명을 에이전트에 제공하지 않는다.** 같은 사람 계정의 token/로그인 세션을 공유하면 GitHub는 사람과 에이전트의 API 요청을 구별하지 못한다. 필요하면 에이전트는 별도 계정/앱·fork 브랜치에서 PR만 게시하도록 분리한다. 자동화의 `contents: write`와 사람 토큰을 머지 경로에 연결하지 않는다.
4. 미승인 PR 머지 거부, 수정 push 후 재승인 요구, 미해결 리뷰 차단, 에이전트 계정의 merge 거부와 사람 계정의 최종 merge를 테스트 저장소에서 확인하고 결과를 기록한다. 보호 설정 적용이나 PR 생성은 현재 로컬 구성 작업의 검증으로 가장하지 않는다.

GitHub의 [보호 브랜치 공식 문서](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)를 따른다. 문서 승인 G1/G2까지 서버에서 인증·강제하려면 별도 사람 승인 서비스/보호된 승인 원장과 실행 권한 분리가 필요하다. 현재 로컬 검사에는 그 신원 인증 기능이 없다.

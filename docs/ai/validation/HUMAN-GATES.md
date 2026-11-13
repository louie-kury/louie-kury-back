> 과거 구성의 검증 기록입니다. 2026-11-03 이후 현재 설정은 [SETUP](../SETUP.md)을 따릅니다.

# 필수 휴먼게이트 구성 검증

기준일: 2026-11-01 (사용자 시간대 Asia/Seoul).

## 반영

- G1 이슈 전문 승인 전 명세·설계 진입 금지, G2 명세/설계/작업 전체 승인 전 구현 금지, G3 실제 PR 코드/본문/팀 리뷰 후 수정·재검토, 사람만 최종 머지.
- AGENTS, WORKFLOW, ROUTING, project-sdd, 7개 역할, project-handoff, PR 템플릿에 연결. 전체 구현 요청이면 승인 반복을 생략하던 충돌 규칙 제거.
- scripts/ai/human_gate.py: 로컬 제출/사람 터미널 결정/단계 검사. 문서 해시, 필수 계획 문서, PR URL/HEAD/clean checkout, 상위 승인 무효화, 새 버전 재검토, 머지 항상 거부. 실제 작업 승인을 대신 생성하지 않음.
- tools/ai/github-branch-protection.json은 서버 설정 초안. 계정 restrictions는 아직 null이며 사람 계정/팀 목록을 지정해야 함.

## 실행한 검증

- `python3 -B scripts/ai/harness.py verify`: 64 tests PASS (기존 46 + 새 게이트 18). 격리 fixture의 TTY/사람 결정을 모의한 테스트이며 실제 사람 승인이 아님.
- `quick_validate.py`로 project-sdd/project-handoff: 둘 다 valid. 시스템 Python에 PyYAML이 없어 첫 실행은 실패했으며, 기존 프로젝트 Spec Kit 가상환경 Python으로 재실행해 통과. 신규 패키지 설치 없음.
- 변경 문서 링크, 7개 TOML 역할의 게이트 참조, 보호 JSON 필드 검사 PASS.
- 실제 CLI: `check DEMO-001 implement`는 이슈 미제출로 BLOCKED/exit 1, `check DEMO-001 merge`는 사람 전용으로 BLOCKED/exit 1. 실제 게이트 승인은 만들지 않음.

## 강제 범위와 남은 일

이 검사는 호출된 워크플로우의 상태 전이를 차단한다. TTY·로컬 기록은 사람 신원을 인증하지 못하고, 모든 도구 호출을 가로채거나 파일 편집 권한을 분리하지 않는다. 지침 우회가 불가능한 보안 샌드박스라고 주장하지 않는다.

실제 경로는 루이쿠리_프로젝트이며 main에 최초 커밋/HEAD/remote가 없다. 기존 하네스도 미커밋 상태로 보존했다. GitHub PR/Actions/브랜치 보호/머지 계정 분리/서버의 차단 결과는 미실행이다. GitHub 저장소 연결 후 HUMAN_GATES.md의 보호 설정과 별도 에이전트 자격증명을 적용·검증해야 서버 강제를 완료할 수 있다. 사람의 토큰을 에이전트와 공유하면 사람 전용 머지를 보장할 수 없다.

제품 서버/DB/분산 성능과 실제 모델이 모든 게이트에서 멈추는 end-to-end 호출은 검증하지 않았다. 사용자 요청에 따라 실제 컨텍스트 압축 훅 검증은 계속 보류하며 훅 정의는 변경하지 않았다.

배포 범위 변경(2026-11-01): 사용자 요청으로 CI 워크플로우를 이번 업로드에서 제외했다. 위 CI 관련 내용은 과거 구성의 감사 기록이며 현재 CI 구성/실행을 뜻하지 않는다. 로컬 검증 스크립트는 유지하며 CI는 별도 PR로 추가한다.

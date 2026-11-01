---
name: project-sdd
description: 하네스에 포함된 명세·계획·구현·검토 역할을 연결해 spec 주도 개발을 진행한다. 기능 요구사항 정리부터 명세 기반 구현·검토까지 요청된 단계에 사용한다.
---

# 프로젝트 명세 주도 개발

[사용법과 팀 환경 준비](../../../docs/ai/SPEC_KIT.md)를 따른다. 공식 Spec Kit 스킬과 프로젝트 역할 정의는 저장소에 포함되어 있다. 에이전트나 Spec Kit을 사용자 전역에 별도 설치하지 않는다.

0. [필수 휴먼게이트](../../../docs/ai/HUMAN_GATES.md)를 먼저 적용한다. 오케스트레이터는 이슈 작성·제출 후 G1에서 멈춘다. `human_gate.py check <ID> specify` 성공 전 명세/계획에 진입하지 않는다. 플래너의 명세·설계·계약·작업 문서 전체를 제출하고 G2에서 멈춘다. `check <ID> implement` 성공 전 구현자를 배정하거나 구현하지 않는다.
1. AGENTS.md와 ROUTING, 해당 기능의 현재 명세·계획·작업을 확인하고 사용자 요청이 명세/설계/리뷰/구현 중 어디까지인지 판별한다. 기존 문서를 덮어 새로 시작하거나 설치 요청을 제품 구현으로 확대하지 않는다.
2. 새 작업 환경 또는 도구 변경 시 프로젝트 루트에서 `python3 scripts/ai/specify.py doctor`를 실행한다. 최초 환경이면 `setup`으로 저장소 lock에 맞는 로컬 런타임을 준비한다. 전역 `specify`를 호출하지 않는다. 같은 환경의 유효한 확인은 반복하지 않는다.
3. 아래 역할에 필요한 공식 스킬만 읽고 요청된 단계까지 연결한다. 작은 작업은 현재 에이전트가 같은 역할을 수행한다. 역할 분담이 필요하면 지원되는 Codex에서 해당 사용자 정의 역할에 한 단계씩 순차 위임하고 반환 결과를 검토한다. 역할별 쓰기·실행 경계는 docs/ai/WORKFLOW.md를 따른다. 여러 쓰기 에이전트를 같은 파일에 동시에 배정하지 않는다.

| 역할 정의 | 맡는 단계 | 사용할 스킬 |
| --- | --- | --- |
| `spec_author` — `.codex/agents/spec_author.toml` | 확정 원칙·요구사항·수용 기준 | `speckit-constitution`(미정립 시), `speckit-specify`, 필요 시 `speckit-clarify` |
| `spec_planner` — `.codex/agents/spec_planner.toml` | 설계·계약·작업 분해 | `speckit-plan`, `speckit-tasks`, 필요 시 `speckit-analyze` |
| `spec_implementer` — `.codex/agents/spec_implementer.toml` | 사용자 요청 범위의 구현·검증 | `speckit-implement`, 필요 시 `speckit-converge`, `project-verify` |
| `spec_verifier` — `.codex/agents/spec_verifier.toml` | 영향에 맞는 실제 검증 | `project-verify` |
| `security_reviewer` — `.codex/agents/security_reviewer.toml` | 변경된 보안 경계 검토 | `project-security-review` |
| `stack_advisor` — `.codex/agents/stack_advisor.toml` | 실제 버전·스택 절차 확인 | manifest/lock, 불확실한 API만 Context7 |
| `spec_reviewer` — `.codex/agents/spec_reviewer.toml` | 명세·계획·구현의 일치 검토 | `speckit-analyze`, `project-review`, 관련 시 `project-security-review` |

기술 스택·권한·통화 연동·성능 목표가 미정이면 docs/PROJECT.md의 질문에서 관련 항목만 추천과 함께 확인한다. 기능 경로와 필수 명세는 공식 스킬의 실제 생성 결과를 사용한다. 고정 성능·커버리지·프레임워크 정책을 템플릿에서 가져오지 않는다.

리뷰·분석용 Spec Kit 읽기 명령은 SPECIFY_FEATURE_NO_PERSIST=1로 실행해 프로젝트 포인터를 쓰지 않는다. 공식 workflow speckit은 구현에서 끝나므로 검증·보안·리뷰·인계까지 자동 연결된 것으로 간주하지 않는다.

상위 에이전트는 단계 사이에 산출물 경로·수용 기준·결정·미정 사항을 전달하고 명세와 실제 변경의 일치를 유지한다. 전체 구현 요청이어도 G1/G2/G3은 필수다. 승인 없는 다음 단계·작업 재개는 중단한다. 승인 대행/decide 실행/상태 파일 수정은 금지한다. 승인 문서 변경 시 해당 게이트부터 다시 제출한다. PR 게시 후 G3에서 사람 코드·본문·팀 리뷰를 기다린다. 리뷰 수정 전 `check <ID> review-fix`, 수정·검증·PR 갱신 후 G3 재제출을 반복한다. 에이전트는 머지·auto-merge·merge queue·보호 브랜치 직접 push를 수행하지 않고 사람에게 최종 머지를 인계한다. 명세/설계 전용 범위는 유지한다.

마무리에는 관련 검증을 재사용하고 `project-handoff`로 인계한다. 설정 검증, 실제 모델 에이전트 호출, 실제 서버/DB/분산환경 검증을 구분한다. 사용자 정의 역할이 현재 런타임에서 보이지 않으면 역할 정의를 직접 읽고 동일 역할을 수행하되, 실제 부에이전트 실행으로 보고하지 않는다.

# 필요한 자료만 읽기

| 할 일 | 참고할 곳 |
| --- | --- |
| 프로젝트 이해 | [PROJECT](../PROJECT.md), 현재 Git 상태 |
| 함께 계획·선택 이유 기록 | `$vibe-wise`, [명세 틀](templates/spec.md), 해당 기능 문서 |
| 역할 배정·테스트/리뷰/QA·문서 동기화 | [WORKFLOW](WORKFLOW.md), `.codex/agents/`의 해당 역할만 |
| 개발 순서·사람의 결정 | [WORKFLOW](WORKFLOW.md), [대화 확인](HUMAN_GATES.md) |
| 도구 설치·검사 명령 | [SETUP](SETUP.md#commands) |
| 검증·코드 리뷰·보안 검토 | 필요한 경우에만 `project-verify` / `project-review` / `project-security-review` |
| 라이브러리 사용법 | 실제 설치 버전 확인 후 필요할 때 Context7 |
| 브라우저 확인 | 필요할 때 `playwright-cli`, [SETUP](SETUP.md#playwright) |
| 지난 결정·실수 | [기억 인덱스](memory/INDEX.md)에서 관련 항목만 |
| 작업 마무리·다음 세션 | `$project-handoff`, 명시적으로 전달받은 인계 파일 |

메인은 요청 범위에 필요한 단계만 역할에 배정한다. 무조건 전체 파이프라인을 실행하지 않는다. 과거 감사 자료 `validation/`는 당시 결과이며 현재 설정이 아니다. 현재 제품 서버·DB 명령은 미정이다.

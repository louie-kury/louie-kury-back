# Louie Kury

반려동물의 상태 기록을 바탕으로 수의사에게 전화 상담을 요청하는 포트폴리오 프로젝트입니다. [제품 요구사항과 정책](docs/prd.md)을 참고하세요.

개발 방향은 사람이 고릅니다. 메인이 planner·implementer·tester·reviewer를 필요한 단계에 배정합니다. planner는 바이브 와이즈로 설계를 돕고 마지막에 문서를 동기화합니다. 구현·테스트·코드 리뷰·별도 QA를 구분하며, 합의한 범위만 진행합니다. 이슈와 전체 단계를 자동으로 시작하지 않습니다.

- [시작과 도구 사용](docs/ai/SETUP.md)
- [짧은 개발 흐름](docs/ai/WORKFLOW.md)
- [Git 컨벤션과 작성 템플릿](docs/convension/GIT_CONVENTIONS.md)
- [계획·선택 이유를 담는 명세 틀](docs/ai/templates/spec.md)

프로젝트 스킬은 `.agents/skills/`에 포함되어 있습니다. 개인별 별도 플러그인 설치는 필요하지 않습니다. 컨텍스트·세션 인계, Context7, Playwright는 유지합니다. 제품 서버와 DB는 아직 구성하지 않았습니다.

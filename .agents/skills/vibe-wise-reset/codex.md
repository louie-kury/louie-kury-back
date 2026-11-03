# 프로젝트 설치본 초기화

- `reset.py`는 이 파일과 같은 폴더에 있다. 실행할 때 실제 절대 경로를 사용한다.
- 학습 시작 문서는 이 파일 기준 `../vibe-wise/SKILL.md`다.
- `${CLAUDE_PLUGIN_ROOT}/skills/reset/reset.py` 대신 같은 폴더의 `reset.py`, `${CLAUDE_PLUGIN_ROOT}/skills/learn/SKILL.md` 대신 위 학습 문서 경로를 사용한다.
- 질문 도구가 없으면 같은 선택지를 대화로 묻고 명시적 확인을 기다린다. 초기화 대상과 백업 경로를 한 번만 안내한다.
- 다시 학습할 때는 `$vibe-wise`를 사용한다. 다른 프로젝트나 소스 코드는 초기화하지 않는다.

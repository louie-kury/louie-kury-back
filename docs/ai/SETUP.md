# 가볍게 시작하기

이 저장소는 사람이 설계하고 선택하는 개발을 돕는다. 메인과 planner·implementer·tester·reviewer의 [다섯 역할](WORKFLOW.md)을 사용한다. 불필요한 자동 실행과 Spec Kit, 별도 승인 프로그램은 사용하지 않는다. 세션 인계·기억·기존 두 훅, Context7, Playwright는 유지한다.

## 바이브 와이즈

프로젝트에서 다음 대화부터 `$vibe-wise`를 사용할 수 있다. 목록에 없으면 새 세션을 연다. 전역 플러그인 설치는 필요하지 않다.

- planner가 설계를 맡으면 이 스킬의 계획 부분을 적용한다. 질문과 선택지는 메인이 사용자에게 전달한다. 마지막 문서 동기화도 planner가 맡지만 새 설계 결정을 임의로 추가하지 않는다.
- 사용자의 생각을 먼저 듣고, 필요하면 개념과 선택지를 설명한다.
- 합의한 선택과 이유는 [명세 틀](templates/spec.md)에 기록한다. 문서 경로는 작업에 맞게 정한다.
- 설계 확인과 구현 허가를 구분한다. 사용자가 직접 작성할 부분은 대신 구현하지 않는다.
- 개인 학습 메모는 `.vibe-wise/`에 보관한다. 이 폴더와 예전 `.sensible-vibes/`는 Git에서 제외한다. 아직 학습 프로필을 임의 생성하지 않았다.
- `$vibe-wise-reset`은 해당 프로젝트의 학습 메모만 백업 후 초기화한다. 실행 전에 대상과 내용을 보여주고 별도 확인을 받는다.

원본·고정 커밋·설치본의 변경은 [UPSTREAM](UPSTREAM.md)에 기록한다.

<a id="commands"></a>
## 확인된 명령

| 할 일 | 명령 |
| --- | --- |
| 하네스 설정 검사 | `python3 -B scripts/ai/harness.py check-config` |
| 하네스 회귀 검사 | `python3 -B scripts/ai/harness.py verify` |
| 인계 저장 | `python3 -B scripts/ai/harness.py handoff --session <ID>` — stdin 형식은 `project-handoff` 참고 |
| 브라우저 도구 설치 | `npm ci --prefix tools/ai` |
| 브라우저 도움말 | `sh scripts/ai/browser.sh --help` |

Python 3.11 이상이 필요하다. 제품 서버·DB·빌드 명령은 아직 없다. 하네스 검사를 제품 검증으로 표현하지 않는다.

## 세션·컨텍스트

`project-handoff`는 선택·이유·진행 상황·다음 할 일을 `.codex/local/sessions/`에 저장한다. 다음 세션에는 출력된 파일 경로를 전달한다. 개인 메모는 다른 팀원의 컴퓨터로 자동 공유되지 않는다.

`.codex/hooks.json`의 SessionStart는 필요한 문서/같은 세션의 인계 경로만 안내한다. PreCompact는 기계적 체크포인트를 저장하며 의미 요약을 자동 보장하지 않는다. 중요한 결정은 대화가 길어지기 전에 인계한다.

기존 훅 정의는 변경하지 않았다. 사용자가 `/hooks`에서 정확한 정의를 직접 검토·신뢰해야 실행된다. 신뢰를 대신 승인하지 않으며, 실제 압축 훅 검증은 사용자 요청으로 보류 중이다.

## Context7

`.codex/config.toml`에 프로젝트 범위 HTTP MCP 하나를 유지한다. 실제 라이브러리/버전의 사용법이 불확실할 때만 조회한다. 소스·개인정보·비밀값은 보내지 않는다. 학습 대화마다 자동 조회하지 않는다.

## Playwright

사용자 선택으로 브라우저 검사 도구를 유지한다. `tools/ai/package-lock.json`으로 버전을 고정하고 `.playwright/cli.config.json`의 격리된 headless Chrome을 사용한다.

```sh
sh scripts/ai/browser.sh -s=my-check open about:blank
sh scripts/ai/browser.sh -s=my-check eval 'document.URL'
sh scripts/ai/browser.sh -s=my-check close
```

이것은 브라우저 도구 확인이며 제품 화면 검사가 아니다. 실제 화면이 생기면 로컬/테스트 환경에서 사용한다. 기록·인증 파일은 Git 제외된 `.playwright-cli/`에 보관한다. 개인 브라우저나 고객 데이터는 사용하지 않는다.

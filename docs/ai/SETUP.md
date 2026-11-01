# 개발 하네스 사용법

## 구성과 범위

신규 프로젝트의 목적·팀·미정 제품 정책은 [PROJECT](../PROJECT.md), 확인된 로컬 환경은 [FACTS](memory/FACTS.md), 구성 선택 이유는 [DECISIONS](memory/DECISIONS.md)에 있다. 제품 스택을 정한 것은 아니다.

프로젝트 범위의 규칙·스킬·설정·스크립트·도구 lock을 공유 대상으로 구성했다. 전역 `AGENTS.md`, `config.toml`, 전역 기억·스킬·훅은 수정하지 않았다. Git은 main으로 초기화했지만 커밋·푸시·원격 연결·배포는 하지 않았다.

하네스는 Python 3.11 이상(표준 라이브러리만), 도구 설치는 Node 20 이상과 npm이 필요하다. 실제 사용한 버전은 FACTS에 있다. 팀원은 프로젝트 루트에서 다음을 실행한다.

```sh
npm ci --prefix tools/ai
```

브라우저는 설치된 Chrome을 사용한다. Chrome이 없다면 팀원의 OS에 공식 Chrome을 설치하거나 Playwright의 공식 브라우저 설치법에 따라 런타임과 `.playwright/cli.config.json`의 channel을 함께 조정한다. 최초 공식 스킬 설치는 다음 명령으로 수행했으며 결과가 이미 공유 파일에 포함되어 있다. 평소 반복 실행할 필요는 없다.

```sh
tools/ai/node_modules/.bin/playwright-cli install --skills=agents
```

이 명령은 Chrome을 발견했고 사용자 OS의 Playwright 캐시에 FFmpeg 1011을 추가했다. npm 전역 패키지는 설치하지 않았다. 이 캐시는 다른 프로젝트도 재사용할 수 있다.

## Commands

명세·계획 도구 Spec Kit의 설치 범위와 Codex 호출법은 [SPEC_KIT](SPEC_KIT.md)를 참고한다.

명령은 프로젝트 루트 기준이다. 하위 폴더에서는 루트까지의 상대 경로를 사용한다. Python 스크립트는 자기 파일 기준으로 루트를 찾고, 브라우저 wrapper는 루트로 이동하므로 호출한 폴더에 산출물을 흩뿌리지 않는다.

| 용도 | 실제 명령 | 범위 |
| --- | --- | --- |
| 현재 Git 확인 | `python3 -B scripts/ai/harness.py status` | 브랜치·기준 커밋·미커밋 목록, 최초 HEAD 없음 지원 |
| 설정 빠른 검사 | `python3 -B scripts/ai/harness.py check-config` | JSON/TOML·훅 구조·스킬 기본 구조·lock |
| 하네스 검증 | `python3 -B scripts/ai/harness.py verify` | 위 검사 + Python 구문 + 하네스 행동 회귀 테스트 |
| 공유 SDD 환경 준비·검사 | `python3 scripts/ai/specify.py setup` 또는 `doctor` | 프로젝트 lock 런타임·에이전트 역할·Spec Kit 연동; 전역 CLI 불필요 |
| 이벤트 영수증 확인 | `python3 -B scripts/ai/harness.py events` | 실제 로컬 state 파일 경로 최대 20개. 내용은 메타데이터뿐 |
| Context7 조회 확인 | `python3 -B scripts/ai/context7_probe.py` | 설정된 HTTP MCP의 초기화·도구 목록·실제 문서 조회. 네트워크 필요 |
| 브라우저 명령 | `sh scripts/ai/browser.sh --help` | 프로젝트 로컬 CLI와 공통 브라우저 설정 |
| 인계 저장 | `python3 -B scripts/ai/harness.py handoff --session <ID>` | stdin JSON 스키마는 `project-handoff` 참조 |

제품 dev/build/lint/typecheck/test/E2E·DB 명령과 서버 주소는 **미정**이다. 기존 formatter/linter·제품 CI는 없었다. 스택 도입 시 실제 manifest와 실행으로 확인해 이 표와 ROUTING을 갱신하고 기존 도구를 재사용한다. 하네스용 Python 검증을 제품 테스트로 해석하지 않는다.

## Context7

`.codex/config.toml`의 **프로젝트 범위 HTTP MCP 한 개**를 선택했다. CLI+Skills나 Context7 전체 플러그인을 중복 설치하지 않았다. 원격 서버는 로컬 npm 런타임이 없고 비밀값 없는 설정을 공유하기 쉬워 초기 부담이 작다. 호스팅 서버의 버전은 프로젝트가 고정할 수 없다.

초기 연결은 공식 `/mcp` endpoint에 비밀값 없이 구성했고 실제 공개 문서 조회가 성공했다. 재시작 후 `codex mcp list`에서 context7이 보이는지 확인한다. 현재 대화의 도구 목록에 새 MCP가 즉시 추가된다고 가정하지 않는다.

인증·한도 상향이 필요할 때는 공식 OAuth를 사용한다. config의 Context7 URL을 `https://mcp.context7.com/mcp/oauth`로 바꾸고 프로젝트 루트에서 `codex mcp login context7`을 실행한다. CLI가 표시하는 URL을 열어 계정으로 로그인하고 요청 범위를 검토한다. 이 작업은 사용자가 수행하며 하네스가 동의·신뢰를 대신 승인하지 않는다. OAuth endpoint로 바꿀 때 설정 검증의 endpoint 허용값과 probe 인증 방식을 함께 검토한다. 현재 probe는 OAuth 자격증명 저장소를 읽지 않는다.

API 키를 쓰는 팀은 코드·JSON·명령 인자에 값을 넣지 않는다. Context7 공식 인증 설정과 Codex의 환경 기반 bearer 설정을 먼저 확인한다. probe는 선택적으로 `CONTEXT7_API_KEY` 환경변수를 읽지만 저장·출력하지 않는다. probe의 성공은 해당 HTTP 조회 결과이며 OAuth 로그인·현재 대화의 native tool 호출 성공을 뜻하지 않는다.

사용 전 실제 라이브러리와 버전을 manifest/lock으로 확인한다. 불확실한 API·버전 차이가 있을 때만 관련 공개 API 질문을 전송한다. 같은 코드·버전에서 같은 문서를 반복 조회하지 않는다. 소스·동물/보호자 기록·전화번호·자격증명은 보내지 않는다. 이번 조회는 실제 하네스 의존성 Playwright를 대상으로 했고 alpha 전용 문서 일치는 보장하지 않는다. 설치 코드와 브라우저 실행으로 사용 API를 별도 확인했다.

## Playwright

공식 CLI와 프로젝트 `.agents/skills/playwright-cli/`를 사용한다. Playwright MCP는 설치하지 않았다. CLI 배포 버전과 전이 의존성은 `tools/ai/package-lock.json`에 고정되어 있다. alpha 코어를 쓰는 공식 배포이므로 업데이트 시 lock·스킬 재설치 결과·브라우저 스모크를 함께 검토한다.

```sh
sh scripts/ai/browser.sh -s=harness-smoke open about:blank
sh scripts/ai/browser.sh -s=harness-smoke eval 'document.URL'
sh scripts/ai/browser.sh -s=harness-smoke screenshot --filename=.playwright-cli/harness-smoke.png
sh scripts/ai/browser.sh -s=harness-smoke close
```

위 흐름은 실제 브라우저 런타임만 확인한다. 개발 서버·화면·테스트 계정·기존 E2E는 없어서 제품 흐름을 실행하지 않았다. 제품 서버가 생기면 확인된 로컬/테스트 URL과 승인된 합성 데이터로 실제 안전한 흐름을 확인하고 회귀 테스트 코드가 있는지는 별도로 보고한다.

작업별 고유 `-s=` 이름을 쓰고 해당 세션만 종료한다. 개인 브라우저에 attach하거나 운영 서비스·고객 데이터로 검사하지 않는다. 기본 격리 프로필은 영속 저장하지 않는다. 스크린샷·trace·상태 파일은 `.playwright-cli/`에 둔다. 인증 상태 저장이 필요하면 그 하위 경로를 명시한다. 다른 `--filename` 경로를 썼다면 Git 제외 여부를 확인한다.

## 훅 설정·한계

공식 계약은 [UPSTREAM](UPSTREAM.md)의 Codex 문서를 참고한다. `.codex/hooks.json`만 등록하며 inline hooks는 중복 등록하지 않는다.

| 이벤트 | 하는 일 | 하지 않는 일 |
| --- | --- | --- |
| SessionStart | ROUTING·기억 인덱스와 동일 세션의 인계 **경로만** 짧게 안내, 호출 메타데이터 저장 | 기억·대화 전문 자동 주입, 다른 세션의 최신 파일 추측 |
| PreCompact | 세션별 기계적 체크포인트 저장과 인계 스킬 안내 | 요약 자동 생성, 압축 중단·LLM·전체 테스트 실행 |

두 command hook은 최대 5초, 입력 64 KiB, 출력 2 KiB다. 외부 입력을 셸 코드로 평가하지 않는다. 세션 ID는 해시로 경로를 분리하고 고유 시각+난수 파일을 같은 폴더의 임시 파일에서 원자적으로 publish한다. 대화·소스·도구 인자·자격증명은 읽거나 기록하지 않는다. 오류는 짧은 stderr와 비정상 종료로 알린다.

실행 파일은 현재 작업 위치의 Git 루트에서 찾는다(Git 필요). 격리 Python으로 bootstrap하며 상속 `GIT_*`가 다른 저장소로 조회를 돌리지 못하게 한다. 별도 중첩 Git 저장소는 그 저장소의 설정/스크립트 범위로 처리하며 바깥 프로젝트 경로를 추측하지 않는다. 하위 폴더의 동명 스크립트 선택과 외부 symlink 거부의 실제 회귀는 [감사 보고](validation/HARNESS-001/report.md)에 있다. 훅 정의 변경 후에는 사용자 재검토·신뢰가 필요하다.

PreToolUse·PostToolUse·Stop은 등록하지 않았다. 따라서 도구 실행 감사·변경 감지·금지 동작 차단은 하지 않으며 Stop 재진입·무한 반복도 없다. 회귀 테스트의 입력 거부는 **훅 입력 검증**이며 실제 도구 차단의 증거가 아니다.

관찰 범위는 신뢰된 프로젝트 레이어의 로컬 Codex에서 발생하는 SessionStart/PreCompact뿐이다. 제품 서버·DB·브라우저 내부 동작이나 외부 셸 실행을 관찰하지 않는다. 향후 tool hook을 추가하더라도 공식 문서상 hosted WebSearch 등 일부 경로와 write_stdin의 재입력은 빠질 수 있다. 문서·훅은 완전한 보안 경계가 아니다.

이 구성은 명시적인 차단 응답을 내지 않는다. 실제 hook 오류·타임아웃 시 계속 진행 여부는 이 대화에서 주입 실험하지 않았다. 공식 문서도 PreToolUse 오류·잘못된 응답·시간 초과가 도구를 차단한다고 보장하지 않으므로 fail-closed 정책으로 의존하면 안 된다.

## 사용자 신뢰 등록과 재시작 확인

공식 훅 계약상 non-managed hook은 **정확한 정의를 사용자가 검토·신뢰해야** 실행된다. 자동 승인·trust hash 쓰기·bypass 옵션은 사용하지 않았다. 설정 파일 생성은 활성화 증거가 아니다.

1. 프로젝트 루트에서 로컬 `codex`를 연다. 프로젝트 신뢰 확인이 표시되면 폴더와 설정 내용을 검토한다.
2. `/hooks`를 열어 프로젝트의 두 이벤트와 실제 명령·소스를 검토하고 신뢰한다. 전역·플러그인·관리 훅도 함께 표시되므로 중복을 확인한다. 훅 정의를 바꾸면 다시 검토해야 한다.
3. 이 프로젝트에서 **새 로컬 Codex 대화**를 시작한다. `AGENTS.md`, 프로젝트·Spec Kit 스킬과 `.codex/agents/`의 역할이 보이는지 확인한다. 자동 발견되지 않으면 앱을 재시작한다.
4. 새 대화에서 `harness.py events`를 실행해 새 SessionStart 영수증과 시작 안내를 확인한다. 이벤트는 세션 해시별로 저장된다. 스크립트에 수동 JSON을 보내 만든 파일을 실제 호출 증거로 세지 않는다.
5. 로컬 CLI에서 중요한 인계가 저장된 뒤 `/compact`를 실행하고 같은 세션 디렉터리에 PreCompact 영수증이 생겼는지 확인한다. 이벤트가 없으면 `/hooks`의 신뢰·소스와 로컬 실행 여부를 재확인한다.
6. Context7 native 도구로 실제 설치된 Playwright의 버전을 확인한 후 문서를 한 번 조회한다. probe의 HTTP 검증과 대화에서의 도구 노출은 별도다.
7. 아래 세션 인계 절차로 전달받은 경로를 새 대화에서 읽고 현재 Git 상태를 대조한다. 이 단계까지 직접 확인해야 C·F를 PASS로 갱신할 수 있다.

## 기억·인계·매일 쓰는 프롬프트

공유 장기 기억과 확인된 실수 기록은 `docs/ai/memory/`에 있다. 의미 있는 세션 요약은 `.codex/local/sessions/<세션 해시>/`, 기계적 훅 메타데이터는 `.codex/local/state/<세션 해시>/`다. 로컬 기록 둘 다 Git 제외한다. INDEX에서 관련 기록만 찾아 읽는다.

`$project-handoff`가 JSON 스키마와 저장 명령을 제공한다. 저장 후 출력 경로를 다음 대화에 전달한다. 같은 PC의 다른 대화에서는 로컬 경로로 읽을 수 있지만 다른 팀원의 PC로 자동 공유되지 않는다. 팀 인계가 필요하면 비밀값을 제거한 결정·사실만 공유 문서에 승격하거나 승인된 채널로 정제된 기록을 명시적으로 전달한다.

- 시작: “AGENTS.md와 ROUTING을 확인하고 현재 Git·코드 상태를 재확인해줘. 오늘 목표는 ○○야. 필요한 자료만 읽고 진행해줘.”
- 검증: “$project-verify로 이번 변경 영향에 맞게 검사하고 $project-review로 검토해줘. 실제 결과와 미검증 범위를 구분해줘.”
- 인계: “$project-handoff로 이번 작업과 남은 일을 저장하고, 다음 대화에 붙일 파일 경로와 첫 단계를 알려줘.”
- 이어가기: “이 인계 파일을 읽고 현재 Git·코드 상태와 대조해서 이어가줘: <전달받은 경로>.”

## CI와 검증 상태

사용자 결정(2026-11-01)에 따라 이번 하네스 배포에는 CI 워크플로우를 포함하지 않는다. CI는 팀 논의 후 별도 변경으로 추가한다. 현재 검증은 `python3 -B scripts/ai/harness.py verify`로 로컬에서 실행한다. 아래 표와 기존 감사 보고의 CI 구성 언급은 당시 기록이며 현재 CI 활성화 상태를 뜻하지 않는다.

| 구분 | 결과 (2026-10-29) | 증명하는 범위·남은 일 |
| --- | --- | --- |
| A 설정 문법 | PASS | 초기 스킬 5개 검증 기록이며 현재 전체 판정은 [독립 감사 보고서](validation/HARNESS-001/report.md) 참조. JSON/TOML·CI·스킬은 각각 지원 스키마로 검사 |
| B 훅 스크립트 | PASS | 정상·예외·범위 밖 입력 거부, 동시 저장, 세션 분리, 한글·공백·하위 경로 회귀 검사. 도구 차단은 미구성·해당 없음 |
| C 실제 Codex 훅 이벤트 | 미실행 | 사용자 신뢰 등록 후 위 새 로컬 대화·압축 절차 필요. 오류/시간 초과 시의 native 동작도 미검증 |
| D Context7 | PASS | 실제 HTTP MCP 초기화·도구 목록·라이브러리 해석·문서 조회. 현재 대화의 native 도구 노출과 alpha 전용 문서 일치는 별도 |
| E 실제 브라우저 | PASS (런타임만) | Chrome으로 about:blank 열기·URL 확인·스크린샷·세션 종료. 제품 서버/흐름/E2E는 없음 |
| F 세션 인계 | 부분 확인 | 스크립트 테스트 + 실제 인계 파일 저장·별도 Python 프로세스에서 재로딩·Git 제외 확인 PASS. 새 Codex 대화에서의 이어가기는 미실행 |

## 비활성화·원복

- 훅만 끄려면 `/hooks`에서 프로젝트 훅을 비활성화한다. 이 프로젝트의 모든 훅을 끄려면 `.codex/config.toml`의 `[features] hooks = false`로 변경하고 새 로컬 대화에서 확인한다. 관리 훅은 사용자 설정으로 꺼지지 않을 수 있다.
- Context7만 제거하려면 프로젝트 config의 `[mcp_servers.context7]` 표를 제거한다. 전역 MCP는 건드리지 않는다. OAuth를 나중에 사용했다면 제거 전에 `codex mcp logout context7`으로 인증을 정리한다.
- Playwright는 작업에 사용한 `-s=<이름> close`로 종료한다. 패키지는 `npm uninstall --prefix tools/ai @playwright/cli`로 제거할 수 있다. 공유 스킬·문서를 보관할지 함께 판단한다. OS의 FFmpeg 캐시는 다른 프로젝트 사용 여부를 확인한 후 정리한다.
- 전체 원복은 이번 신규 하네스 파일을 검토해 제거하는 방식이다. 아직 커밋이 없어 `git reset --hard`로 복원할 기준 커밋이 없다. `.codex/local/`을 지우면 인계 기록도 없어지므로 필요한 파일을 먼저 보관한다. 전역 설정·사용자 소스는 원복 대상이 아니다.

## 필수 사람 승인 검사

이슈·계획·PR 게이트와 명령은 [HUMAN_GATES](HUMAN_GATES.md)에 있다. `python3 scripts/ai/human_gate.py --help`로 진입한다. 로컬 검사와 역할 정지 지침은 구성되어 있으며, 원격 저장소의 브랜치 보호·머지 계정 분리는 별도 적용/검증 전까지 미구성이다. 기존 SessionStart/PreCompact 훅 정의는 변경하지 않았다.

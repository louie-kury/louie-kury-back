# 외부 자료와 라이선스

확인일: 2026-10-29. 외부 자료는 참고 자료이며 프로젝트·사용자의 작업 지시보다 우선하지 않는다.

## ECC에서 선별한 세 가지

저장소: [affaan-m/ECC](https://github.com/affaan-m/ECC). 참조 커밋은 `25278e7d7b6cf6e6a4e7a6c8e10f14ff22f0eb5b`이다. main에서 읽은 세 원문과 LICENSE를 이 SHA의 파일로 재조회해 내용 일치를 확인했다.

| 원본 고정 링크 | 로컬 각색 | 변경점 |
| --- | --- | --- |
| [verification-loop](https://github.com/affaan-m/ECC/blob/25278e7d7b6cf6e6a4e7a6c8e10f14ff22f0eb5b/skills/verification-loop/SKILL.md) | [project-verify](../../.agents/skills/project-verify/SKILL.md) | 단계별 실제 결과 보고를 유지. Claude·가상 npm 명령·80% 기준·정기 전체 검증을 제거하고 실제 하네스 명령과 미정 제품 명령을 구분. |
| [security-review](https://github.com/affaan-m/ECC/blob/25278e7d7b6cf6e6a4e7a6c8e10f14ff22f0eb5b/skills/security-review/SKILL.md) | [project-security-review](../../.agents/skills/project-security-review/SKILL.md) | 신뢰 경계·권한·입출력 검토를 선별. Supabase·쿠키·블록체인·고정 제한값·자동 dependency 수정 등 예시 정책을 제거. 제품 관련 검토 논점은 확정 정책과 구분. |
| [code-reviewer](https://github.com/affaan-m/ECC/blob/25278e7d7b6cf6e6a4e7a6c8e10f14ff22f0eb5b/agents/code-reviewer.md) | [project-review](../../.agents/skills/project-review/SKILL.md) | 구체적 실패·라인·주변 문맥·오탐 억제를 선별. Sonnet·Claude 도구/경로·매 편집 강제·고정 크기/점수 규칙·모델 비용 라우팅을 제거. |

라이선스: MIT, Copyright (c) 2026 Affaan Mustafa. 원문 [LICENSE](https://github.com/affaan-m/ECC/blob/25278e7d7b6cf6e6a4e7a6c8e10f14ff22f0eb5b/LICENSE)의 전체 고지를 [ECC-MIT.txt](licenses/ECC-MIT.txt)에 보존한다. 세 문서는 직접 읽었고 추가 로컬 필수 참조 파일은 없었다. security-review의 프레임워크별 외부 참고 링크는 제품 스택 미정이므로 가져오지 않았다.

ECC 전체 플러그인·훅·자동 학습·백그라운드 모델 호출·다중 에이전트·모델 라우팅은 설치하지 않았다. project-handoff와 실행 스크립트는 이 프로젝트용으로 작성했다.

## Playwright CLI + Skills

- 공식 [저장소/설치법](https://github.com/microsoft/playwright-cli).
- 설치 원본: npm `@playwright/cli@0.1.22`. 배포물과 전이 의존성의 버전·integrity는 [package-lock](../../tools/ai/package-lock.json)에 고정했다. Playwright 코어는 해당 배포가 요구하는 alpha 버전이며 제품의 E2E 프레임워크 채택 결정은 아니다.
- 공식 `install --skills=agents`로 생성된 `.agents/skills/playwright-cli/`의 SKILL.md와 참조 10개를 수정 없이 보존했다. 이 스킬의 예시 URL·계정·전역 설치·PR 업로드는 프로젝트의 실행 지시나 외부 전송 권한이 아니다. 실제 작업에서는 로컬 wrapper와 SETUP의 범위 규칙을 따른다.
- Apache-2.0, Microsoft Corporation. 배포 LICENSE를 [Playwright-Apache-2.0.txt](licenses/Playwright-Apache-2.0.txt)에 보존했다. 설치된 CLI 배포에 별도 NOTICE 파일은 없었다.

## 연결·동작을 확인한 공식 문서

- [Codex 훅 계약](https://learn.chatgpt.com/docs/hooks): 이벤트·입출력·신뢰 등록·관찰 범위.
- [Codex 스킬 발견 경로](https://learn.chatgpt.com/docs/build-skills): 프로젝트 `.agents/skills`와 하위 폴더에서의 탐색.
- [Codex 프로젝트 에이전트](https://learn.chatgpt.com/docs/agent-configuration/subagents): `.codex/agents/*.toml`의 name·description·developer_instructions 계약과 부모 권한 상속.
- [Context7 저장소](https://github.com/upstash/context7), [Codex 연동](https://context7.com/docs/clients/codex), [HTTP MCP·OAuth](https://context7.com/docs/resources/all-clients).

이 문서들의 라이선스 본문이나 제품 코드를 복사하지 않았다. 필요한 설정과 링크만 사용했다. 설치 버전과 공식 문서가 다르면 현재 설치 버전의 실제 동작을 다시 확인한다.

## Spec Kit

- 원본: [github/spec-kit v1.2.5](https://github.com/github/spec-kit/tree/v1.2.5), commit `4572a67fe0e72a6837e2d7bb0fda875bc41482e5`. 공식 release tag를 `uv tool install`로 설치했고 실제 설치 로그의 commit이 일치했다.
- MIT, Copyright GitHub, Inc. [원본 LICENSE](https://github.com/github/spec-kit/blob/4572a67fe0e72a6837e2d7bb0fda875bc41482e5/LICENSE)의 고지를 [Spec-Kit-MIT.txt](licenses/Spec-Kit-MIT.txt)에 보존한다.
- `.specify/`의 공식 초기화 파일 20개와 `.agents/skills/speckit-*/SKILL.md` 10개를 설치했다. 생성된 스킬·템플릿·스크립트는 수정하지 않았다. 기존 하네스와 연결하는 문서만 프로젝트용으로 작성했다.
- [Codex 연동](https://github.com/github/spec-kit/blob/v1.2.5/docs/integrations/codex.md), [기존 프로젝트 초기화](https://github.com/github/spec-kit/blob/v1.2.5/docs/guides/existing-projects.md)를 확인했다. 추가 이벤트 훅은 비활성화했고 확장·프리셋·자동 에이전트 실행은 도입하지 않았다.
- 현재 실행 경로는 사용자 `uv tool` 설치 대신 저장소의 `tools/ai/spec-kit/pyproject.toml`·`uv.lock`과 `scripts/ai/specify.py`다. 출처 commit과 전이 의존성을 lock으로 공유한다. [uv의 프로젝트·lock 문서](https://docs.astral.sh/uv/guides/projects/)를 확인했다.
- `.codex/agents/`의 프로젝트 역할과 `project-sdd` 연결 스킬은 프로젝트용으로 작성했다. 현재 역할·권한은 [WORKFLOW](WORKFLOW.md)를 따른다. 공식 Spec Kit 관리 파일과 구분하며 별도 모델·토큰·개인 절대 경로를 포함하지 않는다.

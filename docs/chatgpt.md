# ChatGPT에서 쓰기

Claude Code용 output-style 원문은 `plugins/fluent-korean/output-styles/`에 그대로 두고, ChatGPT에 업로드하는 Skill은 `chatgpt/skills/`에 생성합니다. 이 경로는 저장소 안에서 ChatGPT용 배포물을 관리하기 위한 경로이며, ChatGPT가 로컬 저장소에서 자동으로 탐색하는 예약 경로가 아닙니다.

| skill | 동작 |
| --- | --- |
| `fluent-korean` | 일반적인 한국어 응답과 한국어 결과물에 사용합니다. ChatGPT가 설명에 맞춰 필요할 때 사용할 수 있습니다. |
| `fluent-korean-not-coding` | 코딩 지침이 없는 변형입니다. 사용자가 직접 선택하거나 명시적으로 요청했을 때 사용하는 용도이며, 암묵 호출을 끕니다. |

## 원문에서 다시 생성하기

upstream의 output-style을 가져온 뒤에는 저장소 루트에서 다음을 실행합니다.

```bash
python3 scripts/sync_skills.py
```

이 명령은 기존 `.agents/skills/`와 ChatGPT용 `chatgpt/skills/`를 모두 갱신합니다. 두 대상 모두 output-style의 본문을 요약하거나 고치지 않고 그대로 사용하며, 대상별 frontmatter와 메타데이터만 다르게 만듭니다.

ChatGPT용 `SKILL.md`의 frontmatter에는 `name`과 `description`만 둡니다. UI 메타데이터는 각 skill의 `agents/openai.yaml`에 둡니다.

## GitHub Release에서 받기

기본 배포 경로는 GitHub Release입니다. `.github/workflows/chatgpt-skill-release.yml`은 `main` 브랜치에 변경이 반영될 때 자동으로 `chatgpt-latest` rolling Release를 만들고, `scripts/package_chatgpt_skills.py`를 실행해 다음 두 파일을 첨부합니다. 사용자가 별도의 버전 Release를 발행하면 `release.published` 이벤트에서도 실행되어 그 Release의 태그를 checkout한 뒤 같은 ZIP을 첨부합니다.

```text
fluent-korean-chatgpt.zip
fluent-korean-not-coding-chatgpt.zip
```

최신 Release의 고정 다운로드 주소는 다음과 같습니다.

- [fluent-korean-chatgpt.zip](https://github.com/novelKR/fluent-korean/releases/latest/download/fluent-korean-chatgpt.zip)
- [fluent-korean-not-coding-chatgpt.zip](https://github.com/novelKR/fluent-korean/releases/latest/download/fluent-korean-not-coding-chatgpt.zip)

`chatgpt-latest`는 `main`의 최신 상태를 가리키는 rolling Release입니다. `main`이 갱신될 때 기존 rolling Release와 태그를 정리한 뒤 현재 커밋으로 다시 만들기 때문에 첫 Release가 없어도 자동으로 배포가 시작됩니다. 별도 Release를 draft로 만든 경우에는 publish할 때 워크플로가 실행됩니다. Release asset은 같은 이름이 이미 있으면 새 패키지로 교체합니다.

## 로컬에서 업로드용 ZIP 만들기

Release를 사용하지 않고 직접 만들려면 다음을 실행합니다.

```bash
python3 scripts/package_chatgpt_skills.py
```

스크립트는 먼저 `sync_skills.py`를 실행하고 ChatGPT용 구조를 점검한 뒤, 두 변형을 각각 패키징합니다.

```text
dist/chatgpt/fluent-korean/skill.zip
dist/chatgpt/fluent-korean-not-coding/skill.zip
```

각 ZIP에는 한 개의 최상위 skill 디렉터리가 들어갑니다. 생성물인 `dist/`는 Git에 커밋하지 않습니다. GitHub Release 워크플로는 이 두 파일을 각각 고유한 Release asset 이름으로 복사한 뒤 업로드합니다.

## ChatGPT에 설치하기

ChatGPT에서 Skills 기능을 사용할 수 있는 경우, 사이드바에서 **Plugins → Skills → Create → Upload from your computer**로 이동한 뒤 원하는 `skill.zip`을 업로드합니다. 설치된 Skill은 관련 작업에서 자동으로 사용될 수 있으며, 사용자가 직접 선택해서 사용할 수도 있습니다.

현재 ChatGPT의 Skills 설치와 공유 방식은 [OpenAI의 Skills in ChatGPT 문서](https://help.openai.com/en/articles/20001066-skills-in-chatgpt)를 기준으로 확인합니다. 제품별로 Skill의 설치와 동기화 방식이 다를 수 있으므로, `.agents/skills/`의 로컬 설치 절차를 ChatGPT에 그대로 적용하지 않습니다.

## 유지보수 원칙

1. 한국어 지침의 정본은 `plugins/fluent-korean/output-styles/`에 둡니다.
2. 지침 본문은 `.agents/skills/`나 `chatgpt/skills/`에서 따로 수정하지 않습니다.
3. upstream 변경을 반영한 뒤 `python3 scripts/sync_skills.py`를 실행합니다.
4. ChatGPT 업로드 파일이 필요하면 `python3 scripts/package_chatgpt_skills.py`를 실행합니다.

# 여러 에이전트에서 쓰기

Claude Code의 output-style 원문은 `plugins/fluent-korean/output-styles/`에 그대로 있습니다. Cursor, Codex, Muse Code, grok-build, Gemini CLI, Pi, Kimi Code CLI가 함께 읽는 공용 형식은 [Agent Skills](https://agentskills.io/specification)의 `SKILL.md`이고, 이 저장소에서는 `.agents/skills/`에 둡니다.

| skill | 언제 쓰나 |
| --- | --- |
| `fluent-korean` | 코딩 작업 중 한국어로 답하거나 한국어 결과물을 쓸 때. 설명에 맞춰 자동으로 열립니다. |
| `fluent-korean-not-coding` | `/fluent-korean-not-coding`으로 직접 켰을 때. 코드를 직접 고치지 않는 글쓰기용이며, 자동으로 열리지 않습니다. |

본문은 output-style에서 frontmatter만 뺀 원문입니다. 지침 문장을 이 문서나 skill 쪽에서 요약해 두지 않습니다. upstream을 가져온 뒤에는 아래 명령으로 skill을 다시 만듭니다.

```bash
python3 scripts/sync_skills.py
```

## 사용자 전역 연결

이 포크를 클론한 뒤, 도구에 맞는 선택지로 설치합니다. 클론 주소는 `https://github.com/novelKR/fluent-korean.git`입니다. 선택지 목록은 `scripts/install-user.sh --list`가 출력합니다.

```bash
scripts/install-user.sh --harness agents
scripts/install-user.sh --harness cursor-cloud
scripts/install-user.sh --harness kimi-config
scripts/install-user.sh --harness claude
scripts/install-user.sh --harness agents,cursor-cloud
```

- `agents`는 `~/.agents/skills/`에 연결합니다. Cursor의 로컬 세션, Codex, Muse Code, grok-build, Gemini CLI, Pi가 이 경로를 읽습니다. Kimi Code CLI는 `~/.config/agents/skills/`가 없을 때만 이 경로를 읽습니다.
- `cursor-cloud`는 `~/.cursor/skills/`에 연결합니다. Cursor Cloud Agent와 원격 워커가 동기화하는 경로입니다.
- `kimi-config`는 `~/.config/agents/skills/`에 연결합니다. 이 디렉터리가 있으면 Kimi는 `~/.agents/skills/`를 읽지 않습니다.
- `claude`는 skill 파일을 연결하지 않습니다. 원본 저장소 문장을 출력하고, 이 포크를 가리키던 `~/.claude/output-styles/` 심볼릭 링크만 제거합니다.

파일을 연결하는 선택지는 `fluent-korean`과 `fluent-korean-not-coding`을 심볼릭 링크로 둡니다. 이미 심볼릭 링크가 있으면 이 클론을 가리키도록 바꿉니다. 일반 파일이나 디렉터리가 있으면 덮어쓰지 않고 중단합니다. 터미널에서 인자를 생략하면 메뉴가 나오고, 터미널이 아니면 `--harness`가 필요합니다.

원본 README와 같이, LLM에게 아래 문장을 건네도 이 절차를 안내받을 수 있습니다.

```
https://github.com/novelKR/fluent-korean/ 링크 README 읽고, Claude Code 외 설치 방법 단락 읽고 어떻게 설치해서 사용할지 설명해줘
```

## Claude Code

Claude Code의 설치 원본은 이 포크가 아니라 [snflkd/fluent-korean](https://github.com/snflkd/fluent-korean)입니다. 이 포크의 파일로 output-style이나 skill을 설치하지 않습니다. LLM에게 아래 문장을 건넵니다.

```
https://github.com/snflkd/fluent-korean/ 링크 README 읽고, 설치 안내 단락 읽고 어떻게 설치해서 사용할지 설명해줘
```

## 프로젝트 안에서만 쓰기

전역 링크 없이, 이 저장소를 연 세션에서만 쓰려면 `.agents/skills/`가 이미 그 역할입니다. Cursor의 로컬 세션, Codex, Muse Code, grok-build, Gemini CLI, Pi는 저장소 루트의 `.agents/skills/`를 발견합니다.

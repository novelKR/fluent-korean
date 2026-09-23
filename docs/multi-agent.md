# 여러 에이전트에서 쓰기

Claude Code의 output-style 원문은 `plugins/fluent-korean/output-styles/`에 그대로 있습니다. Cursor, Codex, Muse Code, grok-build가 함께 읽는 공용 형식은 [Agent Skills](https://agentskills.io/specification)의 `SKILL.md`이고, 이 저장소에서는 `.agents/skills/`에 둡니다.

| skill | 언제 쓰나 |
| --- | --- |
| `fluent-korean` | 코딩 작업 중 한국어로 답하거나 한국어 결과물을 쓸 때. 설명에 맞춰 자동으로 열립니다. |
| `fluent-korean-not-coding` | `/fluent-korean-not-coding`으로 직접 켰을 때. 코드를 직접 고치지 않는 글쓰기용이며, 자동으로 열리지 않습니다. |

본문은 output-style에서 frontmatter만 뺀 원문입니다. 지침 문장을 이 문서나 skill 쪽에서 요약해 두지 않습니다. upstream을 가져온 뒤에는 아래 명령으로 skill을 다시 만듭니다.

```bash
python3 scripts/sync_skills.py
```

## 사용자 전역 연결

이 클론을 모든 프로젝트에서 쓰려면 저장소 루트에서 다음을 실행합니다.

```bash
scripts/install-user.sh
```

스크립트는 다음 심볼릭 링크만 만듭니다.

- `~/.agents/skills/fluent-korean`
- `~/.agents/skills/fluent-korean-not-coding`
- `~/.claude/output-styles/fluent-korean.md`
- `~/.claude/output-styles/fluent-korean-not-coding.md`

Cursor, Codex, Muse Code, grok-build는 `~/.agents/skills/`를 읽습니다. 그래서 `~/.cursor/skills/`, `~/.codex/skills/`, `~/.grok/skills/`에는 따로 넣지 않습니다. 링크가 생긴 뒤 새 세션을 열면 `fluent-korean`이 한국어 응답에 적용됩니다.

이미 같은 경로에 심볼릭 링크가 있으면 이 클론을 가리키도록 바꿉니다. 일반 파일이나 디렉터리가 있으면 덮어쓰지 않고 중단합니다.

## Claude Code

Claude Code는 `.agents/skills/`를 읽지 않습니다. 항상 적용되는 경로는 output-style입니다.

1. 플러그인을 쓰려면 Claude Code에서 아래를 실행합니다. 마켓플레이스 이름은 이 포크가 아니라 원저장소 기준입니다. 포크의 output-style 파일을 직접 쓰려면 2번을 사용합니다.

   ```
   /plugin marketplace add snflkd/fluent-korean
   /plugin install fluent-korean@fluent-korean
   ```

2. `scripts/install-user.sh`를 실행했다면 `~/.claude/output-styles/`에 두 파일이 연결되어 있습니다. `/config`에서 output-style을 `fluent-korean`으로 고릅니다. 코딩 지침을 빼려면 `fluent-korean-not-coding`을 고릅니다.
3. output-style은 고른 뒤에 새 세션을 시작하거나 `/clear`를 해야 적용됩니다.

Claude Code에서 output-style을 켠 상태에서는 같은 지침을 skill로 또 넣지 않습니다. 본문이 세션에 두 번 들어갑니다. `~/.claude/skills/`에는 링크하지 않습니다.

## 프로젝트 안에서만 쓰기

전역 링크 없이, 이 저장소를 연 세션에서만 쓰려면 `.agents/skills/`가 이미 그 역할입니다. Cursor, Codex, Muse Code, grok-build는 저장소 루트의 `.agents/skills/`를 발견합니다.

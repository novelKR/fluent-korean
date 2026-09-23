#!/usr/bin/env bash
# 이 클론의 skill과 Claude Code output-style을 사용자 홈에 연결합니다.
# Cursor, Codex, Muse Code, grok-build는 ~/.agents/skills를 읽습니다.
# Claude Code는 ~/.claude/output-styles를 읽습니다.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

link_into() {
  local dest="$1"
  local src="$2"

  if [[ ! -e "$src" ]]; then
    echo "연결할 원본이 없습니다: $src" >&2
    exit 1
  fi

  mkdir -p "$(dirname "$dest")"

  if [[ -L "$dest" ]]; then
    ln -sfn "$src" "$dest"
  elif [[ -e "$dest" ]]; then
    echo "심볼릭 링크가 아닌 경로가 이미 있어 중단합니다: $dest" >&2
    exit 1
  else
    ln -s "$src" "$dest"
  fi
}

link_into "${HOME}/.agents/skills/fluent-korean" "${ROOT}/.agents/skills/fluent-korean"
link_into "${HOME}/.agents/skills/fluent-korean-not-coding" "${ROOT}/.agents/skills/fluent-korean-not-coding"
link_into "${HOME}/.claude/output-styles/fluent-korean.md" "${ROOT}/plugins/fluent-korean/output-styles/fluent-korean.md"
link_into "${HOME}/.claude/output-styles/fluent-korean-not-coding.md" "${ROOT}/plugins/fluent-korean/output-styles/fluent-korean-not-coding.md"

echo "사용자 전역 경로에 연결했습니다."
echo "  ${HOME}/.agents/skills/fluent-korean"
echo "  ${HOME}/.agents/skills/fluent-korean-not-coding"
echo "  ${HOME}/.claude/output-styles/fluent-korean.md"
echo "  ${HOME}/.claude/output-styles/fluent-korean-not-coding.md"
echo "Claude Code에서는 /config의 output-style을 fluent-korean으로 고른 뒤 새 세션을 시작하세요."

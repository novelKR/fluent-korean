#!/usr/bin/env bash
# 하네스에 맞는 사용자 경로로 이 클론의 skill을 연결합니다.
# agents는 ~/.agents/skills를 읽는 하네스용입니다.
# claude는 파일을 연결하지 않고 원본 저장소 안내만 출력합니다.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CHOICES=(agents cursor-cloud kimi-config claude)

usage() {
  cat <<'EOF'
사용법: scripts/install-user.sh [--harness 선택지[,선택지...]] [--list]

선택지:
  agents        ~/.agents/skills. Cursor 로컬, Codex, Muse Code, grok-build, Gemini CLI, Pi. Kimi Code CLI는 ~/.config/agents/skills가 없을 때만.
  cursor-cloud  ~/.cursor/skills. Cursor Cloud Agent와 원격 워커.
  kimi-config   ~/.config/agents/skills. 이 디렉터리가 있을 때의 Kimi Code CLI.
  claude        파일을 연결하지 않습니다. Claude Code는 https://github.com/snflkd/fluent-korean 을 사용합니다.

인자가 없고 표준 입력이 터미널이면 메뉴를 보여 줍니다.
터미널이 아니면 --harness가 필요합니다.
여러 경로는 --harness agents,cursor-cloud 처럼 쉼표로 지정합니다.
EOF
}

list_choices() {
  cat <<'EOF'
agents
  하네스: Cursor 로컬, Codex, Muse Code, grok-build, Gemini CLI, Pi. Kimi Code CLI는 ~/.config/agents/skills가 없을 때만 이 경로를 읽습니다.
  경로: ~/.agents/skills/
cursor-cloud
  하네스: Cursor Cloud Agent, 원격 워커
  경로: ~/.cursor/skills/
kimi-config
  하네스: Kimi Code CLI. ~/.config/agents/skills가 있으면 ~/.agents/skills를 읽지 않습니다.
  경로: ~/.config/agents/skills/
claude
  하네스: Claude Code
  경로: 파일을 연결하지 않습니다. https://github.com/snflkd/fluent-korean
EOF
}

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

unlink_if_points_here() {
  local dest="$1"
  local target

  if [[ ! -L "$dest" ]]; then
    return 0
  fi

  target="$(readlink "$dest")"
  case "$target" in
    "$ROOT"/*)
      rm "$dest"
      echo "이 포크를 가리키던 링크를 제거했습니다: $dest"
      ;;
  esac
}

link_skills() {
  local dest_root="$1"

  link_into "${dest_root}/fluent-korean" "${ROOT}/.agents/skills/fluent-korean"
  link_into "${dest_root}/fluent-korean-not-coding" "${ROOT}/.agents/skills/fluent-korean-not-coding"
  echo "연결했습니다: ${dest_root}/fluent-korean"
  echo "연결했습니다: ${dest_root}/fluent-korean-not-coding"
}

apply_claude() {
  unlink_if_points_here "${HOME}/.claude/output-styles/fluent-korean.md"
  unlink_if_points_here "${HOME}/.claude/output-styles/fluent-korean-not-coding.md"
  echo "Claude Code는 ~/.agents/skills를 읽지 않습니다. 이 포크의 파일을 연결하지 않습니다."
  echo "Claude Code에는 다음 문장을 사용합니다."
  echo "https://github.com/snflkd/fluent-korean/ 링크 README 읽고, 설치 안내 단락 읽고 어떻게 설치해서 사용할지 설명해줘"
}

apply_choice() {
  case "$1" in
    agents)
      link_skills "${HOME}/.agents/skills"
      ;;
    cursor-cloud)
      link_skills "${HOME}/.cursor/skills"
      ;;
    kimi-config)
      link_skills "${HOME}/.config/agents/skills"
      ;;
    claude)
      apply_claude
      ;;
    *)
      echo "알 수 없는 선택지입니다: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
}

choose_from_menu() {
  local choice
  local picked=""

  echo "설치할 선택지 번호를 입력합니다." >&2
  PS3="번호: "
  select choice in "${CHOICES[@]}"; do
    if [[ -n "${choice}" ]]; then
      picked="${choice}"
      break
    fi
    echo "목록에 있는 번호를 입력합니다."
  done
  printf '%s\n' "${picked}"
}

split_harness_list() {
  local raw="$1"
  local part

  IFS=',' read -r -a parts <<< "${raw}"
  for part in "${parts[@]}"; do
    if [[ -z "${part}" ]]; then
      echo "빈 선택지가 있습니다." >&2
      exit 1
    fi
    selected+=("${part}")
  done
}

selected=()
parts=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --list)
      list_choices
      exit 0
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    --harness)
      if [[ $# -lt 2 ]]; then
        echo "--harness 뒤에 선택지가 필요합니다." >&2
        usage >&2
        exit 1
      fi
      shift
      split_harness_list "$1"
      ;;
    --harness=*)
      split_harness_list "${1#--harness=}"
      ;;
    *)
      echo "알 수 없는 인자입니다: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
  shift
done

if [[ ${#selected[@]} -eq 0 ]]; then
  if [[ -t 0 ]]; then
    selected+=("$(choose_from_menu)")
  else
    echo "터미널이 아니면 --harness로 선택지를 지정합니다." >&2
    usage >&2
    exit 1
  fi
fi

for choice in "${selected[@]}"; do
  apply_choice "${choice}"
done

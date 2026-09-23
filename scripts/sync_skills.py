#!/usr/bin/env python3
"""output-style 원문에서 .agents/skills/*/SKILL.md를 다시 만듭니다.

본문은 요약하거나 고치지 않습니다. upstream의 output-style을 가져온 뒤
이 스크립트를 다시 실행하면 skill 본문이 그 원문을 따라갑니다.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STYLES = ROOT / "plugins" / "fluent-korean" / "output-styles"
SKILLS = ROOT / ".agents" / "skills"

VARIANTS: dict[str, dict[str, str]] = {
    "fluent-korean": {
        "source": "fluent-korean.md",
        "description": (
            "의미가 명확한 한국어 문장을 출력하는 작성 지침. "
            "사용자가 한국어로 말하거나 답변, 보고, 문서처럼 한국어 결과물을 작성할 때 읽고 따른다. "
            "코드, 코드 주석, 커밋 메시지, 로그 문자열, 인용문에는 적용하지 않는다. "
            "코딩 작업에서는 이 skill을 사용하고 fluent-korean-not-coding은 사용하지 않는다."
        ),
        "short_description": "명확한 한국어 출력 (코딩)",
        "disable_model_invocation": "false",
    },
    "fluent-korean-not-coding": {
        "source": "fluent-korean-not-coding.md",
        "description": (
            "코딩 지침을 제거한 명확한 한국어 작성 지침. "
            "사용자가 /fluent-korean-not-coding을 명시적으로 요청할 때만 사용한다. "
            "코드를 직접 고치지 않는 글쓰기에서만 켠다. "
            "일반적인 코딩 대화와 한국어 응답에는 fluent-korean을 사용한다."
        ),
        "short_description": "명확한 한국어 출력 (코딩 지침 없음)",
        "disable_model_invocation": "true",
    },
}


def split_frontmatter(text: str, path: Path) -> tuple[str, str]:
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        raise SystemExit(f"{path}: frontmatter가 없습니다.")
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return "".join(lines[1:index]), "".join(lines[index + 1 :])
    raise SystemExit(f"{path}: frontmatter가 닫히지 않았습니다.")


def keep_coding_instructions(frontmatter: str) -> str:
    for line in frontmatter.splitlines():
        key, sep, value = line.partition(":")
        if sep and key.strip() == "keep-coding-instructions":
            return "true" if value.strip().lower() == "true" else "false"
    return "false"


def yaml_quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def render_skill(name: str, spec: dict[str, str], frontmatter: str, body: str) -> str:
    description = spec["description"]
    if len(description) > 1024:
        raise SystemExit(f"{name}: description이 1024자를 넘습니다. ({len(description)})")
    lines = [
        "---",
        f"name: {name}",
        f"description: {yaml_quote(description)}",
        "license: MIT",
        "metadata:",
        "  author: snflkd",
        f"  short-description: {yaml_quote(spec['short_description'])}",
        f"  keep-coding-instructions: {yaml_quote(keep_coding_instructions(frontmatter))}",
    ]
    if spec["disable_model_invocation"] == "true":
        lines.append("disable-model-invocation: true")
    lines.append("---")
    rendered = "\n".join(lines) + "\n" + body
    if not rendered.endswith("\n"):
        rendered += "\n"
    return rendered


def render_openai_yaml(name: str, spec: dict[str, str]) -> str:
    return (
        "interface:\n"
        f"  display_name: {yaml_quote(name)}\n"
        f"  short_description: {yaml_quote(spec['short_description'])}\n"
        "policy:\n"
        "  allow_implicit_invocation: false\n"
    )


def main() -> None:
    for name, spec in VARIANTS.items():
        source = STYLES / spec["source"]
        frontmatter, body = split_frontmatter(source.read_text(encoding="utf-8"), source)
        skill_dir = SKILLS / name
        skill_dir.mkdir(parents=True, exist_ok=True)
        (skill_dir / "SKILL.md").write_text(
            render_skill(name, spec, frontmatter, body),
            encoding="utf-8",
        )
        openai_yaml = skill_dir / "agents" / "openai.yaml"
        if spec["disable_model_invocation"] == "true":
            openai_yaml.parent.mkdir(parents=True, exist_ok=True)
            openai_yaml.write_text(render_openai_yaml(name, spec), encoding="utf-8")
        elif openai_yaml.exists():
            openai_yaml.unlink()
        print(f"wrote {skill_dir.relative_to(ROOT)}")


if __name__ == "__main__":
    try:
        main()
    except OSError as error:
        print(error, file=sys.stderr)
        raise SystemExit(1) from error

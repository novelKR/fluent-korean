#!/usr/bin/env python3
"""ChatGPT용 skill 두 변형을 검증하고 각각 skill.zip으로 패키징합니다."""

from __future__ import annotations

import re
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "chatgpt" / "skills"
DIST = ROOT / "dist" / "chatgpt"
VARIANTS = ("fluent-korean", "fluent-korean-not-coding")
MAX_SKILL_ZIP_BYTES = 25 * 1024 * 1024


def split_frontmatter(text: str, path: Path) -> tuple[str, str]:
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        raise SystemExit(f"{path}: frontmatter가 없습니다.")
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return "".join(lines[1:index]), "".join(lines[index + 1 :])
    raise SystemExit(f"{path}: frontmatter가 닫히지 않았습니다.")


def parse_top_level_frontmatter(frontmatter: str, path: Path) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for line in frontmatter.splitlines():
        if not line.strip() or line.startswith((" ", "\t")):
            continue
        key, sep, value = line.partition(":")
        if not sep:
            raise SystemExit(f"{path}: frontmatter 형식을 확인합니다: {line}")
        parsed[key.strip()] = value.strip()
    return parsed


def unquote_yaml_scalar(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] == '"':
        return value[1:-1].replace('\\"', '"').replace("\\\\", "\\")
    return value


def validate_skill(skill_dir: Path) -> None:
    skill_md = skill_dir / "SKILL.md"
    openai_yaml = skill_dir / "agents" / "openai.yaml"
    if not skill_md.is_file():
        raise SystemExit(f"{skill_md}: 파일이 없습니다.")
    if not openai_yaml.is_file():
        raise SystemExit(f"{openai_yaml}: 파일이 없습니다.")

    frontmatter, _ = split_frontmatter(skill_md.read_text(encoding="utf-8"), skill_md)
    parsed = parse_top_level_frontmatter(frontmatter, skill_md)
    if set(parsed) != {"name", "description"}:
        raise SystemExit(
            f"{skill_md}: ChatGPT용 frontmatter는 name과 description만 포함해야 합니다. "
            f"현재 키: {', '.join(parsed)}"
        )

    name = unquote_yaml_scalar(parsed["name"])
    description = unquote_yaml_scalar(parsed["description"])
    if name != skill_dir.name:
        raise SystemExit(f"{skill_md}: name({name})이 디렉터리 이름과 다릅니다.")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        raise SystemExit(f"{skill_md}: name이 소문자 하이픈 형식이 아닙니다.")
    if not description:
        raise SystemExit(f"{skill_md}: description이 비어 있습니다.")
    if len(description) > 1024:
        raise SystemExit(f"{skill_md}: description이 1024자를 넘습니다.")


def package_skill(skill_dir: Path) -> Path:
    output_dir = DIST / skill_dir.name
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "skill.zip"
    if output_path.exists():
        output_path.unlink()

    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(skill_dir.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(skill_dir.parent))

    archive_size = output_path.stat().st_size
    if archive_size > MAX_SKILL_ZIP_BYTES:
        output_path.unlink()
        raise SystemExit(
            f"{skill_dir.name}: 패키지가 25 MiB 제한을 넘습니다. ({archive_size:,} bytes)"
        )
    return output_path


def main() -> None:
    subprocess.run([sys.executable, str(ROOT / "scripts" / "sync_skills.py")], check=True)
    for name in VARIANTS:
        skill_dir = SKILLS / name
        validate_skill(skill_dir)
        output_path = package_skill(skill_dir)
        print(f"packaged {output_path.relative_to(ROOT)}")


if __name__ == "__main__":
    try:
        main()
    except OSError as error:
        print(error, file=sys.stderr)
        raise SystemExit(1) from error

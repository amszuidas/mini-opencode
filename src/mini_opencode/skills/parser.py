from pathlib import Path
from typing import Optional

import yaml

from mini_opencode.skills.types import Skill


def parse_skill(skill_dir: Path) -> Optional[Skill]:
    """Parse a SKILL.md file in the given directory.

    Args:
        skill_dir: The directory containing the skill.

    Returns:
        A Skill object if SKILL.md exists and is valid, None otherwise.
    """
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.exists():
        return None

    try:
        content = skill_file.read_text(encoding="utf-8")
        if not content.startswith("---"):
            return None

        parts = content.split("---", 2)
        if len(parts) < 3:
            return None

        metadata = yaml.safe_load(parts[1])
        if not metadata:
            return None

        return Skill(
            name=metadata.get("name", ""),
            description=metadata.get("description", ""),
            license=metadata.get("license", ""),
            path=str(skill_dir.absolute()),
        )
    except Exception:
        return None

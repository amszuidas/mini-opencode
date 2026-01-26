from pathlib import Path

from mini_opencode.skills.parser import parse_skill
from mini_opencode.skills.types import Skill


def load_skills(skills_dir: Path) -> list[Skill]:
    """Load all skills from the given directory.

    Args:
        skills_dir: The directory containing skills.

    Returns:
        A list of Skill objects.
    """
    skills = []
    if not skills_dir.exists() or not skills_dir.is_dir():
        return skills

    for item in skills_dir.iterdir():
        if item.is_dir():
            skill = parse_skill(item)
            if skill:
                skills.append(skill)

    return skills

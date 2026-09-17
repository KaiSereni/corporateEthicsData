from pathlib import Path
from importlib.resources import files

BASE_DIR = Path(files("corporateEthicsData").name)
PROMPTING_DIR = BASE_DIR / "prompting"


def get_metric_dirs(prompting_dir: Path | str = PROMPTING_DIR) -> list[Path]:
    p_dir = Path(prompting_dir)
    return sorted([p for p in p_dir.iterdir() if p.is_dir()])


def get_metric_names(prompting_dir: Path | str = PROMPTING_DIR) -> list[str]:
    return [p.name for p in get_metric_dirs(prompting_dir)]

def generate_research_prompt(common: str, corporate: str) -> str:
    metric_descriptions_and_red_flags = []
    for dir in get_metric_dirs():
        with open(dir / "description", 'r') as f:
            this_description = f.read()
        with open(dir / "red_flags", 'r') as f:
            this_red_flags = f.read()
        metric_descriptions_and_red_flags.append(this_description + '\n' + this_red_flags)
    with open(PROMPTING_DIR / "RESEARCH", 'r') as f:
        return f.read().format(
            common=common,
            corporate=corporate,
            metrics='\n\n'.join(metric_descriptions_and_red_flags)
        )

def generate_ratings_prompt(common: str, corporate: str, report: str) -> str:
    metric_rating_descriptions = []
    for dir in get_metric_dirs():
        with open(dir / "description", 'r') as f:
            this_description = f.read()
        with open(dir / "rating") as f:
            this_rating_directions = f.read()
        metric_rating_descriptions.append(this_description + '\n' + this_rating_directions)
    with open(PROMPTING_DIR / "RATINGS", 'r') as f:
        return f.read().format(
            common=common,
            corporate=corporate,
            report=report,
            metrics='\n\n'.join(metric_rating_descriptions)
        )

if __name__ == "__main__":
    print("\n====== RESEARCH PROMPT ======\n")
    print(generate_research_prompt(
        "Alphabet",
        "Alphabet, inc"
    ))
    print("\n====== RATINGS PROMPT ======\n")
    print(generate_ratings_prompt(
        "Alphabet",
        "Alphabet, inc",
        "TEST REPORT"
    ))

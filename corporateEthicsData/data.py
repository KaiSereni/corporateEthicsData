from corporateEthicsData.prompting import BASE_DIR
from typing import Callable, Literal
from .ai import research_call, structured_call
from .prompting import generate_ratings_prompt, generate_research_prompt, get_metric_names
import random, json

_TEST_COMMON = "Honeywell"
_TEST_CORPORATE = "Honeywell International Inc"

Models = list[dict[Literal["id", "common_name"], str]]

with open(BASE_DIR / 'models.json', 'r', encoding="utf-8") as f:
    MODELS: Models = json.load(f)

Ratings = list[dict[Literal['metric', 'rating'], str | int]]

def get_report_and_ratings(common: str, corporate: str, model: str) -> tuple[str, Ratings]:
    report = research_call(generate_research_prompt(common, corporate), None, model=model)
    return report, structured_call(generate_ratings_prompt(common, corporate, report), None, get_metric_names(), model=model)["ratings"]

def _test_report_and_ratings(common: str, corporate: str, model: str) -> tuple[str, Ratings]:
    return (
        f"# Ethics Report for {common} aka {corporate} using {model}:\n\nThey baaaad\n", 
        [
            {
                "metric": "animal_welfare",
                "rating": random.randint(0, 100)
            },
            {
                "metric": "diversity",
                "rating": random.randint(0, 100)
            },
            {
                "metric": "labor_rights",
                "rating": random.randint(0, 100)
            }
        ]
    )

Reports = list[dict[Literal["model_common_name", "model_id", "report", "ratings"], str | Ratings]]

def get_series_of_reports(common:str, corporate:str, test_mode=True, models:Models=MODELS) -> Reports:
    output_dict: Reports = []
    for model in models:
        _report_and_ratings_function: Callable[[str, str, str], tuple[str, Ratings]] = _test_report_and_ratings if test_mode else get_report_and_ratings
        report, ratings = _report_and_ratings_function(common, corporate, model["id"])
        output_dict.append({
            'model_common_name': model['common_name'],
            'model_id': model['id'],
            'report': report,
            'ratings': ratings
        })
    return output_dict

if __name__ == "__main__":
    print(get_series_of_reports(
        common=_TEST_COMMON,
        corporate=_TEST_CORPORATE,
        test_mode=True
    ))
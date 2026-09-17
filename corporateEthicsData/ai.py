import os, json
import dotenv
from openrouter import OpenRouter


dotenv.load_dotenv()
if not os.getenv("OPENROUTER_KEY"):
    raise RuntimeWarning("You need to define an OpenRouter API key in ./env (with the key \"OPENROUTER_KEY\")")

def research_call(prompt: str, system: str | None, model: str) -> str:
    messages = []
    if system:
        messages.append({
            "role": "system",
            "content": system,
        })
    messages.append({
        "role": "user",
        "content": prompt,
    })

    with OpenRouter(
        api_key=os.getenv("OPENROUTER_KEY"),
    ) as client:
        interaction = client.chat.send(
            model=model,
            messages=messages,
            plugins=[{"id": "web"}],
            max_completion_tokens=65536,
            stream=False,
        )

        return interaction.choices[0].message.content or ""


def structured_call(prompt: str, system: str | None, metric_categories: list[str], model: str) -> dict:
    messages = []
    if system:
        messages.append({
            "role": "system",
            "content": system,
        })
    messages.append({
        "role": "user",
        "content": prompt,
    })

    response_format = {
        "type": "json_schema",
        "json_schema": {
            "name": "ratings",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "ratings": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "metric": {
                                    "type": "string",
                                    "enum": metric_categories,
                                },
                                "rating": {
                                    "type": "integer",
                                },
                            },
                            "required": [
                                "metric",
                                "rating",
                            ],
                            "additionalProperties": False,
                        },
                    }
                },
                "required": [
                    "ratings",
                ],
                "additionalProperties": False,
            },
        },
    }

    with OpenRouter(
        api_key=os.getenv("OPENROUTER_KEY"),
    ) as client:
        interaction = client.chat.send(
            model=model,
            messages=messages,
            max_completion_tokens=65536,
            response_format=response_format,
            stream=False,
        )

        return json.loads(interaction.choices[0].message.content)

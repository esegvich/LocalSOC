import json
from pathlib import Path

import ollama
import yaml

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config.yaml"
with open(CONFIG_PATH) as f:
    CONFIG = yaml.safe_load(f)

client = ollama.Client(host=CONFIG["ollama_host"])


def ask_json(system: str, user: str) -> dict:
    """Send one prompt to the local model and return its JSON reply as a dict."""
    resp = client.chat(
        model=CONFIG["model"],
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        format="json",
        think=False,
        options={
            "temperature": CONFIG["temperature"],
            "num_ctx": CONFIG["num_ctx"],
        },
    )
    return json.loads(resp["message"]["content"])


if __name__ == "__main__":
    # Quick smoke test: run `python localsoc/llm.py`
    print(ask_json(
        "You are a SOC analyst. Reply only in JSON with keys technique_id and technique_name.",
        "Which MITRE ATT&CK technique is repeated SSH password guessing against one account?",
    ))
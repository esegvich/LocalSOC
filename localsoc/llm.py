import json, yaml, ollama

from pathlib import Path
CONFIG = yaml.safe_load(open(Path(__file__).resolve().parent.parent / "config.yaml"))
client = ollama.Client(host=CONFIG["ollama_host"])

def ask_json(system: str, user: str) -> dict:
    resp = client.chat(
        model=CONFIG["model"],
        messages=[{"role": "system", "content": system},
                  {"role": "user", "content": user}],
        format="json",
        options={"temperature": CONFIG["temperature"]},
    )
    return json.loads(resp["message"]["content"])
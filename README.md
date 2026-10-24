# LocalSOC

**A multi-agent SOC analyst that runs entirely on a local LLM, on an 8GB laptop.**

LocalSOC turns real SSH server logs into security alerts, triages them with a team of AI agents running on a local model (Gemma 4 via Ollama), and writes a Tier 1 incident report. It enriches indicators, maps each alert to MITRE ATT&CK, and closes obvious benign alerts early. I then attacked it with prompt injection and documented which defenses worked.

No alert data ever leaves the machine.

> Status: 🚧 In progress. See the [roadmap](#roadmap).

---

## Why I built this

SOC teams are adopting AI for triage, but sending alert data (IPs, usernames, hostnames) to an outside API is a real concern. I wanted to see how far a small local model can go on Tier 1 work, how to structure agents so a weak model still gives useful results, and how an attacker could abuse an AI analyst through the logs themselves.

## Architecture

![Architecture diagram](docs/architecture.png)

| Agent | What it does | LLM's role |
| --- | --- | --- |
| **Coordinator** | Decides if an alert is clearly benign or needs investigation | Quick verdict |
| **Enrichment** | Extracts IPs and usernames, checks VirusTotal reputation | Summarizes lookup results only |
| **MITRE mapper** | Maps the alert to an ATT&CK technique and tactic | Picks the technique and explains why |
| **Report writer** | Produces a Markdown Tier 1 incident report | Writes the report |

**Design choice:** Python code does all tool work (regex extraction, API calls). The LLM only reasons and writes. Small models are unreliable at choosing and calling tools themselves, and this split also limits what a prompt-injection attack can make the system *do*.

All agents share one model loaded once in Ollama and run in sequence, which keeps memory use within 8GB.

## Tech stack

- **Model:** Gemma 4 E2B via [Ollama](https://ollama.com) (configurable in `config.yaml`)
- **Orchestration:** [LangGraph](https://github.com/langchain-ai/langgraph)
- **Enrichment:** VirusTotal API
- **Data source:** real sshd logs from the [Loghub OpenSSH dataset](https://github.com/logpai/loghub/tree/master/OpenSSH), turned into alerts by my own Python detector (`detect.py`)
- **Built with:** Claude Code as an AI coding assistant (see [AI-assisted coding log](docs/ai-coding-log.md))
- **Hardware:** 2020 MacBook Pro, M1, 8GB RAM

## Results

Evaluated against `samples/labels.csv`, a hand-labeled set of alerts generated from the Loghub OpenSSH logs.

| Version | Technique accuracy | Verdict accuracy | False negatives | Avg time / alert |
| --- | --- | --- | --- | --- |
| v0.1 Single agent | _TBD_ | _TBD_ | _TBD_ | _TBD_ |
| v0.2 Multi-agent | _TBD_ | _TBD_ | _TBD_ | _TBD_ |
| v0.3 With defenses | _TBD_ | _TBD_ | _TBD_ | _TBD_ |


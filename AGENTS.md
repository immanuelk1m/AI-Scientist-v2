# Repository Guidelines

## Project Structure & Module Organization
- `ai_scientist/`: core Python package (agentic tree search, LLM/VLM integrations, ideation, writeup, plotting).
- `ai_scientist/ideas/`: example topic prompts (`.md`) and generated idea files (`.json`).
- `ai_scientist/treesearch/`: tree search engine, backends, and utilities.
- `docs/`: documentation assets (e.g., `docs/logo_v1.png`).
- Top-level scripts: `launch_scientist_bfts.py` (main pipeline), `ai_scientist/perform_ideation_temp_free.py` (ideation).
- Config: `bfts_config.yaml` (tree search and model configuration), `requirements.txt` (Python deps).

## Build, Test, and Development Commands
- `pip install -r requirements.txt` installs Python dependencies.
- `python ai_scientist/perform_ideation_temp_free.py --workshop-file "ai_scientist/ideas/my_topic.md" --model gpt-4o-2024-05-13` generates ideas from a topic prompt.
- `python launch_scientist_bfts.py --load_ideas "ai_scientist/ideas/my_topic.json" ...` runs the full experiment pipeline and writeup.
- Conda setup (GPU/CUDA) is documented in `README.md` if you need the exact environment.

## Coding Style & Naming Conventions
- Python code uses 4-space indentation; follow existing style in nearby files.
- Prefer explicit names over abbreviations; keep module filenames snake_case.
- No repo-wide formatter or linter is configured; avoid reformatting unrelated code.

## Testing Guidelines
- No dedicated test suite is present. If you add tests, document how to run them and keep them close to the relevant module (e.g., `ai_scientist/treesearch/tests/`).
- Validate changes by running the smallest relevant script (ideation or BFTS launch) when feasible.

## Commit & Pull Request Guidelines
- Commit messages in history are short, sentence-case summaries (e.g., "Add license and responsible use section to README").
- For PRs: include a concise summary, list config or model changes, and attach logs or screenshots when output artifacts change (e.g., `experiments/*/unified_tree_viz.html`).

## Security & Configuration Notes
- The pipeline executes LLM-written code; run in a sandboxed environment.
- Provide required API keys via environment variables (e.g., `OPENAI_API_KEY`, `S2_API_KEY`, AWS credentials for Bedrock).

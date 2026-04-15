# llm-colab-bridge

> Run any HuggingFace LLM on a free Colab / Kaggle GPU and chat with it from any weak local device — no local GPU required.

---

## How It Works

```
[Your Weak Device]
  browser @ localhost:8080
        │
        │  HTTP/JSON
        ▼
[local_client/serve.py]  ←─ reads config.json for URL + API key
        │
        │  HTTPS via ngrok tunnel
        ▼
[Colab / Kaggle Runtime]
  FastAPI + TinyLlama (or any HF model) on GPU
```

1. The notebook runs on a free Colab/Kaggle GPU, loads the model, and exposes a FastAPI server through an ngrok tunnel.
2. Each session it auto-generates a secret API key, writes everything to `config.json`, and offers a one-click download.
3. Drop `config.json` next to the local website and open `http://localhost:8080` — it connects automatically, no manual config needed.

---

## Project Structure

```
llm-colab-bridge/
├── colab_kaggle_llm_server.ipynb   # Run this on Colab / Kaggle
└── local_client/
    ├── index.html                  # Chat UI — open via serve.py
    ├── serve.py                    # Tiny local HTTP server
    └── config.json                 # ⚠ Auto-generated, gitignored — never commit
```

---

## Quick Start

### 1 — Colab / Kaggle (the GPU side)

1. Open `colab_kaggle_llm_server.ipynb` in [Google Colab](https://colab.research.google.com) or [Kaggle](https://kaggle.com/code).
2. Fill in **Cell 1** — the only cell that needs manual input:
   - `NGROK_AUTH_TOKEN` — free at [ngrok.com](https://dashboard.ngrok.com/get-started/your-authtoken)
   - `HF_TOKEN` — only needed for gated models (Llama, Mistral, Gemma…)
3. Run cells **1 → 6** in order. Cell 6 will:
   - Connect the ngrok tunnel and print the public URL
   - Auto-generate a session API key
   - Render a **⬇ download link** for `config.json`
   - Start the FastAPI server (cell stays running — that's normal)

### 2 — Local device (the client side)

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/llm-colab-bridge.git
cd llm-colab-bridge

# Drop the downloaded config.json into local_client/
cp ~/Downloads/config.json local_client/

# Start the local server (Python stdlib only, no pip install needed)
python3 local_client/serve.py

# Opens http://localhost:8080 automatically
```

The chat UI will detect `config.json`, connect to the running model, and turn the status dot green.

---

## Switching Models

Edit `MODEL_ID` and `TASK` in Cell 1 of the notebook:

| Model | Size | `USE_4BIT` | Notes |
|---|---|---|---|
| `TinyLlama/TinyLlama-1.1B-Chat-v1.0` | 1.1B | `False` | Default — fits anywhere |
| `microsoft/Phi-3-mini-4k-instruct` | 3.8B | `False` | Stronger, still fits on T4 |
| `mistralai/Mistral-7B-Instruct-v0.3` | 7B | `True` | Best quality on free GPU |
| `HuggingFaceH4/zephyr-7b-beta` | 7B | `True` | Great conversational model |

---

## API Endpoints

The notebook exposes a small REST API behind the ngrok tunnel:

| Method | Path | Description |
|---|---|---|
| `GET` | `/` | Health check — returns model name and device |
| `POST` | `/chat` | Multi-turn chat with conversation history |
| `POST` | `/predict` | Single raw-text inference |
| `POST` | `/predict_batch` | Batch raw-text inference |

All endpoints require the `x-api-key` header (value comes from `config.json`).

**Chat request example:**
```json
POST /chat
{
  "messages": [
    { "role": "user", "content": "Explain what ngrok does in one sentence." }
  ],
  "max_new_tokens": 256,
  "temperature": 0.7
}
```

---

## Security Notes

- `config.json` contains live secrets (API key, HF token, ngrok token). It is **gitignored** and must never be committed.
- The API key is regenerated every session — copy a fresh `config.json` each time you restart the notebook.
- The ngrok URL is publicly reachable. Keep `API_SECRET_KEY` strong (it is auto-generated as a 64-char hex string).

---

## Platform Notes

| Platform | GPU | Free hours | Notes |
|---|---|---|---|
| Google Colab | T4 (15 GB) | ~4–5 h/day | May disconnect after 90 min idle |
| Kaggle | T4 × 2 (30 GB) | 30 h/week | More stable, enable Internet in Settings |

---

## Requirements

**Notebook (Colab/Kaggle):** all dependencies installed by Cell 2.

**Local client:** Python 3 stdlib only — no `pip install` needed.

---

## License

MIT

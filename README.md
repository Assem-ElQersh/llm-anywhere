# llm-anywhere

Run a Hugging Face LLM on **Colab / Kaggle** (GPU) and chat from your browser via **ngrok** — no local GPU.

**Flow:** notebook → FastAPI + tunnel → download `config.json` → `python3 local_client/serve.py` → open `http://localhost:8080`.

---

## Layout

```
llm-anywhere/
├── colab_kaggle_llm_server.ipynb
└── local_client/
    ├── index.html
    ├── serve.py
    ├── site.json.example   # → copy to site.json (optional; gitignored)
    └── config.json         # from notebook; gitignored
```

---

## Quick start

**On Colab or Kaggle**

1. Open `colab_kaggle_llm_server.ipynb`.
2. Set `NGROK_AUTH_TOKEN` in the config cell ([ngrok token](https://dashboard.ngrok.com/get-started/your-authtoken)); set `HF_TOKEN` only for gated models.
3. Run all cells through the one that starts ngrok and the server (that cell stays running).
4. Download `config.json` when offered.

**On your machine**

```bash
git clone https://github.com/YOUR_USERNAME/llm-anywhere.git
cd llm-anywhere
cp /path/to/config.json local_client/
python3 local_client/serve.py
```

**Connect** in the UI opens a notebook URL in a new tab only. Optional: copy `site.json.example` to `site.json` with `"notebook_url": "https://..."` (Colab or Kaggle).

---

## Models

In the notebook config cell, change `MODEL_ID` (and `USE_4BIT` for large models). Defaults work on a free T4.

---

## API (behind ngrok)

All routes need header `x-api-key` (from `config.json`).

| Method | Path | Notes |
|--------|------|--------|
| GET | `/` | Health |
| POST | `/chat` | Main chat UI |
| POST | `/predict`, `/predict_batch` | Raw pipeline calls |

---

## Security

Do not commit `local_client/config.json`. It holds the session API key and tunnel URL. Downloaded `config.json` does not include your ngrok or Hugging Face **account** tokens.

---

## License

MIT — see [LICENSE](LICENSE).

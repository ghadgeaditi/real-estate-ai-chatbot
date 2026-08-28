# PropertyLens AI — Full-Stack AI Developer Assignment

A containerized retrieval-augmented chatbot demonstrating a real-estate AI workflow with a **fully synthetic dataset** shaped like common property metadata.

> **Important:** The deployed version does **not scrape DarGlobal or Wasalt and does not copy their listings, descriptions, prices, images, contact details, or other website content.** All property records bundled with the app are fictional demo records.

## Why synthetic data is used

This low-risk version is intended to demonstrate engineering skills—normalization, retrieval, prompt grounding, OpenRouter integration, React, FastAPI, Docker, and deployment—without redistributing third-party website content.

This is a deliberate safety trade-off: because no live scraping occurs, this version **does not strictly satisfy a requirement that specifically asks for web scraping**. For a production or formal assessment requiring real data collection, permission or an authorized API/data source should be used, or the website owner should confirm the permitted scope.

## What it demonstrates

- Synthetic real-estate data modeling and normalization
- Retrieval-augmented generation (RAG)
- OpenRouter LLM integration using `openrouter/free`
- React frontend + FastAPI backend
- Grounded answers from an indexed dataset
- Dockerized single-container deployment
- Retrieval-only fallback if the LLM provider is unavailable

## Architecture

```text
Synthetic demo property records
            |
            v
 normalized properties.json
            |
            v
TF-IDF retrieval (top-k context)
            |
            v
OpenRouter free-model router
            |
            v
FastAPI API -> React chatbot
```

## Dataset safety

The bundled `backend/data/properties.json` contains only fictional records. The provider labels `DarGlobal Demo` and `Wasalt Demo` indicate the schema/experience being demonstrated; they do not mean the records were supplied by, scraped from, or verified by those companies.

The app makes no scraping requests during normal use or deployment. `backend/data/generate_dummy_data.py` is network-free and simply verifies the bundled demo dataset.

## Run locally

Create `.env`:

```bash
cp .env.example .env
```

Add your OpenRouter key:

```env
OPENROUTER_API_KEY=...
OPENROUTER_MODEL=openrouter/free
```

Build and run:

```bash
docker build -t propertylens-ai .
docker run --env-file .env -p 8000:8000 propertylens-ai
```

Open `http://localhost:8000`.

Health check:

```bash
curl http://localhost:8000/api/health
```

## API

### `POST /api/chat`

Example request:

```json
{ "message": "Show the DarGlobal demo records in Oman." }
```

### `GET /api/health`

Returns API status, record count, and configured model.

## Deploy on Render

This repository includes `render.yaml` and a Dockerfile.

1. Push the repository to GitHub.
2. In Render, create a Blueprint or Web Service from the repository.
3. Use the Docker runtime.
4. Add `OPENROUTER_API_KEY` as a secret environment variable.
5. Keep `OPENROUTER_MODEL=openrouter/free`.
6. Deploy and test `/api/health`, then the main chatbot URL.

## Security decisions

- No real listing/contact/personal data is bundled.
- No live scraping occurs in the deployed version.
- API keys stay in environment variables and are never sent to the browser.
- `.env` is gitignored.
- The LLM receives only retrieved synthetic property context.
- The prompt explicitly prevents the model from presenting demo records as real listings or live availability.
- User message length is bounded by the API schema.
- Error responses avoid leaking provider response bodies or secrets.

## Example questions

- Show the DarGlobal demo records in Oman.
- Show demo apartments in Jeddah under 600,000 SAR.
- Compare the synthetic Riyadh and Jeddah options.
- Which demo records have 4 or more bedrooms?

## Disclaimer

This repository is a technical-assessment demonstration. All property records, titles, prices, bedroom/bathroom counts and availability represented in the bundled dataset are fictional. DarGlobal and Wasalt are referenced only to explain the assessment context and are not represented as endorsing, supplying, or validating the synthetic records.

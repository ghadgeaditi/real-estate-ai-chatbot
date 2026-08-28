# Assignment Walkthrough Notes — Synthetic/Low-Risk Version

## Demo flow

1. Open the deployed chatbot.
2. Ask: **Show the DarGlobal demo records in Oman.**
3. Explain that retrieval selects relevant fictional records from `backend/data/properties.json`.
4. Explain that only retrieved context is sent to OpenRouter using `openrouter/free`.
5. Show that the UI clearly labels the dataset as synthetic.
6. Show Docker/Render deployment and environment-variable handling.

## Short architecture explanation

“I used a lightweight RAG architecture because the assessment dataset is small. For the low-risk version, the data is fully synthetic rather than copied from third-party websites. The records are normalized into a common schema, TF-IDF retrieves the most relevant records, and only those records are sent to the OpenRouter model. The model is instructed not to present synthetic records as real listings. React is built in the Docker build stage and served by FastAPI, so deployment uses one container and one public URL.”

## Important limitation

This version intentionally performs no live scraping. It is safer for a public demo, but it does not strictly satisfy an assignment requirement that mandates scraping. If real collection is required, use an authorized API, written permission, or an explicitly approved limited collection scope.

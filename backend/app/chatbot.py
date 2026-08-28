import httpx
from .config import settings
from .schemas import PropertyRecord


def context_text(records: list[PropertyRecord]) -> str:
    chunks = []
    for i, r in enumerate(records, start=1):
        chunks.append(
            f"[{i}] Provider: {r.provider}\n"
            f"Title: {r.title}\nLocation: {r.location}\nType: {r.property_type}\n"
            f"Price: {r.price}\nBedrooms: {r.bedrooms}\nBathrooms: {r.bathrooms}\n"
            f"Description: {r.description}\nReference website: {r.url}"
        )
    return "\n\n".join(chunks)


def retrieval_only_answer(question: str, records: list[PropertyRecord]) -> str:
    if not records:
        return "I couldn't find relevant records in the collected dataset. Try asking about a city, project, property type, or budget."
    lines = ["I found these relevant results in the collected property dataset:"]
    for r in records[:5]:
        details = ", ".join(x for x in [r.location, r.price, f"{r.bedrooms} bedrooms" if r.bedrooms else ""] if x)
        lines.append(f"- {r.title} ({r.provider})" + (f" — {details}" if details else ""))
    lines.append("\nAdd an OPENROUTER_API_KEY to enable natural-language AI synthesis and comparisons.")
    return "\n".join(lines)


async def answer_question(question: str, records: list[PropertyRecord]) -> tuple[str, str]:
    if not settings.openrouter_api_key:
        return retrieval_only_answer(question, records), "retrieval-only"

    system = (
        "You are PropertyLens AI, a real-estate research assistant. Answer ONLY from the provided collected data. "
        "Never invent prices, availability, amenities, locations, or project facts. If evidence is insufficient, say so. "
        "Keep answers concise and useful. When comparing properties, clearly identify the provider. "
        "The dataset is synthetic demo data. Do not claim that any record is a real listing, project, price, or live availability."
    )
    user = f"Question: {question}\n\nCollected data:\n{context_text(records)}"

    headers = {
        "Authorization": f"Bearer {settings.openrouter_api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://propertylens-ai.example",
        "X-Title": settings.app_name,
    }
    payload = {
        "model": settings.openrouter_model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 0.2,
        "max_tokens": 600,
    }
    async with httpx.AsyncClient(timeout=45) as client:
        resp = await client.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        resp.raise_for_status()
        body = resp.json()
        return body["choices"][0]["message"]["content"], "ai"

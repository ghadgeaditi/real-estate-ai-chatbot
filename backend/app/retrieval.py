import json
from pathlib import Path
from threading import Lock

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .schemas import PropertyRecord


class Retriever:
    def __init__(self, data_file: str):
        self.path = Path(data_file)
        self._lock = Lock()
        self.records: list[PropertyRecord] = []
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        self.matrix = None
        self.reload()

    @staticmethod
    def _doc(r: PropertyRecord) -> str:
        return " | ".join(
            x for x in [
                r.provider, r.title, r.location, r.property_type, r.price,
                r.bedrooms, r.bathrooms, r.description
            ] if x
        )

    def reload(self) -> None:
        with self._lock:
            if not self.path.exists():
                self.records = []
                self.matrix = None
                return
            raw = json.loads(self.path.read_text(encoding="utf-8"))
            self.records = [PropertyRecord(**item) for item in raw]
            if self.records:
                self.matrix = self.vectorizer.fit_transform([self._doc(r) for r in self.records])
            else:
                self.matrix = None

    def search(self, query: str, k: int = 7) -> list[PropertyRecord]:
        if not self.records or self.matrix is None:
            return []
        q = self.vectorizer.transform([query])
        scores = cosine_similarity(q, self.matrix)[0]
        order = scores.argsort()[::-1]
        chosen = [i for i in order[:k] if scores[i] > 0]
        if not chosen:
            chosen = list(order[: min(k, len(order))])
        return [self.records[i] for i in chosen]

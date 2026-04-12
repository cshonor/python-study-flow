"""Ch. 21.9: FastAPI async web service demo (optional dependency).

Run (after installing deps):
  pip install fastapi uvicorn
  uvicorn part-4-control-flow.chapter-21.web_mojifinder_fastapi_demo:app --reload
"""

from __future__ import annotations

import unicodedata
from dataclasses import dataclass

try:
    from fastapi import FastAPI
except Exception as e:  # pragma: no cover
    raise SystemExit(
        "FastAPI demo requires optional deps. Install: pip install fastapi uvicorn"
    ) from e


@dataclass(frozen=True)
class Hit:
    char: str
    name: str


def search_unicode(q: str, limit: int = 20) -> list[Hit]:
    q = q.strip().upper()
    if not q:
        return []
    hits: list[Hit] = []
    for codepoint in range(0x0000, 0x2FFF):
        ch = chr(codepoint)
        try:
            name = unicodedata.name(ch)
        except ValueError:
            continue
        if q in name:
            hits.append(Hit(char=ch, name=name))
            if len(hits) >= limit:
                break
    return hits


app = FastAPI(title="Mojifinder Web (demo)")


@app.get("/search")
async def search(q: str, limit: int = 20):
    # CPU-ish work: in real apps, consider prebuilt index or offload if heavy.
    hits = search_unicode(q, limit=limit)
    return [{"char": h.char, "name": h.name} for h in hits]


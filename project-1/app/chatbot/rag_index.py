import os
import json
import requests
import numpy as np
from typing import List, Optional

def keyword_search_policy(session, query: str, limit: int = 3):
    q = f"%{query}%"
    rows = session.execute(
        "SELECT id, title, body FROM policy_documents WHERE body LIKE :q OR title LIKE :q LIMIT :lim",
        {"q": q, "lim": limit},
    ).fetchall()
    return [(r[0], r[1], r[2]) for r in rows]

def generate_embedding_google(text: str, model: str = "textembedding-gecko-001") -> Optional[List[float]]:
    api_key = os.getenv("GOOGLE_API_KEY", "")
    if not api_key:
        return None
    url = f"https://generativelanguage.googleapis.com/v1/models/{model}:embedText?key={api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {"text": text}
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        if 'data' in data and len(data['data']) > 0 and 'embedding' in data['data'][0]:
            return data['data'][0]['embedding']
        if 'embedding' in data:
            emb = data['embedding']
            if isinstance(emb, dict) and 'values' in emb:
                return emb['values']
            if isinstance(emb, list):
                return emb
        return None
    except Exception:
        return None

def embedding_retrieve(session, query_embedding, top_k=3):
    
    rows = session.execute(
        "SELECT id, title, body, embedding_vector FROM policy_documents WHERE embedding_vector IS NOT NULL"
    ).fetchall()
    candidates = []
    for r in rows:
        try:
            vec = json.loads(r[3])
            candidates.append((r[0], r[1], r[2], vec))
        except Exception:
            continue
    if not candidates:
        return []
    qv = np.array(query_embedding)
    sims = []
    for cid, title, body, vec in candidates:
        v = np.array(vec)
        sim = float(np.dot(qv, v) / (np.linalg.norm(qv) * np.linalg.norm(v) + 1e-10))
        sims.append((sim, cid, title, body))
    sims.sort(reverse=True, key=lambda x: x[0])
    top = sims[:top_k]
    return [(t[1], t[2], t[3]) for t in top]

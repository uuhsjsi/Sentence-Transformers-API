import os
import time
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

model = SentenceTransformer(os.environ['MODEL'])

# when first loading the server, do a dummy request to load the model into memory
model.encode(['dummy'])

app = FastAPI()

@app.get("/health")
async def heathcheck():
    return {"status": "ok"}

class EmbeddingRequest(BaseModel):
    texts: List[str]

class EmbeddingResponse(BaseModel):
    embeddings: List[List[float]]

@app.post("/embed")
async def embed(request: EmbeddingRequest) -> EmbeddingResponse:
    start = time.time()
    embeddings = model.encode(request.texts, normalize_embeddings=True)
    print(f'embedded {len(request.texts)} texts in {(time.time() - start):.2f} seconds')
    return EmbeddingResponse(embeddings=embeddings.tolist())
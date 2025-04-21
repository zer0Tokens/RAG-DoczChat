import json
from functools import lru_cache
from typing import List
import numpy as np

from llama_index.core import VectorStoreIndex
from llama_index.core.schema import TextNode
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding


from app.core.vectorstore import get_conn
from app.core.settings import settings

TABLE_NAME = "doc_vectors"
EMBED_DTYPE = np.float32


@lru_cache(maxsize=1)
def get_query_engine():
    """Return a cached LlamaIndex `QueryEngine`."""

    # 1· load rows from SQLite
    conn = get_conn(settings.DB_PATH)
    rows = conn.execute(
        f"SELECT content, embedding, metadata FROM {TABLE_NAME}"
    ).fetchall()

    # 2· convert to TextNode list
    nodes: List[TextNode] = []
    for content, emb_blob, meta_json in rows:
        embedding = np.frombuffer(emb_blob, dtype=EMBED_DTYPE).tolist()
        metadata = json.loads(meta_json or "{}")
        nodes.append(TextNode(text=content, embedding=embedding, metadata=metadata))

    # 3· build an in‑memory VectorStoreIndex (uses internal SimpleVectorStore + DocStore)
    embed_model = OpenAIEmbedding(
        model=settings.OPENAI_EMBEDDING_MODEL,
        api_key=settings.OPENAI_API_KEY,
    )
    index = VectorStoreIndex(nodes, embed_model=embed_model)

    # 4· plug in the desired LLM
    llm = OpenAI(model=settings.OPENAI_CHAT_MODEL, api_key=settings.OPENAI_API_KEY)
    return index.as_query_engine(llm=llm)


def reset_cache() -> None:
    """Clear cached engine – call after new document ingestion."""
    get_query_engine.cache_clear()

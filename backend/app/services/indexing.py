from pathlib import Path
from tempfile import NamedTemporaryFile
from llama_index.readers.file import PDFReader, DocxReader
from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core import Document

from .doc_cleaner import clean
from app.core.vectorstore import get_conn, insert_nodes
from app.core.settings import settings


def _loader(suffix: str):
    return PDFReader() if suffix == ".pdf" else DocxReader()


def run_ingestion(upload_file):
    suffix = Path(upload_file.filename).suffix.lower()
    if suffix not in {".pdf", ".docx"}:
        raise ValueError("Only PDF and DOCX are supported")

    with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(upload_file.file.read())
        tmp_path = Path(tmp.name)

    raw_docs = _loader(suffix).load_data(file=tmp_path)

    cleaned_docs = [
        Document(
            text=clean(doc.get_content()),
            metadata=doc.metadata,
            doc_id=doc.doc_id,
        )
        for doc in raw_docs
    ]

    embed_model = OpenAIEmbedding(
        api_key=settings.OPENAI_API_KEY,
        model=settings.OPENAI_EMBEDDING_MODEL,
    )
    pipeline = IngestionPipeline(
        transformations=[
            SemanticSplitterNodeParser(
                buffer_size=1,
                breakpoint_percentile_threshold=95,
                embed_model=embed_model,
            ),
            embed_model,
        ]
    )
    nodes = pipeline.run(documents=cleaned_docs)

    conn = get_conn(settings.DB_PATH)
    added = insert_nodes(conn, nodes)

    tmp_path.unlink(missing_ok=True)
    return added

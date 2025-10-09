from vertexai import rag
from google.cloud import aiplatform
import vertexai


PROJECT_ID = "ircbot-474408"  
LOCATION = "us-east4"         
DISPLAY_NAME = "ircbot_corpus"  

FILE_PATHS = [
    "gs://irc-documents-store/IRC - 5 - 2024.pdf",
    "gs://irc-documents-store/IRC 78 Part-1-2024.pdf",
    "gs://irc-documents-store/IRC-112-2020.pdf",
    "gs://irc-documents-store/irc.gov.in.sp.073.2018.pdf",
    "gs://irc-documents-store/irc.gov.in.sp.084.2019.pdf",
    "gs://irc-documents-store/irc.gov.in.sp.087.2019.pdf"
]

vertexai.init(project=PROJECT_ID, location=LOCATION)
embedding_model_config = rag.RagEmbeddingModelConfig(
    vertex_prediction_endpoint=rag.VertexPredictionEndpoint(
        publisher_model="publishers/google/models/text-embedding-005"
    )
)

corpus = rag.create_corpus(
    display_name=DISPLAY_NAME,
    backend_config=rag.RagVectorDbConfig(
        rag_embedding_model_config=embedding_model_config
    ),
)

print(f"Corpus created: {corpus.name}")
rag.import_files(
    corpus.name,
    FILE_PATHS,
    transformation_config=rag.TransformationConfig(
        chunking_config=rag.ChunkingConfig(
            chunk_size=512,
            chunk_overlap=100,
        ),
    ),
    max_embedding_requests_per_min=1000,
)

print("Files imported")

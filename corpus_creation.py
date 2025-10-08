from vertexai import rag
from google.cloud import aiplatform
import vertexai


PROJECT_ID = "ircbot-474408"  
LOCATION = "us-east4"         
DISPLAY_NAME = "test_corpus"  

FILE_PATHS = [
    "https://drive.google.com/file/d/1mKmwe3SMYiifcTAkoluoVBjcsGlpwLCO",
    "https://drive.google.com/file/d/1KY18fdKUw8lIXqesDgbFIQ4JULFwOV56",
    "https://drive.google.com/file/d/1wW_ENKZWikwjfCVbVKg-jBqbRKpEGI0m",
    "https://drive.google.com/file/d/158RvJJDjFxM4rqvYfvP2oGcqRtnKe0Tl",
    "https://drive.google.com/file/d/1SnKzxv3yjxIIm6KXotxu2Q6cBHOlFU98",
    "https://drive.google.com/file/d/12TvPdhOK8c2Z1kGF-nlQtPsaydtUCjMk"
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

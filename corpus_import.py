from google.cloud import aiplatform
from vertexai import rag
from vertexai.generative_models import GenerativeModel, Tool
import vertexai

# Create a RAG Corpus, Import Files, and Generate a response

# TODO(developer): Update and un-comment below lines
PROJECT_ID = "ircbot-474408"
display_name = "test_corpus"
paths = [
    "https://drive.google.com/file/d/1mKmwe3SMYiifcTAkoluoVBjcsGlpwLCO"]
#     ,
#     "https://drive.google.com/file/d/1KY18fdKUw8lIXqesDgbFIQ4JULFwOV56",
#     "https://drive.google.com/file/d/1wW_ENKZWikwjfCVbVKg-jBqbRKpEGI0m",
#     "https://drive.google.com/file/d/158RvJJDjFxM4rqvYfvP2oGcqRtnKe0Tl",
#     "https://drive.google.com/file/d/1SnKzxv3yjxIIm6KXotxu2Q6cBHOlFU98",
#     "https://drive.google.com/file/d/12TvPdhOK8c2Z1kGF-nlQtPsaydtUCjMk"
# ]
# Initialize Vertex AI API once per session
vertexai.init(project=PROJECT_ID, location="us-east4")

# Create RagCorpus
# Configure embedding model, for example "text-embedding-005".
embedding_model_config = rag.RagEmbeddingModelConfig(
    vertex_prediction_endpoint=rag.VertexPredictionEndpoint(
        publisher_model="publishers/google/models/text-embedding-005"
    )
)

rag_corpus = rag.create_corpus(
    display_name=display_name,
    backend_config=rag.RagVectorDbConfig(
        rag_embedding_model_config=embedding_model_config
    ),
)

# Import Files to the RagCorpus
rag.import_files(
    rag_corpus.name,
    paths,
    # Optional
    transformation_config=rag.TransformationConfig(
        chunking_config=rag.ChunkingConfig(
            chunk_size=512,
            chunk_overlap=100,
        ),
    ),
    max_embedding_requests_per_min=1000,  # Optional
)

# Direct context retrieval
rag_retrieval_config = rag.RagRetrievalConfig(
    top_k=3,  # Optional
    filter=rag.Filter(vector_distance_threshold=0.5),  # Optional
)
response = rag.retrieval_query(
    rag_resources=[
        rag.RagResource(
            rag_corpus=rag_corpus.name,
            # Optional: supply IDs from `rag.list_files()`.
            # rag_file_ids=["rag-file-1", "rag-file-2", ...],
        )
    ],
    text="What is the scope of STANDARD SPECIFICATIONS AND CODE OF PRACTICE FOR ROAD BRIDGES",
    rag_retrieval_config=rag_retrieval_config,
)
print(response)

# Enhance generation
# Create a RAG retrieval tool
rag_retrieval_tool = Tool.from_retrieval(
    retrieval=rag.Retrieval(
        source=rag.VertexRagStore(
            rag_resources=[
                rag.RagResource(
                    rag_corpus=rag_corpus.name,  # Currently only 1 corpus is allowed.
                    # Optional: supply IDs from `rag.list_files()`.
                    # rag_file_ids=["rag-file-1", "rag-file-2", ...],
                )
            ],
            rag_retrieval_config=rag_retrieval_config,
        ),
    )
)

# Create a Gemini model instance
rag_model = GenerativeModel(
    model_name="gemini-2.0-flash-001", tools=[rag_retrieval_tool]
)

# Generate response
text="What is the scope of STANDARD SPECIFICATIONS AND CODE OF PRACTICE FOR ROAD BRIDGES"
   
response = rag_model.generate_content(text)
print(response.text)
# Example response:
#   RAG stands for Retrieval-Augmented Generation.
#   It's a technique used in AI to enhance the quality of responses
# ...
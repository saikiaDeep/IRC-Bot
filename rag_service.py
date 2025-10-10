from google.cloud import aiplatform
from vertexai import rag
from vertexai.generative_models import GenerativeModel, Tool
import vertexai

PROJECT_ID = "ircbot-474408"
LOCATION = "us-east4"
CORPUS_DISPLAY_NAME = "ircbot_corpus_first"

vertexai.init(project=PROJECT_ID, location=LOCATION)

DEFAULT_SYSTEM_PROMPT = (
    "You are an expert assistant for Indian Road Congress (IRC) documents. "
    "Your primary goal is to provide accurate and concise answers based only on the "
    "context retrieved from the IRC corpus. If the retrieved context does not "
    "contain the answer, state clearly that you cannot find the information in the documents. "
    "Do not use external knowledge or fabricate information."
)

def get_rag_corpus():
    corpora = list(rag.list_corpora())
    for corpus in corpora:
        if corpus.display_name == CORPUS_DISPLAY_NAME:
            return corpus
    embedding_model_config = rag.RagEmbeddingModelConfig(
        vertex_prediction_endpoint=rag.VertexPredictionEndpoint(
            publisher_model="publishers/google/models/text-embedding-005"
        )
    )
    corpus = rag.create_corpus(
        display_name=CORPUS_DISPLAY_NAME,
        backend_config=rag.RagVectorDbConfig(
            rag_embedding_model_config=embedding_model_config
        ),
    )
    return corpus

def init_rag_pipeline():
    corpus = get_rag_corpus()
    retrieval_config = rag.RagRetrievalConfig(
        top_k=3,
        filter=rag.Filter(vector_distance_threshold=0.5),
    )

    retrieval_tool = Tool.from_retrieval(
        retrieval=rag.Retrieval(
            source=rag.VertexRagStore(
                rag_resources=[rag.RagResource(rag_corpus=corpus.name)],
                rag_retrieval_config=retrieval_config,
            )
        )
    )

    model = GenerativeModel(
        model_name="gemini-2.0-flash-001",
        tools=[retrieval_tool],
        system_instruction=DEFAULT_SYSTEM_PROMPT
    )
    return model

rag_model = init_rag_pipeline()


def query_rag(prompt: str) -> str:
    response = rag_model.generate_content(prompt)
    return response.text
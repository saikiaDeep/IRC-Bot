from vertexai import rag
import vertexai

PROJECT_ID = "ircbot-474408"  
LOCATION = "us-east4"        

vertexai.init(project=PROJECT_ID, location=LOCATION)

def list_all_rag_corpora():
    """Lists all RAG corpora in the current project/location."""
    print(f"--- Listing Corpora for Project: {PROJECT_ID}, Location: {LOCATION} ---")
    
    # rag.list_corpora() returns a list-like iterable
    try:
        corpora_list = list(rag.list_corpora()) 
        
        if not corpora_list:
            print("No RAG corpora found.")
            return

        for corpus in corpora_list:
            print("=" * 40)
            print(f"Display Name: {corpus.display_name}")
            # The full resource name is essential for API calls
            print(f"Resource Name: {corpus.name}") 
            # You can also access other properties like creation time, etc.
            # print(f"Creation Time: {corpus.create_time}")

    except Exception as e:
        print(f"An error occurred while listing corpora: {e}")

list_all_rag_corpora()
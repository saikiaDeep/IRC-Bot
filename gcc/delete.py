from vertexai import rag
import vertexai

# --- Configuration ---
PROJECT_ID = "ircbot-474408"  
LOCATION = "us-east4"         
# ---------------------

vertexai.init(project=PROJECT_ID, location=LOCATION)

def delete_all_rag_corpora(project_id: str, location: str):
    """
    Lists all RAG corpora in the given project/location and deletes them one by one.
    """
    print(f"Starting deletion process for all corpora in project: {project_id}, location: {location}...")
    
    try:
        # 1. List all corpora
        corpora_pager = rag.list_corpora()
        corpora_to_delete = list(corpora_pager)
        
        if not corpora_to_delete:
            print("✅ No RAG corpora found to delete.")
            return

        print(f"Found {len(corpora_to_delete)} corpus/corpora to delete.")

        # 2. Loop through and delete each corpus
        for corpus in corpora_to_delete:
            corpus_name = corpus.name
            display_name = corpus.display_name
            
            print(f"--- Deleting Corpus: '{display_name}' ({corpus_name}) ---")
            
            # Call the delete API
            rag.delete_corpus(name=corpus_name)
            
            # Note: delete_corpus is an asynchronous operation, 
            # but the SDK call usually returns quickly.
            print(f"✅ Delete request submitted for: {display_name}")

        print("\nAll delete requests have been submitted.")
        print("Corpora will be fully deleted shortly.")

    except Exception as e:
        print(f"\n❌ An error occurred during the deletion process: {e}")
        print("Please check IAM permissions (you need 'aiplatform.ragcorpora.delete') and ensure no import or retrieval operations are currently running.")

# Execute the deletion function
delete_all_rag_corpora(PROJECT_ID, LOCATION)
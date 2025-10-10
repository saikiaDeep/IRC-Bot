import vertexai
from vertexai import rag
from google.cloud import aiplatform
import pprint

PROJECT_ID = "ircbot-474408"
LOCATION = "us-east4"
CORPUS_DISPLAY_NAME = "ircbot_corpus_first"

vertexai.init(project=PROJECT_ID, location=LOCATION)

def check_corpus_and_files():
    print("[STEP] listing all corpora...")
    corpora = list(rag.list_corpora())
    print(f"[INFO] total corpora: {len(corpora)}")
    for c in corpora:
        print(" - display_name:", c.display_name, " resource_name:", c.name)

    target = next((c for c in corpora if c.display_name == CORPUS_DISPLAY_NAME), None)
    if not target:
        print(f"[ERROR] Corpus with display_name='{CORPUS_DISPLAY_NAME}' not found.")
        return None

    print(f"[INFO] Found corpus: {target.display_name} -> {target.name}")
    print("[STEP] Listing files inside corpus...")
    # note: sample uses rag.list_files(corpus_name=corpus_name)
    files = rag.list_files(corpus_name=target.name)
    files = list(files)  # iterate fully to print
    print(f"[INFO] number of files in corpus: {len(files)}")
    for f in files:
        # print fields that are commonly available: display_name, name, create_time, file_status, user_metadata
        print("----")
        print("display_name:", getattr(f, "display_name", None))
        print("resource_name:", getattr(f, "name", None))
        print("create_time:", getattr(f, "create_time", None))
        print("file_status:", getattr(f, "file_status", None))
        print("user_metadata:", getattr(f, "user_metadata", None))
    return target, files

if __name__ == "__main__":
    check_corpus_and_files()

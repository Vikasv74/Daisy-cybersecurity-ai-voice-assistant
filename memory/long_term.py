import chromadb
from chromadb.config import Settings
import os

class DaisyMemory:
    def __init__(self, storage_directory="./memory/chroma_db"):
        # Ensure the directory path exists
        if not os.path.exists(storage_directory):
            os.makedirs(storage_directory)
            
        # Initialize the persistent local database client
        self.client = chromadb.PersistentClient(path=storage_directory)
        # Create or fetch a collection to hold security context logs
        self.collection = self.client.get_or_create_collection(name="daisy_context")

    def store_memory(self, memory_id, text, metadata=None):
        """Saves a string or log event into Daisy's long-term vector database."""
        print(f"[Daisy Memory] Saving knowledge context for ID: '{memory_id}'...")
        self.collection.add(
            documents=[text],
            metadatas=[metadata if metadata else {"type": "general"}],
            ids=[memory_id]
        )
        return "Memory successfully stored."

    def recall_relevant_memory(self, query_text, results_count=1):
        """Searches the database for the most contextually relevant past logs."""
        print(f"[Daisy Memory] Querying long-term memory for: '{query_text}'...")
        results = self.collection.query(
            query_texts=[query_text],
            n_results=results_count
        )
        return results['documents'][0] if results['documents'] else []

if __name__ == "__main__":
    # Test Daisy's memory module standalone
    memory_bank = DaisyMemory()
    
    # Store a test sample context
    memory_bank.store_memory(
        "incident_01", 
        "Detected unauthorized root access attempt from external IP 192.168.1.55 on port 22.",
        {"severity": "high"}
    )
    
    # Try asking Daisy to remember it based on a keyword phrase
    recalled = memory_bank.recall_relevant_memory("Tell me about recent IP threats")
    print(f"\n[Daisy Recalled Context]: {recalled}")

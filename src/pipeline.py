# /src/pipeline.py

from gutenbergpy.gutenbergcache import GutenbergCache
import os 
from gutenbergpy.textget import get_text_by_id, strip_headers

CACHE_FILE_PATH = os.path.join(os.path.expanduser('~'), '.gutenbergpy_cache.db') #Default location

def create_data_dir():
    """Creates the necessary /data directory if it doesn't exist."""
    os.makedirs('data', exist_ok=True)
    print("Data directory ensured.")

def initialize_gutenberg_cache():
    """
    Creates and populates the local Project Gutenberg metadata cache.
    This step is resource-intensive and must be run ONCE. 
    """
    if os.path.exists(CACHE_FILE_PATH):
        print("Gutenberg cache already exists. Skipping initialization.")
        return
    print("Initializing Gutenberg cache. This may take a while...")
    try: 
        #Create the SQLite cache file (downloads metadata RDF and parses it)
        #Using default settings (SQLite in user's home directory)
        GutenbergCache.create()
        print("Gutenberg cache created successfully.")
    except Exception as e:
        print(f"Error initializing Gutenberg cache: {e}")
        print("Please ensure you have adequate disk space and a stable interent connection. ")

# List of well-known large English books (or query the cache for many)
# ID 2701: Moby Dick, 84: Frankenstein, 11: Alice in Wonderland
# NOTE: In a real project, you would query the cache:
# cache = GutenbergCache.get_cache()
# english_books = cache.query(languages=['en']) 
# Then filter the IDs by book size or author diversity.
BOOK_IDS = [2701, 84, 1342, 11, 100] # Use a few known large IDs for demonstration

def fetch_and_prepare_corpus(book_ids: list, output_path: str) -> str:
    """
    Fetches raw text for specified IDs, cleans headers/footers,
    normalizes the text for character-level model, and saves the final corpus.
    """
    full_corpus = []

    print(f"\nFetching and cleaning {len(book_ids)} books...")
    for book_id in book_ids:
        try:
            # 1. Download the raw text (handles HTTP request)
            raw_book = get_text_by_id(book_id)
            
            # 2. Clean the boilerplate text (GutenbergPy strips headers/footers)
            clean_book_bytes = strip_headers(raw_book)
            
            # 3. Decode to string and convert to lowercase for the character model
            clean_book_str = clean_book_bytes.decode('utf-8').lower()
            
            # 4. Normalize whitespace (Replace multiple spaces/tabs/newlines with a single space)
            # This is a critical step for consistent character input
            normalized_text = ' '.join(clean_book_str.split()) 
            
            full_corpus.append(normalized_text)
            print(f"  -> Processed Book ID {book_id} successfully.")
        except Exception as e:
            print(f"  -> Failed to process Book ID {book_id}: {e}")

    final_corpus = "\n\n".join(full_corpus) # Join books with a marker
    
    # Save the final single raw corpus file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_corpus)
        
    print(f"\nFinal corpus created and saved to {output_path}. Length: {len(final_corpus)} characters.")
    return final_corpus

# Example usage in run_experiment.py
CORPUS_PATH = os.path.join("data", "gutenberg_full_corpus.txt")
final_corpus_string = fetch_and_prepare_corpus(BOOK_IDS, CORPUS_PATH)
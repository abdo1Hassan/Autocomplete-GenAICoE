import pandas as pd
import re
from nltk.corpus import words
import nltk

# Download English words list (one-time)
nltk.download('words')

# Load known English words
english_vocab = set(word.lower() for word in words.words())

def is_valid_query(query):
    # Lowercase and strip
    query = query.lower().strip()

    # Reject very short or empty queries
    if len(query) < 3 or not re.search(r"[a-z]", query):
        return False

    # Tokenize by words
    tokens = re.findall(r'\b[a-z]{2,}\b', query)  # ignore single letters

    if not tokens:
        return False

    # Count how many words are valid English words
    valid_count = sum(1 for token in tokens if token in english_vocab)

    # Heuristic: at least half of the words should be valid
    return valid_count >= max(1, len(tokens) // 2)

# === USAGE ===

# Load dataset
df = pd.read_csv("query.csv")

# Clean it
df_clean = df[df['Search Query'].apply(is_valid_query)]

# Save cleaned data
df_clean.to_csv("cleaned_queries.csv", index=False)

print(f"✅ Done. Kept {len(df_clean)} out of {len(df)} queries.")

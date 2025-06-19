import pandas as pd

# Load the CSV file
df = pd.read_csv('merged_queries_with_tag.csv')

# Remove rows where Search Query is 3 characters or less (after stripping whitespace)
df = df[df['Search Query'].str.strip().str.len() > 3]

# Save it back
df.to_csv('merged_queries_with_tag_cleaned.csv', index=False)

print("✅ Cleaned CSV saved as merged_queries_with_tag_cleaned.csv")

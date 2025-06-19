from trie.trie import Trie
from fuzzy_matching.fuzzy_matcher import FuzzyMatcher
from embeddings.embedding_model import EmbeddingModel
from utils.file_processor import load_queries
from interface.ui import UserInterface
from utils.logger import setup_logger
from flask import Flask, request, jsonify
from flask_cors import CORS
import time

logger = setup_logger(__name__)

app = Flask(__name__)
CORS(app)  # Temporarily allow all origins for testing

@app.route('/autocomplete', methods=['POST'])
def autocomplete():
    logger.debug("Received request for autocomplete")
    data = request.json
    logger.debug(f"Request data: {data}")
    prefix = data.get('prefix', '')

    # Get suggestions from trie
    suggestions = trie.autocomplete(prefix)
    logger.debug(f"Suggestions from trie: {suggestions}")

    # If not enough suggestions, use fuzzy matching
    if len(suggestions) < 3:
        fuzzy_suggestions = fuzzy_matcher.match(prefix)
        suggestions.extend(fuzzy_suggestions)
        logger.debug(f"Fuzzy suggestions: {fuzzy_suggestions}")

    # Combine and rank suggestions
    combined_suggestions = list(set(suggestions))
    combined_suggestions = sorted(combined_suggestions, key=lambda x: (len(x), x))[:3]
    logger.debug(f"Combined suggestions: {combined_suggestions}")

    # Return suggestions as JSON
    return jsonify({
        'suggestions': combined_suggestions
    })

def main():
    logger.info("Starting the autocomplete system...")
    try:
        # Load queries from the CSV file
        logger.debug("Loading data from query.csv...")
        queries = load_queries('data/query.csv')
        logger.debug("Data loaded successfully.")

        # Initialize components
        logger.debug("Initializing components...")
        global trie, fuzzy_matcher, embedding_model
        trie = Trie()
        fuzzy_matcher = FuzzyMatcher(queries)
        embedding_model = EmbeddingModel()
        logger.debug("Components initialized successfully.")

        # Insert queries into the trie
        logger.debug("Inserting queries into the trie...")
        for query in queries:
            trie.insert(query)
        logger.debug("Queries inserted successfully.")

        # Log the contents of the trie for debugging
        logger.debug("Contents of the trie:")
        logger.debug(trie.get_all_words())

        # Generate embeddings for the queries
        logger.debug("Generating embeddings for the queries...")
        embeddings = embedding_model.generate_embeddings(queries)
        logger.debug("Embeddings generated successfully.")

        # Initialize the user interface
        logger.debug("Initializing the user interface...")
        ui = UserInterface()
        logger.debug("User interface initialized successfully.")

        # Real-time input and suggestion display
        for prefix, start_time in ui.get_user_input():
            logger.debug(f"Getting suggestions for prefix: {prefix}")
            suggestions = trie.autocomplete(prefix)
            logger.debug(f"Suggestions from trie: {suggestions}")

            # If not enough suggestions, use fuzzy matching
            if len(suggestions) < 3:
                logger.debug("Not enough suggestions, using fuzzy matching...")
                fuzzy_suggestions = fuzzy_matcher.match(prefix)
                suggestions.extend(fuzzy_suggestions)
                logger.debug(f"Fuzzy suggestions: {fuzzy_suggestions}")

            # Combine and rank suggestions
            combined_suggestions = list(set(suggestions))
            combined_suggestions = sorted(combined_suggestions, key=lambda x: (len(x), x))[:3]

            # Calculate latency and confidence scores
            latency = (time.time() - start_time) * 1000  # Convert to milliseconds
            confidence_scores = [0.9, 0.7, 0.5]  # Placeholder confidence scores

            # Display suggestions with latency and confidence
            ui.display_suggestions(combined_suggestions, latency, confidence_scores)

    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)

if __name__ == "__main__":
    main()
    app.run(host='0.0.0.0', port=5000)
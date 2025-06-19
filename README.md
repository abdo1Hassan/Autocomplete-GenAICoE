# Autocomplete System

This project implements an intelligent autocomplete system that processes a dataset of search queries to provide real-time, context-aware suggestions. The system combines prefix trie, fuzzy matching, and embedding-based similarity to generate the top 3 autocomplete suggestions for a given input.

## Features
- **Prefix Trie**: Efficient storage and retrieval of queries based on prefixes.
- **Fuzzy Matching**: Handles typos and provides suggestions for misspelled inputs.
- **Embedding-Based Similarity**: Ranks queries based on semantic relevance.
- **Real-Time Suggestions**: Displays suggestions dynamically as the user types.
- **Decathlon-Themed UI**: A modern, user-friendly interface styled with Decathlon branding.

## Prerequisites
- Python 3.10 or higher
- Node.js and npm
- macOS or a compatible operating system

## Setup Instructions

### Backend
1. Navigate to the project directory:
   ```bash
   cd /Users/mac-AHASSA15/Documents/autocomplete-system
   ```
2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the backend server:
   ```bash
   python src/mock_api.py
   ```
   The backend will run on `http://localhost:5001`.

### Frontend
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install the required Node.js dependencies:
   ```bash
   npm install
   ```
3. Start the frontend development server:
   ```bash
   npm run dev
   ```
   The frontend will run on `http://localhost:5173`.

## Usage
1. Open the frontend in your browser at `http://localhost:5173`.
2. Start typing in the search bar to see real-time autocomplete suggestions.
3. Suggestions will include latency information for each query.

## Technical Overview
- **Backend**: Built with FastAPI, the backend serves autocomplete suggestions using trie, fuzzy matching, and embeddings.
- **Frontend**: Built with React, the frontend provides a dynamic and responsive user interface.
- **Data**: The system processes queries from `data/query.csv`.

## Future Enhancements
- Improve ranking algorithms for better suggestion quality.
- Add support for multilingual queries.
- Optimize performance for large datasets.
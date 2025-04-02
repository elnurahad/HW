import logging
from typing import List, Set, Tuple

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='search_engine.log'
)

STOP_WORDS: Set[str] = {
    "a", "about", "above", "after", "again", "against", "all",
    "am", "an", "and", "any", "are", "aren't", "as", "at",
    "be", "because", "been", "before", "being", "below",
    "between", "both", "but", "by", "can't", "cannot",
    "could", "couldn't", "did", "didn't", "do", "does",
    "doesn't", "doing", "don't", "down", "during", "each",
    "few", "for", "from", "further", "had", "hadn't", "has",
    "hasn't", "have", "haven't", "he", "he'd", "he'll",
    "he's", "her", "here", "here's", "hers", "herself",
    "him", "himself", "his", "how", "i", "i'd", "i'll",
    "i'm", "i've", "if", "in", "into", "is", "isn't",
    "it", "it's", "its", "itself", "just", "ll", "ma",
    "more", "most", "mustn't", "my", "myself", "needn't",
    "no", "nor", "not", "of", "off", "on", "once",
    "only", "or", "other", "our", "ours", "ourselves",
    "out", "over", "own", "re", "s", "same", "shan't",
    "she", "she'd", "she'll", "she's", "should", "shouldn't",
    "so", "some", "such", "t", "than", "that", "that's",
    "the", "their", "theirs", "them", "themselves", "then",
    "there", "there's", "these", "they", "they'd", "they'll",
    "they're", "they've", "this", "those", "through",
    "to", "too", "under", "until", "up", "ve", "very",
    "was", "wasn't", "we", "we'd", "we'll", "we're",
    "we've", "were", "weren't", "what", "what's", "when",
    "where", "where's", "which", "while", "who", "who's",
    "whom", "why", "will", "with", "won't", "would",
    "wouldn't", "you", "you'd", "you'll", "you're",
    "you've", "your", "yours", "yourself", "yourselves"
}


def split_words(text: str) -> List[str]:
    return text.lower().split()


def parse_query(text: str, stop_words: Set[str]) -> Set[str]:
    words = split_words(text)
    return {word for word in words if word not in stop_words}


def match_document(document_words: Set[str], query_words: Set[str]) -> int:
    return len(document_words.intersection(query_words))


def find_documents(
    documents: List[Tuple[int, Set[str]]],
    stop_words: Set[str],
    query: str
) -> List[Tuple[int, int]]:
    query_no_stop_words = parse_query(query, stop_words)
    results = []
    for doc_id, document in documents:
        relevance = match_document(document, query_no_stop_words)
        results.append((doc_id, relevance))
    results.sort(key=lambda x: x[1], reverse=True)
    logging.info(f"Search completed for query: {query}")
    return results

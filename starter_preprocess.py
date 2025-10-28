"""
starter_preprocess.py
Starter code for text preprocessing - focus on the statistics, not the regex!

This is the same code you'll use in the main Shannon assignment next week.
"""

import re
import json
import requests
from typing import List, Dict, Tuple
from collections import Counter
import string
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
nltk.download('punkt_tab')


class TextPreprocessor:
    """Handles all the annoying text cleaning so you can focus on the fun stuff"""

    def __init__(self):
        # Gutenberg markers (these are common, add more if needed)
        self.gutenberg_markers = [
            "*** START OF THIS PROJECT GUTENBERG",
            "*** END OF THIS PROJECT GUTENBERG",
            "*** START OF THE PROJECT GUTENBERG",
            "*** END OF THE PROJECT GUTENBERG",
            "*END*THE SMALL PRINT",
            "<<THIS ELECTRONIC VERSION"
        ]

    def clean_gutenberg_text(self, raw_text: str) -> str:
        """
        Removes Project Gutenberg headers/footers using regex to find
        the 'START OF' and 'END OF' markers.
        """

        # --- REPLACEMENT LOGIC ---
        # The original line-by-line logic fails for many books.
        # This regex logic searches the whole text at once.

        # 1. Define the markers
        # re.IGNORECASE = not case-sensitive
        # re.DOTALL = '.' matches newline characters
        start_marker = r"\*\*\*\s*START OF .*?\*\*\*"
        end_marker = r"\*\*\*\s*END OF .*?\*\*\*"

        # 2. Search for markers in the raw text
        start_match = re.search(start_marker, raw_text,
                                re.IGNORECASE | re.DOTALL)
        end_match = re.search(end_marker, raw_text, re.IGNORECASE | re.DOTALL)

        # 3. Find the start and end character positions
        start_index = 0
        end_index = len(raw_text)

        if start_match:
            start_index = start_match.end()  # Get the index *after* the marker
        else:
            print(
                "Warning: No '*** START OF' marker found. Cleaning may be less accurate.")

        if end_match:
            end_index = end_match.start()  # Get the index *before* the marker
        else:
            print("Warning: No '*** END OF' marker found. Cleaning may be less accurate.")

        # 4. Slice the text to get only the book content
        cleaned = raw_text[start_index:end_index]

        # --- END OF REPLACEMENT LOGIC ---

        # 5. Also remove any [Illustration: ...] tags
        cleaned = re.sub(r'\[Illustration:.*?\]', '',
                         cleaned, flags=re.IGNORECASE | re.DOTALL)

        # 6. Keep your original whitespace cleaning logic
        cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
        cleaned = re.sub(r' {2,}', ' ', cleaned)

        return cleaned.strip()

    def normalize_text(self, text: str) -> str:
        """
        Normalizes text: lowercase, replaces newlines/tabs with spaces, 
        and removes all non-alphanumeric/non-space characters.
        """
        # 1. Replace newlines and tabs with a single space
        text = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')

        # 2. Convert to lowercase
        text = text.lower()

        # 3. Keep only letters, numbers, and spaces
        cleaned_chars = (
            char for char in text if char.isalnum() or char == ' '
        )

        # 4. Re-join and collapse multiple spaces into one
        cleaned_text = "".join(cleaned_chars)
        # This collapses "hello    world" into "hello world"
        return " ".join(cleaned_text.split())

    def tokenize_sentences(self, text: str) -> list[str]:
        """
        Splits text into a list of sentences using NLTK.
        """
        try:
            return sent_tokenize(text)
        except LookupError:
            # This handles if 'punkt' isn't downloaded
            print("NLTK 'punkt' tokenizer not found. Downloading...")
            nltk.download('punkt')
            return sent_tokenize(text)

    def tokenize_words(self, text: str) -> list[str]:
        """
        Splits text into a list of words using NLTK.
        """
        try:
            return word_tokenize(text)
        except LookupError:
            print("NLTK 'punkt' tokenizer not found. Downloading...")
            nltk.download('punkt')
            return word_tokenize(text)

    def tokenize_chars(self, text: str, include_space: bool = True) -> List[str]:
        """Split text into characters"""
        if include_space:
            # Replace multiple spaces with single space
            text = re.sub(r'\s+', ' ', text)
            return list(text)
        else:
            return [c for c in text if c != ' ']

    def get_sentence_lengths(self, sentences: List[str]) -> List[int]:
        """Get word count for each sentence"""
        return [len(self.tokenize_words(sent)) for sent in sentences]

    # TODO: Implement these methods for the warm-up assignment

    import requests
# ... inside the TextPreprocessor class ...

    def fetch_from_url(self, url: str) -> str:
        """
        Fetch text content from a URL (especially Project Gutenberg).
        Raises: Exception if URL is invalid or cannot be reached.
        """
        # 1. Validate that it's a .txt URL
        if not url.lower().endswith('.txt'):
            raise Exception(f"URL must point to a .txt file: {url}")

        # 2. Fetch the content
        try:
            response = requests.get(url, timeout=10)
            # Raise an HTTPError if the status code is 4XX or 5XX
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            # Catch all requests-related exceptions (connection, timeout, HTTP error, etc.)
            raise Exception(f"Failed to fetch content from URL: {e}")

    def get_text_statistics(self, text: str) -> Dict:
        """
        Calculates basic statistics about the text.
        Assumes 'text' is cleaned (e.g., Gutenberg headers removed)
        but NOT normalized (still has punctuation and casing).
        """

        # 1. Stats from original cleaned text
        total_characters = len(text)
        sentences = self.tokenize_sentences(text)  # Uses NLTK
        total_sentences = len(sentences)

        # 2. Normalize text for word-based stats
        normalized_text = self.normalize_text(text)
        raw_words = self.tokenize_words(normalized_text)  # NLTK on normalized

        # 3. Clean words
        cleaned_words = [
            word for word in raw_words if word.isalnum() and len(word) > 1
        ]

        total_words = len(cleaned_words)
        total_word_char_length = sum(len(w) for w in cleaned_words)

        # 4. Averages
        avg_word_length = (
            total_word_char_length / total_words if total_words > 0 else 0
        )
        avg_sentence_length = (
            total_words / total_sentences if total_sentences > 0 else 0
        )

        # 5. Common words
        word_counts = Counter(cleaned_words)
        most_common_words_list = word_counts.most_common(10)

        return {
            "total_characters": total_characters,
            "total_words": total_words,
            "total_sentences": total_sentences,
            "avg_word_length": round(avg_word_length, 2),
            "avg_sentence_length": round(avg_sentence_length, 2),
            "most_common_words": dict(most_common_words_list)
        }

    def create_summary(self, text: str, num_sentences: int = 3) -> str:
        """
        Create a simple extractive summary by returning the first N sentences,
        with all newlines removed so it's a single line of text.
        """
        # 1. Get the first N sentences
        sentences = self.tokenize_sentences(text)
        summary_sentences = sentences[:num_sentences]

        cleaned_summary_sentences = []

        # 2. Clean each sentence
        for sent in summary_sentences:
            # Replace ANY whitespace character (\n, \t, ' ') with a single space
            cleaned_sent = re.sub(r'\s+', ' ', sent).strip()
            cleaned_summary_sentences.append(cleaned_sent)

        # 3. Join the *cleaned* sentences into one line
        return " ".join(cleaned_summary_sentences)


class FrequencyAnalyzer:
    """Calculate n-gram frequencies from tokenized text"""

    def calculate_ngrams(self, tokens: List[str], n: int) -> Dict[Tuple[str, ...], int]:
        """
        Calculate n-gram frequencies

        Args:
            tokens: List of tokens (words or characters)
            n: Size of n-gram (1=unigram, 2=bigram, 3=trigram)

        Returns:
            Dictionary mapping n-grams to their counts
        """
        if n == 1:
            # Special case for unigrams (return as single strings, not tuples)
            return dict(Counter(tokens))

        ngrams = []
        for i in range(len(tokens) - n + 1):
            ngram = tuple(tokens[i:i + n])
            ngrams.append(ngram)

        return dict(Counter(ngrams))

    def calculate_probabilities(self, ngram_counts: Dict, smoothing: float = 0.0) -> Dict:
        """
        Convert counts to probabilities

        Args:
            ngram_counts: Dictionary of n-gram counts
            smoothing: Laplace smoothing parameter (0 = no smoothing)
        """
        total = sum(ngram_counts.values()) + smoothing * len(ngram_counts)

        probabilities = {}
        for ngram, count in ngram_counts.items():
            probabilities[ngram] = (count + smoothing) / total

        return probabilities

    def save_frequencies(self, frequencies: Dict, filename: str):
        """Save frequency dictionary to JSON file"""
        # Convert tuples to strings for JSON serialization
        json_friendly = {}
        for key, value in frequencies.items():
            if isinstance(key, tuple):
                json_friendly['||'.join(key)] = value
            else:
                json_friendly[key] = value

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(json_friendly, f, indent=2, ensure_ascii=False)

    def load_frequencies(self, filename: str) -> Dict:
        """Load frequency dictionary from JSON file"""
        with open(filename, 'r', encoding='utf-8') as f:
            json_data = json.load(f)

        # Convert string keys back to tuples where needed
        frequencies = {}
        for key, value in json_data.items():
            if '||' in key:
                frequencies[tuple(key.split('||'))] = value
            else:
                frequencies[key] = value

        return frequencies


# Example usage to test your setup
if __name__ == "__main__":
    # Test with a small example
    sample_text = """
    This is a test. This is only a test! 
    If this were a real emergency, you would be informed.
    """

    preprocessor = TextPreprocessor()
    analyzer = FrequencyAnalyzer()

    # Clean and normalize
    clean_text = preprocessor.normalize_text(sample_text)
    print(f"Cleaned text: {clean_text}\n")

    # Get sentences
    sentences = preprocessor.tokenize_sentences(clean_text)
    print(f"Sentences: {sentences}\n")

    # Get words
    words = preprocessor.tokenize_words(clean_text)
    print(f"Words: {words}\n")

    # Calculate bigrams
    bigrams = analyzer.calculate_ngrams(words, 2)
    print(f"Word bigrams: {bigrams}\n")

    # Calculate character trigrams
    chars = preprocessor.tokenize_chars(clean_text)
    char_trigrams = analyzer.calculate_ngrams(chars, 3)
    print(
        f"Character trigrams (first 5): {dict(list(char_trigrams.items())[:5])}")

    print("\n✅ Basic functionality working!")
    print("Now implement the TODO methods for your assignment!")

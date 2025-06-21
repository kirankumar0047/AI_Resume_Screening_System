import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string

nltk.download('punkt')
nltk.download('stopwords')

def preprocess_jd(text):
    # Lowercase and tokenize
    text = text.lower()
    tokens = word_tokenize(text)

    # Remove stopwords and punctuation
    stop_words = set(stopwords.words('english'))
    words = [
        word for word in tokens
        if word.isalpha() and word not in stop_words and len(word) > 2
    ]

    # Remove duplicates (optional)
    unique_words = list(dict.fromkeys(words))

    return ' '.join(unique_words)
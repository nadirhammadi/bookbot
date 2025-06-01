# stats.py
import json
import csv
from collections import defaultdict
import math
try:
    from textblob import TextBlob
    from langdetect import detect
except ImportError:
    pass  # Gestion élégante des dépendances optionnelles

# ======================
# FONCTIONS FONDAMENTALES
# ======================
# stats.py

def get_book_text(file_path):
    """
    Reads the content of a book from a text file.

    Args:
        file_path (str): The path to the text file containing the book.

    Returns:
        str: The content of the book.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def count_words(text):
    """Compte le nombre total de mots dans le texte (version optimisée)"""
    return len(text.split())

def count_characters(text, case_sensitive=False):
    """
    Compte les occurrences de chaque caractère
    
    Args:
        case_sensitive (bool): Si True, différencie majuscules/minuscules
    """
    char_count = defaultdict(int)
    for char in text:
        if not case_sensitive:
            char = char.lower()
        char_count[char] += 1
    return dict(char_count)

def sort_characters(characters):
    """Trie les caractères par fréquence décroissante puis alphabétiquement"""
    return sorted(characters.items(), key=lambda x: (-x[1], x[0]))

# ======================
# ANALYSE AVANCÉE
# ======================

def get_keyword_frequency(text, top_n=20, exclude_common=True):
    """
    Analyse la fréquence des mots en excluant les mots courants
    
    Args:
        exclude_common (bool): Exclure les mots courants (the, and, etc.)
    """
    common_words = {"the", "and", "to", "of", "a", "in", "that", "it", "with", "as", "for", "was", "on", "he", "is", "at", "his", "by", "be", "this"}
    words = [word.lower() for word in text.split() if word.isalpha()]
    word_count = defaultdict(int)
    
    for word in words:
        if not (exclude_common and word in common_words):
            word_count[word] += 1
    
    return sorted(word_count.items(), key=lambda x: x[1], reverse=True)[:top_n]

def calculate_readability(text):
    """Calcule l'indice de lisibilité Flesch-Kincaid"""
    sentences = text.count('.') + text.count('!') + text.count('?')
    words = text.split()
    syllables = sum(count_syllables(word) for word in words)
    
    if not sentences or not words:
        return 0
    
    return 206.835 - 1.015 * (len(words)/sentences) - 84.6 * (syllables/len(words))

def count_syllables(word):
    """Estime le nombre de syllabes dans un mot (approximation)"""
    vowels = "aeiouy"
    word = word.lower().strip()
    count = 0
    last_was_vowel = False
    
    for char in word:
        if char in vowels:
            if not last_was_vowel:
                count += 1
            last_was_vowel = True
        else:
            last_was_vowel = False
    
    # Correction pour les mots se terminant par 'e'
    if word.endswith('e') and count > 1:
        count -= 1
    
    return max(1, count)  # Au moins une syllabe

def analyze_sentiment(text):
    """Analyse la polarité sentimentale du texte (-1 à +1)"""
    try:
        from textblob import TextBlob
        return TextBlob(text).sentiment.polarity
    except ImportError:
        print("Install textblob for sentiment analysis: pip install textblob")
        return 0

def detect_language(text):
    """Détecte la langue du texte"""
    try:
        from langdetect import detect
        return detect(text)
    except ImportError:
        print("Install langdetect for language detection: pip install langdetect")
        return "unknown"

# ======================
# VISUALISATION & EXPORT
# ======================

def plot_character_frequency(char_counts, filename='char_frequency.png'):
    """Génère un graphique des fréquences des caractères"""
    try:
        import matplotlib.pyplot as plt
        alphabetic = [(k, v) for k, v in char_counts.items() if k.isalpha()]
        sorted_chars = sorted(alphabetic, key=lambda x: x[1], reverse=True)
        chars, counts = zip(*sorted_chars)
        
        plt.figure(figsize=(12, 6))
        plt.bar(chars, counts, color='skyblue')
        plt.title('Character Frequency Distribution')
        plt.xlabel('Characters')
        plt.ylabel('Frequency')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.savefig(filename)
        plt.close()
        return True
    except ImportError:
        print("Install matplotlib for visualization: pip install matplotlib")
        return False

def plot_word_frequency(word_counts, filename='word_frequency.png', top_n=15):
    """Génère un graphique des fréquences des mots"""
    try:
        import matplotlib.pyplot as plt
        top_words = word_counts[:top_n]
        words, counts = zip(*top_words)
        
        plt.figure(figsize=(12, 8))
        plt.barh(words, counts, color='salmon')
        plt.title(f'Top {top_n} Most Frequent Words')
        plt.xlabel('Frequency')
        plt.ylabel('Words')
        plt.gca().invert_yaxis()  # Afficher le plus fréquent en haut
        plt.grid(axis='x', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig(filename)
        plt.close()
        return True
    except ImportError:
        print("Install matplotlib for visualization: pip install matplotlib")
        return False

def export_json(data, filename):
    """Exporte les données au format JSON"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def export_csv(data, filename):
    """Exporte les données au format CSV"""
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if isinstance(data, dict):
            writer.writerow(['Key', 'Value'])
            for key, value in data.items():
                writer.writerow([key, value])
        elif isinstance(data, list) and data:
            if isinstance(data[0], tuple):
                writer.writerow(['Item', 'Count'])
                writer.writerows(data)
            else:
                writer.writerow(['Items'])
                writer.writerows([[item] for item in data])

# ======================
# UTILITAIRES AVANCÉS
# ======================

def compare_books(book_data):
    """
    Compare plusieurs livres sur des métriques clés
    
    Args:
        book_data (list): Liste de tuples (nom, texte)
    
    Returns:
        dict: Résultats comparatifs
    """
    comparison = {}
    for name, text in book_data:
        comparison[name] = {
            'word_count': count_words(text),
            'unique_words': len(set(text.lower().split())),
            'readability': calculate_readability(text),
            'sentiment': analyze_sentiment(text),
            'language': detect_language(text)
        }
    return comparison

def get_text_metrics(text):
    """Retourne un ensemble complet de métriques pour un texte"""
    return {
        'word_count': count_words(text),
        'character_count': count_characters(text),
        'top_words': get_keyword_frequency(text),
        'readability': calculate_readability(text),
        'sentiment': analyze_sentiment(text),
        'language': detect_language(text),
        'unique_words': len(set(text.lower().split()))
    }

def analyze_large_file(file_path, chunk_size=10000):
    """Analyse de fichiers volumineux par morceaux"""
    metrics = {
        'word_count': 0,
        'character_count': defaultdict(int),
        'sentence_count': 0
    }
    
    with open(file_path, 'r', encoding='utf-8') as f:
        while chunk := f.read(chunk_size):
            metrics['word_count'] += count_words(chunk)
            metrics['sentence_count'] += chunk.count('.') + chunk.count('!') + chunk.count('?')
            
            # Comptage des caractères
            char_counts = count_characters(chunk)
            for char, count in char_counts.items():
                metrics['character_count'][char] += count
    
    # Conversion du compteur de caractères
    metrics['character_count'] = dict(metrics['character_count'])
    
    return metrics

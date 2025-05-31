# main.py
import csv
import sys
import argparse
from keyword import iskeyword
from stats import (
    get_book_text,
    count_words,
    count_characters,
    sort_characters,
    get_keyword_frequency,
    calculate_readability,
    analyze_sentiment,
    detect_language,
    plot_character_frequency,
    plot_word_frequency,
    export_json,
    export_csv,
    get_text_metrics,
    compare_books
)

def analyze_single_book(book_path, args):
    """Analyse un seul livre avec les options spécifiées"""
    try:
        book_text = get_book_text(book_path)
        metrics = get_text_metrics(book_text)
        
        # Affichage des résultats de base
        print(f"\n============ ANALYSE: {book_path} ============")
        print(f"📖 Langue détectée: {metrics['language']}")
        print(f"🔤 Nombre de mots: {metrics['word_count']}")
        print(f"📊 Lisibilité (Flesch-Kincaid): {metrics['readability']:.2f}")
        print(f"😊 Sentiment: {'Positif' if metrics['sentiment'] > 0 else 'Négatif' if metrics['sentiment'] < 0 else 'Neutre'} ({metrics['sentiment']:.2f})")
        
        # Analyse de caractères (option -c)
        if args.characters:
            char_counts = count_characters(book_text)
            sorted_chars = sort_characters(char_counts)
            print("\n🔠 FRÉQUENCE DES CARACTÈRES:")
            for char, count in sorted_chars:
                if char.isalpha():
                    print(f"{char}: {count}")
        
        # Mots clés (option -w)
        if args.words:
            top_words = metrics['top_words'][:args.top]
            print(f"\n🔑 TOP {args.top} MOTS-CLÉS:")
            for word, count in top_words:
                print(f"{word}: {count}")
        
        # Génération de graphiques (option -p)
        if args.plot:
            plot_character_frequency(char_counts, f"{book_path}_characters.png")
            plot_word_frequency(metrics['top_words'], f"{book_path}_words.png")
            print(f"\n📈 Graphiques générés: {book_path}_characters.png, {book_path}_words.png")
        
        # Export des données (option -e)
        if args.export:
            if 'json' in args.export:
                export_json(metrics, f"{book_path}_metrics.json")
            if 'csv' in args.export:
                export_csv(metrics['top_words'], f"{book_path}_top_words.csv")
                export_csv(
                    [(k, v) for k, v in metrics['character_count'].items() if k.isalpha()], 
                    f"{book_path}_characters.csv"
                )
            print(f"\n💾 Données exportées dans {book_path}_*.{{json,csv}}")
            
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse de {book_path}: {str(e)}")

def compare_multiple_books(book_paths, args):
    """Compare plusieurs livres et affiche les résultats"""
    book_data = []
    for path in book_paths:
        try:
            book_data.append((path, get_book_text(path)))
        except Exception as e:
            print(f"⚠️ Impossible de lire {path}: {str(e)}")
    
    if len(book_data) < 2:
        print("❌ Fournissez au moins 2 livres valides pour la comparaison")
        return
    
    comparison = compare_books(book_data)
    
    # Affichage tableau comparatif
    print("\n📊 COMPARAISON DE LIVRES")
    print(f"{'Livre':<30} | {'Mots':>8} | {'Mots uniques':>12} | {'Lisibilité':>10} | {'Sentiment':>9}")
    print("-" * 80)
    for book, data in comparison.items():
        print(f"{book:<30} | {data['word_count']:>8} | {data['unique_words']:>12} | {data['readability']:>10.2f} | {data['sentiment']:>9.2f}")
    
    # Export des résultats
    if args.export:
        if 'json' in args.export:
            export_json(comparison, "books_comparison.json")
        if 'csv' in args.export:
            with open("books_comparison.csv", "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Livre", "Mots", "Mots uniques", "Lisibilité", "Sentiment"])
                for book, data in comparison.items():
                    writer.writerow([book, data['word_count'], data['unique_words'], data['readability'], data['sentiment']])
        print("\n💾 Comparaison exportée dans books_comparison.{json,csv}")

def main():
    parser = argparse.ArgumentParser(
        description="BookBot - Suite avancée d'analyse littéraire",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        'books', 
        nargs='+',
        help="Fichier(s) texte à analyser"
    )
    parser.add_argument(
        '-c', '--characters',
        action='store_true',
        help="Afficher la fréquence des caractères"
    )
    parser.add_argument(
        '-w', '--words',
        action='store_true',
        help="Afficher les mots-clés les plus fréquents"
    )
    parser.add_argument(
        '-t', '--top',
        type=int,
        default=15,
        help="Nombre d'éléments à afficher pour les tops"
    )
    parser.add_argument(
        '-p', '--plot',
        action='store_true',
        help="Générer des graphiques des distributions"
    )
    parser.add_argument(
        '-e', '--export',
        nargs='*',
        choices=['json', 'csv'],
        help="Exporter les résultats dans les formats spécifiés"
    )
    parser.add_argument(
        '-cmp', '--compare',
        action='store_true',
        help="Comparer les métriques entre plusieurs livres"
    )
    
    args = parser.parse_args()
    
    # Validation des arguments
    if args.top < 1:
        print("❌ Le nombre d'éléments à afficher doit être positif")
        sys.exit(1)
    
    # Mode comparaison
    if args.compare:
        compare_multiple_books(args.books, args)
    # Mode analyse individuelle
    else:
        for book_path in args.books:
            analyze_single_book(book_path, args)
            print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    main()
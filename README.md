# 📚 BookBot
> This project was developed solely for educational purposes to practice Python programming skills.
> BookBot is an advanced literary analysis tool built for educational purposes.  
> It extracts statistical and linguistic insights from books — perfect for students, researchers, and literature enthusiasts.

![Python](https://img.shields.io/badge/Python-3.7%2B-blue?logo=python)

---

## 🌟 Features

### 📊 Quantitative Analysis
- Word and character counting
- Character frequency (sorted)
- Top N most frequent words
- Unique word detection

### 🧠 Linguistic Metrics
- Flesch-Kincaid readability score
- Sentiment analysis (polarity)
- Automatic language detection
- Vocabulary density

### 📈 Visualization
- Character frequency bar charts
- Word frequency histograms
- Comparative summary tables

### 💾 Data Export
- JSON and CSV reports
- PNG images for charts

---

## 🚀 Usage

### 🔍 Basic book analysis
```bash
python main.py path/to/your_book.txt
```

### 📊 Full analysis with export
```bash
python main.py book.txt --characters --words --plot --export json csv
```

### 📚 Compare multiple books
```bash
python main.py book1.txt book2.txt book3.txt --compare
```

### 🧰 Command-line options
| Option | Description |
|--------|-------------|
| `-c`, `--characters`     | Show character frequency |
| `-w`, `--words`          | Show top frequent words |
| `-t`, `--top`            | Number of top elements to display (default: 15) |
| `-p`, `--plot`           | Generate visual charts |
| `-e`, `--export`         | Export results to `json`, `csv` or both |
| `--compare`              | Enable multi-book comparison mode |

---

## 📋 Sample Output

### 📝 Single Book Analysis
```
============ ANALYZE: books/frankenstein.txt ============
📖 Language detected: en
🔤 Word count: 78,125
📊 Readability (Flesch-Kincaid): 72.34
😊 Sentiment: Negative (-0.12)

🔠 CHARACTER FREQUENCY:
e: 45921
t: 30365
a: 26743
...

🔑 TOP 10 KEYWORDS:
monster: 142
creature: 98
life: 87
...

📈 Charts generated: frankenstein.txt_characters.png
💾 Data exported: frankenstein.txt_metrics.json
```

### 📚 Book Comparison
```
📊 BOOK COMPARISON
Book                          |   Words | Unique Words | Readability | Sentiment
--------------------------------------------------------------------------------
books/frankenstein.txt        |   78125 |        12345 |       72.34 |     -0.12
books/dracula.txt             |  162345 |        23456 |       65.78 |     -0.08
books/pride_prejudice.txt     |  122345 |        18976 |       80.12 |      0.15
```

---

## 🗂️ Project Structure

```
bookbot/
├── main.py              # CLI entry point
├── stats.py             # Core text analysis logic
├── books/               # Sample books
├── outputs/             # Generated exports
├── .gitignore
└── README.md
```

---

## 🛠 Requirements

- Python 3.7+
- `matplotlib` — for chart generation
- `textblob` — for sentiment analysis
- `langdetect` — for language detection
- `argparse` — for CLI parsing (built-in)

Install dependencies:
```bash
pip install -r requirements.txt
```

---

## 🧪 About

This is a personal project to practice Python programming, created as part of the [Boot.dev](https://www.boot.dev) curriculum.

---

## 🔖 License

MIT License — Free to use, modify, and distribute.

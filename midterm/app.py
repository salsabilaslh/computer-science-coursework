import gradio as gr
import sqlite3
import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup

DB_PATH = os.path.join(os.path.dirname(__file__), "quotes.db")

# =========================
# GET QUOTES
# =========================
def get_quotes():
    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id,
               SUBSTR(text, 1, 80) || '...' as text,
               author
        FROM quotes
        """
    )

    rows = cursor.fetchall()

    conn.close()

    return rows

# =========================
# WORD COUNT
# =========================
def word_count():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT text FROM quotes")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return "No data available."

    words = []
    for r in rows:
        words.extend(r[0].split())

    return f"Total words across all quotes: {len(words)}"


# =========================
# TRANSLATE TO KOREAN
# =========================
def translate_korean():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT text, author FROM quotes")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return "No data available."

    result = ""

    for i, r in enumerate(rows, start=1):
        text = r[0]
        author = r[1]

        url = "https://translate.googleapis.com/translate_a/single"
        params = {
            "client": "gtx",
            "sl": "en",
            "tl": "ko",
            "dt": "t",
            "q": text
        }

        response = requests.get(url, params=params)
        translated = response.json()[0][0][0]

        result += f"{i}. {translated} - {author}\n\n"

    return result


# =========================
# TRANSLATE TO INDONESIAN
# =========================
def translate_indonesian():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT text, author FROM quotes")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return "No data available."

    result = ""

    for i, r in enumerate(rows, start=1):
        text = r[0]
        author = r[1]

        url = "https://translate.googleapis.com/translate_a/single"
        params = {
            "client": "gtx",
            "sl": "en",
            "tl": "id",
            "dt": "t",
            "q": text
        }

        response = requests.get(url, params=params)
        translated = response.json()[0][0][0]

        result += f"{i}. {translated} - {author}\n\n"

    return result

# =========================
# TRANSLATE SINGLE TEXT
# =========================
def translate_text(text, target_lang):
    if not text:
        return ""

    url = "https://translate.googleapis.com/translate_a/single"

    params = {
        "client": "gtx",
        "sl": "en",
        "tl": target_lang,
        "dt": "t",
        "q": text
    }

    response = requests.get(url, params=params)
    translated = response.json()[0][0][0]

    return translated


# =========================
# WORD COUNT SINGLE TEXT
# =========================
def count_words(text):
    if not text:
        return 0

    return f"{len(text.split())} words"

# =========================
# DASHBOARD STATS
# =========================
def get_stats():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # total quotes
    cursor.execute("SELECT COUNT(*) FROM quotes")
    total_quotes = cursor.fetchone()[0]

    # total authors
    cursor.execute("SELECT COUNT(DISTINCT author) FROM quotes")
    total_authors = cursor.fetchone()[0]

    # average words
    cursor.execute("SELECT text FROM quotes")
    rows = cursor.fetchall()

    total_words = 0

    for r in rows:
        total_words += len(r[0].split())

    avg_words = round(total_words / total_quotes, 2)

    # longest quote
    longest_quote = max(
        rows,
        key=lambda x: len(x[0].split())
    )[0]

    # shortest quote
    shortest_quote = min(
        rows,
        key=lambda x: len(x[0].split())
    )[0]

    conn.close()

    return (
        total_quotes,
        total_authors,
        avg_words,
        longest_quote,
        shortest_quote
    )

# =========================
# SEARCH QUOTES
# =========================
def search_quotes(keyword):

    conn = sqlite3.connect(DB_PATH)

    query = f"""
    SELECT id,
           SUBSTR(text, 1, 80) || '...' as text,
           author
    FROM quotes
    WHERE text LIKE '%{keyword}%'
    """

    df = pd.read_sql_query(
        query,
        conn
    )

    conn.close()

    return df

    
# =========================
# TOP AUTHORS
# =========================
def top_authors():

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT author,
           COUNT(*) as total_quotes
    FROM quotes
    GROUP BY author
    ORDER BY total_quotes DESC
    """

    df = pd.read_sql_query(
        query,
        conn
    )

    conn.close()

    return df

# =========================
# AUTHORS CHART
# =========================
def authors_chart():

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT author,
           COUNT(*) as total_quotes
    FROM quotes
    GROUP BY author
    ORDER BY total_quotes DESC
    LIMIT 10
    """

    df = pd.read_sql_query(
        query,
        conn
    )

    conn.close()

    fig, ax = plt.subplots()

    ax.bar(
        df["author"],
        df["total_quotes"]
    )

    ax.set_title(
        "Top Authors"
    )

    ax.set_xlabel(
        "Author"
    )

    ax.set_ylabel(
        "Number of Quotes"
    )

    plt.xticks(rotation=45)

    return fig

# =========================
# SCRAPE QUOTES
# =========================
def scrape_quotes():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for page in range(1, 6):

        url = f"http://quotes.toscrape.com/page/{page}/"

        response = requests.get(url)

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        quotes = soup.find_all(
            "div",
            class_="quote"
        )

        for q in quotes:

            text = q.find(
                "span",
                class_="text"
            ).get_text()

            author = q.find(
                "small",
                class_="author"
            ).get_text()

            cursor.execute(
                """
                INSERT INTO quotes(text, author)
                VALUES(?, ?)
                """,
                (text, author)
            )

    conn.commit()
    conn.close()

    return "Quotes added successfully!"

# =========================
# RANDOM QUOTE
# =========================
def random_quote():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT text, author
        FROM quotes
        ORDER BY RANDOM()
        LIMIT 1
        """
    )

    row = cursor.fetchone()

    conn.close()

    return f'"{row[0]}"\n\n— {row[1]}'

# =========================
# INITIALIZE DATABASE
# =========================
def initialize_quotes():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM quotes"
    )

    count = cursor.fetchone()[0]

    conn.close()

    if count < 100:
        scrape_quotes()

# =========================
# UI
# =========================
initialize_quotes()

with gr.Blocks() as app:
    gr.Markdown("# Quotes Analysis Dashboard")
    gr.Markdown("An interactive dashboard for exploring quotes, multilingual translation, keyword search, and data analysis.")

    with gr.Tab("View Quotes"):

        gr.Markdown("### Quotes List")
            
        table = gr.Dataframe(
            value=get_quotes(),
            headers=["id", "text", "author"],
            interactive=False,
            row_count=(200, "dynamic")
        )
    
        gr.Markdown("### Real-Time Translation")
    
        selected_quote = gr.Textbox(
            label="Selected Quote",
            lines=3
        )
    
        with gr.Row():

            btn_kr = gr.Button("🇰🇷 Translate to Korean")
            btn_id = gr.Button("🇮🇩 Translate to Indonesian")

        translated_output = gr.Textbox(
                label="Translation Result",
                lines=4
        )
    
        word_count_output = gr.Textbox(
            label="Word Count"
        )
        
        # SELECT ROW
        def select_quote(evt: gr.SelectData):
            rows = get_quotes()
            row_index = evt.index[0]
        
            return rows[row_index][1]
            
        table.select(
            fn=select_quote,
            outputs=selected_quote
        )
    
        # TRANSLATE KR
        btn_kr.click(
            fn=lambda x: translate_text(x, "ko"),
            inputs=selected_quote,
            outputs=translated_output
        )
    
        # TRANSLATE ID
        btn_id.click(
            fn=lambda x: translate_text(x, "id"),
            inputs=selected_quote,
            outputs=translated_output
        )
    
        # WORD COUNT
        selected_quote.change(
            fn=count_words,
            inputs=selected_quote,
            outputs=word_count_output
        )
            

    with gr.Tab("Search"):

        with gr.Column(scale=1):
    
            gr.Markdown("## Search Quotes")
    
            keyword = gr.Textbox(
                label="Keyword"
            )
    
            search_btn = gr.Button(
                "Search"
            )
    
            search_output = gr.Dataframe(
                headers=["id", "text", "author"],
                interactive=False,
                row_count=10
            )
    
            search_btn.click(
                fn=search_quotes,
                inputs=keyword,
                outputs=search_output
            )
    
    with gr.Tab("Dashboard"):

        gr.Markdown("## Quotes Dashboard")
    
        with gr.Row():
    
            total_quotes = gr.Number(
                label="Total Quotes"
            )
    
            total_authors = gr.Number(
                label="Total Authors"
            )
    
            avg_words = gr.Number(
                label="Average Words"
            )
    
        longest_quote = gr.Textbox(
            label="Longest Quote",
            lines=3
        )

        shortest_quote = gr.Textbox(
            label="Shortest Quote",
            lines=2
        )
    
        stats_btn = gr.Button(
            "Show Dashboard Analytics"
        )

        gr.Markdown("## Quote of the Day")
        
        random_output = gr.Textbox(
            lines=4,
            label="Today's Quote"
        )
        
        random_btn = gr.Button(
            "Generate Random Quote"
        )
        
        random_btn.click(
            fn=random_quote,
            outputs=random_output
        )
    
        stats_btn.click(
            fn=get_stats,
            outputs=[
                total_quotes,
                total_authors,
                avg_words,
                longest_quote,
                shortest_quote
            ]
        )

        
    with gr.Tab("Analysis"):

        gr.Markdown("## Top Authors")
    
        authors_table = gr.Dataframe(
            headers=["author", "total_quotes"]
        )
    
        authors_btn = gr.Button(
            "Show Top Authors"
        )
    
        authors_btn.click(
            fn=top_authors,
            outputs=authors_table
        )

        gr.Markdown("## 📈 Authors Visualization")

        plot_output = gr.Plot()
        
        chart_btn = gr.Button(
            "Show Authors Chart"
        )
        
        chart_btn.click(
            fn=authors_chart,
            outputs=plot_output
        )
        
        gr.Markdown("## Dataset Word Statistics")
    
        output2 = gr.Textbox(
            label="Analysis Result"
        )
    
        btn2 = gr.Button(
            "Word Count"
        )
    
        btn2.click(
            word_count,
            outputs=output2
        )


app.launch()

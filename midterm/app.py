import gradio as gr
import sqlite3
import os
import requests
import pandas as pd

from fastapi import FastAPI
from gradio import mount_gradio_app

css = """
.gradio-container {
    max-width: 800px;
    margin: auto;
}
button {
    border-radius: 8px !important;
    font-weight: 500;
}
"""

DB_PATH = os.path.join(os.path.dirname(__file__), "quotes.db")

# =========================
# GET QUOTES
# =========================
def get_quotes():
    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, text, author FROM quotes"
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
# FASTAPI CRUD
# =========================
fastapi_app = FastAPI()

@fastapi_app.post("/quotes")
def create_quote(text: str, author: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO quotes (text, author) VALUES (?, ?)",
        (text, author)
    )
    conn.commit()
    conn.close()

    return {"message": "Quote added"}

@fastapi_app.put("/quotes/{quote_id}")
def update_quote(quote_id: int, text: str, author: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE quotes SET text=?, author=? WHERE id=?",
        (text, author, quote_id)
    )
    conn.commit()
    conn.close()

    return {"message": "Quote updated"}

@fastapi_app.delete("/quotes/{quote_id}")
def delete_quote(quote_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM quotes WHERE id=?", (quote_id,))
    conn.commit()
    conn.close()

    return {"message": "Quote deleted"}

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@fastapi_app.get("/api")
def root():
    return {"message": "Quotes API is running"}

@fastapi_app.get("/quotes")
def get_quotes_api():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM quotes")
    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]

# =========================
# UI
# =========================
with gr.Blocks() as ui:
    gr.Markdown("# Global Quotes Insight Platform")
    gr.Markdown("A multilingual quote analysis platform featuring real-time translation, word analysis, and interactive data visualization.")

    with gr.Tab("View Quotes"):

        gr.Markdown("### Quotes List")
            
        table = gr.Dataframe(
            headers=["id", "text", "author"],
            interactive=False,
            row_count=(50, "dynamic")
        )
    
        btn = gr.Button("Load Quotes")
    
        btn.click(
            fn=get_quotes,
            outputs=table
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
    with gr.Tab("Analysis"):
        output2 = gr.Textbox(label="Analysis Result")
    
        btn2 = gr.Button("Word Count")
        btn2.click(word_count, outputs=output2)

app = mount_gradio_app(
    fastapi_app,
    ui,
    path="/"
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=7860
    )

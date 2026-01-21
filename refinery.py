import json
import html
import re
import os
import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from datetime import datetime

def clean_html(raw_html):
    """Strips HTML tags and unescapes symbols."""
    clean_text = html.unescape(raw_html)
    clean_text = re.sub(r'<[^>]+>', '', clean_text)
    return clean_text.strip()

def setup_database(db_path):
    """Initializes the SQLite database with separate time columns for easy SQL filtering."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Chat_Logs (
            Log_Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Date TEXT,
            Time TEXT,
            Raw_Timestamp TEXT,
            Prompt TEXT,
            Response TEXT,
            Chat_Id TEXT,
            Topic TEXT
        )
    """)
    conn.commit()
    return conn

def run_refinery():
    root = tk.Tk()
    root.withdraw()

    print("Opening File Picker...")
    file_path = filedialog.askopenfilename(title="Select Gemini JSON", filetypes=[("JSON files", "*.json")])
    if not file_path: return

    with open(file_path, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)[::-1]

    folder = os.path.dirname(file_path)
    db_path = os.path.join(folder, "Gemini_Vault.db")
    json_out_path = os.path.join(folder, "Gemini_Refined.json")
    
    conn = setup_database(db_path)
    cursor = conn.cursor()

    refined_json_list = []

    print(f"Refining... Preserving ISO Timestamps in JSON + SQL Mapping.")

    for block in raw_data:
        # --- 1. Clean Prompt & Response ---
        raw_prompt = block.get('title', '').replace('Eingegebener Prompt: ', '')
        prompt = clean_html(raw_prompt)
        
        response = ""
        if 'safeHtmlItem' in block:
            responses = [clean_html(item['html']) for item in block['safeHtmlItem'] if 'html' in item]
            response = "\n".join(responses)

        # --- 2. Time Processing ---
        raw_timestamp = block.get('time', '') # The "Gold Standard" string
        date_str, time_str = None, None
        
        if raw_timestamp:
            try:
                # We extract the readable parts for the DB columns
                dt_obj = datetime.fromisoformat(raw_timestamp.replace('Z', '+00:00'))
                date_str = dt_obj.strftime('%Y-%m-%d')
                time_str = dt_obj.strftime('%H:%M:%S')
            except ValueError:
                pass

        # --- 3. SQL Injection (Separate columns for ease of use) ---
        cursor.execute("""
            INSERT INTO Chat_Logs (Date, Time, Raw_Timestamp, Prompt, Response)
            VALUES (?, ?, ?, ?, ?)
        """, (date_str, time_str, raw_timestamp, prompt, response))

        # --- 4. JSON Mapping (Keeping it Pure & Scientific) ---
        refined_json_list.append({
            "timestamp": raw_timestamp,
            "prompt": prompt,
            "response": response
        })

    conn.commit()
    conn.close()
    
    with open(json_out_path, 'w', encoding='utf-8') as f:
        json.dump(refined_json_list, f, indent=4, ensure_ascii=False)

    print(f"\nSuccess! High-Fidelity Data stored in: {folder}")
    messagebox.showinfo("Success", "Process finished! CLean Json and db files have been created.")

if __name__ == "__main__":
    run_refinery()


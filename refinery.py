import json
import html
import re
import os
import tkinter as tk
from tkinter import filedialog

def clean_html(raw_html):
    """Strips HTML tags and unescapes symbols."""
    clean_text = html.unescape(raw_html)
    clean_text = re.sub(r'<[^>]+>', '', clean_text)
    # We keep the \n and other formatting characters for structure
    return clean_text.strip()

def run_refinery():
    root = tk.Tk()
    root.withdraw()

    print("Opening File Picker...")
    file_path = filedialog.askopenfilename(
        title="Select your Gemini Takeout JSON",
        filetypes=[("JSON files", "*.json")]
    )

    if not file_path:
        print("No file selected. Exiting.")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print("Refining: Renaming 'title' to 'prompt' and purging noise...")
    
    data = data[::-1]
    refined_list = []

    for block in data:
        # Create a new dictionary to control the order of keys (looks cleaner)
        new_block = {}
        
        # 1. Capture the Prompt (formerly title)
        if 'title' in block:
            new_block['prompt'] = clean_html(block['title']).replace('Eingegebener Prompt: ', '')
        
        # 2. Capture the Time
        if 'time' in block:
            new_block['time'] = block['time']

        # 3. Capture and Flatten the Response
        if 'safeHtmlItem' in block:
            ai_responses = [clean_html(item['html']) for item in block['safeHtmlItem'] if 'html' in item]
            new_block['response'] = "\n".join(ai_responses)

        refined_list.append(new_block)

    folder = os.path.dirname(file_path)
    output_path = os.path.join(folder, "Gemini_Refined_v2.json")

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(refined_list, f, indent=4, ensure_ascii=False)

    print(f"\nSuccess! Your 'Loom' now uses the 'Prompt/Response' format.")
    print(f"Saved to: {output_path}")

if __name__ == "__main__":
    run_refinery()
# Gemini Takeout Refinery 🛠️

**Rescue your data. Refine your history. Ready your AI.**

The Gemini Takeout Refinery is a high-performance Python utility designed to transform raw Google Gemini Takeout exports into structured, clean, and human-readable datasets. Whether you are building a personal AI "Second Brain" or simply want to archive your conversations, this tool handles the heavy lifting of data sanitization.



## ✨ Key Features
- **Prompt-Centric Mapping:** Automatically renames 'titles' to 'prompts' for a more intuitive AI-focused structure.
- **Chronological Correction:** Reverses the default Google order to restore the natural flow of your conversations.
- **HTML Purification:** Deep-cleans CSS/HTML noise and unescapes symbols while preserving essential formatting like newlines.
- **Metadata Pruning:** Strips away redundant Google-specific headers and activity controls to keep your files lean.
- **Zero-Friction UI:** Includes a built-in Windows file picker—no more moving files into specific folders or editing paths.

## 🚀 How to Use
1. **Launch:** Run `refinery.py`.
2. **Select:** A Windows explorer window will appear. Select your Gemini Takeout `.json` file from any location on your drive.
3. **Refine:** The script will process the data and generate a new file named `Gemini_Refined_v2.json` in the same directory as your original.

## 🛠️ Tech Stack
- **Language:** Python 3.x
- **Libraries:** `json`, `tkinter` (File UI), `re` (Regex), `html`
- **License:** MIT

## 🗺️ Roadmap
- [ ] **SQLite Database Integration:** Direct injection for efficient long-term storage.
- [ ] **Vectorization Engine:** Generating vector embeddings for every chat log to enable semantic search.
- [ ] **Local RAG Support:** Preparing data for seamless integration with Local LLMs (Llama 3, Mistral) via LM Studio.
- [ ] **AI-Powered Topic Tagging:** Automated categorization of chat entries using local inference.
- [ ] **Batch Processing:** Refine multiple Takeout files simultaneously.

---
*Created by AlexArchitect — Refining the digital loom.*

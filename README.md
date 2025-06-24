# MCP News Aggregator

A minimal, AI-powered news aggregator server ("MCP server") that fetches news from multiple free sources, lets you ask for news in natural language, uses OpenAI to extract keywords and summarize articles, and allows you to save articles to a reading list.

---

## 🚀 Overview

This project is a proof-of-concept (POC) for an AI-powered news aggregator. It acts as a "web content fetching" tool, providing real-time news from the internet and leveraging OpenAI for smart filtering and summarization.

- **Backend:** Python + FastAPI
- **AI Model:** OpenAI (GPT-3.5-turbo or compatible)
- **News Sources:** Multiple free RSS feeds (NYT, Ars Technica, The Verge, Reddit, CNET, Engadget)
- **Reading List:** In-memory (no database required)

---

## ✨ Features

- **Natural Language News Search:**
  - Ask for news in plain English (e.g., "Show me the latest news about electric cars and battery technology from this week").
  - The server uses AI to extract keywords from your query and fetches relevant articles.
- **AI Summarization:**
  - The first article in the results is summarized using OpenAI.
- **Reading List:**
  - Save articles to your personal reading list.
  - View all saved articles.
- **Multiple News Sources:**
  - Fetches from NYT Technology, Ars Technica, The Verge, Reddit Technology, CNET, and Engadget.

---

## 🛠️ Setup

1. **Clone the Repository**
   ```sh
   git clone https://github.com/masudsajid/NewsMCP.git
   cd NewsMCP
   ```

2. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```

3. **Set Up OpenAI API Key**
   - Create a `.env` file in the project root:
     ```env
     OPENAI_API_KEY=sk-...yourkey...
     ```

---

## ▶️ Running the Server

Start the FastAPI server with:
```sh
uvicorn server:app --reload
```
- The server will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🧪 Usage & Testing

### **Interactive API Docs**
- Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) in your browser.
- You can test all endpoints directly from this page.

### **Endpoints**

#### **POST `/news`**
- **Description:** Fetch and summarize news articles based on your query.
- **Request Example:**
  ```json
  {
    "query": "Summarize the latest AI breakthroughs in the past week",
    "max_articles": 5
  }
  ```
- **Response:** List of articles, with the first article summarized by AI.

#### **POST `/reading-list`**
- **Description:** Save an article to your reading list.
- **Request Example:**
  ```json
  {
    "title": "Example Article",
    "link": "https://example.com/article",
    "summary": "This is a summary."
  }
  ```
- **Response:** `{ "status": "saved" }`

#### **GET `/reading-list`**
- **Description:** View all saved articles in your reading list.
- **Response:** List of saved articles.

---

## 📝 Notes
- The reading list is stored in memory and will reset if the server restarts.
- Your OpenAI API key is required and should **never** be committed to git (it's in `.gitignore`).
- You can add more RSS feeds by editing the `RSS_FEEDS` list in `server.py`.

---

## 📂 Project Structure

```
.
├── server.py         # Main FastAPI server
├── requirements.txt  # Python dependencies
├── .env              # Your OpenAI API key (not tracked by git)
├── .gitignore        # Ignores .env
└── README.md         # This file
```

---

## 🤖 Credits
- Built as a minimal POC for an AI-powered news aggregator ("MCP server").
- Uses OpenAI for keyword extraction and summarization. 
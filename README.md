# 📬 EmailsNewsletter

A Python application that connects to your email inbox using the **Nylas API** and extracts a summarized list of all newsletters you've received. Ideal for cleaning up your inbox or quickly catching up on updates from your favorite sources.

---

## 🚀 Features

- 🔐 Authenticates users via **Nylas** for secure access to email data.
- 📥 Fetches emails categorized as **newsletters**.
- 🧠 Automatically summarizes newsletter content using AI-powered text summarization.
- 🧹 Filters and organizes summaries for an easy-to-read overview.
- 💡 Built for extensibility and integration into personal dashboards or productivity apps.

---

## 🛠️ Setup & Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/afafelwafi/EmailsNewsletter.git
   cd EmailsNewsletter
   ```

2. **Create and activate a virtual environment** (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Nylas credentials**:
   - Create an application on [Nylas Dashboard](https://developer.nylas.com/).
   - Add your credentials to a `.env` file in the root directory:
     ```
     NYLAS_CLIENT_ID=your_client_id
     NYLAS_CLIENT_SECRET=your_client_secret
     NYLAS_ACCESS_TOKEN=your_access_token
     ```

---

## 📧 How It Works

1. Authenticates with Nylas and accesses your inbox.
2. Filters emails marked as newsletters (based on metadata or sender patterns).
3. Extracts plain text or HTML content.
4. Uses a summarization model (e.g., Hugging Face Transformers or GPT-based) to generate concise summaries.
5. Displays or exports the summaries in a readable format (terminal, file, or web UI).

---

## 🧪 Example Output

```
Subject: The Data Science Weekly - Issue 342  
From: datasci@newsletter.com  
Summary: This week's issue covers new tools for LLM fine-tuning, a hands-on guide to vector databases, and top picks from the PyData conference.
```

---

## 🧰 Tech Stack

- Python 3
- Nylas API
- dotenv
- AI Text Summarization (Hugging Face, LLama 7B quanticized)

---

## 🧩 To-Do / Improvements

- [ ] Categorization by sender/topic.
- [ ] Integration with Google Calendar or Notion for tracking.
- [ ] Export summaries to PDF/Markdown. (streamlit app is already integrated in the code)

---

## 🤝 Contributing

Feel free to fork this repo, submit issues, or open PRs! Contributions are welcome and appreciated 🙌

---


## 🖥️ Streamlit App

A lightweight Streamlit interface is included so you can:

- 🔍 View summaries in an interactive dashboard
- 📤 Export summaries directly from the UI

To run the app:

```bash
streamlit run app.py
```

Make sure your `.env` file is properly configured before launching the app.

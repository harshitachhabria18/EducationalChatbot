## EducationalChatbot
An AI-powered chatbot web application built using Flask, Google Gemini API, and HTML/CSS that answers educational questions only. The chatbot features voice input, multilingual support, light/dark theme toggle, session-based chat history, and automatic question classification to ensure responses remain focused on academic topics.

---

## Features

### AI & Learning
- Educational Question Filter — Questions are first classified using Gemini to check if they are academic in nature. Non-educational queries are    blocked automatically.
- AI-Powered Answers — Uses Gemini 2.5 Flash to generate relevant, accurate, and well-formatted educational responses.
- Concise Mode — Optional toggle to get short and to-the-point answers when you need a quick explanation.

### Voice & Input
- Voice Input — Users can speak questions using the browser microphone via the Web Speech API. Works in the selected language automatically.
- Auto-growing Textarea — Input box expands as you type. Press Enter to send, Shift+Enter for a new line.
- Suggestion Chips — Quick-start prompts on the empty screen to help users get started instantly.

### Theme
- Light & Dark Mode — Toggle between a warm dark theme and a clean light theme with a single click. Preference is saved to localStorage and restored on next visit.

### Multilingual Support
- 9 Languages Supported — Interface and voice input work in English, Hindi, Gujarati, Spanish, French, German, Chinese, Arabic, and Japanese.
- Dynamic UI Translation — All labels, placeholders, buttons, and suggestion chips update instantly when a language is selected.
- Localized Voice Recognition — The microphone listens in the currently selected language for accurate transcription.
- Persistent Language Preference — Selected language is saved to localStorage and restored on next visit.

### Chat Experience
- Session-Based History — Maintains full Q&A history during the session for a continuous chat experience.
- Markdown Rendering — Bot responses support bold, italics, lists, headings, and inline code formatting.
- Clear Chat — One-click button to wipe the session history and start fresh.
- Responsive Design — Works seamlessly on desktop and mobile screens.

---

## Tech Stack

- Backend: Flask (Python)

- Frontend: HTML, CSS, JavaScript

- AI Model: Google Gemini 2.5 Flash API

- Voice Recognition: Web Speech API

- Session Management: Flask-Session (filesystem)

---

## Installation

### Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/educational-chatbot.git
cd educational-chatbot
```

### Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

### Install dependencies
```bash
pip install -r requirements.txt
```

---

## Environment Variables
Create a .env file in the root directory:

```env
GEMINI_API_KEY=your_gemini_api_key_here
FLASK_SECRET_KEY=your_random_secret_key_here
GEMINI_MODEL=gemini-2.5-flash
```

---

## Run Locally

```bash
python app.py
```

---

Visit:

```text
http://localhost:5000 
```

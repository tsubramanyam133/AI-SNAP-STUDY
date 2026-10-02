# 📚 Snap & Study

> **Snap it. Understand it. Learn it.**

Snap & Study is an AI-powered visual study assistant that helps students understand educational content from images. Users can upload photos of textbooks, handwritten notes, diagrams, mathematical problems, programming questions, and question papers, then interact with an AI assistant to get explanations, solutions, summaries, and practice questions.

---

## ✨ Features

- 📸 **AI Image Understanding**
  - Upload textbook pages, notes, diagrams, and question papers.
  - AI analyzes the content using Gemini Vision capabilities.

- 💬 **AI Study Chatbot**
  - Ask questions about uploaded study material.
  - Continue the conversation with contextual follow-up questions.

- 🧮 **Step-by-Step Problem Solving**
  - Solve mathematical and technical problems.
  - Get formulas, calculations, and explanations step by step.

- 📝 **Smart Summarization**
  - Convert lengthy study material into concise notes.
  - Extract important concepts and revision points.

- ❓ **Practice Question Generator**
  - Generate easy, medium, and conceptual questions.
  - Useful for exam preparation and self-assessment.

- 🌐 **Translation Support**
  - Translate visible educational content into the requested language.
  - Useful for multilingual learning.

- 📊 **Diagram & Chart Explanation**
  - Understand engineering diagrams, scientific illustrations, charts, and graphs.

- 💻 **Programming Assistance**
  - Analyze code from screenshots.
  - Explain programming concepts and identify errors.

- 🧠 **Context-Aware Conversations**
  - Ask follow-up questions without repeatedly uploading the same material.

- 🎨 **Simple Streamlit Interface**
  - Clean and beginner-friendly interface.
  - Designed for quick interaction with study materials.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| 🐍 Python | Application development |
| 🎈 Streamlit | Web application interface |
| 🤖 Google Gemini | AI vision and conversational intelligence |
| 🧠 Gemini Interactions API | Context-aware AI conversations |
| 📸 Gemini Vision | Image understanding |
| 🔐 Streamlit Secrets | Secure API key management |

---

## 🏗️ System Architecture

```text
                    ┌──────────────────────┐
                    │       Student       │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Streamlit UI      │
                    │   Snap & Study       │
                    └──────────┬───────────┘
                               │
                    ┌──────────┴───────────┐
                    │                      │
                    ▼                      ▼
             📸 Study Image          💬 User Question
                    │                      │
                    └──────────┬───────────┘
                               │
                               ▼
                  ┌─────────────────────────┐
                  │   Google Gemini         │
                  │   Gemini 3.8 Flash      │
                  │   Vision + AI           │
                  └────────────┬────────────┘
                               │
                               ▼
                  ┌─────────────────────────┐
                  │ AI Generated Response   │
                  │                         │
                  │ • Explanation           │
                  │ • Solution              │
                  │ • Summary               │
                  │ • Questions             │
                  │ • Translation           │
                  └────────────┬────────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      Student         │
                    └──────────────────────┘
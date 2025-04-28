# 💡 RAG-FinAdvisor: AI-Powered Financial Advisory Chatbot

**RAG-FinAdvisor** is an intelligent, AI-based financial chatbot that provides personalized investment, loan, and insurance advice. It leverages Retrieval-Augmented Generation (RAG) with Google Cloud's Vertex AI (Gemini model) and LangChain to deliver context-aware, document-driven responses to user queries.

---

## 🚀 Features

- 💬 Conversational chatbot interface
- 📄 Document-based context retrieval using LangChain
- 🤖 Real-time AI response generation using Vertex AI (Gemini)
- 🧠 Financial advice for Investment, Loan, and Insurance
- 📊 Built-in calculators (SIP, EMI, PPF, FD, etc.)
- ☁️ Google Cloud Platform integration
- 🔐 Secure credential handling via base64-encoded `.env`

---

## 🧰 Tech Stack

| Layer        | Technologies Used                                      |
|--------------|---------------------------------------------------------|
| Frontend     | HTML5, CSS3, JavaScript, Jinja (Flask Templates)       |
| Backend      | Python, Flask                                           |
| AI/ML        | LangChain, Vertex AI (Gemini), Prompt Engineering      |
| Document DB  | PDF documents via PyPDF loader                         |
| Cloud        | Google Cloud Platform, Vertex AI, Firebase (optional)  |

---

## 🧠 How It Works

1. Loads a financial knowledge base (PDF)
2. Splits document using LangChain into context chunks
3. Accepts user input via forms or chatbot
4. Combines input + context into a custom AI prompt
5. Sends prompt to Vertex AI (Gemini)
6. Displays the response in a user-friendly format

---

## 🛠️ Installation & Setup
git clone https://github.com/your-username/rag-finadvisor.git
cd rag-finadvisor


 # Set up virtual environment & install dependencies


python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt


# Add your GCP credentials in .env file


GOOGLE_CREDENTIALS_BASE64=your_base64_credentials
PROJECT_ID=your_gcp_project_id
LOCATION=us-central1


 # Run the app
python app.py
<img![image](https://github.com/user-attachments/assets/f37be401-40ce-4ff3-a2bd-f80131cfcc2f)


Future Enhancements
🔍 Semantic search using vector embeddings (FAISS)

💬 Conversational memory with multi-turn dialogue

🌐 Multilingual support (regional/local languages)

📱 Mobile version with Flutter or React Native

🔐 User authentication & query history with Firebase






# 🤖 PYCoder — Python Programming Assistant

PYCoder is a chatbot built with **Streamlit** and the **Groq API** that helps beginner developers with programming questions, with a focus on **Python**. Every answer follows a consistent, didactic structure: a conceptual explanation, a code example, a line-by-line breakdown, and a link to the official documentation.

> The app interface and the assistant's answers are in **Brazilian Portuguese (pt-BR)**.

---

## 📑 Table of Contents

- [Features](#-features)
- [How It Works](#-how-it-works)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Customization](#-customization)
- [Deployment](#-deployment)
- [Troubleshooting](#-troubleshooting)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-LICENSE)
- [Contact](#-contact)

---

## ✨ Features

- 💬 **Chat interface** powered by Streamlit's native chat components
- 🧠 **Conversation memory** — the full message history of the session is sent to the model, so follow-up questions work naturally
- 📚 **Structured answers** — every reply includes:
  1. **Clear explanation** of the concept
  2. **Code example** in Python
  3. **Code breakdown** explaining each part
  4. **Reference documentation** link (📚 section)
- 🎯 **Focused scope** — the system prompt restricts the assistant to programming topics (algorithms, data structures, libraries, frameworks)
- 🔑 **Flexible API key handling** — reads `GROQ_API_KEY` from the environment, or lets the user paste it in the sidebar
- ⚡ **Fast inference** via Groq
- 🛡️ **Error handling** for client initialization and API failures

---

## ⚙️ How It Works

```
User question ──► Streamlit chat input
                       │
                       ▼
        System prompt + session history
                       │
                       ▼
          Groq Chat Completions API
          (model: openai/gpt-oss-20b)
                       │
                       ▼
        Structured answer rendered as Markdown
                       │
                       ▼
          Saved to st.session_state.messages
```

1. The app resolves the Groq API key (environment variable first, sidebar input as fallback).
2. When the user sends a message, it is appended to `st.session_state.messages`.
3. The app builds the payload: the **system prompt** (`CUSTOM_PROMPT`) followed by the entire conversation history.
4. The request is sent to Groq's chat completions endpoint with `temperature=0.7` and `max_tokens=2048`.
5. The response is displayed and stored in the session history for the next turn.

---

## 🧰 Tech Stack

| Component | Purpose |
|-----------|---------|
| [Python 3.9+](https://www.python.org/) | Language |
| [Streamlit](https://docs.streamlit.io/) | Web UI and chat components |
| [Groq Python SDK](https://console.groq.com/docs) | LLM API client |
| [python-dotenv](https://pypi.org/project/python-dotenv/) *(optional)* | Loading variables from a `.env` file |

**Model:** `openai/gpt-oss-20b` (served by Groq)

---

## 📁 Project Structure

```
pycoder/
├── main.py            # Application entry point (UI + chat logic)
├── requirements.txt   # Python dependencies
├── .env               # Local environment variables (NOT committed)
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python **3.9 or newer**
- A free **Groq API key** — create one at [console.groq.com/keys](https://console.groq.com/keys)

### 1. Clone the repository

```bash
git clone https://github.com/<123PAU34>/<PythonProjects>.git
cd <python-for-ai>
```

### 2. Create and activate a virtual environment (recommended)

```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows (PowerShell)
python -m venv venv
venv\Scripts\Activate.ps1
```

### 3. Install dependencies

Create a `requirements.txt` file with:

```text
streamlit
groq
python-dotenv
```

Then run:

```bash
pip install -r requirements.txt
```

### 4. Set your API key

Choose **one** of the options in the [Configuration](#-configuration) section below.

### 5. Run the app

```bash
streamlit run main.py
```

The app opens at **http://localhost:8501**.

---

## 🔐 Configuration

The app looks for the Groq API key in this order:

1. The `GROQ_API_KEY` environment variable
2. The **password field in the sidebar** (if the variable isn't set)

### Option A — Environment variable

```bash
# macOS / Linux
export GROQ_API_KEY="your_api_key_here"

# Windows (PowerShell)
$env:GROQ_API_KEY="your_api_key_here"
```

### Option B — `.env` file

1. Create a `.env` file in the project root:

   ```env
   GROQ_API_KEY=your_api_key_here
   ```

2. In `main.py`, **uncomment** the two lines that load it:

   ```python
   from dotenv import load_dotenv
   ...
   load_dotenv()
   ```

### Option C — Sidebar input

Just launch the app and paste your key into the **"Digite sua API Key da Groq"** field. The key is kept only in the running session and is masked on screen.

> ⚠️ **Never commit your API key.** Add `.env` to your `.gitignore`:
>
> ```gitignore
> .env
> venv/
> __pycache__/
> ```

---

## 💡 Usage

1. Open the app and provide your API key (if not already configured).
2. Type a question in the chat box, for example:
   - *"What is a list comprehension?"*
   - *"How do I read a CSV file with pandas?"*
   - *"Explain the difference between a list and a tuple."*
   - *"How does recursion work?"*
3. Read the structured answer: explanation → code → breakdown → documentation link.
4. Ask follow-up questions — the assistant remembers the conversation within the session.

> **Note:** The conversation history lives in `st.session_state`, so it is cleared when you refresh the page or start a new session.

---

## 🛠️ Customization

All the main settings are easy to find in `main.py`:

| What | Where | Default |
|------|-------|---------|
| Assistant behavior and answer format | `CUSTOM_PROMPT` | PYCoder persona, 4-part answer structure |
| Model | `model=` in `chat.completions.create` | `openai/gpt-oss-20b` |
| Creativity | `temperature=` | `0.7` |
| Maximum answer length | `max_tokens=` | `2048` |
| Page title / icon / layout | `st.set_page_config(...)` | `PYCODER`, 🤖, wide |
| Support button | `st.link_button(...)` in the sidebar | `mailto:` link |

**Tips**

- Want another language? Translate `CUSTOM_PROMPT` and the UI strings.
- Want other topics (JavaScript, SQL, etc.)? Edit rule 1 and the persona in the system prompt.
- Want more deterministic answers? Lower `temperature` (e.g. `0.2`).
- You can swap the model for any chat model available on your Groq account. See [Groq's supported models](https://console.groq.com/docs/models).

---

## ☁️ Deployment

### Streamlit Community Cloud

1. Push the project to GitHub (without your `.env`).
2. Go to [share.streamlit.io](https://share.streamlit.io) and create a new app pointing to `main.py`.
3. In **App settings → Secrets**, add:

   ```toml
   GROQ_API_KEY = "your_api_key_here"
   ```

   > Streamlit exposes secrets as environment variables too, so `os.getenv("GROQ_API_KEY")` in the app will pick it up. If it doesn't in your setup, users can still paste the key in the sidebar.

### Docker (optional)

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY main.py .
EXPOSE 8501
CMD ["streamlit", "run", "main.py", "--server.address=0.0.0.0"]
```

```bash
docker build -t pycoder .
docker run -p 8501:8501 -e GROQ_API_KEY=your_api_key_here pycoder
```

---

## 🩺 Troubleshooting

| Problem | Likely cause / fix |
|---------|--------------------|
| *"Por favor, insira sua API Key da Groq..."* | No key found. Set `GROQ_API_KEY` or paste it in the sidebar. |
| `ModuleNotFoundError: No module named 'groq'` | Dependencies aren't installed. Run `pip install -r requirements.txt`. |
| `.env` is ignored | Make sure `load_dotenv()` and its import are **uncommented** in `main.py`. |
| Authentication / 401 error | The API key is invalid or expired. Generate a new one in the Groq console. |
| Rate limit / 429 error | You hit Groq's usage limits. Wait a moment and retry. |
| Model not found | The model name may have changed or isn't enabled for your account. Check the Groq models list and update `model=`. |
| Answers get cut off | Increase `max_tokens`. |

---

## 🗺️ Roadmap

- [ ] Streaming responses (token-by-token output)
- [ ] "Clear conversation" button
- [ ] Model selector in the sidebar
- [ ] Trimming/summarizing long histories to save tokens
- [ ] Persistent chat history
- [ ] Multi-language interface

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the project
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m "Add my feature"`
4. Push to the branch: `git push origin feature/my-feature`
5. Open a Pull Request

---

## 📄 License

Distributed under the **MIT License**. Add a `LICENSE` file to the repository, or replace this section with the license of your choice.

---

## 📬 Contact

Questions or suggestions? Open an [issue](../../issues) or reach out via the support button inside the app.

---

<p align="center">Made with 🐍 and Streamlit</p>
<p align="center">Este README foi gerado com CLAUDE e revisado pelo autor.</p>

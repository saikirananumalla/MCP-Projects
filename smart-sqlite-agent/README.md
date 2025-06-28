# 🧠 Smart Agent SQLite

A lightweight AI agent that connects a powerful language model (OpenAI or Ollama) to a local SQLite database through tool calling. Built using [`llama-index`](https://github.com/jerryjliu/llama_index) and [`fastmcp`](https://github.com/jerryjliu/fastmcp), this project lets you ask natural language questions and receive structured responses by triggering predefined database tools.

## 🚀 What It Does

This project builds a **Tool-Using AI Agent** that:

* Accepts natural language queries (like "What is John's age?")
* Uses an LLM (e.g., `gpt-4o` or `llama3.2`) to decide which database tool to call
* Fetches or modifies data in an SQLite database
* Returns the final answer conversationally

Under the hood, we use:

* 🛠️ `FastMCP`: to expose our database tools as HTTP endpoints
* 🤖 `llama-index`: to create a tool-aware function agent
* 🔌 `McpToolSpec`: to register and communicate with the MCP tools
* 🧠 `OpenAI GPT-4o` or `Ollama` for the model logic

## 🏗️ Tech Stack

| Component   | Technology           |
| ----------- | -------------------- |
| Agent + LLM | `llama-index`        |
| Model       | `OpenAI` or `Ollama` |
| Tool Server | `fastmcp`            |
| Tools       | Custom SQLite        |
| Interface   | Python CLI           |

---

## 📂 Project Structure

```
smart-agent-sqlite/
│
├── server.py             # Runs the MCP server and defines tools
├── client.py             # Async CLI to talk to the agent
├── agent_service.py      # (Optional) callable agent interface for future UI/APIs
├── .env                  # Contains OPENAI_API_KEY
├── demo.db               # Sample SQLite database
├── requirements.txt
└── README.md
```

---

## 🛠️ Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/your-username/smart-agent-sqlite.git
cd smart-agent-sqlite
```

### 2. Install dependencies

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Set up your environment

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_key_here
```

If using Ollama:

```bash
ollama run llama3
```

### 4. Start the MCP Tool Server

```bash
python server.py
```

### 5. Run the LLM Agent Client

```bash
python client.py
```

---

## 🚪 Example Tools

```python
@mcp.tool()
def insert_person(name: str, age: int, interest: str) -> bool:
    ...

@mcp.tool()
def read_data(query: str = "SELECT * FROM people") -> list:
    ...
```

These tools are automatically discovered and used by the agent.

---

## 🤖 Agent Logic (How It Works)

1. User enters a natural-language message
2. `llama-index`'s `FunctionAgent` evaluates tool needs
3. Chosen tool is called via `BasicMCPClient`
4. Tool result is processed by the agent

---

## 💡 Future Ideas

* Add chat memory with `Context.chat_history`
* Expose via FastAPI or Streamlit
* Add web UI (optional)

---

## 📜 License

MIT License. Built for learning, prototyping, and experimentation.

---

## References:

Daily Dose of Data Science
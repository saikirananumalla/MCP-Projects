import sqlite3
from fastmcp import FastMCP

# Initialize the MCP server with a name
mcp = FastMCP("Sqlite MCP Server")

# Ensure the database exists

def init_db():
    conn = sqlite3.connect("demo.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS people (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            interest TEXT
        );
    """)
    conn.commit()
    conn.close()
    print("[DEBUG] Initialized SQLite database and 'people' table.")


@mcp.tool()
def insert_person(name: str, age: int, interest: str) -> bool:
    """Insert a person's data into the 'people' table (name, age, interest)."""
    try:
        print(f"[DEBUG] Inserting: name={name}, age={age}, interest={interest}")
        conn = sqlite3.connect("demo.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO people (name, age, interest) VALUES (?, ?, ?)",
            (name, age, interest)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"[ERROR] Insertion failed: {str(e)}")
        return False


@mcp.tool()
def read_data(query: str = "SELECT * FROM people") -> list:
    """Execute a SQL SELECT query and return all results."""
    try:
        print(f"[DEBUG] Running SQL query: {query}")
        conn = sqlite3.connect("demo.db")
        results = conn.execute(query).fetchall()
        conn.close()
        return results
    except Exception as e:
        print(f"[ERROR] Query failed: {str(e)}")
        return []

@mcp.tool()
def greet(name: str) -> str:
    return (
        f"Hello, {name}! \n\n"
        "I'm a smart agent built by Sai Kiran. "
        "I use GPT-powered reasoning to interact with an SQLite database using natural language. "
        "Ask me anything—from inserting records to fetching data—and I'll handle the logic behind the scenes!"
    )

# Start the MCP server
if __name__ == "__main__":
    init_db()
    print("Starting Server...")
    mcp.run(transport="sse", port=8000)

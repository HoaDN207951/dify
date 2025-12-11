from fastmcp import FastMCP
import os
import time
import re

mcp = FastMCP("File System Agent")

EXPORT_DIR = "sql_exports"
if not os.path.exists(EXPORT_DIR):
    os.makedirs(EXPORT_DIR)

@mcp.tool()
def save_to_sql_file(content: str, filename: str = None) -> str:
    """
    Saves text content to a .sql file in the exports directory.
    
    Args:
        content: The SQL queries or text to save.
        filename: (Optional) The name of the file. e.g., 'backup.sql'
    """
    # Sanitize filename
    if filename:
        safe_name = os.path.basename(filename)
        # Ensure extension
        if not safe_name.endswith('.sql'):
            safe_name += '.sql'
    else:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        safe_name = f"query_dump_{timestamp}.sql"

    full_path = os.path.join(EXPORT_DIR, safe_name)

    try:
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully saved SQL content to: {full_path}"
    except Exception as e:
        return f"Error saving file: {str(e)}"

if __name__ == '__main__':
    mcp.run(transport="sse")
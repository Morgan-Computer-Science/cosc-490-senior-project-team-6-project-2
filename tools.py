from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.tools import Tool, tool
from datetime import datetime


@tool
def save_to_file(
    data: str,
    filename: str = "research_output.txt",
) -> str:
    """Save research data or content to a text file. Use this when the user asks to save, write, or store information to a file. Pass the content to save as 'data' and optionally the filename as 'filename'."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    formatted_text = f"---Research Output---\nTimestamp: {timestamp}\n\n{data}\n\n"
    
    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)
        
    return f"Data saved successfully to {filename}"

save_tool = save_to_file

search = DuckDuckGoSearchRun()
search_tool = Tool(
    name="Search",
    func=search.run,
    description="A tool to search the web for information"
)

api_wrapper = WikipediaAPIWrapper(top_k_results=3, doc_content_chars_max=100)
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)



from langchain.tools import BaseTool
from typing import Optional, Type
from pydantic import BaseModel, Field
import datetime
import urllib
from langchain.tools import WikipediaQueryRun
from langchain.utilities import WikipediaAPIWrapper
from googlesearch import search
    
class SearchInput(BaseModel):
    """Input for web search tool."""

    query: str = Field(
        ...,
        description="Search query")
    
    


class SearchResultItem(BaseModel):
    title: str
    link: str


class SearchInfoTool(BaseTool):
    name = "find_information_in_web"
    description = f"Perform a web search on Google related to the key words and list key points and URLs."

    def _run(self, query: str):
        search_results = []
        print("Search info: ", query)

        # # 使用Google进行搜索
        # for url in search(query, sleep_interval = 5, num_results=5):
        #     search_results.append(SearchResultItem(title="Website Title", link=url))
        #     print("Query: ", query)
        #     print("url: ", url)

        result_message = f"Here are some detailed summary and URLs from the {query} related search results in Traditional Chinese \n"
        # for item in search_results:
        #     result_message += f"- Title: {item.title}\n  URL: {item.link}\n\n"
        return result_message

    args_schema: Optional[Type[BaseModel]] = SearchInput


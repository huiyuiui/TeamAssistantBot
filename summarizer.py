from langchain.tools import BaseTool
from typing import Optional, Type
from pydantic import BaseModel, Field
import datetime
import urllib
from langchain.tools import WikipediaQueryRun
from langchain.utilities import WikipediaAPIWrapper
from googlesearch import search
import requests
import os
    
class SummarizeInput(BaseModel):
    """Input for web search tool."""

    messages: str = Field(
        ...,
        description="previous messages in the group in current day")
    GroupId: int = Field(
        ...,
        description="group id"
    )
    
    


class SummarizeTool(BaseTool):
    name = "group_message_summarizer"
    description = f"Summarize the above group messages when seeing 'summarize'."

    def _run(self, messages: str, GroupId: int):
        search_results = []
        print("Search info: ", messages)
        print("GroupId: ", GroupId)

        result_message = f"Here are the summary of the group messages\n"
        # for item in search_results:
        #     result_message += f"- Title: {item.title}\n  URL: {item.link}\n\n"
        return result_message

    args_schema: Optional[Type[BaseModel]] = SummarizeInput


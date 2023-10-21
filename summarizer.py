from langchain.tools import BaseTool
from typing import Optional, Type
from pydantic import BaseModel, Field
import datetime
import urllib
from langchain.tools import WikipediaQueryRun
from langchain.utilities import WikipediaAPIWrapper
from googlesearch import search
    
class SummarizeInput(BaseModel):
    """Input for web search tool."""
    summary: str = Field(
        ...,
        description="Summary of the chat")

    

class SummarizeTool(BaseTool):
    name = "group_message_summarizer"
    description = f"Summarize the input chat messages when seeing 'summary' considering time scale."

    def _run(self, summary: str):
        return summary

    args_schema: Optional[Type[BaseModel]] = SummarizeInput



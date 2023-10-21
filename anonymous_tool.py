# from langchain.tools import BaseTool
# from langchain.agents import AgentType
# from typing import Optional, Type
# from pydantic import BaseModel, Field

# class AnonymousInput(BaseModel):
#     # 依據匿名留言的回復心情，回傳貼圖
#     """The input schema for AnonymousTool."""

#     message: str = Field(
#         ...,
#         description="The message to be replied by AnonymousTool.")
#     emoji: str = Field(
#         ...,
#         description="")


# class WikiTool(BaseTool):
#     name = "find_wikipedia_information"
#     description = f"Use wikipedia resources to find unknown information."

#     def _run(self, title: str, link: str):
#         print("Wiki")
#         print('標題：'+title)
#         print('描述：'+link)

#         return title, link

#     args_schema: Optional[Type[BaseModel]] = WikiInput
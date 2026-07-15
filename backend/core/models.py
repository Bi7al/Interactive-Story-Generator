from typing import List,Dict,Any,Optional
from pydantic import BaseModel, Field


class StoryOptionLLM(BaseModel):
    text:str=Field(description='The Text of the option shown to the user')
    next_node:Dict[str,Any]=Field(description="The next node description and its options")

class StoryNodeLLM(BaseModel):
    content:str=Field(description="The Main Content Of the Story Node")
    isEnding:bool=Field(description="Wether this node is an ending node")
    isWinning:bool=Field(description='Wether this node is winning ending node')
    options:Optional[List[StoryOptionLLM]]=Field(default=None,description="The Options for this Node")
class StoryLLMResponse(BaseModel):
    title:str=Field(description="The title of the story")
    rootNode:StoryNodeLLM=Field(description="The Root Node of the story")

from typing import List,Optional,Dict
from datetime import datetime
from pydantic import BaseModel



class StoryOptionsSchema(BaseModel):
    text:str
    node_id:Optional[int]=None

class StoryNode(BaseModel):
    content:str
    is_winning:bool=False
    is_ending:bool=False


class CompleteStoryNodeResponse(StoryNode):
    id:int
    options:List[StoryOptionsSchema]

    class config:
        from_attributes=True

class StoryBase(BaseModel):
    title:str
    session_id:Optional[str]=None
    class config:
        from_attributes=True


class CreateStoryRequest(BaseModel):
    theme:str



class CompleteStoryResponse(StoryBase):
    id:int
    created_at:datetime
    root_node:CompleteStoryNodeResponse
    all_nodes:Dict[int,CompleteStoryNodeResponse]

    class config:
        from_attributes=True

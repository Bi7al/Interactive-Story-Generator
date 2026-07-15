from sqlalchemy.orm import Session
from core.config import settings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from core.prompts import STORY_PROMPT
from models.story import Story,StoryNode
from core.models import StoryLLMResponse,StoryNodeLLM






class StoryGenerator:
    @classmethod
    def _get_llm(self):

        llm = ChatGoogleGenerativeAI(
            model="gemini-3.5-flash",
            api_key=settings.API_KEY
        )
        return llm
    @classmethod
    def generate_story(
        self,
        db:Session,
        session_id:str,
        theme:str
    )->Story:
        llm=self._get_llm()
        story_parser=PydanticOutputParser(pydantic_object=StoryLLMResponse)
        prompt=ChatPromptTemplate.from_messages(
            [
                ("system",STORY_PROMPT),
                ("human",f"create the story with this theme:{theme}")
            ]
        ).partial(format_instructions=story_parser.get_format_instructions())

        raw_response =llm.invoke(prompt.invoke({}))
        response_text= raw_response
        if hasattr(raw_response,"content"):
            response_text=raw_response.content
        # 2. Fix the Pydantic error: Unpack Gemini's list/dict blocks if they occur
        if isinstance(response_text, list):
            # If it's a list of blocks, extract text from the first valid text block
            blocks = []
            for block in response_text:
                if isinstance(block, dict) and "text" in block:
                    blocks.append(block["text"])
                elif isinstance(block, str):
                    blocks.append(block)
            response_text = "".join(blocks)
        elif isinstance(response_text, dict) and "text" in response_text:
            response_text = response_text["text"]
        # --- FIX END ---
        
        story_structure = story_parser.parse(response_text)


        story_db = Story(title=story_structure.title,session_id=session_id)
        db.add(story_db)
        db.flush()

        root_node_data=story_structure.rootNode

        if isinstance(root_node_data,dict):
            root_node_data=StoryNodeLLM.model_validate(root_node_data)
        
        self._process_story_node(db,story_db.id,root_node_data,is_root=True)
        

        db.commit()
        return story_db
    

    @classmethod
    def _process_story_node(self,db:Session,story_id:int,node_data:StoryNodeLLM,is_root:bool=False)->StoryNode:
        node=StoryNode(
            story_id=story_id,
            content=node_data.content if hasattr(node_data,"content") else node_data['content'],
            is_root=is_root,
            is_ending=node_data.isEnding if hasattr(node_data,"isEnding") else node_data['isEnding'],
            is_winning=node_data.isWinning if hasattr(node_data,"isWinning") else node_data['isWinning'],
            options=[])
        db.add(node)
        db.flush()
        if not node.is_ending and (hasattr(node_data,"options") and node_data.options):
            options_list=[]
            for option_data in node_data.options:
                next_node=option_data.next_node
                if isinstance(next_node,dict):
                    next_node= StoryNodeLLM.model_validate(next_node)
                
                child_node=self._process_story_node(db,story_id,next_node,False)
                options_list.append({
                    "text":option_data.text,
                    "node_id":child_node.id
                })
            node.options=options_list
        db.flush()
        return node

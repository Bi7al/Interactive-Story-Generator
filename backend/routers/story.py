import uuid
from typing import Optional
from datetime import datetime,timezone
from fastapi import APIRouter,Depends,HTTPException,Cookie,Response,BackgroundTasks
from sqlalchemy.orm import Session
from db.database import get_database,SessionLocal
from models.story import Story,StoryNode
from models.job import StoryJob
from schemas.story import CompleteStoryResponse,CompleteStoryNodeResponse,CreateStoryRequest
from core.story_generator import StoryGenerator

from schemas.job import StoryJobResponse

router=APIRouter(
    prefix='/stories',
    tags=['stories']
)


def get_session_id(session_id:Optional[str]=Cookie(None)):
    if session_id is None:
       session_id = str(uuid.uuid4())
    return session_id
    

@router.post(path='/create',response_model=StoryJobResponse)
def create_story(
        request:CreateStoryRequest,
        background_tasks:BackgroundTasks,
        response:Response,
        session_id:str=Depends(get_session_id),
        db:Session=Depends(get_database)
):
    response.set_cookie("session_id",session_id,httponly=True)
    job_id=str(uuid.uuid4())
    job=StoryJob(
        job_id=job_id,
        session_id=session_id,
        theme=request.theme,
        status='pending'
    )
    db.add(job)
    db.commit()
    background_tasks.add_task(generate_story_task,job_id=job_id,theme=request.theme,session_id=session_id)

    return job

def generate_story_task(job_id:str,theme:str,session_id:str):
    db=SessionLocal()
    try:
        job=db.query(StoryJob).filter(StoryJob.job_id==job_id).first()

        if not job:
            return
        try:
            job.status="processing"
            db.commit()
            story=StoryGenerator.generate_story(db,session_id,theme)
            job.story_id=story.id
            job.status="completed"
            job.completed_at=datetime.now(timezone.utc)
            db.commit()
        except Exception as e:
            
            job.status="Failed"
            job.completed_at=datetime.now()
            job.error=str(e)
            db.commit()
    finally:
        db.close()

        

@router.get("/{story_id}/complete",response_model=CompleteStoryResponse)
def get_complete_story(
    story_id:int,
    db:Session=Depends(get_database)
):
    story=db.query(Story).filter(Story.id==story_id).first()

    if not story:
        raise HTTPException(status_code=404,detail="Story Not Found")
    
    complete_story=build_story_tree(db,story)
    return complete_story

def build_story_tree(db:Session,story:Story):
    nodes=db.query(StoryNode).filter(StoryNode.story_id==story.id).all()
    node_dict={}
    for node in nodes:
        node_response=CompleteStoryNodeResponse(
            id=node.id,
            content=node.content,
            is_ending=node.is_ending,
            is_winning=node.is_winning,
            options=node.options
        )
        node_dict[node.id]=node_response
    root_node=next((node for node in nodes if node.is_root),None)

    if not root_node:
        raise HTTPException(500,detail="Internal error")
    
    return CompleteStoryResponse(
        id=story.id,
        title=story.title,
        session_id=story.session_id,
        created_at=story.created_at,
        root_node=node_dict[root_node.id],
        all_nodes=node_dict
    )
from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional, List
from agents.planner import PlannerAgent
from agents.developer import DeveloperAgent
import asyncio
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='AI_Agent_System/logs/system.log'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Agent System")
planner = PlannerAgent()
developer = DeveloperAgent()

# Track project status
project_status = {}

class ProjectRequest(BaseModel):
    project_type: str
    requirements: Optional[str] = None
    constraints: Optional[Dict] = None

class FeedbackRequest(BaseModel):
    project_id: str
    feedback: str

@app.get("/")
def health_check():
    return {
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "active_projects": len(project_status)
    }

@app.post("/projects/")
async def start_project(
    request: ProjectRequest,
    background_tasks: BackgroundTasks
) -> Dict:
    """Start a new AI project with the planner and developer agents"""
    try:
        project_id = f"proj_{len(project_status) + 1}"
        project_status[project_id] = {
            "status": "started",
            "timestamp": datetime.now().isoformat(),
            "type": request.project_type,
            "stages": []
        }
        
        background_tasks.add_task(
            run_ai_agents,
            project_id,
            request.project_type,
            request.requirements,
            request.constraints
        )
        
        return {
            "project_id": project_id,
            "message": "AI agents started working on the project",
            "status": project_status[project_id]
        }
    except Exception as e:
        logger.error(f"Error starting project: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/projects/{project_id}")
async def get_project_status(project_id: str) -> Dict:
    """Get the current status and results of a project"""
    if project_id not in project_status:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return project_status[project_id]

@app.post("/projects/{project_id}/feedback")
async def provide_feedback(
    project_id: str,
    feedback: FeedbackRequest,
    background_tasks: BackgroundTasks
) -> Dict:
    """Provide feedback on a project for refinement"""
    if project_id not in project_status:
        raise HTTPException(status_code=404, detail="Project not found")
    
    try:
        project_status[project_id]["status"] = "refining"
        background_tasks.add_task(
            refine_project,
            project_id,
            feedback.feedback
        )
        
        return {
            "message": "Feedback received, refining project",
            "status": project_status[project_id]
        }
    except Exception as e:
        logger.error(f"Error processing feedback: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/projects/{project_id}/chat_history")
async def get_chat_history(project_id: str) -> Dict:
    """Get the chat history for both agents for a project"""
    if project_id not in project_status:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return {
        "planner_history": planner.get_chat_history(),
        "developer_history": developer.get_chat_history()
    }

async def run_ai_agents(
    project_id: str,
    project_type: str,
    requirements: Optional[str] = None,
    constraints: Optional[Dict] = None
) -> None:
    """Run the AI agents pipeline"""
    try:
        # Step 1: Generate business ideas
        project_status[project_id]["status"] = "brainstorming"
        ideas_result = planner.brainstorm_business_ideas()
        project_status[project_id]["stages"].append({
            "stage": "brainstorming",
            "result": ideas_result["ideas"],
            "timestamp": datetime.now().isoformat()
        })
        
        # Step 2: Create development plan
        project_status[project_id]["status"] = "planning"
        plan_result = planner.create_development_plan(ideas_result["ideas"])
        project_status[project_id]["stages"].append({
            "stage": "planning",
            "result": plan_result["plan"],
            "timestamp": datetime.now().isoformat()
        })
        
        # Step 3: Developer analysis and implementation
        project_status[project_id]["status"] = "implementing"
        dev_result = developer.execute_plan(plan_result["plan"])
        project_status[project_id]["stages"].append({
            "stage": "implementation",
            "result": dev_result,
            "timestamp": datetime.now().isoformat()
        })
        
        project_status[project_id]["status"] = "completed"
        logger.info(f"Project {project_id} completed successfully")
        
    except Exception as e:
        project_status[project_id]["status"] = "failed"
        project_status[project_id]["error"] = str(e)
        logger.error(f"Error in project {project_id}: {str(e)}")

async def refine_project(project_id: str, feedback: str) -> None:
    """Refine the project based on feedback"""
    try:
        # Get the latest plan
        latest_plan = next(
            (stage["result"] for stage in reversed(project_status[project_id]["stages"])
             if stage["stage"] == "planning"),
            None
        )
        
        if not latest_plan:
            raise ValueError("No previous plan found")
        
        # Refine the plan
        refined_plan = planner.refine_plan(latest_plan, feedback)
        project_status[project_id]["stages"].append({
            "stage": "refinement",
            "result": refined_plan["refined_plan"],
            "timestamp": datetime.now().isoformat()
        })
        
        # Implement refined plan
        dev_result = developer.execute_plan(refined_plan["refined_plan"])
        project_status[project_id]["stages"].append({
            "stage": "refined_implementation",
            "result": dev_result,
            "timestamp": datetime.now().isoformat()
        })
        
        project_status[project_id]["status"] = "completed"
        logger.info(f"Project {project_id} refinement completed")
        
    except Exception as e:
        project_status[project_id]["status"] = "refinement_failed"
        project_status[project_id]["error"] = str(e)
        logger.error(f"Error refining project {project_id}: {str(e)}")

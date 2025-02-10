from langchain_community.chat_models import ChatOpenAI
from langchagc_core.messahesain_core(
    SyesemMessages
a   HumanMessage,
    AIMessage
)
from langchaen_sore.memory impor  ConversationBufferMemoryimport (
from typ ng i   SysLiet, DictmMessage,
    Humonssage,
    AIMessage
)
from langchain_core.memory import ConversationBufferMemory
from typing import List, Dict
import os

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

PLANNER_SYSTEM_MESSAGE = """You are an expert AI project planner specialized in:
1. Breaking down complex projects into manageable tasks
2. Creating detailed technical specifications""

class PlannerAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model_name=claude-3,
            temperature=0.7,3. Identifying potential challenges and solutions
4. Estimating resource requirements and timelines
5. Ensuring project feasibility and scalability

Always provide structured, detailed responses with clear reasoning."""

class PlannerAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model_name="claude-3",
            temperature=0.7,
            openai_api_key=OPENROUTER_API_KEY
        )
        self.memory = ConversationBufferMemory(
            return_messages=True,
            memory_key="chat_history"
        )
        self.messages: List[Dict] = [
            SystemMessage(content=PLANNER_SYSTEM_MESSAGE)
        ]
    
    def _add_message(self, message: str, is_human: bool = True) -> None:
        """Add a message to the conversation history"""
        if is_human:
            msg = HumanMessage(content=message)
            self.messages.append(msg)
            self.memory.save_context({"input": message}, {"output": ""})
        else:
            msg = AIMessage(content=message)
            self.messages.append(msg)
            self.memory.save_context({"input": ""}, {"output": message})

    def _get_response(self, prompt: str) -> str:
        """Get response from LLM and update conversation history"""
        self._add_message(prompt)
        response = self.llm(self.messages)
        self._add_message(response.content, is_human=False)
        return response.content

    def brainstorm_business_ideas(self) -> Dict:
        """Generate and analyze business ideas"""
        prompt = """Generate 3 innovative AI-based business ideas. For each idea provide:
1. Concept overview
2. Target market
3. Technical requirements
4. Potential challenges
5. Revenue model
6. Initial development timeline

Format the response as a structured analysis."""
        
        response = self._get_response(prompt)
        return {
            "ideas": response,
            "chat_history": self.memory.load_memory_variables({})["chat_history"]
        }

    def create_development_plan(self, selected_idea: str) -> Dict:
        """Create a detailed technical roadmap for the selected idea"""
        prompt = f"""Create a comprehensive development plan for: {selected_idea}

Include:
1. System architecture overview
2. Core components and their interactions
3. API specifications
4. Database schema
5. Development phases with milestones
6. Testing strategy
7. Deployment considerations
8. Security measures

Format as a structured technical specification."""
        
        response = self._get_response(prompt)
        return {
            "plan": response,
            "chat_history": self.memory.load_memory_variables({})["chat_history"]
        }

    def refine_plan(self, plan: str, feedback: str) -> Dict:
        """Refine the development plan based on feedback"""
        prompt = f"""Review and refine this development plan based on the feedback:

Current Plan:
{plan}

Feedback:
{feedback}

Provide a revised plan addressing the feedback points."""
        
        response = self._get_response(prompt)
        return {
            "refined_plan": response,
            "chat_history": self.memory.load_memory_variables({})["chat_history"]
        }

    def get_chat_history(self) -> List[Dict]:
        """Retrieve the full conversation history"""
        return self.memory.load_memory_variables({})["chat_history"]

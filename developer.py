from langchain_community.chat_models import ChatOpenAI
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage
)
from langchain_core.memory import ConversationBufferMemory
from typing import List, Dict
import os
import json

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

DEVELOPER_SYSTEM_MESSAGE = """You are an expert AI developer specialized in:
1. Implementing complex software systems
2. Writing clean, maintainable code
3. Following best practices and design patterns
4. Handling edge cases and error conditions
5. Creating comprehensive documentation

Always provide detailed implementation plans and code snippets when relevant."""

class DeveloperAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model_name="gpt-4-turbo",
            temperature=0.5,
            openai_api_key=OPENROUTER_API_KEY
        )
        self.memory = ConversationBufferMemory(
            return_messages=True,
            memory_key="chat_history"
        )
        self.messages: List[Dict] = [
            SystemMessage(content=DEVELOPER_SYSTEM_MESSAGE)
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

    def analyze_requirements(self, plan: str) -> Dict:
        """Analyze technical requirements and identify implementation details"""
        prompt = f"""Analyze the following development plan and break down the technical requirements:

{plan}

Provide:
1. Core technology stack recommendations
2. External dependencies and libraries needed
3. API endpoints specification
4. Data models and schema definitions
5. Implementation complexity assessment
6. Potential technical challenges
7. Security considerations

Format as a structured technical analysis."""
        
        response = self._get_response(prompt)
        return {
            "analysis": response,
            "chat_history": self.memory.load_memory_variables({})["chat_history"]
        }

    def create_implementation_plan(self, requirements: str) -> Dict:
        """Create detailed implementation steps based on requirements"""
        prompt = f"""Create a detailed implementation plan for these requirements:

{requirements}

Include:
1. Step-by-step implementation tasks
2. Code structure and organization
3. Key functions and classes needed
4. Database migrations
5. API implementation details
6. Testing requirements
7. Deployment steps

Format as a structured development plan."""
        
        response = self._get_response(prompt)
        return {
            "implementation_plan": response,
            "chat_history": self.memory.load_memory_variables({})["chat_history"]
        }

    def generate_code(self, component: str, specs: str) -> Dict:
        """Generate code for a specific component based on specifications"""
        prompt = f"""Generate implementation code for this component:

Component: {component}
Specifications: {specs}

Provide:
1. Complete code implementation
2. Inline documentation
3. Usage examples
4. Test cases
5. Error handling
6. Performance considerations

Format as a structured code document."""
        
        response = self._get_response(prompt)
        return {
            "code": response,
            "chat_history": self.memory.load_memory_variables({})["chat_history"]
        }

    def review_code(self, code: str) -> Dict:
        """Review code and provide improvement suggestions"""
        prompt = f"""Review this code implementation:

{code}

Analyze for:
1. Code quality and best practices
2. Potential bugs or issues
3. Performance optimizations
4. Security vulnerabilities
5. Error handling improvements
6. Documentation completeness

Provide detailed feedback and suggestions."""
        
        response = self._get_response(prompt)
        return {
            "review": response,
            "chat_history": self.memory.load_memory_variables({})["chat_history"]
        }

    def execute_plan(self, plan: str) -> Dict:
        """Execute the development plan and generate implementation"""
        # First analyze requirements
        requirements = self.analyze_requirements(plan)
        
        # Create implementation plan
        implementation = self.create_implementation_plan(requirements["analysis"])
        
        # Generate core component code
        code_components = self.generate_code("core_system", implementation["implementation_plan"])
        
        # Review the generated code
        review = self.review_code(code_components["code"])
        
        return {
            "requirements": requirements["analysis"],
            "implementation": implementation["implementation_plan"],
            "code": code_components["code"],
            "review": review["review"],
            "chat_history": self.memory.load_memory_variables({})["chat_history"]
        }

    def get_chat_history(self) -> List[Dict]:
        """Retrieve the full conversation history"""
        return self.memory.load_memory_variables({})["chat_history"]

# AI Agent System

A robust system of AI agents that collaborate to plan and develop software projects.

## Architecture

### Components

1. **Planner Agent**
   - Brainstorms business ideas
   - Creates detailed technical roadmaps
   - Handles project planning and specifications
   - Maintains conversation history
   - Provides structured analysis and recommendations

2. **Developer Agent**
   - Analyzes technical requirements
   - Creates implementation plans
   - Generates code with documentation
   - Performs code reviews
   - Maintains development conversation history

3. **Main System**
   - FastAPI backend for agent orchestration
   - Async task processing
   - Project status tracking
   - Error handling and logging
   - Chat history management

## Setup

1. Install dependencies:
```bash
pip install -r AI_Agent_System/backend/requirements.txt
```

2. Set up environment variables in `config/.env`:
```env
OPENROUTER_API_KEY=your_api_key_here
```

## Local Testing

Run the agent interaction test script:
```bash
python AI_Agent_System/tests/test_agents.py
```

This will:
- Generate business ideas
- Create development plans
- Analyze requirements
- Generate sample code
- Perform code review
- Save chat histories for analysis

Chat histories are saved in `AI_Agent_System/logs/` with timestamps for review.

## API Endpoints

### Project Management

- `GET /` - Health check
- `POST /projects/` - Start a new project
- `GET /projects/{project_id}` - Get project status
- `POST /projects/{project_id}/feedback` - Provide feedback
- `GET /projects/{project_id}/chat_history` - Get agent chat histories

### Request Examples

Start a new project:
```json
POST /projects/
{
    "project_type": "web_application",
    "requirements": "Create a task management system",
    "constraints": {
        "technology": "Python/FastAPI",
        "timeline": "2 weeks"
    }
}
```

Provide feedback:
```json
POST /projects/{project_id}/feedback
{
    "feedback": "Add authentication system and user roles"
}
```

## Features

1. **Conversation Memory**
   - Both agents maintain chat histories
   - Context-aware responses
   - Traceable decision-making

2. **Structured Output**
   - Detailed analysis and plans
   - Code generation with documentation
   - Comprehensive code reviews

3. **Error Handling**
   - Robust error catching and logging
   - Status tracking for each project stage
   - Detailed error reporting

4. **Async Processing**
   - Background task execution
   - Non-blocking API endpoints
   - Progress tracking

5. **Project Refinement**
   - Feedback incorporation
   - Plan iteration
   - Continuous improvement

## Development Workflow

1. Planner Agent:
   - Generates business ideas
   - Creates technical specifications
   - Refines plans based on feedback

2. Developer Agent:
   - Analyzes requirements
   - Creates implementation plans
   - Generates and reviews code

3. System:
   - Orchestrates agent interactions
   - Tracks project progress
   - Manages chat histories
   - Handles errors and logging

## Best Practices

1. **Testing**
   - Run local tests before deployment
   - Review chat histories for quality
   - Verify agent interactions

2. **Monitoring**
   - Check system logs regularly
   - Monitor project statuses
   - Review chat histories

3. **Maintenance**
   - Keep dependencies updated
   - Review and clean logs
   - Monitor API performance

## Future Improvements

1. Integration with version control
2. Enhanced error recovery
3. More specialized agent roles
4. Advanced project analytics
5. Real-time progress updates

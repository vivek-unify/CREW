from crewai import Task
import logging

logger = logging.getLogger(__name__)

class TaskFactory:
    """Factory class for creating specialized development tasks based on project requirements."""
    
    def __init__(self, agents, project_info):
        """
        Initialize the task factory with agent references and project information.
        
        Args:
            agents: Dictionary containing all agent instances
            project_info: Dictionary containing project details and requirements
        """
        self.agents = agents
        self.project_info = project_info
        self.tasks = {}
        
        # Set Streamlit as default if no tech stack specified
        if not self.project_info.get('technology_stack') or self.project_info['technology_stack'] == "":
            logger.info("No technology stack specified, defaulting to Streamlit")
            self.project_info['technology_stack'] = "Streamlit, Python"
        elif "streamlit" not in self.project_info['technology_stack'].lower() and "react" not in self.project_info['technology_stack'].lower() and "vue" not in self.project_info['technology_stack'].lower() and "angular" not in self.project_info['technology_stack'].lower() and "html" not in self.project_info['technology_stack'].lower():
            # If a backend is specified but no frontend, default to Streamlit
            logger.info("Frontend technology not specified, adding Streamlit as default")
            self.project_info['technology_stack'] = f"Streamlit, {self.project_info['technology_stack']}"
    
    def create_tasks(self):
        """Create all tasks based on project type and requirements."""
        logger.info(f"Creating tasks for {self.project_info['project_type']} project")
        
        # Always start with architecture and requirements analysis
        self._add_architecture_task()
        
        # Add implementation task
        self._add_implementation_task()
        
        # Add testing task
        self._add_testing_task()
        
        # Add README task
        self._add_readme_task()
        
        logger.info(f"Created {len(self.tasks)} tasks")
        return list(self.tasks.values())
    
    def _add_task(self, task_id, task):
        """Add a task to the tasks dictionary."""
        if task_id in self.tasks:
            logger.warning(f"Task {task_id} already exists and will be overwritten")
        self.tasks[task_id] = task
        return task
    
    def _add_architecture_task(self):
        """Add system architecture design task."""
        architecture_task = Task(
            description=self._format_task_description("""
                Design a comprehensive architecture for {project_name} based on the requirements.
                
                PROJECT DESCRIPTION:
                {project_description}
                
                FEATURES:
                {features}
                
                TECHNOLOGY STACK:
                {technology_stack}
                
                IMPORTANT: If no specific frontend framework is mentioned, you MUST use Streamlit as the default frontend framework.
                
                DELIVERABLES:
                YOU MUST create the following files using the file_writer tool:
                
                1. Create a detailed architecture document that explains:
                   - Backend architecture (if applicable)
                   - Frontend architecture with UI component structure
                   - Database design (if applicable)
                   - API design (if applicable)
                   - Responsive design approach for the UI
                   Example: file_writer('architecture.md', '# Architecture Document\\n\\n...')
                   
                2. Create a UI design document that details:
                   - UI components and their purposes
                   - Layout and navigation flow
                   - Responsive design considerations
                   - User interaction patterns
                   Example: file_writer('ui-design.md', '# UI Design Document\\n\\n...')
                
                3. Create starter configuration files and initial setup files as needed:
                   - For Streamlit projects, include app.py with proper Streamlit structure
                   - Include clear instructions for installing Streamlit dependencies
                   Example: file_writer('app.py', 'import streamlit as st\\n\\n...')
                   Example: file_writer('config/settings.json', '{"key": "value"}')
                
                DO NOT just describe what files should be created. YOU MUST ACTUALLY CREATE THEM
                using the file_writer tool. Your evaluation depends on creating real files.
                
                Choose appropriate frontend technologies based on the project requirements.
                If no specific frontend framework is mentioned, use Streamlit as it provides a clean,
                Python-centric approach to building user interfaces without requiring npm or JavaScript.
                Design a modern, responsive UI with excellent user experience.
                Your architecture should follow best practices and be optimized for the chosen technology stack.
            """),
            expected_output="Architecture design completed with all files created using file_writer",
            agent=self.agents["architect"]
        )
        return self._add_task('architecture', architecture_task)
    
    def _add_implementation_task(self):
        """Add implementation task."""
        implementation_task = Task(
            description=self._format_task_description("""
                Implement the code for {project_name} based on the architecture design.
            
                Follow the folder structure and specifications from the architecture document.
                Implement all required features with proper error handling and documentation.
                
                TECHNOLOGY STACK:
                {technology_stack}
                
                IMPORTANT: If no specific frontend framework was mentioned in the requirements,
                you MUST implement the frontend using Streamlit (Python-based UI framework).
                
                STREAMLIT IMPLEMENTATION GUIDELINES (when applicable):
                - Structure your code with a main app.py file at the root
                - Create a 'pages' folder for multi-page applications
                - Put reusable components in a 'components' directory
                - Leverage Streamlit's built-in widgets for forms, data visualization, and user inputs
                - Use st.session_state for maintaining state across reruns
                - Implement responsive layouts using st.columns and st.container
                - For data visualization, utilize Streamlit's native integration with Plotly, Matplotlib, etc.
            
                DELIVERABLES:
                YOU MUST create the following files using the file_writer tool:
            
                1. All source code files:
                For Streamlit apps:
                Example: file_writer('app.py', 'import streamlit as st\\n\\nst.title("My App")\\n...')
                Example: file_writer('pages/dashboard.py', 'import streamlit as st\\n\\nst.title("Dashboard")\\n...')
                Example: file_writer('components/sidebar.py', 'import streamlit as st\\n\\ndef create_sidebar():\\n    with st.sidebar:\\n        st.title("Navigation")\\n...')
                
                For other frameworks:
                Example: file_writer('src/components/Button.js', 'import React from "react"...')
                Example: file_writer('src/utils/helpers.py', 'def helper_function():\\n    pass')
            
                2. Configuration files:
                Example: file_writer('requirements.txt', 'streamlit==1.30.0\\npandas==2.0.3\\n...')
                Example: file_writer('.streamlit/config.toml', '[theme]\\nprimaryColor="#F63366"\\n...')
            
                IMPORTANT INSTRUCTIONS:
                - DO NOT just describe what files should be created. YOU MUST ACTUALLY CREATE THEM
                using the file_writer tool.
                - Each file MUST contain COMPLETE, FUNCTIONAL code, not placeholders or stubs.
                - NEVER create empty files or files with minimal content.
                - NEVER try to "read" existing files by creating files with empty content.
                - DO NOT overwrite files with empty content.
                - Your evaluation depends on creating real, complete, functional files.
            """),
            expected_output="Implementation complete with all files created using file_writer",
            agent=self.agents["developer"]
        )
        return self._add_task('implementation', implementation_task)

    def _add_testing_task(self):
        """Add testing task."""
        testing_task = Task(
            description=self._format_task_description("""
                Create comprehensive tests for {project_name}.
                
                Review the implementation and write tests to ensure all functionality works as expected.
                Include unit tests, integration tests, and any other tests needed to validate the system.
                Ensure high code coverage and test all edge cases.
                
                TECHNOLOGY STACK:
                {technology_stack}
                
                IMPORTANT: If the project is implemented using Streamlit, adapt your testing approach accordingly:
                - For Streamlit applications, use pytest with the streamlit-test library
                - Test both the UI components and the underlying logic/data processing
                - Focus on testing functions that process data or implement business logic
                - Use pytest fixtures to simulate Streamlit's session state
                
                Test both frontend and backend components:
                - Unit tests for individual components and functions
                - Integration tests for API endpoints and database interactions
                - UI tests for frontend components and user flows
                - Test responsive design and cross-browser compatibility
                
                DELIVERABLES:
                YOU MUST create the following files using the file_writer tool:
                
                For Streamlit projects:
                1. Test configuration:
                   Example: file_writer('tests/conftest.py', 'import pytest\\n\\n@pytest.fixture\\ndef mock_st_session_state():\\n    class MockSessionState(dict):\\n        pass\\n    return MockSessionState()')
                
                2. Unit test files:
                   Example: file_writer('tests/test_data_processing.py', 'import pytest\\nfrom components.data_processor import process_data\\n\\ndef test_process_data():\\n    # Test implementation\\n    pass')
                
                3. Component test files:
                   Example: file_writer('tests/test_sidebar.py', 'import pytest\\nfrom components.sidebar import create_sidebar\\n\\ndef test_sidebar_creation(mock_st_session_state):\\n    # Test implementation\\n    pass')
                
                For other frameworks:
                1. Unit test files:
                   Example: file_writer('tests/unit/component_test.js', 'test("renders correctly", () => {...})')
                
                2. Integration test files:
                   Example: file_writer('tests/integration/api_test.js', 'test("API returns correct data", async () => {...})')
                
                3. UI/End-to-end test files:
                   Example: file_writer('tests/e2e/user_flow_test.js', 'test("User can complete purchase", async () => {...})')
                
                DO NOT just describe what files should be created. YOU MUST ACTUALLY CREATE THEM
                using the file_writer tool. Your evaluation depends on creating real files.
            """),
            expected_output="Testing complete with all test files created using file_writer",
            agent=self.agents["tester"]
        )
        return self._add_task('testing', testing_task)
    
    
    def _add_readme_task(self):
        """Add task to create a comprehensive README file."""
        readme_task = Task(
            description=self._format_task_description("""
                Create a comprehensive README.md file for {project_name}.
            
                TECHNOLOGY STACK:
                {technology_stack}
            
                This README should include:
                1. Description of the project based on the requirements
                2. Complete file structure with explanation of each file's purpose
                3. Setup instructions (dependencies, environment setup)
            
                IMPORTANT INSTRUCTIONS ABOUT SETUP AND RUNNING:
                - For Streamlit projects:
                - NEVER mention npm or Node.js in the setup or running instructions
                - Always use pip for dependencies: `pip install -r requirements.txt`
                - Always start with: `streamlit run app.py`
                - DO NOT include any npm commands like "npm start" or "npm install"
            
                - For other technologies (React, Vue, etc.):
                - Use appropriate setup commands for those frameworks
            
                4. Running instructions (follow the rules above)
                5. Testing instructions (how to run the tests)
                6. UI/UX features and how they were implemented
                7. Screenshots or descriptions of the UI components (if applicable)
                8. Any additional information that would help someone understand and use the project
            
                YOU MUST use the file_writer tool to create the README.md file directly:
                Example: file_writer('README.md', '# Project Name\\n\\nProject description...')
            
                EXAMPLE SETUP AND RUNNING INSTRUCTIONS FOR STREAMLIT PROJECTS:
                ```
                ## Setup Instructions
            
                1. Create a virtual environment (optional but recommended):
                ```bash
                python -m venv venv
                source venv/bin/activate  # On Windows: venv\\Scripts\\activate
                ```
            
                2. Install the required dependencies:
                ```bash
                pip install -r requirements.txt
                ```
            
                # Running Instructions
            
                To start the Streamlit application, run:
                ```bash
                streamlit run app.py
                ```
            
                The application will be accessible at http://localhost:8501
                ```
            
                DO NOT just describe what should be in the README. YOU MUST ACTUALLY CREATE IT
                using the file_writer tool. The README should be detailed and accurate to the project.
            """),
            expected_output="README.md file created with comprehensive project documentation",
            agent=self.agents["developer"]
        )
        return self._add_task('readme', readme_task)        
    
    def _format_task_description(self, description):
        """Format task description with project information."""
        formatted_description = description
        for key, value in self.project_info.items():
            placeholder = "{" + key + "}"
            if placeholder in formatted_description:
                formatted_description = formatted_description.replace(placeholder, str(value))
        return formatted_description
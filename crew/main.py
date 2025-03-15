import os
import sys
import logging
import json
from datetime import datetime
from crewai import Crew, Process

import agents
from file_writer import write_file
from task_factory import TaskFactory

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("crewai_execution.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def main():
    try:
        logger.info("Starting CrewAI Development Process")
        print("\n🚀 CrewAI Development System 🚀")
        print("================================")
        
        # Get project information
        project_name = input("Enter the project name: ").strip()
        project_description = input("Enter a detailed description of the project: ").strip()
        features = input("List key features (comma separated): ").strip()
        
        # Add hint about Streamlit as default
        technology_stack = input("Enter the technology stack (leave blank for Streamlit-based solution): ").strip()
        
        # Default to Streamlit if no technology specified
        if not technology_stack:
            print("💡 No technology stack specified. Defaulting to Streamlit for frontend with Python backend.")
            technology_stack = "Streamlit, Python"
        
        logger.info(f"Project: {project_name} using {technology_stack}")
        
        # Prepare project info dictionary
        project_info = {
            "project_name": project_name,
            "project_description": project_description,
            "features": features,
            "technology_stack": technology_stack,
            "project_type": "custom" # Default to custom project type
        }
        
        # Create output directory
        output_dir = f"{project_name.lower().replace(' ', '_')}_project"
        os.makedirs(output_dir, exist_ok=True)
        os.chdir(output_dir)
        logger.info(f"Created output directory: {output_dir}")
        
        # Save project info for reference
        os.makedirs("project_config", exist_ok=True)
        with open("project_config/project_info.json", "w") as f:
            json.dump(project_info, f, indent=2)
        
        # Create agent instances dictionary
        agent_instances = {
            "architect": agents.Architect_agent,
            "developer": agents.Developer_agent,
            "tester": agents.Tester_agent
        }
        
        # Create tasks based on project info
        task_factory = TaskFactory(
            agents=agent_instances,
            project_info=project_info
        )
        tasks = task_factory.create_tasks()
        
        # Define the crew with sequential process
        print("\nCreating development crew with Architect, Developer, and Tester agents...")
        crew = Crew(
            agents=[
                agents.Architect_agent,
                agents.Developer_agent,
                agents.Tester_agent
            ],
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        )
        
        print("\nStarting development process. This may take some time...")
        logger.info("Starting crew execution")
        crew_output = crew.kickoff()
        logger.info("Crew execution completed")
        
        # Count the number of files created
        file_count = 0
        for root, dirs, files in os.walk('.'):
            # Skip the project_config directory which is created by the script itself
            if "project_config" in root:
                continue
            file_count += len(files)
        
        print(f"\n🎉 Your project '{project_name}' has been successfully generated!")
        print(f"📁 Location: {os.path.abspath('.')}")
        print(f"📝 Total files created: {file_count}")
        
        # Add Streamlit-specific instructions if applicable
        if "streamlit" in technology_stack.lower():
            print("\n🔹 To run your Streamlit application:")
            print("  1. Install dependencies: pip install -r requirements.txt")
            print("  2. Start the app: streamlit run app.py")
        
        print("\nSee the README.md file for detailed information about the project.")
        
    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
        print("\n\nProcess interrupted. Exiting gracefully.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error in main execution: {e}", exc_info=True)
        print(f"\n❌ An error occurred: {e}")
        print("Please check the logs for more details.")
        sys.exit(1)

if __name__ == "__main__":
    main()
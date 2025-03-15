import os
import logging
from crewai.tools import tool

logger = logging.getLogger(__name__)

# Track files that have been created
created_files = {}

@tool("Create a file with specific content")
def write_file(filepath: str, content: str) -> bool:
    """
    Write content to a file, creating directories as needed.
    
    Args:
        filepath: Path to the file (relative to current directory)
        content: Content to write to the file
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Clean filepath if it starts with /
        if filepath.startswith('/'):
            filepath = filepath.lstrip('/')
            
        # Create the full path
        full_path = os.path.join(os.getcwd(), filepath)
        
        # Don't allow empty content or overwriting with empty content
        if not content.strip():
            logger.warning(f"Attempted to create file with empty content: {filepath}")
            print(f"⚠️ Warning: Attempted to create file with empty content: {filepath}")
            return False
        
        # Track if this would overwrite a file
        if filepath in created_files:
            # Don't allow overwriting with empty content
            if not content.strip():
                logger.warning(f"Attempted to overwrite file with empty content: {filepath}")
                print(f"⚠️ Warning: Attempted to overwrite file with empty content: {filepath}")
                return False
            
            # If it has the same content, don't rewrite
            if created_files[filepath] == content:
                logger.info(f"File content identical, not rewriting: {filepath}")
                print(f"ℹ️ File content identical, not rewriting: {filepath}")
                return True
                
            logger.info(f"Overwriting existing file: {filepath}")
            print(f"🔄 Overwriting existing file: {filepath}")
        
        # Create directory if it doesn't exist
        directory = os.path.dirname(full_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            logger.info(f"Created directory: {directory}")
        
        # Write content to the file
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Track this file and its content    
        created_files[filepath] = content
            
        logger.info(f"Created file: {full_path}")
        print(f"✅ Created file: {filepath}")
        return True
    except Exception as e:
        logger.error(f"Error creating file {filepath}: {e}")
        print(f"❌ Error creating file {filepath}: {e}")
        return False
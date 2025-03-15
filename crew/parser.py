import os
import re
import logging

logger = logging.getLogger(__name__)

def parse(file_path):
    """
    Parses the specified markdown file to extract file paths and corresponding code blocks.
    Then writes each code block to its designated file, ensuring that all files are created
    with proper directory structure.
    """
    if not os.path.exists(file_path):
        logger.warning(f"File '{file_path}' does not exist.")
        return None

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {e}")
        return None

    # Regular expression to capture file blocks
    pattern = r"Path:\s*(?P<filepath>.+?)\s*(?:Code|Content):\s*'''(?P<code>.*?)'''"
    matches = re.finditer(pattern, content, re.DOTALL)

    files_created = 0
    directories_created = set()

    for match in matches:
        filepath = match.group("filepath").strip()
        code = match.group("code").strip()

        # Ensure the filepath is relative
        if filepath.startswith('/'):
            filepath = filepath.lstrip('/')

        # Create the full path relative to the current working directory
        full_path = os.path.join(os.getcwd(), filepath)

        # Create directory if it doesn't exist
        directory = os.path.dirname(full_path)
        if directory and not os.path.exists(directory):
            try:
                os.makedirs(directory, exist_ok=True)
                directories_created.add(directory)
                logger.info(f"Created directory: {directory}")
            except Exception as e:
                logger.error(f"Error creating directory {directory}: {e}")
                continue

        # Write the extracted code to the target file
        try:
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(code)
            logger.info(f"Wrote content to '{full_path}'")
            files_created += 1
        except Exception as e:
            logger.error(f"Error writing to file {full_path}: {e}")

    if files_created == 0:
        logger.warning("No valid file blocks found in the output.")
    else:
        logger.info(f"Successfully created {files_created} file(s) in {len(directories_created)} directories.")

    return files_created
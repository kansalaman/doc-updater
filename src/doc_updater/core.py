#!/usr/bin/env python3
import subprocess
import os
import re
from typing import List, Tuple
import argparse
import sys
from openai import OpenAI

__version__ = "0.1.0"

class ReadmeUpdater:
    def __init__(self, readme_path: str = "README.md"):
        self.readme_path = readme_path
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        if not os.getenv('OPENAI_API_KEY'):
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        
    def get_staged_files(self) -> List[str]:
        """Get list of staged files in git."""
        cmd = ["git", "diff", "--cached", "--name-only"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        files = result.stdout.strip().split('\n')
        return [f for f in files if f]  # Filter out empty strings
    
    def analyze_code_changes(self, files: List[str]) -> List[Tuple[str, str]]:
        """Analyze changes in staged files using OpenAI."""
        updates = []
        for file in files:
            if file.endswith('.py'):
                cmd = ["git", "diff", "--cached", file]
                result = subprocess.run(cmd, capture_output=True, text=True)
                diff = result.stdout
                
                if not diff:
                    continue
                
                updates.append((file, diff))
                
        return updates
    
    def update_readme(self, updates: List[Tuple[str, str]]) -> bool:
        """Update README.md content using AI."""
        if not updates:
            return False
            
        # Read current README content
        with open(self.readme_path, 'r') as f:
            current_content = f.read()

        # Format the updates into a readable string with diffs
        changes_text = "\n".join([f"File: {file}\n{diff}\n" for file, diff in updates])

        prompt = f"""Please update this README to include clear instructions for setting up and using the pre-commit hook. 
        The README should focus on installation steps, configuration requirements (like OpenAI API key), and how to use 
        the pre-commit hook. Keep the content concise and user-friendly.
        
        Recent code changes:
        {changes_text}
        
        Current README:
        {current_content}"""

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a technical documentation expert. Create clear, concise documentation focused on setup and usage instructions."},
                {"role": "user", "content": prompt}
            ]
        )
        
        new_content = response.choices[0].message.content.strip()
        
        # Write the updated content
        with open(self.readme_path, 'w') as f:
            f.write(new_content)
        
        # Stage the README if we made changes
        subprocess.run(["git", "add", self.readme_path])
        return True

def main():
    parser = argparse.ArgumentParser(description='Update README based on code changes')
    parser.add_argument('--readme', default='README.md', help='Path to README file')
    parser.add_argument('--version', action='version', version=f'readme-updater {__version__}')
    args = parser.parse_args()
    
    try:
        updater = ReadmeUpdater(args.readme)
        staged_files = updater.get_staged_files()
        updates = updater.analyze_code_changes(staged_files)
        
        if updater.update_readme(updates):
            print("README.md updated based on code changes")
            return 0
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(main()) 
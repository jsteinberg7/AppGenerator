import os
import argparse
import subprocess
import sys
import requests
from dotenv import load_dotenv

from prompts import generate_initial_prompt, code_review_prompt
from ui import AppGenerator
from PyQt5.QtWidgets import QApplication


load_dotenv()
CLAUDE_SECRET_KEY = os.getenv('CLAUDE_SECRET_KEY')
CLAUDE_API_URL = 'https://api.anthropic.com/v1/messages'
# subprocess.run("export QT_QPA_PLATFORM=cocoa", shell=True)

def generate_code(prompt, platform):
    headers = {
        'Content-Type': 'application/json',
        'X-API-Key': CLAUDE_SECRET_KEY,
        "anthropic-version": "2023-06-01"
    }

    data = {
        'messages': [
            {"role": "user",
             "content": [
                 {"type": "text",
                 "text": generate_initial_prompt(platform, prompt)
                 }
                ]
             }
            ],
        'model': 'claude-2.1',
        'max_tokens': 4096
    }
    
    response = requests.post(CLAUDE_API_URL, headers=headers, json=data)
    
    if response.status_code == 200:
        result = response.json()
        return result['content'][0]['text']
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None
    
def create_project(project_name, prompt, platform):
    create_folder(project_name)
    generated_code, commands = implement_project(project_name, prompt, platform)
    run_setup_commands(commands)

def create_folder(project_name):
    # Create the project folder
    os.makedirs(f"GeneratedProjects/{project_name}", exist_ok=True)
    print(" > mkdir ", project_name)
    
    # Change the current directory to the project folder
    os.chdir(f"GeneratedProjects/{project_name}")

    print(f" > cd GeneratedProjects/{project_name}")
    
def implement_project(project_name, prompt, platform):
    # Generate code and commands using the Claude API
    generated_code = generate_code(prompt, platform)
    
    if generated_code:
        # Split the generated code into code files and commands
        code_files, commands = generated_code.split('CMDS:')

        # Extract + clean commands list
        commands = [line for line in commands.strip().replace('\n', '').split('---') if line][0].split('CMD_SPLIT')
        
        # Create code files
        for file_content in code_files.strip().split('FILENAME:')[1:]:
            if file_content.strip():
                file_parts = file_content.strip().split('---', 1)
                if len(file_parts) == 2:
                    file_name = file_parts[0].strip().replace('---', '')
                    file_code = file_parts[1].strip().replace('---', '')
                    with open(file_name, 'w') as file:
                        file.write(file_code)
                    print(f"Created file: {file_name}")
                else:
                    print(f"Skipping invalid file content: {file_content.strip()}")

        
        # Create a README file, including the prompt, generated_code, and setup commands, in a beautiful markdown format
        with open('README.md', 'w') as file:
            file.write(f"# {project_name}\n\n")
            file.write("## Prompt\n\n")
            file.write(f"{prompt}\n\n")
            file.write("## Generated Code\n\n")
            file.write("```dart\n")
            file.write(generated_code)
            file.write("\n```\n\n")
            file.write("## Setup Commands\n\n")
            for command in commands:
                file.write(f"```bash\n{command.strip()}\n```\n\n")

        print("Created README.md")

        print(f"Project '{project_name}' created successfully!")
    else:
        print("Failed to generate code and commands.")
        
    return generated_code, commands

def run_setup_commands(commands):
    for command in commands:
        if command.strip():
            print(f" > {command.strip()}")
            subprocess.run(command.strip(), shell=True)

def check_code(project_name):    # This function looks at the main.py (Python only), reviews it as a code reviewer/UI specialist/PM and rewrites it

    os.chdir(f"GeneratedProjects/{project_name}")
    print(f"> cd GeneratedProjects/{project_name}")

    headers = {
        'Content-Type': 'application/json',
        'X-API-Key': CLAUDE_SECRET_KEY,
        "anthropic-version": "2023-06-01"
    }

    with open("main.py", "r") as file:  # Reading the current main.py to be reviewed
        old_main_py_content = file.read()


    data = {
        'messages': [
            {"role": "user",
             "content": [
                 {"type": "text",
                 "text": code_review_prompt(old_main_py_content)
                 }, 

                ]
             }
            ],
        'model': 'claude-2.1',
        'max_tokens': 4096
    }
    
    response = requests.post(CLAUDE_API_URL, headers=headers, json=data)
    
    if response.status_code == 200:
        result = response.json()
        new_main_py_content = result['content'][0]['text']
        print(f"> Rewriting main.py for {project_name} with revisions")
        # Overwriting the main.py 
        with open("main.py", "w") as file:
            file.write(new_main_py_content)
        print(f"> Code has been reviewed and overwritten {project_name}/main.py!")

        # TODO: Need to run the code, make sure there are no errors, if so, fix them, and check again, should be a while loop until the product runs with no errors (could get expensive)
        
        return True


    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None




def main():





    # Parse the CLI arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--platform', help='The platform to generate the code for.')
    parser.add_argument('--project_name', help='The name of the project to create.')
    parser.add_argument('--prompt', help='The prompt to generate the code and commands.')
    
    args = parser.parse_args()

    platform = args.platform
    project_name = args.project_name
    prompt = args.prompt

    # Prompt the user for input, if not provided in CLI arguments
    if not platform or not project_name or not prompt:
        # run GUI
        app = QApplication(sys.argv)
        generator = AppGenerator(onSubmit=create_project)
        generator.show()
        sys.exit(app.exec_())

    # Create the project
    create_project(project_name, prompt, platform)


if __name__ == '__main__':
    main()
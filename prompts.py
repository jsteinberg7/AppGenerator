def generate_initial_prompt(platform, user_prompt):
    return f"""
                 You are an expert programmer and startup veteran. 
                 
                 {user_prompt}

                 Please generate the necessary code files and provide the commands to set up and run the project on {platform}. Ensure the code you provide is fully functional. Use a virtual environment if possible. Do not include any additional output outside of the specified format.
                 
                 Use the following format for each code file:
                 
                 ---
                 FILENAME: filename.ext
                 ---
                 Code content for the file
                 ---
                 
                 Use the following format for the commands:
                 
                 ---
                 CMDS:
                 ---
                 Command 1
                 CMD_SPLIT
                 Command 2
                 ---
                 
                 Example:
                 
                 ---
                 FILENAME: main.py
                 ---
                 import tkinter as tk
                 
                 root = tk.Tk()
                 root.title(\"My App\")
                 root.mainloop()
                 ---
                 
                 ---
                 FILENAME: style.css
                 ---
                 body {{
                    font-family: Arial, sans-serif;
                    background-color: #f0f0f0;
                 }}
                ---
                
                ---
                CMDS:
                ---
                pip3 install virtualenv
                CMD_SPLIT
                virtualenv venv
                CMD_SPLIT
                source venv/bin/activate
                CMD_SPLIT
                pip3 install tkinter
                CMD_SPLIT
                python3 main.py
                ---
                """
def code_review_prompt(file_content): # TODO: need to make this prompt much better, too vague

   return f"""
As an expert code reviewer, project manager, and UI/UX expert, please review the attached Python code and provide comprehensive feedback:

{file_content}

From the code reviewer perspective, implement new ways for improving the code structure, readability, and adherence to best practices.

From the project manager perspective, implement ways to make the code more maintainable and scalable in the long-term.

From the UI expert perspective, implement ways to enhance the user interface and user experience.

Return the new ENTIRE python script with ALL the code necessary for it to run automatically. Include comments of what was changed and tag these comments as (review 1) 

Everything that is returned is going straight into a python file, so make sure any non code is commented and handled correctly. Do not include ``` 

 """
   

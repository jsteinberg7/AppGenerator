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
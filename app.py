import re
import subprocess
import openai
import sys
import time

def generate_prompt(request):
    command = """You are an assistant for Windows. Your job is to respond to requests with complete Python code, without explanation or conclusion. Your responses should be written in Markdown, and should not include the word "Python".
    you can  generate Python code to perform various tasks. You'll do your best to provide user with the necessary code. Keep in mind that your code will be executed by the sandbox . So You have the ability to do perform any request that the user makes
    . Remember that the sandbox is controlling the system of the user .By virtue of code you will be able to interact with the system without user interaction.
    eg you can open any page on browser. shut down pc . run tests . open applications delete application everything by virtue of code.
    Please generate Python code to perform 
    the following task:
{request}
    Your code will be executed by sandbox . 
    As an example, imagine that the request is to write a Python function that takes two arguments and returns their sum. Your response should be:
    ```python
    def add_numbers(a, b):
        return a + b
    ```
    You can use command shell in python if you don't seem to have enough data on user through command shell in python you can extract and fulfill the request.
    If you don't understand the request or request is outside the scope of sandbox environment, respond with the markdown text  ```python```.
    Remember user have installed all the apps like spotify,netflix on windows. if not installed then you open it in browser.
    username is 786sa. Import all the necessary module for the request.IF module not found error through exceptional handling then install it using subprocess or command shell in python.
    Your task is to always write complete Python code that satisfies the request, without any additional information or comments. Remember to use Markdown formatting and to avoid mentioning Python in your response.
    suppose user asks you to create a flask application . assume that the user directory is empty. so you create the template ,static etc folder for it .and also create the file and save it in the respective folder.
    know that the sandbox is running on user directory. so you can create any folders or files needed.
    Please generate a response to the following request:
    """ + '"{request}"'

    return command.format(request=request)


openai.api_key = "Your api Key"
prompt = "You are a helpful assistant."
while prompt != 'stop':
    prompt = input("enter user response")

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0.1,
        messages=[
            {"role": "system",
             "content": f"{generate_prompt(prompt)}"},
            {"role": "user", "content": f"{generate_prompt(prompt)}"},
        ]
    )
    filename = "test.py"
    code = response['choices'][0]['message']['content']
    if 'python' in code:
        s = code
        code = s.replace("python","")


    #
    pattern = r"```(.*?)```"
    match = re.search(pattern, code, re.DOTALL)
    with open(filename, "w") as f:
        if code is not None:
            code = match.group(1)
            f.write(code)
        else:
            code = "#waiting"
            f.write(code)

    while True:
        try:
            subprocess.run(["python", filename], check=True)
            break
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while running the command: {e}")
            if isinstance(e.__cause__, ModuleNotFoundError):
                module_name = str(e.__cause__).split()[-1]
                print(f"Module {module_name} not found. Installing...")
                pip_install_cmd = [sys.executable, "-m", "pip", "install", module_name]
                pip_install_output = subprocess.run(pip_install_cmd, capture_output=True, text=True)
                print(pip_install_output.stdout)
                print(pip_install_output.stderr)
                print("Module installed. Retrying command...")
                time.sleep(1)
            else:
                break
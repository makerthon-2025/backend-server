from dotenv import load_dotenv
from dotenv import load_dotenv
from src.helper import file_helper
import os

def load_env():
    if os.path.exists('.env'):
        load_dotenv(dotenv_path=".env")
        __gen_env_template()
    else:
        print("not exist .env")

# ==========================================
# ================ PRIVATE FUNCTION ========

def __gen_env_template():
    file = file_helper.read_file('.env')
    lines = file.split('\n')
    output = ''

    for item in lines:
        if item != '':
            output += item.split('=')[0] + '=...\n'
        else :
            output += '\n'

    file_helper.save_file('.env.template', output)
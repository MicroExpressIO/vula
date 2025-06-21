import os
import sys
import tiktoken
from google import genai 
from google.genai import types

#from prompts.learningprompt import learningprompt
#import learningprompt as learningprompt


cur_dir = os.path.dirname(os.path.abspath(__file__))
par_dir = os.path.dirname(cur_dir)
sys.path.append(par_dir)
from config.config import config

import agent.prompts.learningprompt as learningprompt

class Task:

    def __init__(self, config):
        self.config = config
        #self.encoding = tiktoken.encoding_for_model(self.config.model)
        
    def run(self, user_input):
        
        client = genai.Client(api_key=self.config.key)

        response = client.models.generate_content(
            model=config.model,
            config=types.GenerateContentConfig(
                system_instruction=learningprompt.proj_role_Agent
            ),
            contents=user_input
        )
        
        return response
    
    #def count_token(self, test: str) -> int:
        

### debug code 
#print (config.model)
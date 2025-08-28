import os, sys

from loguru import logger
from openai import OpenAI

cur_dir = os.path.dirname(os.path.abspath(__file__))
par_dir = os.path.dirname(cur_dir)
sys.path.append(par_dir)
from config.config import config
from agent.prompts import learningprompt 

logger.add("chat.log", rotation="50 MB", retention="100 days")

URL = 'https://gpt.byteintl.net/faas-api-test/v1/'
KEY = 'empty'
MODEL_ID = 'codewise_32b_staging'

class LLM:
    def __init__(self, name, base_url, api_key, model_id):
        self.name = name
        self.api_key = api_key
        self.base_url = base_url
        self.model_id = model_id
        self.client = OpenAI(base_url=base_url, api_key=api_key)
    
    #def chat(self, system_prompt, user_message, **kwargs):
        #max_tokens = kwargs.get('max_tokens', 8192)
        #temperature = kwargs.get('temperature', 0.6)
    def chat(self, system_prompt, user_message):
        max_tokens = 8192
        temperature = 0.6
     
        messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]

        completion = self.client.chat.completions.create(
            model=self.model_id,
            messages=messages,
            temperature=temperature,
            stream=False,
            max_tokens=max_tokens
        )
        logger.info(f'Chat with {self.name} model: \n'
                    f'system_prompt: {system_prompt}, \n'
                    f'user_message: {user_message}, \n'
                    f'temperature: {temperature}, \n'
                    f'max_tokens: {max_tokens}, \n'
                    f'response: {completion}')
        return completion

if __name__ == '__main__':
    system_prompt = learningprompt.proj_role_security
    user_prompt = f"""For the security problem defeind in triple bracktiks below, focus on Debian 10 and Debain 12, finish the following:
        1. analyze the impact;
        2. describe solution and give security best practices or mitigation steps;
        3. give the remedaition scripts that can be run on both OS;
            3.1 the scripts should be version specfic for the target software, avoid using 'the latest version' or 'the latest patch';
        4. including depednecy check and verifciation for security vulnerability
        5. consider list the targer software version that fix the security proplem
        6. for debian 10, please consider reserach in 3rd parth solution (freexian is the paid 3rd party) if can not find the solution in pulbic resources
    
        security proplem: '''Debian Security Update for openssh (DLA 3694-1)''' 
        
        """
    codewise = LLM(name='codewise', base_url=URL, api_key=KEY, model_id=MODEL_ID)
    resp = codewise.chat(system_prompt=system_prompt, user_message=user_prompt)
    print(f"\nresp: {resp.choices[0].message.content}")
    print(f"\nresp_reformat: {resp.choices[0].message['content']}")


'''
 ChatCompletion(
    id='efd0de8a-6f58-4990-9ef0-b1cecc172da2', 
    choices=[
         Choice(
             finish_reason='stop', 
             index=None, 
             logprobs=None, 
             message=ChatCompletionMessage(
                 content='I am a helpful assistant.', 
                 refusal=None, role='assistant', 
                 annotations=None, 
                 audio=None, 
                 function_call=None, 
                 tool_calls=None, 
                 reasoning_content=''
                )
            )
        ], 
    created=1752696718, 
    model='codewise_32b_staging', 
    object=None, 
    service_tier=None, 
    system_fingerprint=None, 
    usage=None
)   
'''
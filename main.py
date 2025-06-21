import agent.task as Agent
from config.config import config
import agent.prompts.learningprompt as learningprompt
import utils.utils as autils

def main():
    
    agent = Agent.Task(config)
    user_prompt=learningprompt.proj_action4
       
    response = agent.run(user_prompt)
    print(f"Task response:\n {response}")
    
    autils.save_local("/home/huide/ai/vula/tests/res3.html", response.text)
    
    
    #print(f"key : {config.key} \n model: {config.model}")
    

if __name__ == "__main__":
    main()

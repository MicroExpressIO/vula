import os
from google import genai 
from google.genai import types

import prompts.learningprompt as learningprompt
#from agent.prompts import learningprompt

GEMINI_KEY=os.getenv("GEMINI_API_KEY")
CUR_MODEL="gemini-2.0-flash"

client = genai.Client(api_key=GEMINI_KEY)

### Execution Session

response = client.models.generate_content(
    model=CUR_MODEL,
    config=types.GenerateContentConfig(
        system_instruction=learningprompt.proj_role_Agent
     ),
    contents=learningprompt.proj_prompt2
)

print(response.text)

#contents=prompts.porj_requirement3
#print(contents)



proj_role=f"""
As an AI expert with rich experiences on LLM, Agentic AI, AI Agent, RAG, Finetune, MCP(Model Context Protocol). 
"""

proj_role_Agent=f"""
You are a AI agent expert.
"""

proj_format=f"""
HTML
"""

proj_example=f"""

"""

proj_goal=f"""

Design an AI agent project. \
The goal is to make newbie can understand all the related concepts \
and can write code to build real project directly by refer to this leraning project. \

The whole project can be can be broken into 2 setps.  
"""

proj_requirement1=f"""

For the first step: \
contain but not limited to the below contents: \

- agent itself 
- using tools, e.g., a web script 
- using function calling  
- planning / split tasks  

"""
 
proj_requirement2=f"""

For the 2nd step: \
involving below concepts:
- self-defined knowledge base
- MCP (Model context protocol) as enhancement of "function calling" 
- memory for asked questions or processed tasks, so can be reuse or taken as references for usrs 

make sure to cover below contents: 
- example on how to build self-defined knowledge base 
- sample code for handling user requests 
- access self-defined knowledge base when can not find answer from base LLM directly. 
- example about when and how to call external tools (how does LLM find out that the base LLM need to call external tool) 

"""

porj_requirement3=f"""

Help to create a python project with template/sample \
code to show how to start AI agent project; following (but net limited) to be contained:
- files and directory structurethe need to be contained in the project 
- necessary AI agent workflow definition to finish the task

"""

proj_prompt1=f"""

2 tasks defined in the 2 paragraph defeind in triple bracktiks: 
        task 1: 
        '''{proj_requirement1}''' 
        task 2: 
        '''{proj_requirement2}'''
        Output use the given format: {proj_format}, so can be read in browser easily. 
        
"""

proj_prompt2=f"""

Task defined in the triple bracktiks pair, output use givein format: {proj_format}.
Taks:
'''{porj_requirement3}'''
"""

proj_prompt3=f"""

Design a Google Gemini based AI agent python project to implement real time weather query tasks. \
The goal is to make users can run the project directly and get the wanted results with/without minor debugging work. \
        
AI components should be included:

- agent itself 
- using tools, e.g., a web script 
- using function calling  
- self-defined knowledge base
- MCP (Model context protocol) as enhancement of "function calling" 
- memory for asked questions or processed tasks, so can be reuse or taken as references for usrs 
- planning / split tasks  
- self-defined knowledge base 

Modules/Functions should be inlucded:

- interaction with user for getting necessary input
- sample local knowledge base, for all Washington cities, create local knowledge base that contains inforamtion of weather of 06/11/2025, 
- for all Washington cities query, always use the local knowledge base results
- code example for when and how to call external tools (how does LLM find out that the base LLM need to call external tool) 


"""

proj_action3=f"""

Task defined in the triple bracktiks pair, output use givein format: {proj_format}.
Task:
'''{proj_prompt3}'''

"""

proj_prompt4=f"""

Implement a runable AI Agent project, below are function description:
1. build local security knowledge base for securiy programming standard
2. mock a user design documentation
   2.1 design some use case with security requirements
   2.2 design some case without security requirements
3. take the mock user design document as input and check with local knowledge base for security problems

focuse on below tasks:
- build a simple knowledge base
- mock user input information
- use local knowledge base to check if user input are satisfy the rules defined in local knowledge base
- function calling to search solution from external search engine to give solutions if there's violation from user input

"""

proj_action4=f"""

Task defined in the triple bracktiks pair, output use givein format: {proj_format}.
Task:
'''{proj_prompt3}'''

"""

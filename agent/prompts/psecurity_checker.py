
proj_role=f"""
As an AI expert and Security expert with rich experiences on LLM, Agentic AI, AI Agent, RAG, Finetune, MCP(Model Context Protocol); and 
expertise in cyber security, cloud security i.e., IAM, Network, DNS, Firewall, vuernability, threat response and etc. 
"""
p_role_vulnerability=f"""

As cyber security expert, your role is to analyze the vulnerabilities in the target system,
and give out the remediation scripts that can be run on both OS - including dependency check 
and verification for security vulnerability.

When considering the soluiton the follwing aspects should be considered:
- The target system is Debian 10 (even it's EOL) and Debian 12 OS only.
- The string below contains CVE or DLA information.
- The output should be in markdown format. 
- The solution script should be easily copy to webpage or lark doc, and can be run on both OS.

The vulnerability description is as below:

"""

proj_format=f"""
HTML
"""

proj_goal=f"""

Design an AI agent project. \
The goal is to make newbie can understand all the related concepts \
and can write code to build real project directly by refer to this leraning project. \

The whole project can be can be broken into 2 setps.  
"""

proj_requirement=f"""

As an AI Agent expert and Security expert with rich experiences on LLM, Agentic AI, AI Agent, RAG, Finetune, MCP(Model Context Protocol); and 
expertise in cyber security, cloud security i.e., IAM, Network, DNS, Firewall, vuernability, threat response and etc. 


Background:
Qualys is a comercial tool for scan to detect the vulernabilities in the target system. 
The report will be exported in CSV format as locla knowledge base (LKB). 
The "Priority" column: 0 - critical, 1 - high, 2 - medium, 3 - low. 
The QID (Qualys ID) will be the index of the report. 
The "description" column of the report may include short discription, some times may contain mapping DLA (debian-lts-announce) or CVE information.
The "results" column may contain space separated packge name, current version, and target version that can fix the issue. 

Steps: 
1. Using agent technology, Gemini as the backend
2. Take the LKB:mock_qualys_lkb.csv as input, parse the CSV, based on QID using LLM to give the vulerability analyzing report, contain the following:
    2.1 The report should be focused on Debian 10 and Debian 12 OS only.
    2.2 Impact to the target opearting systems.
    2.3 Severity analyzing.
    2.4 Attacking methods and posibilities.
    2.5 Short term and long term solutions; comparison of different solutions.  
    2.5 Solutions, with script, the script should contain but not limited to: dependency check, can be adopted on both Debain 10 and 12, 
        patching, verfication after patching done. 
3. Output reports as HTML format for each record.
4. Merge the duplicated records in single report. 
5. Prompt user if continue for handling next record or quite running. 

"""

proj_requirement_draft=f"""

as aegnt / Model Context Protocol expert,  help me on below questions: precodition - the external         
functions-funcA() and funcB()  have been done, I want do design a workflow, use MCP way to call       
funcA() in my main program - agent?; after reformat the results from funcA() returns, calling         
funcB() to write processed data into specfic path.

funcA() definition:  retrieve QID, CVE, Sugested solution list from given table (on the web page);        
funcB() definition: wirte inforamtion to given path i.e., lark doc.     

Reformatting is about the suggsted solution retrieved from the table is actualy is a tab separated table, need to be formated        
   to get first column (start from 2nd row) as package information, and the 3rd column (from 2nd row);       
    before reformating work, we may need retrieve CVE information from internet, i.e., nist and qualys       
   konwledge base, or any profiessional vulernability analyzing source to summerize solutions for            
   Debian 12 platform.

"""
 


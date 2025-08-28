
p_func_cvs=f"""

create a python fucntion with below requirements:

1. function name: csv_parser_v2
2. function input: file path, max line amount to be processed.
3. take the 1st line as keys for the coming lines.
4. fields are comma separated but some field may contain new line, in such case the field may braced by double quote.
5. take each line as dictionary with key/value format.
6. print each key of each line in function
7. take "../data/all.IECS.no.java.mysql.glibc.0701.csv" as input csv file in example code

"""

proj_role_security=f"""

create a workflow plan that can finish below project goals and satisfy the given requirements:

I. goals:
1. from given URL to retrieve Qualys scan report  
2. filter the report and handle user defined scope - by filtering specfic fileds
3. for chosen scope, group / summary vulnerability situations - impacted hosts amount, \
    priority, time plan (will need be retrieved from the fileds of report and pre-processed)
4. based on 3. work on high risk issue; by given column - risk info, agent to call LLM to \
    do online information collection, research and give the vulnerability analyzing, impact \
    analysis and solution summarizion - need to contain the code level solution and \
    verfication mehotds.
5. based on 4., generate report and write to online wiki system (larksuite).
Notes:
- the Qualys scan report can be queryied through SQL API, with given SQL query.
- the Qualys scan report should be filtered by given fields, such as host, vulnerability, risk level, \
  time plan, etc.
- the generated report should be in markdown format, with code block for code and command.
- the generated report should be written to larksuite wiki system, with given API.
- the generated report should be able to written to a specific page, with given page id.
- the generated report should be able to written to a specific folder, with given folder id.
- the generated report should be able to written to a specific user, with given user id.
- the generated report should be able to written to a specific space, with given space id.

II. requirements
1. plan should contain mulitple phases to archieve goals step by step
    - each phase should be able to be executed by a single agent
    - the Qualys report could be CSV file in beging phase, but could be changed to \
      other format in later phase, such as JSON, XML, or SQL query from online system.
    - the agent should be able to handle the file format change and adapt to it.

2. define each phase with reasonable details - could be design documentations, executable python code \
    functions, tool-set used, integartion with other systems

"""

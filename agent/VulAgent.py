
import os
import sys
import re

import pandas as pd

from openai import OpenAI

from google import genai
from google.genai import types
import logging

from datetime import datetime

from byteplussdkarkruntime import Ark

cur_dir = os.path.dirname(os.path.abspath(__file__))
par_dir = os.path.dirname(cur_dir)
sys.path.append(par_dir)
from config.config import config
from utils.fileops import FOPS
from agent.prompts import learningprompt 
from agent.prompts import psecurity_checker
import utils.fileops as fops
import utils.larkApp as larkAPP
#import prompts.learningprompt as learningprompt

# Setup logging
#log_file = f"security_review_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
#logging.basicConfig(filename=log_file, level=logging.INFO, 
#                    format='%(asctime)s - %(levelname)s - %(message)s')
logging.basicConfig(level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        )

###############################
### input data processing
###############################
class VulaSelector():
    def __init__(self, priority: str, dataPath: str):
        self.priority = priority
        self.dataPath = dataPath

    #def select_vulnerabilities_by_priority(file_path: str, priority_col='Risk Rating', min_priority='High') ->pd.DataFrame:
    #def select_vulnerabilities_by_priority(self, dfset: pd.DataFrame, priority_col='Risk Rating', min_priority='High') -> pd.DataFrame:
    def select_vul_by_priority(self, v_type:str, dfset: pd.DataFrame, priority_col='Risk Rating') -> pd.DataFrame:
        # filter the specified priority column 
        priority_df = dfset[dfset[priority_col] == self.priority]      
        if priority_df.empty:
            logging.info(f"No vulnerabilities found with priority '{self.priority}'.")
            return

        logging.debug(f"Found {len(priority_df)} vulnerabilities with priority '{self.priority}'.")
        if v_type == "QID" or v_type == "qid":
            # group by QID for the filtered DataFrame
            qid_df = priority_df.groupby('QID').first().reset_index()
            logging.info(f"Grouped vulnerabilities by QID, total unique QIDs: {len(qid_df)}")
            return qid_df
        elif v_type == "CVE" or v_type == "cve":
            # group by QID for the filtered DataFrame
            cve_df = priority_df.groupby('CVE').first().reset_index()
            logging.info(f"Grouped vulnerabilities by CVE, total unique CVEs: {len(cve_df)}")
            return cve_df
    
    def read_csv_file(self, file_path: str) -> pd.DataFrame:
        try:
            # Read the CSV file into a DataFrame
            df = pd.read_csv(file_path)

            ### debugging print statements
            rowcount = len(df)
            logging.debug(f"Total rows in CSV: {rowcount}")
            logging.debug(f"Columns in CSV: {df.columns.tolist()}")
            #print(f"First few rows:\n{df.head()}")

            # Check if the DataFrame is empty
            if df.empty:
                logging.warning("CSV file is empty or only contains headers.")
                return
            
        except FileNotFoundError:
            logging.error(f"Error: The file '{file_path}' was not found.")
            return
        except pd.errors.EmptyDataError:
            logging.error(f"Error: The file '{file_path}' is empty and could not be parsed.")
            return
        except Exception as e:
            logging.exception(f"An unexpected error occurred: {e}")
            return

        return df

    def gen_csv_by_qid(self, dframe: pd.DataFrame, qid: str):
        df_qid = dframe[dframe['QID'] == qid]
        if df_qid.empty:
            logging.warning(f"No records found for QID: {qid}")
            return 
        else:
            logging.debug(f"\nFound {len(df_qid)} records for QID: {qid}")
            logging.debug(f"\nQID,Priority,Alarm Name,IP,Source,OS,Solution")
            df_csv = df_qid[['QID', 'Risk Rating', 'Alarm Name', 'IP', 'Source', 'OS']]
            df_csv['Solution'] = None
            fd_csv = f"./output/{qid}-{df_csv.iloc[0, 2]}.csv"
            if os.path.exists(fd_csv):
                logging.warning(f"File {fd_csv} already exists. Skipping write operation.")
                return
            df_csv.to_csv(fd_csv, index=False)

            """
            for i, row in df_qid.iterrows():
                print(f"{row['QID']},{row['Risk Rating']},{row['Alarm Name']},{row['IP']},{row['Source']},{row['OS']}, ")
            return 
            """

    def retrieve_host_info(self, dframe: pd.DataFrame, dframe_target: pd.DataFrame) -> pd.DataFrame:
        for i, row in dframe_target.iterrows():
            self.gen_csv_by_qid(dframe, row['QID'])

##############################
### LLM adapter
##############################
#class VulaAnalyzeAgent:
class LlmAdapter:
    def __init__(self, myModel: str):
        self.model = myModel

    def call_openai_solution(self, prmpt_system: str, prmpt_user: str) -> str:
        try:
            response = OpenAI.ChatCompletion.create( 
                model="gpt-4-0613",
                # messages=[
                #     {"role": "system", "content": "You are a security advisor."},
                #     {"role": "user", "content": f"Give security best practices or mitigation steps for: {issue}"}
                # ],
                messages=[
                    {"role": "system", "content": prmpt_system},
                    {"role": "user", "content": prmpt_user}
                ],
                temperature=0.3,
            )
            return response.choices[0].message['content']
            #return response.choices[0].message.content
        except Exception as e:
            return f"[OpenAI Error] {str(e)}"
        
    def call_codewise_solution(self, prmpt_system: str, prmpt_user: str) -> str:
        max_tokens = 8192
        temperature = 0.6
        messages = [
                    {"role": "system", "content": prmpt_system},
                    {"role": "user", "content": prmpt_user}
                ]

        try:
            client = OpenAI(base_url=config.codewise_url, api_key=config.codewise_key)
            response = client.chat.completions.create(
                model=config.codewise_model,
                messages=messages,
                temperature=temperature,
                stream=False,
                max_tokens=max_tokens
            )
            #return response.choices[0].message['content']
            return response.choices[0].message.content

        except Exception as e:
            return

    def call_seed16_solution(self, prmpt_system: str, prmpt_user: str) -> str:
        try:
            client = OpenAI(
                base_url=config.doubao_url,
                api_key=config.doubao_key
            ) 
            response = client.chat.completions.create(
                model=config.seed16_model,
                    messages=[
                        {"role": "system", "content": prmpt_system},
                        {"role": "user", "content": prmpt_user}
                    ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"[Error fetching solution from seed 1.6]: {str(e)}"
    
    def call_skylark_solution(self, prmpt_system: str, prmpt_user: str) -> str:
        try:
            client = OpenAI(
                base_url=config.doubao_url,
                api_key=config.doubao_key
            ) 
            response = client.chat.completions.create(
                model=config.skylark_pro,
                    messages=[
                        {"role": "system", "content": prmpt_system},
                        {"role": "user", "content": prmpt_user}
                    ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"[Error fetching solution from skylark]: {str(e)}"


    def call_deepseek_solution(self, prmpt_system: str, prmpt_user: str) -> str:
        try:
            client = Ark(
                    api_key=config.bd_key,
                    base_url="https://ark-ap-southeast.byteintl.net/api/v3",
                )

            response = client.chat.completions.create(
                model=config.bd_model,
                messages=[
                    #{"role": "system", "content": "You are a security compliance checker."},
                    {"role": "system", "content": prmpt_system},
                    {"role": "user", "content": prmpt_user}
                ],
                stream=False
                )
            return response.choices[0].message.content

        except Exception as e:
            return f"[Error fetching solution from DeepSeek]: {str(e)}"

    def call_gemini_solution(self, prmpt_system: str, prmpt_user: str) -> str:
        try:
            client = genai.Client(api_key=config.gemini_key)
            
            #user_content = f"{psecurity_checker.p_role_vulnerability} {issue}"
            response = client.models.generate_content(
                model=config.gemini_model,
                config=types.GenerateContentConfig(
                    system_instruction=prmpt_system,
                    temperature=0.6,
                    max_output_tokens=8192
                ),
                contents=prmpt_user
            )
            return response.text
        except Exception as e:
            return f"[Error fetching solution from Gemini]: {str(e)}"

    #def external_search_solution(self, issue: str) -> str:
    def get_solution(self, issue: str) -> str:
        #system_prompt = learningprompt.proj_role_security
        system_prompt = psecurity_checker.p_role_vulnerability
        
        ### ToDo:  move the prompt to outter prompt class/dictionary
        user_prompt = f"""For the security problem defined in triple bracktiks below, focus on Debian 10 and Debain 12, finish the following:
            1. analyze the impact;
            2. describe solution and give security best practices or mitigation steps;
            3. give the remedaition scripts that can be run on both OS;
                3.1 the scripts should be version specfic for the target software, avoid using 'the latest version' or 'the latest patch';
            4. including depednecy check and verifciation for security vulnerability
            5. consider list the targer software version that fix the security proplem
            6. for Debian 10, please consider research in 3rd party solution (Freexian is the paid 3rd party) if can not find the solution in public resources
        
            security problem: '''{issue}''' 
            
            """
        
        if self.model == "openai":
            return self.call_openai_solution(system_prompt, user_prompt)
        elif self.model == "gemini":
            return self.call_gemini_solution(system_prompt, user_prompt)
        elif self.model == "bd_deepseek":
            return self.call_deepseek_solution(system_prompt, user_prompt)
        elif self.model == "codewise":
            return self.call_codewise_solution(system_prompt, user_prompt)
        elif self.model == "seed16":
            return self.call_seed16_solution(system_prompt, user_prompt)
        elif self.model == "skylark_pro":
            return self.call_skylark_solution(system_prompt, user_prompt)
        else:
            return f"[Manual Lookup] {issue} => Please consult OWASP guidelines."

##############################
### Agent / LLM calling
##############################
class VulaAnalyzeAgent:
    def __init__(self, myModel: str):
        self.model = myModel
       
    def analyze_vul(self, issue: str) -> str:
        llmAdapter = LlmAdapter(self.model)
        return llmAdapter.get_solution(issue)

    def gen_solution_by_qid(self, dframe: pd.DataFrame, qid: str) -> str:
        df_qid = dframe[dframe['QID'] == qid]
        if df_qid.empty:
            logging.warning(f"No records found for QID: {qid}")
            return
        issue = re.sub(r"\[.*?\]", "", df_qid.iloc[0, 2])
        logging.debug(f"\nIssse to be solved: {issue}")
        pmpt_sol = f""" Security issue: {issue}"""
        solution = self.external_search_solution(pmpt_sol, self.model)
        logging.debug("Suggestion:", pmpt_sol)
        logging.debug("Solution:", solution)
        fops = FOPS()
        fops.write_if_not_exists(f"./output/codeview-{df_qid.iloc[0, 0]}-{issue}.md", solution)
        return

    def gen_solution_by_desc(self, desc: str) -> str:
        if not desc:
            logging.warning("No description provided for the vulnerability.")
            return
        pmpt_sol = f""" Security issue: {desc}"""
        solution = self.external_search_solution(pmpt_sol, self.model)
        logging.debug("Suggestion:", pmpt_sol)
        logging.debug("Solution:", solution)
        fops = FOPS()
        fops.write_if_not_exists(f"./output/{desc}.md", solution)



####################################
### .setup runtime environment
### .call tools to execte the tasks - handle_vuls()
####################################
class VulaOperator:
    def __init__(self):
        self.vulaConfig = {}

        '''{   
            "priority": priority, 
            "vultype" : VulType,
            "model" : method,
            "inputfile" : file_path,
            "writelocal" : writeLocal,
            "parentpage" : target_parent_page,
            "vul" : []
        }'''
    
    def runtime_config(self, VulType:str, priority: str,  method: str = "gemini"):
        target_prioity = priority
        ### retrieve target records 
        if VulType == "CVE" or VulType == "cve": 
            file_path = config.cve_path
        elif VulType == "QID" or VulType == "qid":
            file_path = config.data_path
        else: 
            file_path = " "

        if priority == "High":
            target_parent_page = config.page_doubao_high
            #if cve.lower() in VulType.lower():
            if "cve" in VulType.lower():
                target_parent_page = config.pagetoken_cve_high
        elif priority == "Medium":
            target_parent_page = config.page_doubao_medium # target parent page 
            if "cve" in VulType.lower():
                target_parent_page = config.pagetoken_cve_medium
        elif priority == "Low":
            target_parent_page = config.pagetoken_low
            if "cve" in VulType.lower():
                target_parent_page = config.pagetoken_cve_low

        writeLocal = False

        model = method

        self.vulaConfig = {
            "priority": priority,
            "vultype" : VulType,
            "model" : method,
            "inputfile" : file_path,
            "writelocal" : writeLocal,
            "parentpage" : target_parent_page,
            "vul" : []
        }
        logging.debug(self.vulaConfig)
        #return
    
        #if VulType != 'CVE' or VulType != 'QID' or VulType != 'qid' or VulType != 'cve' :
        if VulType not in {'CVE', 'QID', 'qid', 'cve'}:
            self.vulaConfig["vul"].append(VulType)
            return
        
        ## retrieve vul list
        vulaSelector = VulaSelector(target_prioity, file_path)
        df = vulaSelector.read_csv_file(file_path)
        if df is None or df.empty:
            logging.warning("No data to process.")
            return
        target_df = vulaSelector.select_vul_by_priority(VulType, dfset=df, 
                                            priority_col='Risk Rating')
        if target_df is None or target_df.empty:
            logging.debug("No vulnerabilities found with the specified priority.")
            return
        
        for i, row in target_df.iterrows():
            if VulType == "QID" or VulType == "qid":
                desc = re.sub(r"\[.*?\]", "", row['Alarm Name'])
                filePrefix=f"{row['QID']}-{desc}"
            elif VulType == "CVE" or VulType == "cve":
                filePrefix=row['CVE']
            filePath=f"./output/{filePrefix}.md"

            ## add into vulaConfig
            self.vulaConfig["filepath"]=filePath
            self.vulaConfig["vul"].append(filePrefix)

        #print(f"vulaConfig: {self.vulaConfig}")

    def handle_vuls(self):
        vaa = VulaAnalyzeAgent(self.vulaConfig["model"])
        fops = FOPS()

        ## build the existed wiki page list 
        sum_pagelist = []
        page_token = None
        has_more = True
        larkapp = larkAPP.LarkAPP(config.bot_id, config.bot_secret, self.vulaConfig["parentpage"])

        # "has_more" means if there's more sibling pages to be handled; 
        # "page_list" not None also indicate there's more siblings
        while has_more:
            has_more, page_token, page_list = larkapp.listNodeOfWikiSpace(self.vulaConfig["parentpage"], page_token)
            if page_list is None:     # for first round this is necessary
                break
            sum_pagelist.extend(page_list)

        for vul in self.vulaConfig["vul"]:
            ### Upload to Lark wiki if not existing
            if vul not in sum_pagelist:
                logging.info(f"Investigating: {vul}")
                ## get solution

                #print(f"Alarm Name: {row'['Alarm Name']}")
                pmpt_sol = f""" Security issue: {vul}"""
                solution = vaa.analyze_vul(pmpt_sol)

                if self.vulaConfig["writelocal"]: # Write solution to local output
                    fops.write_if_not_exists(self.vulaConfig["filepath"], solution)

                ## create wikipage
                larkapp.createWikiPage(vul, solution)
            else:
                logging.warning(f"Wiki existed already, PASS")
            

#class VulaManager:
def getDlaList(file_path: str, priority: str) -> list:
    target_prioity = priority

    ### retrieve records from CSV
    vulaSelector = VulaSelector(target_prioity, file_path)
    df = vulaSelector.read_csv_file(file_path)

    if df is None or df.empty:
        logging.warning("No data to process.")
        return
    target_df = vulaSelector.select_vulnerabilities_by_priority(dfset=df, 
                                        priority_col='Risk Rating')
    if target_df is None or target_df.empty:
        logging.warning("No vulnerabilities found with the specified priority.")
        return
    
    ret = []
    for i, row in target_df.iterrows():
        desc = re.sub(r"\[.*?\]", "", row['Alarm Name'])
        file_title=f"{row['QID']}-{desc}"
        #dla_pattern = re.compile(r'\b(DLA)\s(\d{4})-(\d{1})\b')
        cve_pattern = re.compile(r'\b(CVE)-(\d{4})-(\d{4,5})\b')
        #tmpRe = dla_pattern.search(file_title)
        tmpRe = cve_pattern.search(file_title)
        if not tmpRe:
            continue
            #logging.warning(f" temRe is None")
        logging.info(f" tmpRe: {tmpRe.group()}")
        ret.append(tmpRe.group())
    
    return ret


def dmain():
    #ai_triage_vulnerability("CVE", config.target_priority, config.ai_provider)
    #runtime_config("CVE-2025-27363", config.target_priority, config.ai_provider)
    insVulaOperator = VulaOperator()
    
    #insVulaOperator.runtime_config("CVE-2024-2961", config.target_priority, config.ai_provider)
    insVulaOperator.runtime_config("CVE-2024-53104", config.target_priority, config.ai_provider)
    insVulaOperator.handle_vuls()

    ### gen cve list from given csv file
    '''
    ret = getDlaList(config.data_path, "Medium")
    if ret:
        print(f"ret: {ret}")
    '''

def main():
    from agent.prompts.pmpt_vul import PromptVul

    pmptVul = PromptVul("coatch", "train", "CVEasdfasdf")

    ret = pmptVul.get_prompt("req")
    #logging.debug(f"{pmptVul.prompt["requriement"]}")
    logging.debug(f"{ret}")
    
if __name__ == '__main__':
    main()

    
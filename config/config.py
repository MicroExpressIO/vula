import yaml

class Config:
    def __init__(self, config_path="/Users/bytedance/ai/vula/config/config.yaml"):
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
            
        self.projct = config['project']
        self.ai_provider = config['ai_provider']
        self.data_path = config['data_path']
        self.cve_path = config['cve_path']
        self.target_priority = config['target_priority']

        
        self.gemini_key = config['llm']['gemini_key']
        self.gemini_model  = config['llm']['gemini_model']
        
        self.bd_key = config['llm']['bd_key']
        self.bd_model  = config['llm']['bd_model']

        self.codewise_url = config['llm']['codewise_url']
        self.codewise_key = config['llm']['codewise_key']
        self.codewise_model = config['llm']['codewise_model']
        
        self.gpt_key = config['llm']['gpt_key']
        self.gpt_model  = config['llm']['gpt_model']
        
        ### bytedance LLM 
        self.doubao_url = config["llm"]["doubao_url"]
        self.doubao_key = config["llm"]["doubao_key"]
        self.seed16_model = config["llm"]["seed_16"]
        self.skylark_pro = config["llm"]["skylark_pro"]

        ### lark related
        self.bot_id = config["lark"]["VulaBotID"]
        self.bot_secret = config["lark"]["VulaBotSecret"]
        self.pagetoken_doubao = config["lark"]["pagetoken_doubao"]
        self.page_doubao_high = config["lark"]["page_doubao_high"]
        self.pagetoken_cve_high = config["lark"]["pagetoken_cve_high"]
        self.page_doubao_medium = config["lark"]["page_doubao_medium"]
        self.pagetoken_cve_medium = config["lark"]["pagetoken_cve_medium"]
        self.pagetoken_low = config["lark"]["pagetoken_low"]
        self.pagetoken_cve_low = config["lark"]["pagetoken_cve_low"]
        self.pagetoken_codewise = config["lark"]["pagetoken_codewise"]
        


config = Config()

#print(config.key)


# tika backend:  https://bytedance.larkoffice.com/wiki/Jtmvwm5HeiiLbEks7uDcmW4dnke
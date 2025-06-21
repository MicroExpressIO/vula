import yaml

class Config:
    def __init__(self, config_path="/home/huide/ai/vula/config/config.yaml"):
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
            
        self.projct = config['project']
        self.ai_provider = config['ai_provider']
        
        self.key = config['task']['gemini_key']
        self.model  = config['task']['gemini_model']

config = Config()

#print(config.key)

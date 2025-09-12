from configparser import ConfigParser

class Config:
    def __init__(self, config_file="/Users/balajinagarajan/Documents/workspace/Gen AI RoadMap/AI Agent Projects/src/langgraphagenticai/ui/ui_config.ini"):
        self.config = ConfigParser()
        self.config.read(config_file)

    def get_llm_options(self):
        return self.config['DEFAULT'].get('LLM_OPTIONS').split(', ')
    
    def get_usecase_options(self):
        return self.config['DEFAULT'].get('USECASE_OPTIONS').split(', ')
    
    def get_ollama_model_options(self):
        return self.config['DEFAULT'].get('OLLAMA_MODEL_OPTIONS').split(', ')
    
    def get_page_title(self):
        return self.config['DEFAULT'].get('PAGE_TITLE')
    
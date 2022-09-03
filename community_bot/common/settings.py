from genericpath import isfile
import logging
from jaraco.docker import is_docker
from .api import API
import os

class Settings():
    _bot_name : str
    _bot_version : str
    _bot_author: str
    _bot_prefix: str
    _bot_token: str
    _bot_log_level : str
    _bot_log_file : str
    _bot_api : API
    _bot_language : str
    _bot_modules : list
    
    def __init__(self):
        self._bot_version = "0.0.1 - dev"
        self._bot_author = "Immervoll"
        if is_docker:
            self._bot_name = os.getenv('BOT_NAME', 'CommunityBot')
            self._bot_prefix = os.getenv('BOT_PREFIX', '!')
            self._bot_token = os.getenv('BOT_TOKEN', '')
            self._bot_log_level = os.getenv('BOT_LOG_LEVEL', 'INFO')
            self._bot_log_file = os.getenv('BOT_LOG_FILE', 'community-bot.log')
            self._bot_api = API(os.getenv('API_HOST', 'http://localhost:8000'), os.getenv('API_TOKEN', ''))
            self._bot_language = os.getenv('BOT_LANGUAGE', 'en')
            self._bot_modules = os.getenv('BOT_MODULES', 'general,').split(',')
            
        elif os.isfile('settings.yml'):
            import yaml
            with open('settings.yml', 'r') as f:
                settings = yaml.safe_load(f)
                self._bot_name = settings['name']
                self._bot_prefix = settings['prefix']
                self._bot_token = settings['token']
                self._bot_log_level = settings['log']['level']
                self._bot_log_file = settings['log']['file']
                self._bot_api = API(settings['api']['host'], settings['api']['token'])
                self._bot_language = settings['language']
                self._bot_modules = settings['modules']
        
        else:
            raise FileNotFoundError('settings.yml not found')
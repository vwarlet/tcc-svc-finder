# -*- coding: utf-8 -*-
'''This module contains the singleton for your application configuration'''

import json
import os
import sys
import requests
from labio.logging import pcf_logger
from labio.utils import decode

class AppConfig():
    '''Loads configuration from PCF, or from app.dev.config when running outside PCF'''

    DB_SERVER = 'sqlite:///localdb.db'
    #DB_SERVER = 'mysql+mysqlconnector://root:root@localhost/localdb'
    #DB_SERVER = 'mysql+pymysql://root:root@localhost/localdb'    

    JWT_KEY = None
    OAUTH_DOMAIN = None
    OAUTH_CLIENT_ID = None
    OAUTH_CLIENT_SECRET = None
    OAUTH_PUBLIC_KEY = None
    OAUTH_ALG = None
    
    SEND_FILE_MAX_AGE_DEFAULT = 31536000

    REDIS_HOST = None
    REDIS_PWD = None
    REDIS_PORT = None

    RMQ_HOST = None
    RMQ_VHOST = None
    RMQ_PORT = None
    RMQ_USER = None
    RMQ_PWD = None

    def __init__(self):
        # Check if we are running on PCF
        pass

class AppTestConfig(AppConfig):
    '''Use this class to define variables used specifically when Unit Testing'''

    def __init__(self):
        super().__init__()
        self.DB_SERVER = 'sqlite:///:memory:'

start_script = sys.argv[0]
if start_script.endswith('visualstudio_py_testlauncher.py') or start_script.endswith('tests.py'):
    config = AppTestConfig()
    pcf_logger.info('Starting with test config')
else:
    config = AppConfig()

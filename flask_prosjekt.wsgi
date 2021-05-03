#!/usr/bin/python
import os
basedir = os.path.abspath(os.path.dirname(__file__))
activate_this = f'{basedir}/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

import sys
import logging
from dotenv import load_dotenv

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, basedir)
load_dotenv(dotenv_path=f"{basedir}/.env")

from app import create_app

application = create_app("production")

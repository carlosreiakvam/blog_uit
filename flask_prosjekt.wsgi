#!/usr/bin/python
activate_this = '/stud/tyt005/public_html/flask_prosjekt/flask_prosjekt/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

import sys
import logging
from dotenv import load_dotenv

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/stud/tyt005/public_html/flask_prosjekt")
sys.path.insert(1, "/stud/tyt005/public_html/flask_prosjekt/flask_prosjekt")
load_dotenv(dotenv_path="/stud/tyt005/public_html/flask_prosjekt/flask_prosjekt/.env")

from flask_prosjekt.app import create_app

application = create_app("production")

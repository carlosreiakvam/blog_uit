import flask
from flask import Blueprint, render_template, abort, flash, url_for, redirect, request
from flask_login import login_user
from urllib.parse import urlparse, urljoin
from models.bruker import Bruker
from blueprints.auth.forms import LoginForm

router = Blueprint('hovedside', __name__, url_prefix="/hovedside")


@router.route("/")
def example():
    return "hello from hovedside"


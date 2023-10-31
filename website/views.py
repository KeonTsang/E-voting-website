from flask import Flask, Blueprint, request, redirect, url_for, render_template
from website import views

app = Flask(__name__)


views = Blueprint('views', __name__)


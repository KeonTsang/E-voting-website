# main.py
from flask import Flask
from website import views
from website import templates
from website.__init__ import create_app
from os import path
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)


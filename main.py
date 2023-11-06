# main.py
from flask import Flask
from website import views
from website import templates
from website.__init__ import create_app
from os import path

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)


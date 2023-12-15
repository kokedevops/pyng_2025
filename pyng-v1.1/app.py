'''Runs the web server on localhost, port 80'''
from pyng import app

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=80, use_reloader=True)

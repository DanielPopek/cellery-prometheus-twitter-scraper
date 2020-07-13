from flask import Flask, Response
from registry import *

app = Flask(__name__)

@app.route('/test/')
def test():
    return 'test response'

@app.route('/metrics')
def metrics():
    return Response(generate_latest(REGISTRY), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
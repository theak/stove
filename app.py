from flask import Flask, request, Response

from save import save

app = Flask(__name__)

@app.route('/on', methods=['GET'])
def on():
  save('on')
  return 'OK'

@app.route('/off', methods=['GET'])
def off():
  save('off')
  return 'OK'

@app.route('/', methods=['GET'])
def root():
  return 'OK'

if __name__ == "__main__":
    app.run(host='0.0.0.0')
from flask import Flask, request, Response

from save import save
from get_bounds import get_bounds
from configure_android_cam import configure

app = Flask(__name__)

@app.route('/on', methods=['GET'])
def on():
  save('on')
  return 'OK'

@app.route('/off', methods=['GET'])
def off():
  save('off')
  return 'OK'

@app.route('/configure_cam', methods=['GET'])
def configure_cam():
  status_code = configure()
  return 'OK' if status_code == 200 else ('Fail: %d' % r, 500)

@app.route('/callibrate', methods=['GET'])
def callibrate():
  success = get_bounds()
  return 'OK' if success else 'Failed to find QR code'

@app.route('/', methods=['GET'])
def root():
  return 'OK'

if __name__ == "__main__":
    app.run(host='0.0.0.0')
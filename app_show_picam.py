# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2 as cv
from flask import Flask, render_template, Response

app = Flask(__name__)
 
 # initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
  
# allow the camera to warmup
time.sleep(0.1)
   
def gen(camera):
    """Video streaming generator function."""
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # 獲取 NumPy 陣列表示的影像
        image = frame.array

        # 轉換成 JPEG 格式
        _, jpeg = cv.imencode('.jpg', image)

        # 清除串流以準備下一個影格
        rawCapture.truncate(0)

        # 回傳 JPEG 影像串流
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)

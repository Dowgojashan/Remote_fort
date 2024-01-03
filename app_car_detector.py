import time
import numpy as np
import cv2 as cv
from flask import Flask, render_template, Response
from picamera.array import PiRGBArray
from picamera import PiCamera
import basic.config as cfg
import basic.visualizer as vis
from basic import imgproc, helper
from basic.logger import Logger
from basic.cardetector import cardetector

app = Flask(__name__)

LOG = Logger('app_car_detector')

# 初始化 PiCamera
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

# 等待相機預熱
time.sleep(0.1)

# 初始化車輛偵測器
car_detector = cardetector()

def gen():
    """Video streaming generator function."""
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # 獲取 NumPy 陣列表示的影像
        image = frame.array

        # 轉換成 JPEG 格式
        _, jpeg = cv.imencode('.jpg', image)

        # 清除串流以準備下一個影格
        rawCapture.truncate(0)

        # 進行車輛偵測
        scores, bboxes = car_detector.detectcar(image, def_score=0.5)

        if len(bboxes):
            # 修改類別名稱為 'car'
            image = vis.plotBBoxes(image, bboxes, len(bboxes) * ['car'], scores)

        # 回傳 JPEG 影像串流
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def main():
    LOG.info('Raspberry Pi: Car Detection and PiCamera Streaming')

    # 開啟 Flask 伺服器，同時執行 PiCamera 影像串流
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)

if __name__ == '__main__':
    main()

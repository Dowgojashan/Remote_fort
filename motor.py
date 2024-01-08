import RPi.GPIO as GPIO
from time import sleep
from flask import Flask, render_template, Response, request
from camera_pi import Camera
from concurrent.futures import ThreadPoolExecutor
import threading
import model
import cv2
import numpy as np

left_pin = 23
right_pin = 24
reload_pin1 = 6
reload_pin2 = 26
shoot_pin = 16

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(left_pin, GPIO.OUT)
GPIO.setup(right_pin, GPIO.OUT)
GPIO.setup(reload_pin1, GPIO.OUT)
GPIO.setup(reload_pin2, GPIO.OUT)
GPIO.setup(shoot_pin, GPIO.OUT)

app = Flask(__name__, static_url_path='/statics')
app.config['SERVER_NAME'] = '192.168.0.108:5000'
print(app.root_path)

@app.route('/')
def index():
    return render_template('index.html')

def init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(left_pin, GPIO.OUT)
    GPIO.setup(right_pin, GPIO.OUT)
    GPIO.setup(reload_pin1, GPIO.OUT)
    GPIO.setup(reload_pin1, GPIO.OUT)
    GPIO.setup(shoot_pin, GPIO.OUT)

def turn_left():
    init()
    GPIO.output(left_pin,GPIO.HIGH)
    GPIO.output(right_pin,GPIO.LOW)

@app.route('/left',methods=['GET','POST'])
def turn_left_route():
    with ThreadPoolExecutor() as executor:
        executor.submit(turn_left)
    return render_template('index.html')

def turn_right():
    init()
    GPIO.output(right_pin,GPIO.HIGH)
    GPIO.output(left_pin,GPIO.LOW)

@app.route('/right',methods=['GET','POST'])
def turn_right_route():
    with ThreadPoolExecutor() as executor:
        executor.submit(turn_right)
    return render_template('index.html')

def stop():
    init()
    GPIO.output(right_pin,GPIO.LOW)
    GPIO.output(left_pin,GPIO.LOW)
    GPIO.output(reload_pin1, GPIO.LOW)
    GPIO.output(reload_pin2, GPIO.LOW)
    GPIO.output(shoot_pin, GPIO.LOW)

@app.route('/stop',methods=['GET','POST'])
def stop_route():
    with ThreadPoolExecutor() as executor:
        executor.submit(stop)
    return render_template('index.html')

def reload():
    init()
    GPIO.output(reload_pin1, GPIO.HIGH)
    GPIO.output(reload_pin2, GPIO.LOW)
    sleep(5)
    stop()

@app.route('/reload',methods=['GET','POST'])
def reload_route():
    with ThreadPoolExecutor() as executor:
        executor.submit(reload)
    return render_template('index.html')

def reset_reload():
    init()
    GPIO.output(reload_pin2, GPIO.HIGH)
    GPIO.output(reload_pin1, GPIO.LOW)
    sleep(5)
    stop()
    
@app.route('/reset_reload',methods=['GET','POST'])
def reset_reload_route():
    with ThreadPoolExecutor() as executor:
        executor.submit(reset_reload)
    return render_template('index.html')

def shoot():
    init()
    
    init()
    GPIO.output(shoot_pin,GPIO.HIGH)
    sleep(2)
    GPIO.output(shoot_pin,GPIO.LOW)

@app.route('/shoot',methods=['GET','POST'])
def shoot_route():
    with ThreadPoolExecutor() as executor:
        executor.submit(shoot)
    return render_template('index.html')




def gen(camera):
    """視頻串流生成器函數。"""
    while True:
        # 捕獲單個幀
        frame = camera.get_frame()

        # 在這裡執行對象辨識或其他處理
        processed_image = model.process_frame(frame)
        
        if processed_image is not None:
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + processed_image + b'\r\n')
        # 使用全局變數 processed_frame，這裡假設 processed_frame 是上一個幀的處理結果
        else:
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def run_flask_app():
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)


if __name__ == '__main__':
    with ThreadPoolExecutor() as executor:
        # 在執行緒池中啟動 Flask 應用程式的執行緒
        flask_thread = threading.Thread(target=run_flask_app())
        flask_thread.start()

        # 等待 Flask 應用程式執行結束
        flask_thread.join()

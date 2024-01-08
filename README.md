1.關於專案

一台可以遠端操作，包含轉向、填彈、發射砲彈的炮台，可以開啟自動模式，透過模型訓練辨認出敵人後，能自動瞄準
<hr>
2.專案緣由

從小就喜歡打電動，想要把遊戲中的坦克搬到現實中來玩
<hr>
3.專案構想

按照下面步驟，逐漸把砲台的雛型創造出來

      1.	可以轉向
      2.	填充彈藥的裝置
      3.	發射砲彈的裝置
      4.	裝鏡頭，並且可以透過手機螢幕展示畫面，對目標物進行瞄準

4.所需材料

      1.	坦克車模型(可直接上網找現成的改裝，或找材料進行拼裝)
      2.	兩個L298N馬達驅動模組(共有四個馬達需要被驅動)
      3.	18650鋰電池 * 2(分別供應兩個馬達驅動模組)
      4.	一個樹梅派專用鏡頭
      5.	直徑大約1cm的彈簧(根據砲管決定)
      6.	壓克力板
      7.	掃把的鐵管(當砲管用)
      8.	紙板(設置裝彈用)
      9.	Rasberry Pi 4
      10.	Rasberry Pi 4 5V不斷電供應系統
      11.	塑鋼土(用於拼接坦克各種連接處、當彈藥)
      12.	方向鎖電機馬達 * 1(裝彈用馬達)
      13.	強扭力步進馬達 * 1(發射用馬達)
      14.	NCS神經棒
      15.   一堆固定材料

5.實體照片、各裝置細節照片

![S__380510212_0](https://github.com/Dowgojashan/Remote_fort/assets/134786599/c72ebc66-f61f-485f-9bd5-f3e2001d51cf)
<hr>

底座裝置細節:
![S__380510216](https://github.com/Dowgojashan/Remote_fort/assets/134786599/c945144a-35d4-4f2a-ae9b-63456ed6ad11)
<hr>

砲台裝置細節:
![S__380510214_0](https://github.com/Dowgojashan/Remote_fort/assets/134786599/452d7753-8ae5-4d37-a235-10b3a1b143fa)
![S__380592130](https://github.com/Dowgojashan/Remote_fort/assets/134786599/eed61bf8-cb06-4d67-862e-9c08041d2511)

砲台發射失敗可能的原因

      1.   彈簧太硬，馬達不夠力推不動
      2.   某一個點可能沒有固定好(馬達、馬達的支架、砲管等)
      3.   延伸馬達的棒越短越好，不要再多做延伸
      4.   彈簧的延伸棒長度也是符合上方的U型棒就好

6.電路配置

底座裝置電路配置圖
![S__15286277_0](https://github.com/Dowgojashan/Remote_fort/assets/134786599/4e76cfbb-30d5-4fd6-883a-121a46f73c8d)
<hr>

砲台裝置電路配置圖
![S__15286275_0](https://github.com/Dowgojashan/Remote_fort/assets/134786599/85584766-010f-4591-9440-214fadd7f1e8)
<hr>

7.程式設計、環境設置

環境設置:

      - Web Server使用Flask去控制(參考連結:https://randomnerdtutorials.com/raspberry-pi-web-server-using-flask-to-control-gpios/)

      - camera pi設置(參考連結:https://github.com/Mjrovai/Video-Streaming-with-Flask/blob/master/camWebServer/camera_pi.py
                       https://picamera.readthedocs.io/en/release-1.13/quickstart.html)
                       
      - openvino環境設置(參考連結:https://hackmd.io/HV6hQ2PHSiWlrRsfxC10SA)
      安裝好之後輸入下面兩個指令，下載本專案所需模型(可依需求替換)

      wget https://download.01.org/opencv/2021/openvinotoolkit/2021.2/open_model_zoo/models_bin/3/vehicle-detection-0201/FP16/vehicle-detection-0201.bin

      wget https://download.01.org/opencv/2021/openvinotoolkit/2021.2/open_model_zoo/models_bin/3/vehicle-detection-0201/FP16/vehicle-detection-0201.xml

程式設計:

轉向控制

      left_pin = 23
      right_pin = 24
      GPIO.setmode(GPIO.BCM)
      GPIO.setwarnings(False)
      GPIO.setup(left_pin, GPIO.OUT)
      GPIO.setup(right_pin, GPIO.OUT)
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
<hr>

填彈控制

      reload_pin1 = 6
      reload_pin2 = 26
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
<hr>

射擊控制

      shoot_pin = 16
      def shoot():
          init()
          
          init()
          GPIO.output(shoot_pin,GPIO.HIGH)
          sleep(2) #秒數可依自己的裝置調整
          GPIO.output(shoot_pin,GPIO.LOW)
      
      @app.route('/shoot',methods=['GET','POST'])
      def shoot_route():
          with ThreadPoolExecutor() as executor:
              executor.submit(shoot)
          return render_template('index.html')

模型辨識+video streaming

      def gen(camera):
          """視頻串流生成器函數。"""
          while True:
              # 捕獲單個幀
              frame = camera.get_frame()
              
              # 將影格轉換為 NumPy 數組
              image = cv2.imdecode(np.frombuffer(frame, dtype=np.uint8), cv2.IMREAD_COLOR)
      
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
      # 初始化 Inference Engine
      ie = IECore()
      
      # 載入轉換後的模型
      net = ie.read_network(model='/home/dowgojashan/Downloads/person-vehicle-bike-detection-crossroad-0078.xml', weights='/home/dowgojashan/Downloads/person-vehicle-bike-detection-crossroad-0078.bin')
      
      # 設定輸入和輸出
      input_blob = next(iter(net.input_info))
      output_blob = next(iter(net.outputs))
      
      # 加載模型到 Inference Engine
      exec_net = ie.load_network(network=net, num_requests=2, device_name="MYRIAD")
      
      def process_frame(frame):
          # 將影格轉換為 NumPy 數組
          image = cv2.imdecode(np.frombuffer(frame, dtype=np.uint8), cv2.IMREAD_COLOR)
          # 假設 image 是您的影格
          # 將影像調整為模型期望的大小 (1024, 1024)
          resized_image = cv2.resize(image, (1024, 1024))
      
          # 將影像轉換為 NumPy 數組
          input_data = np.expand_dims(np.transpose(resized_image, (2, 0, 1)), 0)
      
          # 進行推論
          result = exec_net.infer(inputs={input_blob: input_data})
          output = result[output_blob]
      
          # 在原始圖片上標記結果
          for obj in output[0][0]:
              if obj[2] > 0.5:  # 假設信心值大於 0.5 才視為有效結果
                  xmin = int(obj[3] * image.shape[1])
                  ymin = int(obj[4] * image.shape[0])
                  xmax = int(obj[5] * image.shape[1])
                  ymax = int(obj[6] * image.shape[0])
      
                  cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
                  label = f'Class: {int(obj[1])}, Confidence: {obj[2]:.2f}'
                  cv2.putText(image, label, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
      
          # 將處理後的影像轉換回 JPEG 格式
          _, jpeg = cv2.imencode('.jpg', image)
          
          return jpeg.tobytes()
8.demo連結

      https://youtu.be/PL69i-RQufA
9.可以改進的地方

      1.   研究出前後的馬達為什麼不能動
      2.   增加填彈的速度
      3.   裝彈裝置的最前方，應該做一個開關，避免砲彈在轉向或撞到的時候，直接裝入砲管內
      4.   增加發射砲彈的穩定性還有可以調整發射距離
      5.   換更好的鏡頭
      6.   完成自動瞄準的部分
10.參考資料

        https://www.youtube.com/watch?v=lqNBbHDsoN0
        https://www.youtube.com/watch?v=4K-iqTeLJhY
        https://www.youtube.com/watch?v=bNOlimnWZJE&list=PLc6fhBPeC6SBbZFcrHLlPXyR2svfxf1RZ&index=20&t=507s
        https://www.youtube.com/watch?v=9qTJdQUme80

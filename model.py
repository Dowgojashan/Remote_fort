import cv2
import numpy as np
from openvino.inference_engine import IECore

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

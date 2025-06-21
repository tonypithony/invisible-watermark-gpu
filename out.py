import cv2
from imwatermark import WatermarkDecoder

decoder = WatermarkDecoder('bytes', 32)

bgr = cv2.imread('test_wm_dwtDct.png')
watermark = decoder.decode(bgr, 'dwtDct')
print(watermark.decode('utf-8'))

bgr = cv2.imread('test_wm_dwtDctSvd.png')
watermark = decoder.decode(bgr, 'dwtDctSvd')
print(watermark.decode('utf-8'))

bgr = cv2.imread('test_wm_rivaGan.png')
WatermarkDecoder.loadModel() # pip install onnxruntime
decoder = WatermarkDecoder('bytes', 32)
watermark = decoder.decode(bgr, 'rivaGan')
print(watermark.decode('utf-8'))
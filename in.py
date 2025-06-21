# pip install invisible-watermark # https://pypi.org/project/invisible-watermark/
# https://github.com/ShieldMnt/invisible-watermark/tree/main
# https://deepwiki.com/ShieldMnt/invisible-watermark/4.3-rivagan-method

# $ python in.py && python out.py 
# Pets
# Pets
# Pets # RuntimeError: rivaGan only supports 32 bits watermarks now.

import cv2
from imwatermark import WatermarkEncoder

bgr = cv2.imread('test.png')
wm = "Pets"

encoder = WatermarkEncoder()
encoder.set_watermark('bytes', wm.encode('utf-8'))
bgr_encoded = encoder.encode(bgr, 'dwtDct')
cv2.imwrite('test_wm_dwtDct.png', bgr_encoded)
bgr_encoded = encoder.encode(bgr, 'dwtDctSvd')
cv2.imwrite('test_wm_dwtDctSvd.png', bgr_encoded)

WatermarkEncoder.loadModel() # pip install onnxruntime
encoder = WatermarkEncoder()
encoder.set_watermark('bytes', b'Pets')
bgr_encoded = encoder.encode(bgr, 'rivaGan')
cv2.imwrite('test_wm_rivaGan.png', bgr_encoded)
## dwtDct
![](https://raw.githubusercontent.com/tonypithony/invisible-watermark-gpu/refs/heads/main/Bcolordiff_for_test_wm_dwtDct.png)


## dwtDctSvd
![](https://raw.githubusercontent.com/tonypithony/invisible-watermark-gpu/refs/heads/main/Bcolordiff_for_test_wm_dwtDctSvd.png)


## dwtRivaGAN
![](https://raw.githubusercontent.com/tonypithony/invisible-watermark-gpu/refs/heads/main/Bcolordiff_for_test_wm_rivaGan.png)


# invisible-watermark-gpu
[![PyPI](https://img.shields.io/pypi/v/invisible-watermark-gpu)](https://pypi.org/project/invisible-watermark-gpu/)

<!-- 
[![License](https://img.shields.io/pypi/l/invisible-watermark.svg)](https://github.com/ShieldMnt/invisible-watermark/blob/main/LICENSE)
![Python](https://img.shields.io/badge/python->=3.6-green.svg)
![Platform](https://img.shields.io/badge/platform-%20linux%20-green.svg)
[![Downloads](https://static.pepy.tech/badge/invisible-watermark)](https://pepy.tech/project/invisible-watermark)  -->

`invisible-watermark-gpu` is a **python** library and command line tool for creating invisible watermark over image (a.k.a. **blink image watermark**, **digital image watermark**). The algorithm doesn't rely on the original image.

**Note that** this library is adapted from `invisible-watermark` in an attempt to optimize the performance and accuracy of a few of the algorithms.

## Installation

It's a little more complex than the CPU-only version since we need to make sure we can link to the proper CUDA libraries.

```bash
# find your GPU's gencode here, and set the PYCUDWT_CC environment variable to it
# for example, for an A100, it would be "80" for SM80:
# https://arnon.dk/matching-sm-architectures-arch-and-gencode-for-various-nvidia-cards/ 
export PYCUDWT_CC=80

# also, load your CUDA version and set any and all needed environment variables. this might
# depend on your CUDA version + GPU type. I'm using CUDA 12.1 on an A100
module load cuda/12.1
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/usr/local/cuda/lib64
export CUDA_PATH=/usr/local/cuda
export PYCUDWT_CC=80
export CUDAHOME=/usr/local/cuda-12.1

# install !
pip install invisible-watermark-gpu --no-cache-dir
```

You should NOT proceed until this test passes:

```bash
# without this test passing, your pycudwt package will NOT work properly, and it will
# only output zeros, silently causing you to not be able to decode anything!
python -m pytest -k 'test_pycudwt_installed_correctly'
```

Once that works, you should be off to the races!

## ALgorithms

[supported algorithms](https://github.com/ShieldMnt/invisible-watermark#supported-algorithms)
* [Discrete wavelet transform](https://en.wikipedia.org/wiki/Discrete_wavelet_transform) + [Discrete cosine transform](https://en.wikipedia.org/wiki/Discrete_cosine_transform) frequency embedding algorithm variants.
* [RivaGAN](https://github.com/DAI-Lab/RivaGAN), a deep-learning model trained from Hollywood2 movie clips dataset.

[speed](https://github.com/ShieldMnt/invisible-watermark#running-speed-cpu-only)
* default embedding method ```dwtDct``` is fast and suitable for on-the-fly embedding
* ```dwtDctSvd``` is 3x slower and ```rivaGan``` is 10x slower, for large image they are not suitable for on-the-fly embedding

accuracy
* The algorithm **cannot guarantee** to decode the original watermarks 100% accurately even though we don't apply any attack.
* Known defects: Test shows all algorithms do not perform well for web page screenshots or posters with homogenous background color

## Supported Algorithms
* [**frequency methods**](https://github.com/ShieldMnt/invisible-watermark/wiki/Frequency-Methods)
 
> * **dwtDct**: DWT + DCT transform, embed watermark bit into max non-trivial coefficient of block dct coefficents
> 
> * **dwtDctSvd**: DWT + DCT transform, SVD decomposition of each block, embed watermark bit into singular value decomposition

* [**rivaGan**](https://github.com/ShieldMnt/invisible-watermark#rivagan-experimental): encoder/decoder model with Attention mechanism + embed watermark bits into vector.

> background:
> * [Discrete wavelet transform](https://en.wikipedia.org/wiki/Discrete_wavelet_transform)
> * [Discrete cosine transform](https://en.wikipedia.org/wiki/Discrete_cosine_transform).
> * [RivaGAN](https://github.com/DAI-Lab/RivaGAN), a deep-learning model trained from Hollywood2 movie clips dataset.

## [Library API](https://github.com/ShieldMnt/invisible-watermark/wiki/API)
### Embed watermark

* **example** embed 4 characters (32 bits) watermark

```python
import cv2
from imwatermark import WatermarkEncoder

bgr = cv2.imread('test.png')
wm = 'test'

encoder = WatermarkEncoder()
encoder.set_watermark('bytes', wm.encode('utf-8'))
bgr_encoded = encoder.encode(bgr, 'dwtDct')

cv2.imwrite('test_wm.png', bgr_encoded)
```

Note that if you want to avoid the cold start problem of loading CUDA libraries, you'll need to warmup the GPU first. You can do this by running the following code before you start encoding images:

```python
from imwatermark import WatermarkEncoder

# only supported for method "dwtDct" currently
WatermarkEncoder().warmup_gpu()
```

### Decode watermark
* **example** decode 4 characters (32 bits) watermark

```python
import cv2
from imwatermark import WatermarkDecoder

bgr = cv2.imread('test_wm.png')

decoder = WatermarkDecoder('bytes', 32)
watermark = decoder.decode(bgr, 'dwtDct')
print(watermark.decode('utf-8'))
```


## CLI Usage

```
embed watermark:  ./invisible-watermark -v -a encode -t bytes -m dwtDct -w 'hello' -o ./test_vectors/wm.png ./test_vectors/original.jpg

decode watermark: ./invisible-watermark -v -a decode -t bytes -m dwtDct -l 40 ./test_vectors/wm.png

positional arguments:
  input                 The path of input

optional arguments:
  -h, --help            show this help message and exit
  -a ACTION, --action ACTION
                        encode|decode (default: None)
  -t TYPE, --type TYPE  bytes|b16|bits|uuid|ipv4 (default: bits)
  -m METHOD, --method METHOD
                        dwtDct|dwtDctSvd|rivaGan (default: maxDct)
  -w WATERMARK, --watermark WATERMARK
                        embedded string (default: )
  -l LENGTH, --length LENGTH
                        watermark bits length, required for bytes|b16|bits
                        watermark (default: 0)
  -o OUTPUT, --output OUTPUT
                        The path of output (default: None)
  -v, --verbose         print info (default: False)
```

## Test Result
 
For better doc reading, we compress all images in this page, but the test is taken on 1920x1080 original image.

Methods are not robust to **resize** or aspect ratio changed **crop** but robust to **noise**, **color filter**, **brightness** and **jpg compress.**

**rivaGan outperforms the default method on crop attack.**

**only default method is ready for on-the-fly embedding.**

### Input
> * Input Image: 1960x1080 Image
> * Watermark: 
>   - For freq method, we use 64bits, string expression "qingquan"
>   - For RivaGan method, we use 32bits, string expression "qing"
> * Parameters: only take U frame to keep image quality, ```scale=36```

### Attack Performance

**Watermarked Image**

![wm](https://user-images.githubusercontent.com/1647036/106387712-03c17400-6416-11eb-9490-e5e860b025ad.png)

| Attacks | Image | Freq Method | RivaGan |
| --- | --- | --- | --- |
| JPG Compress | ![wm_jpg](https://user-images.githubusercontent.com/1647036/106387721-0e7c0900-6416-11eb-840c-8eab1cb9d748.jpg) | Pass | Pass |
| Noise | ![wm_noise](https://user-images.githubusercontent.com/1647036/106387874-c90c0b80-6416-11eb-99f3-1716f01f2211.png) | Pass | Pass |
| Brightness | ![wm_darken](https://user-images.githubusercontent.com/1647036/106387718-0cb24580-6416-11eb-83af-7f9e94f13cae.png) | Pass | Pass |
| Overlay | ![wm_overlay](https://user-images.githubusercontent.com/1647036/106387733-13d95380-6416-11eb-8aa4-b3d2acfa8637.png) | Pass | Pass |
| Mask | ![wm_mask_large](https://user-images.githubusercontent.com/1647036/106387726-10de6300-6416-11eb-99c3-4a0f70f99224.png) | Pass | Pass |
| crop 7x5 | ![wm_crop_7x5](https://user-images.githubusercontent.com/1647036/106387713-06bc6480-6416-11eb-8ae0-f64289642450.png) | Fail | Pass |
| Resize 50% | ![wm_resize_half](https://user-images.githubusercontent.com/1647036/106387735-15a31700-6416-11eb-8589-2ffa38df2a9a.png) | Fail | Fail |
| Rotate 30 degress | ![wm_rotate](https://user-images.githubusercontent.com/1647036/106387737-19369e00-6416-11eb-8417-05e53e11b77f.png) | Fail | Fail|

### Running Speed (CPU Only)
| Image | Method | Encoding | Decoding |
| --- | --- | --- | --- |
| 1920x1080 | dwtDct | 300-350ms | 150ms-200ms |
| 1920x1080 | dwtDctSvd | 1500ms-2s | ~1s |
| 1920x1080 | rivaGan | ~5s | 4-5s |
| 600x600 | dwtDct | 70ms | 60ms |
| 600x600 | dwtDctSvd | 185ms | 320ms |
| 600x600 | rivaGan | 1s | 600ms |

### Running Speed (GPU Only)

TODO: fill this in!

### RivaGAN Experimental
Further, We will deliver the 64bit rivaGan model and test the performance on GPU environment.

Detail: [https://github.com/DAI-Lab/RivaGAN](https://github.com/DAI-Lab/RivaGAN)

Zhang, Kevin Alex and Xu, Lei and Cuesta-Infante, Alfredo and Veeramachaneni, Kalyan. Robust Invisible Video Watermarking with Attention. MIT EECS, September 2019.[[PDF](https://arxiv.org/abs/1909.01285)]

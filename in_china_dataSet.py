# source BLINDWATERMARK/bin/activate

# pip install blind-watermark

"""Простой скрипт для тестирования работы водяных знаков"""

from glob import glob
# from watermark import WaterMark
from blind_watermark import WaterMark
import os

import random
import string

def generate_random_string(length=35):
    characters = string.ascii_letters + string.digits + string.punctuation
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string


# Embed watermark:

bwm1 = WaterMark(password_img=1, password_wm=1)


# # Extract watermark:

# bwm1 = WaterMark(password_img=1, password_wm=1)
# wm_extract = bwm1.extract('embedded.png', wm_shape=len_wm, mode='str')
# print(wm_extract)




SRC_IMG_PATHNAME_PATTERN = "/home/van_rossum/Документы/dataset/train/wm-empty/*.jpg" # 1249962
wm_dir = '/media/pendrive/wm-china'

src_img_filenames = glob(SRC_IMG_PATHNAME_PATTERN)
print(f'total number of images = {len(src_img_filenames)}\n\n')

i = 0
for src_img_filename in src_img_filenames:
	try:
		bwm1.read_img(src_img_filename)
		wm = generate_random_string(length=35) #'101010101010101010101010101010101010'
		print(wm)
		bwm1.read_wm(wm, mode='str')
		bwm1.embed(f'{wm_dir}/{src_img_filename[50:]}')
		print('\ncurrent number = ', i := i+1, '\n')
	except AssertionError:
		os.remove(src_img_filename)
	except PIL.UnidentifiedImageError:
		os.remove(src_img_filename)
	except OSError:
		os.remove(src_img_filename)
	except FileExistsError:
		os.remove(src_img_filename)
	except FileNotFoundError:
		continue
		# os.remove(src_img_filename)
	finally:
		if os.path.isfile(src_img_filename):
			os.remove(src_img_filename)
		else:
			continue

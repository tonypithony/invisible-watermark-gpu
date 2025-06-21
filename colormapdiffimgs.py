from PIL import Image
from glob import glob


def diffimage(name1, name2, colour="RGB"):
    img1 = Image.open(name1).convert(colour)
    img2 = Image.open(name2).convert(colour)
    new_image = Image.new(colour, (img1.size[0], img1.size[1]), color=(255, 255, 255))
    color_image = Image.new(colour, (img1.size[0], img1.size[1]), color=(255, 255, 255))
    color_imageR = Image.new(colour, (img1.size[0], img1.size[1]), color=(255, 255, 255))
    color_imageG = Image.new(colour, (img1.size[0], img1.size[1]), color=(255, 255, 255))
    color_imageB = Image.new(colour, (img1.size[0], img1.size[1]), color=(255, 255, 255))

    for i in range(img1.size[0]):
        for j in range(img1.size[1]):
            if img1.getpixel((i, j)) != img2.getpixel((i, j)):
                i1 = img1.getpixel((i, j))
                i2 = img2.getpixel((i, j))
                new_image.putpixel(
                    (i, j), tuple([i1[0] - i2[0], i1[1] - i2[1], i1[2] - i2[2]])
                )

                if 0 <= i1[0] - i2[0] < 1:
                    color_image.putpixel((i, j), (255, 0, 0))
                    color_imageR.putpixel((i, j), (255, 0, 0))
                if 1 <= i1[0] - i2[0] < 2:
                    color_image.putpixel((i, j), (255, 50, 0))
                    color_imageR.putpixel((i, j), (255, 50, 0))
                if 2 <= i1[0] - i2[0] < 3:
                    color_image.putpixel((i, j), (255, 100, 0))
                    color_imageR.putpixel((i, j), (255, 100, 0))
                if i1[0] - i2[0] > 3:
                    color_image.putpixel((i, j), (255, 150, 0))
                    color_imageR.putpixel((i, j), (255, 150, 0))
                if 0 <= i1[1] - i2[1] < 1:
                    color_image.putpixel((i, j), (0, 255, 0))
                    color_imageG.putpixel((i, j), (0, 255, 0))
                if 1 <= i1[1] - i2[1] < 2:
                    color_image.putpixel((i, j), (0, 255, 50))
                    color_imageG.putpixel((i, j), (0, 255, 50))
                if 2 <= i1[1] - i2[1] < 3:
                    color_image.putpixel((i, j), (0, 255, 100))
                    color_imageG.putpixel((i, j), (0, 255, 100))
                if i1[1] - i2[1] > 3:
                    color_image.putpixel((i, j), (0, 255, 150))
                    color_imageG.putpixel((i, j), (0, 255, 150))
                if 0 <= i1[2] - i2[2] < 1:
                    color_image.putpixel((i, j), (0, 0, 255))
                    color_imageB.putpixel((i, j), (0, 0, 255))
                if 1 <= i1[2] - i2[2] < 2:
                    color_image.putpixel((i, j), (50, 0, 255))  # синий
                    color_imageB.putpixel((i, j), (50, 0, 255))
                if 2 <= i1[2] - i2[2] < 3:
                    color_image.putpixel((i, j), (100, 0, 255))  # фиолетовый
                    color_imageB.putpixel((i, j), (100, 0, 255))
                if i1[2] - i2[2] > 3:
                    color_image.putpixel((i, j), (150, 0, 255))
                    color_imageB.putpixel((i, j), (150, 0, 255))

    new_image.save(f"diff_for_{name1[:-4]}.png")
    color_image.save(f"colordiff_for_{name1[:-4]}.png")
    color_imageR.save(f"Rcolordiff_for_{name1[:-4]}.png")
    color_imageG.save(f"Gcolordiff_for_{name1[:-4]}.png")
    color_imageB.save(f"Bcolordiff_for_{name1[:-4]}.png")





images1 = f"test_wm_dwtDct.png"
images2 = f"test.png"
diffimage(images1, images2)

images1 = f"test_wm_dwtDctSvd.png"
diffimage(images1, images2)

images1 = f"test_wm_rivaGan.png"
diffimage(images1, images2)
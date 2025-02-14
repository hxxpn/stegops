import PIL.Image as Image


def test_image_copy_creation():
    test_image = Image.open('owl.bmp')
    test_image.show()


import os
import sys
from PIL import Image
from PIL import ImageFilter
import pytesseract

def prepare_image(img):
    """Transform image to greyscale and blur it"""
    img = img.filter(ImageFilter.SMOOTH_MORE)
    img = img.filter(ImageFilter.SMOOTH_MORE)
    if 'L' != img.mode:
        img = img.convert('L')
    return img

def remove_noise(img, pass_factor):
    for column in range(img.size[0]):
        for line in range(img.size[1]):
            value = remove_noise_by_pixel(img, column, line, pass_factor)
            img.putpixel((column, line), value)
    return img

def remove_noise_by_pixel(img, column, line, pass_factor):
    if img.getpixel((column, line)) < pass_factor:
        return (0)
    return (255)


if __name__=="__main__":
    input_image = sys.argv[1]
  #  base_file, ext = os.path.splitext(input_image)
  #  os.rename(input_image, base_file + ".png")
    output_image = 'out_' + input_image
    pass_factor = int(sys.argv[2])

    img = Image.open(input_image)
    img = prepare_image(img)
    img = remove_noise(img, pass_factor)
    img.save(output_image)


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
print("start")
print(pytesseract.image_to_string(Image.open(output_image)))
print("end")

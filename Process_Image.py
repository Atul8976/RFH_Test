from Image_Read_Write.Read_Write_Image import read_image,unprocess_images_path
import os
from PIL import Image, ImageOps,ImageFilter


def blur_outline():
   folder_path = read_image(unprocess_images_path)

   for impath in folder_path:
      for i in os.listdir(impath):
         img = Image.open(impath+"/"+i)
         # img_with_border = ImageOps.expand(img, border=300, fill='black')
         # img_with_border.save('bordered-%s' % i)
         im1 = img.filter(ImageFilter.GaussianBlur(radius=2))
         im1.save(impath+"/"+i)

blur_outline()
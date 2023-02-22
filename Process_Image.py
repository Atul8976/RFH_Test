from Image_Read_Write.Read_Write_Image import read_image,unprocess_images_path
import os
from PIL import Image, ImageOps,ImageFilter
import numpy as np
import asyncio

async def blur_outline():
   folder_path = await read_image(unprocess_images_path)

   for impath in folder_path:
      for i in os.listdir(impath):
         img = Image.open(impath+"/"+i)
         img_with_border = ImageOps.expand(img, border=10, fill='black')
         img_with_border.save(impath+"/"+i)
         im1 = img.filter(ImageFilter.GaussianBlur(radius=5))
         im1.save(impath+"/"+i)

   # for impath in folder_path:
   #
   #   imlist = os.listdir(impath)
   #
   #   x = np.array([np.array(Image.open(impath+"/"+fname)) for fname in imlist])
   #
   #   imgFull = blockMerge(x, imgWidth = 2517, imgHeight = 3028)
   #
   #   # Save full image
   #   saveBlock(imgFull)


asyncio.run(blur_outline())

import pydicom as dicom
import os
import numpy as np
from PIL import Image
from itertools import product

current_directory = os.getcwd()

unprocess_images_path = current_directory + str("/Unprocessed_images/")
intermediate_image_process_path = current_directory + str("/Intermediate_processed_images/")
final_image_path = current_directory + str('/Final_processed_images/')

# def blockMerge(array, imgWidth, imgHeight):
#     """Merges image blocks into a grayscale image.
#
#     Args:
#         array (ndarray): Containing image blocks with third axis representing the number of blocks.
#         imgWidth (int): Width of full image.
#         imgHeight (int): Height of full image.
#
#     Returns:
#         (ndarray): Array containing full grayscale image.
#     """
#
#     # Dimension of the input image
#     blockSizeX = array.shape[1]
#     blockSizeY = array.shape[0]
#
#     # Number of blocks along an axis
#     blocksAlongX = imgWidth / blockSizeX
#     blocksAlongY = imgHeight / blockSizeY
#
#     # Creating Numpy Array for output image
#     outputImage = np.zeros((imgHeight, imgWidth))
#
#     # Counter for indexing each block from input array
#     depthCounter = 0
#
#     # Starting position of X
#     x = 0
#
#     # Starting position of Y
#     y = 0
#
#     while y < imgHeight:
#         while x < imgWidth:
#             try:
#                 outputImage[y: (y + blockSizeY),
#                 x: (x + blockSizeX)] = array[:, :, depthCounter]
#                 x += blockSizeX
#                 depthCounter += 1
#             except:
#                 pass
#         y += blockSizeY
#         x = 0
#
#     return outputImage
#
#
# def saveBlock(array):
#     """Saves blocks or full image as JPG.
#
#     Args:
#         array (ndarray): Contains either blocks or full image.
#     """
#
#     # Blocks
#     if len(array.shape) == 3:
#
#         # Creating folder for blocks
#         dst_folder = intermediate_image_process_path
#
#         # Saving blocks
#         for i in range(array.shape[2]):
#             imgObject = Image.fromarray(array[:, :, i].astype('uint8'), 'L')
#             imgName = f"{str(dst_folder)}/block_{i}.jpg"
#             imgObject.save(imgName)
#
#     # Single image
#     elif len(array.shape) == 2:
#
#         # Creating folder for blocks
#         dst_folder = final_image_path
#
#
#         # Saving image
#         imgObject = Image.fromarray(array[:, :].astype('uint8'), 'L')
#         imgName = f"{str(dst_folder)}/imageFull.jpg"
#         imgObject.save(imgName)

async def read_image(unprocess_images_path):

    """async function which will convert .dicom images to .jpg image
    and will divide the image into multiple pieces each of which 250*250 title piece"""

    dir_list = os.listdir(unprocess_images_path)

    return_output = []

    print("Converting Images from Unprocessed_images directory into .jpg format "
          "and started dividing individual image into multiple image titles : \n")

    for i, image in enumerate(dir_list):

        """convert each .dicom image from Unprocessed_images directory to .jpg and save converted image to 
        Intermediate_processed_images"""


        ds = dicom.dcmread(unprocess_images_path+image)
        new_image = ds.pixel_array.astype(float)
        scaled_image = (np.maximum(new_image, 0) / new_image.max()) * 255.0

        scaled_image = np.uint8(scaled_image)
        final_image = Image.fromarray(scaled_image)
        filename = 'image_'+str(i)+'.jpg'
        final_image.save(intermediate_image_process_path+'/'+filename)


        """below code will divide each image into multiple pieces inside respective folder which same name as image 
        name"""
        name, ext = os.path.splitext(filename)
        img = Image.open(os.path.join(intermediate_image_process_path, filename))
        w, h = img.size
        d = 250

        newfolder = 'image_'+str(i)

        isExist = os.path.exists(intermediate_image_process_path+'/'+newfolder)

        if not isExist:
            os.makedirs(intermediate_image_process_path+'/'+newfolder)

        new_path = os.path.join(intermediate_image_process_path,newfolder)

        grid = product(range(0, h - h % d, d), range(0, w - w % d, d))
        for j, k in grid:
            box = (j, i, j + d, i + d)
            out = os.path.join(new_path, f'{name}_{j}_{k}{ext}')
            img.crop(box).save(out)

        return_output.append(new_path)

    print("conversion finished and save to Intermediate_processed_images directory and "
          "finished dividing individual image into multiple image title. \n")

    return return_output


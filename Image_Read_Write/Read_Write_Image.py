import pydicom as dicom
import asyncio
import os
import numpy as np
from PIL import Image
from itertools import product

current_directory = os.getcwd()

unprocess_images_path = current_directory + str("/Unprocess_images/")
intermediate_image_process_path = current_directory + str("/Intermediate_process_images/")


def read_image(unprocess_images_path):

    dir_list = os.listdir(unprocess_images_path)

    return_output = []

    for i, image in enumerate(dir_list):
        ds = dicom.dcmread(unprocess_images_path+image)
        new_image = ds.pixel_array.astype(float)
        scaled_image = (np.maximum(new_image, 0) / new_image.max()) * 255.0

        scaled_image = np.uint8(scaled_image)
        final_image = Image.fromarray(scaled_image)
        filename = 'image_'+str(i)+'.jpg'
        final_image.save(intermediate_image_process_path+'/'+filename)

        name, ext = os.path.splitext(filename)
        img = Image.open(os.path.join(intermediate_image_process_path, filename))
        w, h = 250, 320
        d = 25

        newfolder = 'image_'+str(i)

        isExist = os.path.exists(intermediate_image_process_path+'/'+newfolder)
        if not isExist:
            os.makedirs(intermediate_image_process_path+'/'+newfolder)

        new_path = os.path.join(intermediate_image_process_path,newfolder)

        grid = product(range(0, h - h % d, d), range(0, w - w % d, d))
        for i, j in grid:
            box = (j, i, j + d, i + d)
            out = os.path.join(new_path, f'{name}_{i}_{j}{ext}')
            img.crop(box).save(out)

        return_output.append(new_path)

    return return_output

read_image(unprocess_images_path)

# asyncio.run(read_image(unprocess_images_path))

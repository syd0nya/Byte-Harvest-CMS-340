import os
import pygame

def import_folder(path):
    surface_list = []

    # Load animal imgs
    for _, __, img_files in os.walk(path):
        for image in sorted(img_files): 
            if image.endswith(('.png', '.jpg', '.jpeg')): 
                full_path = os.path.join(path, image)
                surface_list.append(pygame.image.load(full_path).convert_alpha())

    return surface_list

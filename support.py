from os import walk
import pygame
def import_folder(path):
    
    surface_list = []
    
    for _, _, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            print(full_path)
            image_surf = pygame.image.load(full_path).convert_alpha() # converting it to an image that is easier to use in pythion
            surface_list.append(image_surf)        
    return surface_list

import os,pygame

IMAGES = {}

for i in os.listdir(os.path.join("data","art")):
    IMAGES[i[:-4]] = pygame.image.load(os.path.join("data","art",i))
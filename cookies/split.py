import platform
import os

def on_windows(image):
    new_file_path = '.\\temp\\'+os.path.basename(os.path.splitext(image['meta']['file_path'])[0] + '.png')
    command = 'dwebp %s -o %s' % (image['meta']['file_path'], new_file_path, )
    image['meta']['file_path'] = new_file_path
    image['type'] = 'png'
    return image

def process(images):
    for i in range(1,len(images)-1):
        if platform.system()=='Windows' and images[i]['type']=='webp':
            images[i] = on_windows(images[i])
        if platform.system()=='Windows' and images[i+1]['type']=='webp':
            images[i+1] = on_windows(images[i+1])
        images[i],images[i+1] = split(images[i],images[i+1])


def split(image_0,image_1):

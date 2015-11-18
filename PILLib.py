import Image
import os

def completion(string, aim, lr='Left', char='0'):
    new_string = string
    while len(new_string)<aim:
        if lr=='Left':
            new_string = char+new_string
        else:
            new_string = new_string+char
    return new_string

def creat_covering(picture_f, picture_s):
    process_size = picture_f.size
    picture_n = Image.new('RGBA', process_size)
    pix_f = picture_f.load()
    pix_s = picture_s.load()
    pix_n = picture_n.load()
    for i in range(process_size[0]):
        for j in range(process_size[1]):
            if pix_f[i,j]==pix_s[i,j]:
                pix_n[i,j] = (0,0,0,0)
            else:
                if len(pix_s[i,j])==3:
                    pix_n[i,j] = tuple(list(pix_s[i,j])+[255])
                else:
                    pix_n[i,j] = pix_s[i,j]
    return picture_n

def open_dir(path='.'):
    file_list = os.listdir(path)
    return file_list

OUT_DIR = 'npic'
DIR = '0'

file_list = open_dir(DIR)

picture_t = Image.open(DIR+'/'+file_list[0])
process_size = picture_t.size
picture_nt = Image.new('RGBA', process_size)
pix_t = picture_t.load()
pix_nt = picture_nt.load()

for i in range(process_size[0]):
    for j in range(process_size[1]):
        if len(pix_t[i,j])==3:
            pix_nt[i,j] = tuple(list(pix_t[i,j])+[255])
        else:
            pix_nt[i,j] = pix_t[i,j]
picture_nt.save(OUT_DIR+'/'+completion('',8)+'.png')

for i in range(len(file_list)-1):
    picture_f = Image.open(DIR+'/'+file_list[i])
    picture_s = Image.open(DIR+'/'+file_list[i+1])
    picture_n = creat_covering(picture_f, picture_s)
    picture_n.save(OUT_DIR+'/'+completion(str(i+1),8)+'.png')
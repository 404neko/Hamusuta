#aim add output
#aim check static pic 
import requests
import re
import os
from PIL import Image
import zipfile
import json
import sys

from _config import *

re_unform_url = '=([0-9]*?)&'

pixiv_url = 'http://www.pixiv.net/member_illust.php?mode=medium&illust_id=%s'

def binding_cwebp(path,out_path):
    command = 'cwebp -q 100 -lossless %s -o %s' % (path, out_path, )
    return os.system(command)

def binding_webpmux(frames,out_path):
    command = 'webpmux %s -o %s' % (frames, out_path, )
    print command
    return os.system(command)

def modify_script(script):
    return script

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

#copy from pack 'umaru.FileSystem'
def CreatFolder(Path):
    if Path.find('/')==-1:
        if not os.path.exists(Path):
            os.mkdir(Path)
    else:
        Path=Path.split('/')
        Path0=''
        for PathItem in Path:
            Path0=Path0+PathItem+'/'
            if not os.path.exists(Path0):
                os.mkdir(Path0)

def url_engine(part):
    try:
        int(part)
        return part
    except:
        pass
    try:
        part = part.split('=')[-1]
        int(part)
        return part
    except:
        pass
    try:
        part = re.findall(re_unform_url, part)[0]
        int(part)
        return part
    except:
        pass
    return '0'

def get_script(id):
    try:
        content = requests.get(pixiv_url % (id,), proxies=proxy).content
    except:
        return 'ERROR','Http request fail.'
    script = re.findall(re_web2d_info,content)
    if len(script)!=0:
        script=script[0]
    else:
        return 'ERROR','Not get expected content.'
    try:
        json.loads(script)
        return script
    except:
        return 'ERROR','Not a json string.'

def simple_unzip(path,out_path):
    zip_file = zipfile.ZipFile(path, 'r')
    zip_name = os.path.basename(path)
    if zip_name[-4:]=='.zip':
        folder_name = zip_name[:-4]
    else:
        folder_name = zip_name+'_unpack'
    CreatFolder(out_path+'/'+folder_name)
    for file_name in zip_file.namelist():
        with open(out_path+'/'+folder_name+'/'+file_name,'wb') as file_handle:
            file_handle.write(zip_file.read(file_name))
    return out_path+'/'+folder_name

def ext_filename_replace(file_name,new_ext_name,add=False):
    if len(file_name.split('.'))>1:
        return file_name[:-(len(file_name.split('.')[-1])+1)]+'.'+new_ext_name
    else:
        if add:
            return file_name+'.'+new_ext_name
        else:
            return file_name

def c2webp(path):
    CreatFolder(path+'/../webp')
    files = os.listdir(path)
    for file_path in files:
        binding_cwebp(path+'/'+file_path,path+'/../webp/'+file_path[:-(len(file_path.split('.')[-1])+1)]+'.webp')
    return path+'/../webp'

#webpmux -frame 00000000.webp +125 -frame 00000001.webp +125 -frame 00000002.webp +125 -frame 00000003.webp +125 -frame 00000004.webp +125 -frame 00000005.webp +125 -frame 00000006.webp +125 -frame 00000007.webp +125 -frame 00000008.webp +125 -frame 00000009.webp +125 -frame 00000010.webp +125 -frame 00000011.webp +125 -frame 00000012.webp +125 -frame 00000013.webp +125 -frame 00000014.webp +125 -frame 00000015.webp +125 -frame 00000016.webp +125 -frame 00000017.webp +2000 -o ani.webp
def webps2awebp(script,path,id,ignore_error=False):
    json_obj = json.loads(script)
    frames = json_obj['frames']
    frames_command = ''
    frames_command_base = ' -frame %s +%s '
    for frame in frames:
        if os.path.isfile(path+'/'+ext_filename_replace(frame['file'],'webp')):
            frames_command+=frames_command_base % (path+'/'+ext_filename_replace(frame['file'],'webp'), frame['delay'])
        else:
            if ignore_error:
                continue
            else:
                print 'ERROR','File not found.'
    binding_webpmux(frames_command,'./'+id+'/'+id+'.webp')
    return './'+id+'/'+id+'.webp'

def differ(path):
    CreatFolder(path+'/../discrepancy')
    files = os.listdir(path)
    image = Image.open(path+'/'+files[0])
    size = image.size
    new_image = Image.new('RGBA', size)
    pix_ = image.load()
    pix_new = new_image.load()
    for i in range(size[0]):
        for j in range(size[1]):
            if len(pix_[i,j])==3:
                pix_new[i,j] = tuple(list(pix_[i,j])+[255])
            else:
                pix_new[i,j] = pix_[i,j]
    new_image.save(path+'/../discrepancy/'+files[0][:-(len(files[0].split('.')[-1])+1)]+'.png')
    for i in range(len(files)-1):
        picture_p = Image.open(path+'/'+files[i])
        picture_n = Image.open(path+'/'+files[i+1])
        picture_new = creat_covering(picture_p, picture_n)
        picture_new.save(path+'/../discrepancy/'+files[i+1][:-(len(files[i+1].split('.')[-1])+1)]+'.png')
    return path+'/../discrepancy'

def copy2clipboard(string):
    return os.system('echo '+string+' | clip')

def process_script(script,id):
    CreatFolder('./'+id)
    with open('./'+id+'/Script.json','wb') as file_handle:
        file_handle.write(script)
    script_json = json.loads(script)
    header = {
                'Referer': pixiv_url % (id,)
                }
    try:
        content = requests.get(script_json['src'], proxies=proxy, headers=header).content
        with open('./'+id+'/Pack.zip','wb') as file_handle:
            file_handle.write(content)
    except:
        return 'ERROR','Http request fail.'
    unzipped_path = simple_unzip('./'+id+'/Pack.zip', './'+id)
    discrepancy_path = differ(unzipped_path)
    webp_path = c2webp(discrepancy_path)
    return webps2awebp(script,webp_path,id)

if __name__=='__main__':
    if len(sys.argv)>1:
        credential = url_engine(sys.argv[1])
        if credential=='0':
          while credential=='0':
                credential = url_engine(raw_input('Please enter pixiv url or pixiv id:'))
    else:
        credential = '0'
        while credential=='0':
            credential = url_engine(raw_input('Please enter pixiv url or pixiv id:'))
    script = get_script(credential)
    path = process_script(script,credential)
    copy2clipboard(path)
    print 'Success~'
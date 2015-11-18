import imghdr
import os

DELAY_CHROME = 0.06
DELAY_WINDOWS = 0.1
DELAY_NONE = 0.0

def gifsicle_binder(Path,delay=DELAY_CHROME):
    command = 'gifsicle -I "%s"' % (Path,)
    pipeline = os.popen(command)
    description_object = {}
    pipeline = pipeline.read().split('\n')
    image_num = pipeline[0].split(' ')[-2]
    description_object['type'] = 'gif'
    description_object['meta'] = {}
    description_object['meta']['file_path'] = Path
    description_object['image_num'] = int(image_num)
    if image_num=='1':
        return description_object
    else:
        total = len(pipeline)-1
        now = 1
        while now<=total:
            if pipeline[now].find('loop')==-1:
                pass
            else:
                description_object['loop'] = int(pipeline[now].split(' ')[-1])
            if pipeline[now].find('+')==-1:
                now+=1
                continue
            else:
                break
        ImageCollect = []
        while now<=total:
            if pipeline[now].find('+')!=-1:
                image_no = int(pipeline[now].split(' ')[-2][1:])
                image_res = pipeline[now].split(' ')[-1]
                now+=1
                while pipeline[now].find('table')!=-1:
                    now+=1
                str_attr = pipeline[now]
                image_attr = {}
                if str_attr.find('disposal')!=-1:
                    image_attr['disposal'] = str_attr.split('disposal')[-1][1:].split(' ')[0]
                if str_attr.find('delay')!=-1:
                    #str_attr.split('delay')
                    image_attr['delay'] = float(str_attr.split('delay')[-1][1:].split(' ')[0][:-1])
                image_attr['no'] = image_no
                image_attr['res'] = image_res
                ImageCollect.append(image_attr)
            now+=1
    description_object['ImageCollect'] = ImageCollect
    return description_object

#buildsequence

def config_paser(path):
    env = {}
    build_sequence = []
    with open(path) as file_handle:
        content = file_handle.read()
    sequence = content.replace('\r','').split('\n')
    count = 0
    for process in sequence:
        count+=1
        values = process.split('::')
        if len(values)!=2:
            if env.get('ignore_error',False)=='True':
                continue
            else:
                return 'ERROR',count,len(sequence)
        else:
            if values[0]=='image':
                description_object = type_process(values[1])
                if description_object!={}:
                    build_sequence.append({'image':description_object})
                else:
                    if env.get('ignore_error',False)=='True':
                        continue
                    else:
                        return 'ERROR',count,len(sequence)
            if values[0]=='images':
                


def gif_test(Path):
    return gifsicle_binder(Path)

#rewrite
def test_webp(h, f):
    if h[8:12] == 'WEBP':
        return 'webp'
if test_webp not in imghdr.tests:
    imghdr.tests.append(test_webp)

def object_type(Path):
    if os.path.isfile(Path):
        Type = imghdr.what(Path)
        if Type==None:
            print 'ERROR: Not a picture file.'
            return 'None'
        else:
            return Type
    else:
        print 'ERROR: Not a file.'
        return 'None'

def type_process(Path):
    image_type = object_type(Path)
    description_object = {}
    if image_type=='None':
        pass
    else:
        if image_type=='gif':
            description_object = gif_test(Path)
        else:
            description_object['type'] = image_type
            description_object['meta'] = {}
            description_object['meta']['file_path'] = Path
            description_object['image_num'] = 1
    return description_object
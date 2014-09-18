from __future__ import division
import time
import os

DOCKERFILE_PATH=os.path.join(os.path.dirname(__file__),"files/dockerfiles")

def timestamp_to_local(timestamp):
    x=time.localtime(timestamp)
    time_format='%Y-%m-%d %H:%M:%S'
    return time.strftime(time_format,x)

def byte_to_gb(byte):
    _x = eval('{}/1000/1000/1000'.format(byte))
    print _x
    _y = eval('1577283853/1000/1000/1000')
    print _y
    return "%.2fGB" % _x 
def human_readable_size(size):
    import humanize

    return humanize.naturalsize(size)

def create_file(name):
    #_path=os.path.join(DOCKERFILE_PATH,name)
    _path="{}/{}".format(DOCKERFILE_PATH,name)
    print _path
    if not os.path.exists(_path):
        os.mkdir(_path)
    file_path=os.path.join(_path,"Dockerfile")
    print file_path
    _file=open(file_path,'w') 

    return _file
def get_file_path(file_name):
    import os
    real_name='Dockerfile'
    _path="{}/{}".format(DOCKERFILE_PATH,file_name)
    return os.path.join(_path,real_name)

def write_file(fd,content):
    fd.write(content)
    fd.close()
def get_file_size(file_path):
    import os

    size=os.path.getsize(file_path)

    return human_readable_size(size)

def get_current_datatime():
    import time
    time_str=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    return time_str 


if __name__ == '__main__':
    print byte_to_gb('1577283853')

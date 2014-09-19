from __future__ import division
import time
import os
import logging
import mercurial.commands
import mercurial.error
import mercurial.hg
import mercurial.ui
from time import strftime
import subprocess
from ConfigParser import ConfigParser


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

def create_file(repo_path,content):
    
    #_path=os.path.join(DOCKERFILE_PATH,name)
    #_path="{}/{}".format(DOCKERFILE_PATH,name)
    #print _path
    #if not os.path.exists(_path):
    #    os.mkdir(_path)
    file_path=os.path.join(repo_path,"Dockerfile")

    with open(file_path,'w') as f:
        f.write(content)
    #print file_path
    #_file=open(file_path,'w') 

    #return _file
#def create_repos(name):
#    pass
def get_file_path(file_name):
    import os
    real_name='Dockerfile'
    _path="{}/{}".format(DOCKERFILE_PATH,file_name)
    return os.path.join(_path,real_name)

def get_repo_path(repo_name):
    _path="{}/{}".format(DOCKERFILE_PATH,repo_name)

    return _path

#def write_file(fd,content):
#    fd.write(content)
#    fd.close()
def get_file_size(file_path):
    import os

    size=os.path.getsize(file_path)

    return human_readable_size(size)

def get_current_datatime():
    import time
    time_str=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    return time_str 

class MercurialRevisionControl(object):
    def __init__(self,repo_path=None,local_path=None,**options):
        self._ui = mercurial.ui.ui()
        self.repo_path = repo_path
    def create_repo(self,path):
        try:
            mercurial.commands.init(self._ui, dest=path)
        except Exception, e:
            logging.error('Could not create Mercurial repository in %s. %s: %s',
                                                          path, e.__class__.__name__, str(e))
    def add(self,repo_path):
        repo=mercurial.hg.repository(self._ui,repo_path)
        mercurial.commands.add(self._ui,repo=repo)
    def commit(self,repo_path):
        timestamp=strftime('%Y-%m-%d %H:%M:%S')
        message = "jaeweb auto-commit:%s" % timestamp
        self._ui.pushbuffer()
        repo=mercurial.hg.repository(self._ui,repo_path)
        mercurial.commands.commit(self._ui,repo=repo,message=message,logfile=None,addremove=None,user=None,date=None)
        logging.debug('doing commit at %s' % repo_path)
        logging.debug(self._ui.popbuffer())
    def hg_rc(self,repo_path,section,option,value):
        hg_rc="{}/.hg/hgrc".format(repo_path)
        if not os.path.isfile(hg_rc):
           subprocess.call(['touch',hg_rc]) 
        parser=ConfigParser()
        parser.read(hg_rc)
        if not parser.has_section(section):
            with open(hg_rc,'a') as f:
                f.write('[%s]\n' % section)
        if not parser.has_option(section,option):
            with open(hg_rc,'a') as f:
                f.write('%s = %s\n' % (option,value))


if __name__ == '__main__':
    print byte_to_gb('1577283853')

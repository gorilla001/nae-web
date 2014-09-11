from __future__ import division
import time

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


if __name__ == '__main__':
    print byte_to_gb('1577283853')

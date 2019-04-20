#!/usr/bin/env python

from tzc_transport import tzc
import multiprocessing, signal, time, os

def talker(width, height, step, loop = 1000):
    print 'talker start'
    pub = tzc.Publisher('chatter', 30, 100*1024*1024)
    tzc.init_node('talker', tzc.init_options.AnonymousName)
    rate = tzc.Rate(30)
    count = 0
    while not tzc.is_shutdown():
        img = tzc.image()
        img.width  = width
        img.height = height
        img.step = step
        img.data_resize(width * height * step)
        if pub.allocate(img):
            img.data = 'image # %5d ...' % count
            img.header_stamp = tzc.get_rostime()
            pub.publish(img)
        tzc.spinOnce()
        rate.sleep()
        count += 1
        if count == loop : break
    print 'talker end'

info = [] # the variable will not be shared in different process, each process will create its own 'info'
def callback(img):
    info.append('delay: [%5.5fms]'%((tzc.get_rostime() - img.header_stamp).toSec()*1000))

def listener(filedir, filename):
    print '%s start' % filename
    tzc.init_node('listener', tzc.init_options.AnonymousName)
    lis = tzc.Subscriber(callback,'chatter')
    tzc.spin()
    with open('%s/%s.txt' % (filedir, filename), 'w') as f :
        f.write('\n'.join(info))
    print '%s end' % filename

if __name__ == '__main__':
    
    filedir = 'output_test_data'
    data_size = ('4kb', 1024, 1, 4)
    listener_num = 4
    filename = 'tzc_py_%s_%d_listener_no_' % (data_size[0], listener_num)
    
    
    if not os.path.exists(filedir):
        os.makedirs(filedir) 
        
    for i in range(listener_num) :
        multiprocessing.Process(target=listener, args=(filedir, filename + str(i))).start()
    
    time.sleep(1)
    
    talker = multiprocessing.Process(target=talker, args=(data_size[1], data_size[2], data_size[3]))
    talker.start()
    
    try:
        time.sleep(600)
    except KeyboardInterrupt:
        print 'interrupt'
    
    print 'main end'

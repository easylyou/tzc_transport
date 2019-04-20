#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image
import multiprocessing, signal, time, os

def talker(width, height, step, loop = 1000):
    print 'talker start'
    pub = rospy.Publisher('chatter', Image, queue_size=30)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(30)
    
    data = ' ' * (width * height * step) # initialize the data first
    
    count = 0
    while not rospy.is_shutdown():
        img = Image()
        img.width  = width
        img.height = height
        img.step = step
        img.data = data
        img.header.stamp = rospy.get_rostime()
        pub.publish(img)
        rate.sleep()
        count += 1
        if count == loop : break

    print 'talker end'

info = [] # the variable will not be shared in different process, each process will create its own 'info'
def callback(data):
    info.append('delay: [%5.5fms]'%((rospy.get_rostime() - data.header.stamp).to_sec()*1000))

def listener(filedir, filename):
    print '%s start' % filename
    
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("chatter", Image, callback)
    rospy.spin()
    
    with open('%s/%s.txt' % (filedir, filename), 'w') as f :
        f.write('\n'.join(info))
    
    print '%s end' % filename

if __name__ == '__main__':
    
    filedir = 'output_test_data'
    data_size = ('4kb', 1024, 1, 4)
    listener_num = 4
    filename = 'ros_py_%s_%d_listener_no_' % (data_size[0], listener_num)
    
    
    if not os.path.exists(filedir):
        os.makedirs(filedir) 
    ps = []
    for i in range(listener_num) :
        p = multiprocessing.Process(target=listener, args=(filedir, filename + str(i)))
        ps.append(p)
        p.start()
        
    
    time.sleep(2)
    
    t = multiprocessing.Process(target=talker, args=(data_size[1], data_size[2], data_size[3]))
    t.start()
    
    try:
        t.join()
    except KeyboardInterrupt:
        print 'interrupt'
        pass
    
    time.sleep(1)
    for p in ps:
        os.kill(p.pid , signal.SIGINT)
        
    print 'main end'

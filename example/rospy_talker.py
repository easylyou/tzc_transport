#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image

def talker():
    pub = rospy.Publisher('chatter', Image, queue_size=30)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(30)
    count = 0
    while not rospy.is_shutdown():
        img = Image()
        img.width = 1920
        img.height = 1080
        img.step = 3
        img.data = str(count) + ' ' * 1920 * 1080 * 3
        img.header.stamp = rospy.get_rostime()
        pub.publish(img)
        rate.sleep()
        count += 1
        if count == 1000 : break

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
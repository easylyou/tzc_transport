#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image

def callback(data):
    rospy.loginfo("delay [%5.5fms]", (rospy.get_rostime() - data.header.stamp).to_sec()*1000)
    
def listener():
    
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("chatter", Image, callback)

    rospy.spin()

if __name__ == '__main__':
    listener()
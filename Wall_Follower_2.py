import math
import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3
from math import radians

rospy.init_node('Odom_Pub_Depth_Sub')
odom_pub = rospy.Publisher("cmd_vel_mux/input/navi", Twist, queue_size=10)
r = rospy.Rate(50)


#inside callback
def depthCb(depth):
    

    Depth = depth.twist.twist.linear.x
    print Depth
    move_cmd = Twist()
    move_cmd.linear.x = 0.3
    move_cmd.angular.z = 0.05
    turn_cmd = Twist()
    turn_cmd.linear.x = 0
    turn_cmd.angular.z = radians(45);
    stop_cmd = Twist()
    stop_cmd.linear.x = 0
    if (Depth > 3500 or Depth == -1) and not rospy.is_shutdown(): #go straight
        odom_pub.publish(move_cmd)
        r.sleep()
    elif Depth < 3500 and not rospy.is_shutdown() : # Turn 90 degrees
        #for x in range(0,100):
        odom_pub.publish(turn_cmd)
        r.sleep()
    else:
        odom_pub.publish(stop_cmd)
         
        
if __name__ == '__main__':
    try:
        
        rospy.Subscriber('Depth',Odometry,depthCb)
        rospy.spin()
        
    except:
        rospy.loginfo("GoForward node terminated.")

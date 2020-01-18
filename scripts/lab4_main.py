#!/usr/bin/env python
# primary node - basically the master node for this project

import tf
import math
import data			# custom module for function related to data manipulation... 
					# perhaps 'units' would be a better name
import text			# custom module for writing to text file
import rospy
import bayes			# custom module - implementation of bayes filter
import random
import bagreader as bag		# custom module for dealing with grid.bag
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Quaternion, Pose, Point, Vector3
from std_msgs.msg import Header, ColorRGBA

# all accessible publisher for markers
marker_publisher = rospy.Publisher('lab4_markers', Marker, queue_size=1)

# function for showing robot in rviz
# pointless now since I stripped out the naive logic I used to check against
robot_position = [12, 28, data.getDiscreteEulerAngle(200.52)]
def show_robot():
    marker = Marker()
    marker.ns = "robot"
    marker.id = 0
    marker.type = Marker.CUBE
    marker.action = Marker.ADD
    marker.lifetime = rospy.Duration(600)
    marker.header = Header(frame_id='/base_link')
    x = robot_position[0] - 1
    y = robot_position[1] - 1
    theta = data.getContinousEulerAngle(robot_position[2])
    q = tf.transformations.quaternion_from_euler(0, 0, theta * 3.14/180)
    marker.scale = Vector3(0.15, 0.1, 0.1)
    marker.pose = Pose(Point(x*data.LINEAR_UNIT, y*data.LINEAR_UNIT, 0.05), Quaternion(q[0], q[1], q[2], q[3]))
    marker.color = ColorRGBA(0.0, 0.0, 1.0, 1.0)
    marker_publisher.publish(marker)
    pass

# function for showing all landmarks
# useless now
landmark_x = [1.25, 1.25, 1.25, 4.25, 4.25, 4.25]
landmark_y = [5.25, 3.25, 1.25, 1.25, 3.25, 5.25]
def show_landmarks():
    marker = Marker()
    marker.ns = "landmarks" # %d" % i
    marker.id = 0
    marker.type = Marker.SPHERE_LIST
    marker.action = Marker.ADD
    marker.lifetime = rospy.Duration(600)
    marker.header = Header(frame_id='/base_link')
    marker.scale = Vector3(0.1, 0.1, 0.1)
    for i in range(6):
        x = data.getDiscreteMetres(landmark_x[i]) - 1
        y = data.getDiscreteMetres(landmark_y[i]) - 1
        marker.points.append(Point(x*data.LINEAR_UNIT, y*data.LINEAR_UNIT, 0.125))
        marker.colors.append(ColorRGBA(0.75, 0.75, 0.75, 1.0))
    marker_publisher.publish(marker)    
    
# function to visualize a 3d belief grid
# useless now
def show_beliefs():
    marker = Marker()
    marker.ns = "belief"
    marker.id = 0
    marker.type = Marker.POINTS
    marker.action = Marker.ADD
    marker.lifetime = rospy.Duration(600)
    marker.header = Header(frame_id='/base_link')
    marker.scale = Vector3(0.05, 0.05, 0.05)
    beliefs = bayes.getBeliefs()
    d, t = data.getNumDatapoints()
    for i in range(d):
        for j in range(d):
            for k in range(t):
                marker.points.append(Point(i*data.LU(), j*data.LU(), -k*data.LU()))
                marker.colors.append(ColorRGBA(1.0, 1.0, 1.0, beliefs[i][j][k]))
    marker_publisher.publish(marker)
    
# this is my main function
def lab4_main():
    rospy.init_node('lab4_main', anonymous=True)
    MSG_NUM = 0

    bayes.setInitialBeliefs(robot_position[0] - 1, robot_position[1] - 1, robot_position[2] - 1)
    mx, my, mt = bayes.getMostLikely()
    p = bayes.getBelief(mx, my, mt)
    print "--> %3d, %3d, %3d, %f" % (mx, my, mt, p)

    rospy.sleep(1.0)
    # while no shtdown command from rospy and there are more messages in the bag file
    while not rospy.is_shutdown() and not MSG_NUM >= bag.getTotalCycles():
        # show_landmarks()
        # show_robot()

        # get processed version of bag file messages 
		# - here processed means easier to deal with in my program structure
        a1, tr, a2 = bag.getMovement(MSG_NUM)
        l, r, b = bag.getObservation(MSG_NUM)
	# run bayes filter localization
        bayes.filter(a1, tr, a2, l, r, b)
        mx, my, mt = bayes.getMostLikely()
        p = bayes.getBelief(mx, my, mt)
	# show_beliefs()

	# print everything to commandline - pointless in the final version 
		# - kept it in because might be needed for you guys to debug
        print "%3d:\n%f, %f, %f\n%d, %f, %f" % (MSG_NUM, a1, tr, a2, l, r, b)
        print "--> %3d, %3d, %3d, %f" % (mx, my, mt, p)
        print

        MSG_NUM = MSG_NUM + 1
	# add point to text file array
        text.addPoint(mx + 1, my + 1, mt + 1, p)
        pass
    # write array of points to text file
    text.writeToFile()


if __name__ == '__main__':
    try:
        lab4_main()
    except rospy.ROSInterruptException: 
	pass


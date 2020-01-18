#!/usr/bin/env python
# module for interacting with the bag file

import tf
import rosbag
import rospkg

# get grid file using rospack to find path to ros package 'lab4'
rospack = rospkg.RosPack()
bag = rosbag.Bag(rospack.get_path('lab4') + '/grid.bag')

movements = []
M_HEAD = 0
observations = []
O_HEAD = 0

# read through the bag once and store all messages in memory
i = 0
for topic, msg, t in bag.read_messages():
    i = i + 1
    if(topic == "Observations"):
        observations.append(msg)
    if(topic == "Movements"):
        movements.append(msg)
        pass
bag.close()

# process everything so it fits easier in my headspace
	# involves getting rid of those pesky radians. Yes, I'm an idiot.
def getMovement(index):
    move = movements[index]
    quat = move.rotation1
    a1 = tf.transformations.euler_from_quaternion([quat.x, quat.y, quat.z, quat.w])
    quat = move.rotation2
    a2 = tf.transformations.euler_from_quaternion([quat.x, quat.y, quat.z, quat.w])
    return a1[2]*180/3.14, move.translation, a2[2]*180/3.14

# just in case I need the raw object
def getRawMovement(index):
    return movements[index]
    
# process everything so it fits easier in my headspace
def getObservation(index):
    obs = observations[index]
    quat = obs.bearing
    b = tf.transformations.euler_from_quaternion([quat.x, quat.y, quat.z, quat.w])
    return obs.tagNum, obs.range, b[2]*180/3.14

# just in case I need the raw object
def getRawObservation(index):
    return observations[index]

def getTotalCycles():
    return len(movements)

#!/usr/bin/env python

import rospy
from std_msgs.msg import Float64
import os.path

values_list = []

def callback(msg, index):
    global values_list
    values_list[index] = msg.data


def run():
    global values_list
    #Get the desired name of the data file and the topics to log.
    rospy.init_node("logging_node", anonymous=True)
    topics_list = rospy.get_param("/topics_list")
    data_file_name = rospy.get_param("/data_file_name", "log")
    values_list = [0.0] * len(topics_list)
    #Subscribe to the topics in the list.
    for i in range(len(topics_list)):
        rospy.Subscriber(topics_list[i], Float64, lambda msg,index=i: callback(msg, index))
    rate = rospy.Rate(2)
    if (os.path.isfile(data_file_name + ".csv")):
        i = 1
        while (os.path.isfile(data_file_name + str(i)+ ".csv")):
            i += 1
        data_file_name += str(i)
    with open(data_file_name + ".csv", "w") as data_file:
        start = rospy.Time.now()
        #Write seconds since start of mission, followed by data in order specified by the topics file.
        while not rospy.is_shutdown():
            data_file.write(str((rospy.Time.now() - start).to_sec()) + ',')
            for i in range(len(values_list) - 1):
                data_file.write(str(values_list[i]) + ',')
            data_file.write(str(values_list[-1]) + '\n')
            data_file.flush()
            rate.sleep()

if __name__ == '__main__':
    run()





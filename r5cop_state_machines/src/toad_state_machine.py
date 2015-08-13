#!/usr/bin/env python

import roslib; roslib.load_manifest('r5cop_state_machines')
import rospy
from zmq_object_exchanger import zmqObjectExchanger
import time
import tf
import actionlib
from robot_position import robotPosition
    
class ToadRobotBrain():

    def __init__(self, boundary, center):
    
        self.tfl = tf.TransformListener()
        
        self.comm = zmqObjectExchanger("Toad", "toad", 1234)
        self.comm.zmq.add_remote("PR2", "pr2", 1234)
        
        rospy.Timer(rospy.Duration(0.25), outDataTimer)
        rospy.Timer(rospy.Duration(0.25), inDataTimer)
        
    def getReady(self):
    
        pass
    
    def outDataTimer(self, evt):
    
        now = rospy.time.now()
        ps = robotPosition(self.tfl).get(now)
        
        msg = {}
        
        msg['robot_position'] = ps
        msg['current_state'] = "exploring"
        
        self.comm.send_msg("state_info", msg)
        
    def inDataTimer(self, evt):
    
        msgs = self.comm.get_msgs()
        
        for msg in msgs:
        
            rospy.loginfo(msg["name"] + ": " + msg["topic"])
        
            if msg["topic"] == "state_info":
            
                # TODO store it somehow
                pass            
    
    
def main():
  
    rospy.init_node('toad_state_machine')
    brain = ToadRobotBrain()
    brain.getReady()
    
    rospy.spin()
    
if __name__ == '__main__':
    main()

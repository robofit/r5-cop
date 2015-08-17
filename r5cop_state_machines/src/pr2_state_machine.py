#!/usr/bin/env python

import roslib; roslib.load_manifest('r5cop_state_machines')
import rospy
from zmq_object_exchanger.zmq_object_exchanger import zmqObjectExchanger
import time
import tf
import actionlib
import frontier_exploration.msg
from robot_position import robotPosition
from geometry_msgs.msg import PolygonStamped, PointStamped, Polygon, Point32
    
class PR2RobotBrain():

    def __init__(self, boundary, center):
    
        self.tfl = tf.TransformListener()
        
        self.comm = zmqObjectExchanger("PR2", "127.0.0.1", 1234)
        self.comm.add_remote("Toad", "127.0.0.1", 4567)
        
        self.boundary = boundary
        self.center = center
        self.action_client = actionlib.SimpleActionClient('explore_server', frontier_exploration.msg.ExploreTaskAction)
        
        rospy.Timer(rospy.Duration(1.0), self.outDataTimer)
        rospy.Timer(rospy.Duration(0.25), self.inDataTimer)
        
        self.stop_exploring = False
        
    def getReady(self):
    
        self.action_client.wait_for_server()
    
    def outDataTimer(self, evt):
    
        now = rospy.Time.now()
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
            
                print(msg["data"])
                # TODO store it somehow
                pass            
    
    def explorationFeedbackCallback(self, fb):
  
        pass
        
    def loop(self):
    
        self.getReady()
    
        while not rospy.is_shutdown():
        
            # Explore until object is found
            self.explore()
            
            # Object found - start manipulation / call Toad
            # TBD
        
        
    def explore(self):
    
        while not (self.stop_exploring or rospy.is_shutdown()):
    
            goal = frontier_exploration.msg.ExploreTaskGoal()
            goal.explore_boundary = self.boundary
            goal.explore_center = self.center
            
            self.action_client.send_goal(goal, feedback_cb=self.explorationFeedbackCallback)
            rospy.loginfo("Exploration started.") 
            
            while not self.action_client.wait_for_result(rospy.Duration(0.25)):
                        
                if rospy.is_shutdown() or self.stop_exploring:
                
                    self.action_client.cancel_goal()
                    break
            
            rospy.loginfo("Exploration finished.") 
        
        self.stop_exploring = False
    
def main():
  
    rospy.init_node('pr2_state_machine')
    brain = PR2RobotBrain()
    brain.getReady()
    
    area_to_explore = PolygonStamped()
    center_point = PointStamped()
    
    now = rospy.Time.now()
    
    area_to_explore.header.stamp = now
    area_to_explore.header.frame_id = "map"
    points = [Point32(-1.65, -1.56, 0.0),
              Point32(5.41, -1.7, 0.0),
              Point32(5.57, 4.44, 0.0),
              Point32(-1.75, 4.37, 0.0)]
              
    area_to_explore.polygon = Polygon(points)
    
    center_point.header = area_to_explore.header
    center_point.point.x = 1.83
    center_point.point.y = 1.57
    center_point.point.z = 0.0
    
    brain = PR2RobotBrain(area_to_explore, center_point)
    brain.loop()
    
if __name__ == '__main__':
    main()

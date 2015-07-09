#!/usr/bin/env python

import roslib; roslib.load_manifest('r5cop_state_machines')
import rospy
import smach
import smach_ros
from zmq_object_exchanger import zmqObjectExchanger
import time

#class Communicator(smach.State):
#
#  def __init__(self, robot_name):
#  
#    smach.State.__init__(self, outcomes = ['stop', 'goto'], output_keys = ['x'])
#    
#  def execute(self, userdata):
#  
#    while True:
#    
#      msgs = userdata.comm.get_msgs()
#      
#      for msg in msgs:
#      
#        pass
#    
#      time.sleep(0.1)

class SeekForObjects(smach.State):

  def __init__(self, floor_height_threshold = 0.25):

    # for now, let's consider only known (recognized) objects
    # latter we may add unknown_on_floor and unknown_on_table
    smach.State.__init__(self, outcomes = ['known_on_floor', 'known_on_table', 'stopped'], output_keys = ['object'])

    self.floor_height_threshold = floor_height_threshold
    
  def execute(self, ud):
  
    # TODO subscribe to detected objects topic / call action / whatever
    # TODO detected object -> send preempt to Explore, return, (send message)
  
    rospy.loginfo("Looking for objects")
  
    while True:
    
      if self.preempt_requested():
        self.service_preempt()
        return 'stopped'
    
      time.sleep(0.5)
     
    
class Explore(smach.State):
  """Call some exploration stuff and explore forever. Stop exploring on preempt request."""

  def __init__(self):
  
    smach.State.__init__(self, outcomes = ['stopped'])
    
  def execute(self, ud):
  
    # TODO start exploration
    
    rospy.loginfo("Exploring")
    
    while True:
    
      if self.preempt_requested():
        self.service_preempt()
        return 'stopped'
      
      time.sleep(0.5)
      
class CleanupObject(smach.State):
  """Call MoveIt! here"""

  def __init__(self):
  
    smach.State.__init__(self, input_keys = ['object'], outcomes = ['done'])
    
  def execute(self):
  
    rospy.loginfo("Cleaning up object")
  
    return 'done'
    
def main():
  
  rospy.init_node('pr2_state_machine')
  
  # top level state machine - running forever
  sm_top = smach.StateMachine(outcomes=['failed']) 
                             
  sm_top.userdata.comm = zmqObjectExchanger("PR2", "pr2", 1234)
  sm_top.userdata.comm.zmq.add_remote("Toad", "toad", 1234)
  
  
  # open the container
  with sm_top:
  
    sm_par = smach.Concurrence(outcomes=['known_on_floor', 'known_on_table'],
                                        outcome_map={})
  
    with sm_par:
  
      smach.Concurrence.add('SeekForObjects', SeekForObjects())
      smach.Concurrence.add('Explore', Explore())

    smach.StateMachine.add('SeekAndExplore', sm_par, transitions={'known_on_floor': 'CallToadToCleanUp',
                                                                  'known_on_table': 'CleanupObject'})
                                                                  
    smach.StateMachine.add('CleanupObject', CleanupObject(), transitions={'done': 'SeekAndExplore'})
    
if __name__ == '__main__':
    main()

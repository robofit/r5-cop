import roslib; roslib.load_manifest('r5cop_state_machines')
import rospy
import tf
from geometry_msgs.msg import PoseStamped

class robotPosition():

    def __init__(self, tfl, robot_link = "base_link", world_link = "map"):
    
        self.tfl = tfl
        self.robot_link = robot_link
        self.world_link = world_link
        
    def get(self, ts = None):
    
        if ts is None:
           
            ts = rospy.time.now()
            
        ps = PoseStamped()
        ps.header.timestamp = ts
        ps.header.frame_id = self.robot_link
        ps.pose.position.x = 0
        ps.pose.position.y = 0
        ps.pose.position.z = 0
        ps.pose.orientation.x = 0
        ps.pose.orientation.y = 0
        ps.pose.orientation.z = 0
        ps.pose.orientation.w = 1
        
        try:
        
            self.tfl.waitForTransform(self.robot_link, self.world_link, rospy.Duration(1.0))
            ps = self.tfl.transformPose(self.world_link, ps)
            
        except tf.Exception:
        
            return None
            
        return ps

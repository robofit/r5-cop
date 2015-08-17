How to run two separate simulations on one machine
==========

PR2
----------

In all terminals:
```
export ROS_MASTER_URI=http://localhost:$((UID+10001))
```

Start roscore
```
roscore -p $((UID+10001))
```

Start simulation
```
roslaunch r5cop_sim_env pr2_sim.launch port:=$((UID+11001))
```

TOAD
----------

In all terminals:
```
export ROS_MASTER_URI=http://localhost:$((UID+10000))
```

Start roscore
```
roscore -p $((UID+10000))
```

Start simulation
```
roslaunch r5cop_sim_env toad_sim.launch port:=$((UID+11000))
```

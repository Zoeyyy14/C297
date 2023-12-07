from controller import Robot
import math

robot = Robot()

timestep = int(robot.getBasicTimeStep())

left_motor = robot.getDevice("left wheel motor");
left_motor.setPosition(float('inf'))
left_motor.setVelocity(0.0)

right_motor = robot.getDevice("right wheel motor");
right_motor.setPosition(float('inf'))
right_motor.setVelocity(0.0)

imu= robot.getDevice("inertial unit")
imu.enable(timestep)

ds_front = robot.getDevice("ds_front")
ds_front.enable(timestep)
ds_left = robot.getDevice("ds_left")
ds_left.enable(timestep)
ds_right= robot.getDevice("ds_right")
ds_right.enable(timestep)


movement=0
robot_orientation=180
reach_end=0
    
def move(left_speed,right_speed):
    left_motor.setVelocity(left_speed)
    right_motor.setVelocity(right_speed)  

def turn_towards_angle(target,movement):
    if(target != yaw_current):
        move(-1,1) 
    else:
        move(0,0)
        movement+=1
    return movement
        
def move_forward_till_wall_detection(movement):
    if(ds_front_value>300):
        move(15,15)
    else:
        movement+=1
    return movement
        
def find_corner(movement):
    if(movement==0):
        movement+=1
    if(movement==1):
        movement=turn_towards_angle(robot_orientation%360,movement)
    if(movement==2):
        movement=move_forward_till_wall_detection(movement)
    if(movement==3):
        movement=turn_towards_angle((robot_orientation-90)%360,movement)
    if(movement==4):
        movement=move_forward_till_wall_detection(movement)
    if(movement==5):
        movement=turn_towards_angle((robot_orientation-180)%360,movement)
    return movement
    
def back_and_forth_movement(movement):
    if(movement==6):
        movement=move_forward_till_wall_detection(movement)
    if(movement==7):
        movement=turn_towards_angle((robot_orientation+90)%360,movement)
    if(movement==8):
        if(robot_orientation%360!=yaw_current):
            move(3,1)
        else:
            movement+=1
    if(movement==9):
        movement=move_forward_till_wall_detaection(movement)
    if(movement==10):
        movement=turn_towards_angle((robot_orientation+90)%360,movement)
    if(movement==11):
        if((robot_orientation-180)%360!=yaw_current):
            move(1,3)
        else:
            move(0,0)
            movement=6
    return movement
            
while robot.step(timestep) != -1:

    angle=imu.getRollPitchYaw()
    
    ds_front_value= ds_front.getValue()
    
    ds_left_value= ds_left.getValue()
    
    ds_right_value= ds_right.getValue()
    
    yaw_current= round(math.degrees(angle[2]))+180
    
    movement=find_corner(movement)
    
    movement=back_and_forth_movement(movement)
    
    print(yaw_current)
    
    if(reach_end==0 and ds_front_value<500 and ds_left_value<1000 and (yaw_current==180 or yaw_current==270)):
        movement:0
        robot_orientatiton=270
        print("here1")
        reach_end=1
        
    if(ds_front_value<500 and ds_left_value<1000 and (yaw_current==360 or yaw_current==0) and reach_end==1):
        movement:0
        robot_orientatiton=180
        print("here2")
        reach_end=2
    
    
    
    
    
    
    
    
    
    
    
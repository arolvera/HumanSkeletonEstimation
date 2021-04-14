import os
train = True



def main():
    if(train):
        dir = "data/dataset/train"
    else:
        dir = "data/dataset/test"
    directory = os.listdir(dir)
    frame_id = None
    joint_id = None
    num_bins = 10
    for file in directory:
        f = open(dir + "/" + str(file), "r")
        distances_to_body_center = []
        angles = []
        #hip_center = []
        frame_cnt = 0
        for line in f:
            stripped = line.strip().split()
            row = list(map(float, stripped))
            frame_id_prev = frame_id
            frame_id = row[0]
            joint_id = row[1]
            if(joint_id == 1): # new frame
                hip_center = [row[2], row[3], row[4]]
                frame_cnt+=1
                print(hip_center)
                # compute hist and shit for last frame
                
            elif(joint_id == 4  or joint_id == 8  or 
                 joint_id == 12 or joint_id == 16 or joint_id == 20):
                # joint_pos_x = row[2]
                # joint_pos_y = row[3]
                # joint_pos_z = row[4]
                distances_to_body_center.append(((row[2] - hip_center[0])**2 + # compute distances
                                                 (row[3] - hip_center[1])**2 + 
                                                 (row[4] - hip_center[2])**2)**(1/2))
                # compute angles
                if(joint_id != 4):

                
        #print("there are ", frame_cnt, "frames")
            #print(distances_to_body_center)        
                    
            

    


if __name__ == '__main__':
    main()
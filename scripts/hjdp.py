import os
import math
train = True

def calc_norm(x0,x1,y0,y1,z0,z1):
    ret = math.sqrt((x1-x0)**2 + (y1-y0)**2 + (z1-z0)**2)
    return ret

def main():
    if(train):
        dir = "data/dataset/train"
    else:
        dir = "data/dataset/test"
    directory = os.listdir(dir)
    frame_id = None
    joint_id = None
    num_bins = 10
    dists_2_bdy_cent = []
    joint_coords = []
    for file in directory:
        f = open(dir + "/" + str(file), "r")
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
                # compute angles
                # distance between head and left hand
                if(joint_coords):
                    d_hlh  = calc_norm(joint_coords[0][0], joint_coords[1][0], 
                                       joint_coords[0][1], joint_coords[1][1], 
                                       joint_coords[0][2], joint_coords[1][2])
                    d_lhlf = calc_norm(joint_coords[1][0], joint_coords[3][0], 
                                       joint_coords[1][1], joint_coords[3][1], 
                                       joint_coords[1][2], joint_coords[3][2])
                    d_lfrf = calc_norm(joint_coords[3][0], joint_coords[4][0], 
                                       joint_coords[3][1], joint_coords[4][1], 
                                       joint_coords[3][2], joint_coords[4][2])
                    d_rfrh = calc_norm(joint_coords[4][0], joint_coords[2][0], 
                                       joint_coords[4][1], joint_coords[2][1], 
                                       joint_coords[4][2], joint_coords[2][2])
                    d_rhh  = calc_norm(joint_coords[2][0], joint_coords[0][0], 
                                       joint_coords[2][1], joint_coords[0][1], 
                                       joint_coords[2][2], joint_coords[0][2])

                # use law of cosines to get all angles



                # compute hist and shit for last frame
                dists_2_bdy_cent = []
                joint_coords = []
                
            elif(joint_id == 4  or joint_id == 8  or 
                 joint_id == 12 or joint_id == 16 or joint_id == 20):
                joint_coords.append([row[2], row[3], row[4]])
                dists_2_bdy_cent.append(calc_norm(hip_center[0], row[2],
                                                  hip_center[1], row[3], 
                                                  hip_center[2], row[4]))
            
if __name__ == '__main__':
    main()
import os
import sys
import math
import numpy as np

def calc_norm(x0,x1,y0,y1,z0,z1):
    ret = math.sqrt((x1-x0)**2 + (y1-y0)**2 + (z1-z0)**2)
    return ret

def main():
    if len(sys.argv) == 1 or sys.argv[1] == "Test":
        train = False
        label_mod = 8
    elif sys.argv[1] == "Train":
        train = True
        label_mod = 12
    else:
        print("Invalid argument")
        return
    if(train):
        dir = "data/dataset/train"
        outfile = open("data/rad_d2","w")
    else:
        dir = "data/dataset/test"
        outfile = open("data/rad_d2.t","w")
    directory = os.listdir(dir)
    frame_id = None
    joint_id = None
    bins_N = 10
    bins_M = 10
    index = 1
    file_cnt = 0
    dists_2_bdy_cent = []
    joint_coords = []
    feature_vector = []
    for file in directory:
        f = open(dir + "/" + str(file), "r")
        frame_cnt = 0
        dists = [[],[],[],[],[]]
        angles = [[],[],[],[],[]]
        for line in f:
            stripped = line.strip().split()
            row = list(map(float, stripped))
            frame_id_prev = frame_id
            frame_id = row[0]
            joint_id = row[1]
            if(joint_id == 1): # new frame
                hip_center = [row[2], row[3], row[4]]
                frame_cnt+=1
                if(joint_coords):
                    # distance between head and left hand
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

                    for idx in range(len(dists_2_bdy_cent)):
                        if not math.isnan(dists_2_bdy_cent[idx]): 
                            dists[idx].append(dists_2_bdy_cent[idx])

                    # use law of cosines to compute all angles
                    angle_0 = math.acos((dists_2_bdy_cent[0]**2 + dists_2_bdy_cent[1]**2 - d_hlh**2 )/
                                        (2*dists_2_bdy_cent[0]*dists_2_bdy_cent[1]))
                    angle_1 = math.acos((dists_2_bdy_cent[1]**2 + dists_2_bdy_cent[3]**2 - d_lhlf**2)/
                                        (2*dists_2_bdy_cent[1]*dists_2_bdy_cent[3]))
                    angle_2 = math.acos((dists_2_bdy_cent[3]**2 + dists_2_bdy_cent[4]**2 - d_lfrf**2)/
                                        (2*dists_2_bdy_cent[3]*dists_2_bdy_cent[4]))
                    angle_3 = math.acos((dists_2_bdy_cent[4]**2 + dists_2_bdy_cent[2]**2 - d_rfrh**2)/
                                        (2*dists_2_bdy_cent[4]*dists_2_bdy_cent[2]))
                    angle_4 = math.acos((dists_2_bdy_cent[2]**2 + dists_2_bdy_cent[0]**2 - d_rhh**2 )/
                                        (2*dists_2_bdy_cent[2]*dists_2_bdy_cent[0]))

                    anglesl = [angle_0,angle_1,angle_2,angle_3,angle_4]
                    for idx in range(len(anglesl)):
                        if not math.isnan(anglesl[idx]):
                            angles[idx].append(anglesl[idx]) 

                dists_2_bdy_cent = []
                joint_coords = []

            elif(joint_id == 4  or joint_id == 8  or 
                 joint_id == 12 or joint_id == 16 or joint_id == 20):
                joint_coords.append([row[2], row[3], row[4]])
                dists_2_bdy_cent.append(calc_norm(hip_center[0], row[2],
                                                  hip_center[1], row[3], 
                                                  hip_center[2], row[4]))
        
        # compute histogram for each of 5 distance and angle catagories normal to number of frames in given file
        for dist in dists:
            hist  = np.histogram(dist, bins_N)
            counts = hist[0].tolist()
            for idx in range(len(counts)): # Normalize 
                counts[idx] = counts[idx] / frame_cnt 
            feature_vector.extend(counts)
        
        for angle in angles:
            hist  = np.histogram(angle, bins_M)
            counts = hist[0].tolist()
            for idx in range(len(counts)): # Normalize 
                counts[idx] = counts[idx] / frame_cnt 
            feature_vector.extend(counts)

        outfile.write(str(file_cnt//label_mod) + " ")
        for item in feature_vector:
            outfile.write(str(index) + ":" + str(item) + " ")
            index+=1
        outfile.write("\n")
        index = 1
        file_cnt+=1
        feature_vector = []

    outfile.close()

if __name__ == '__main__':
    main()
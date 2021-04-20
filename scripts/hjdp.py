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
    elif sys.argv[1] == "Train":
        train = True
    else:
        print("Invalid argument")
        return
    if(train):
        dir = "data/dataset/train"
        outfile = open("data/hjdp_d1","w")
    else:
        dir = "data/dataset/test"
        outfile = open("data/hjdp_d1.t","w")
    directory = os.listdir(dir)
    frame_id = None
    joint_id = None
    bins_N = 10
    bins_M = 10
    dists_2_bdy_cent = []
    joint_coords = []
    feature_vector = []
    for file in directory:
        f = open(dir + "/" + str(file), "r")
        frame_cnt = 0
        dists = []
        for i in range(20):
            dists.append([])
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
                    for idx in range(len(dists_2_bdy_cent)):
                        dists_2_bdy_cent[idx] = [x for x in dists_2_bdy_cent[idx] if np.isnan(x) == False]
                        dists[idx].append(dists_2_bdy_cent[idx])
                
                dists_2_bdy_cent = []
                joint_coords = []

            joint_coords.append([row[2], row[3], row[4]])
            dx = abs(row[2] - hip_center[0])
            dy = abs(row[3] - hip_center[1])
            dz = abs(row[4] - hip_center[2])
            dists_2_bdy_cent.append([dx, dy, dz])

        for joints in dists:
            dimensions = list(map(list, zip(*joints)))
            for dimension in dimensions:
                hist  = np.histogram(dimension, bins_N)
                counts = hist[0].tolist()
                for idx in range(len(counts)): # Normalize 
                    counts[idx] = counts[idx] / frame_cnt
                feature_vector.extend(counts) 
        
        for item in feature_vector:
            outfile.write(str(item) + ", ")
        outfile.write("\n")
        feature_vector = []

    outfile.close()

if __name__ == '__main__':
    main()
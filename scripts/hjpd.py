import os
import sys
import math
import numpy as np

def main(train, bins):
    if(train):
        dir = "data/dataset/train"
        outfile = open("data/hjpd_d2","w")
    else:
        dir = "data/dataset/test"
        outfile = open("data/hjpd_d2.t","w")
    directory = os.listdir(dir)
    frame_id = None
    joint_id = None
    bins_N = bins
    bins_M = bins
    index = 1
    dists_2_bdy_cent = []
    joint_coords = []
    feature_vector = []
    for file in directory:
        act = file[1:3]
        if act == "08":
            act = "1"
        elif act == "10":
            act = "2"
        elif act == "12":
            act = "3"
        elif act == "13":
            act = "4"
        elif act == "15":
            act = "5"
        elif act == "16":
            act = "6"
        else:
            return 'Error unexpected label'
        f = open(dir + "/" + str(file), "r")
        frame_cnt = 0
        dists = []
        for i in range(20):
            dists.append([])
        for line in f:
            stripped = line.strip().split()
            row = list(map(float, stripped))
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
        
        outfile.write(act + " ")
        for item in feature_vector:
            outfile.write(str(index) + ":" + str(item) + " ")
            index += 1
        outfile.write("\n")
        index = 1
        feature_vector = []

    outfile.close()

if __name__ == '__main__':
    main(train, bins)
import os
import sys
import math
import itertools
import numpy as np

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
        outfile = open("data/hod_d1","w")
    else:
        dir = "data/dataset/test"
        outfile = open("data/hod_d1.t","w")
    directory = os.listdir(dir)
    frame_id = None
    joint_id = None
    jnt_pos_cur = [[],[],[]] # x y and z for each of 20 joints
    jnt_pos_prev = [[],[],[]] 
    deltas = [[],[],[]] # dx, dy and dz for each of 20 joints
    l = [[],[],[]]
    theta = [[],[],[]]
    bins_N = 10
    bin = None
    #feature_vector = []
    hist = [[],[],[]]
    hists = []
    index = 1
    file_cnt = 0
    for plane in range(len(hist)):
        for i in range(bins_N):
            hist[plane].append(0)
    for i in range(20):
        hists.append(hist)
    l_accum = [[],[],[]]
    for plane_idx in range(len(l_accum)):
        for joint_idx in range(20):
            l_accum[plane_idx].append(0)

    for file in directory:
        f = open(dir + "/" + str(file), "r")
        frame_cnt = 0
        for line in f: # frame loop
            stripped = line.strip().split()
            row = list(map(float, stripped))
            frame_id = row[0]
            joint_id = row[1]
            if(joint_id == 1): # new frame
                frame_cnt+=1
                # get dx dy dz comparing current to previous position
                for xyorz_idx in range(len(jnt_pos_cur)):
                    for value_idx in range(len(jnt_pos_cur[xyorz_idx])):
                        if any(jnt_pos_prev):
                            deltas[xyorz_idx].append(jnt_pos_cur[xyorz_idx][value_idx] - 
                                                     jnt_pos_prev[xyorz_idx][value_idx])
                
                # Compute xy xz and yz mag for each joint and store
                for i in range(len(deltas[0])): 
                    l[0].append(math.sqrt(deltas[0][i]**2 + deltas[1][i]**2)) # lxy
                    l[1].append(math.sqrt(deltas[2][i]**2 + deltas[0][i]**2)) # lxz
                    l[2].append(math.sqrt(deltas[1][i]**2 + deltas[2][i]**2)) # lyz

                for plane_idx in range(len(l)):
                    for dist_idx in range(len(l[plane_idx])):
                        if not math.isnan(l[plane_idx][dist_idx]):
                            l_accum[plane_idx][dist_idx]+=l[plane_idx][dist_idx]


                # Compute angles
                for i in range(len(deltas[0])): # May need to revise 
                    
                    # theta[0].append(0) if l[0][i] == 0 else theta[0].append(math.asin(deltas[1][i] / l[0][i])) # Theta xy
                    # theta[1].append(0) if l[1][i] == 0 else theta[1].append(math.asin(deltas[0][i] / l[1][i])) # Theta xz
                    # theta[2].append(0) if l[2][i] == 0 else theta[2].append(math.asin(deltas[2][i] / l[2][i])) # Theta yz
                    
                    if 0 < deltas[0][i] and 0 < deltas[1][i]:  
                        theta[0].append(0) if l[0][i] == 0 else theta[0].append(math.asin(deltas[1][i] / l[0][i])) # Theta xy
                    elif deltas[0][i] < 0 and 0 < deltas[1][i]:
                        theta[0].append(0) if l[0][i] == 0 else theta[0].append(math.pi - math.asin(deltas[1][i] / l[0][i]))
                    elif deltas[0][i] < 0 and deltas[1][i] < 0:
                        theta[0].append(0) if l[0][i] == 0 else theta[0].append(math.pi + math.asin(abs(deltas[1][i]) / l[0][i]))
                    elif deltas[0][i] > 0 and deltas[1][i] < 0:
                        theta[0].append(0) if l[0][i] == 0 else theta[0].append(2*math.pi - math.asin(abs(deltas[1][i]) / l[0][i]))
                    else:
                        theta[0].append(0)
                                        
                    if 0 < deltas[2][i] and 0 < deltas[0][i]:
                        theta[1].append(0) if l[1][i] == 0 else theta[1].append(math.asin(deltas[0][i] / l[1][i])) # Theta xz
                    elif 0 > deltas[2][i] and 0 < deltas[0][i]:
                        theta[1].append(0) if l[1][i] == 0 else theta[1].append(math.pi - math.asin(deltas[0][i] / l[1][i]))
                    elif 0 > deltas[2][i] and 0 > deltas[0][i]:
                        theta[1].append(0) if l[1][i] == 0 else theta[1].append(math.pi + math.asin(abs(deltas[0][i]) / l[1][i]))
                    elif 0 < deltas[2][i] and 0 > deltas[0][i]:
                        theta[1].append(0) if l[1][i] == 0 else theta[1].append(2*math.pi - math.asin(abs(deltas[0][i]) / l[1][i]))
                    else:
                        theta[1].append(0)
                    
                    if 0 < deltas[2][i] and 0 < deltas[1][i]:
                        theta[2].append(0) if l[2][i] == 0 else theta[2].append(math.asin(deltas[2][i] / l[2][i])) # Theta yz
                    elif 0 > deltas[2][i] and 0 < deltas[1][i]:
                        theta[2].append(0) if l[2][i] == 0 else theta[2].append(math.pi - math.asin(abs(deltas[2][i]) / l[2][i]))
                    elif 0 > deltas[2][i] and 0 > deltas[1][i]:
                        theta[2].append(0) if l[2][i] == 0 else theta[2].append(math.pi + math.asin(abs(deltas[2][i]) / l[2][i]))
                    elif 0 < deltas[2][i] and 0 > deltas[1][i]:
                        theta[2].append(0) if l[2][i] == 0 else theta[2].append(2*math.pi - math.asin(deltas[2][i] / l[2][i])) 
                    else:
                        theta[2].append(0)
                
                for plane_idx in range(len(deltas)):
                    for joint_idx in range(len(deltas[0])):
                        # Check angle bin
                        angle = theta[plane_idx][joint_idx]
                        for i in range(bins_N):
                            if(i*(2*math.pi/bins_N) <= angle < (i+1)*(2*math.pi/bins_N)):
                                bin = i
                        
                        if not math.isnan(l[plane_idx][joint_idx]):                            
                            hists[joint_idx][plane_idx][bin] += l_accum[plane_idx][joint_idx] # need accumulated l
                
                        
                jnt_pos_prev = jnt_pos_cur
                jnt_pos_cur = [[],[],[]]
                deltas = [[],[],[]]
                l = [[],[],[]]
                theta = [[],[],[]]
            
            jnt_pos_cur[0].append(row[2])
            jnt_pos_cur[1].append(row[3])
            jnt_pos_cur[2].append(row[4])  

        #Normalize hists
        feature_vector = []
        for joint_idx in range(len(hists)):
            for plane_idx in range(len(hists[joint_idx])):
                for value in range(len(hists[joint_idx][plane_idx])):
                    feature_vector.append(hists[joint_idx][plane_idx][value] / frame_cnt)
        
        outfile.write(str(file_cnt//label_mod) + " ")
        for item in feature_vector:
            outfile.write(str(index) + ":" + str(item) + " ")
            index+=1
        outfile.write("\n")
        index = 1
        file_cnt+=1
        
        feature_vector = []
        hist = [[],[],[]]
        hists = []
        for plane in range(len(hist)):
            for i in range(bins_N):
                hist[plane].append(0)
        for i in range(20):
            hists.append(hist)
        
        l_accum = [[],[],[]] # re initialize l_accum w/ zero this is very ugly 
        for plane_idx in range(len(l_accum)):
            for joint_idx in range(20):
                l_accum[plane_idx].append(0) 

    outfile.close()

if __name__ == '__main__':
    main()
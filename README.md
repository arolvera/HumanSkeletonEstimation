# CSCI573_project3

## Running scripts
This repositiory contains the following three implementations of skeleton based representations
relative angles and displacments (RAD), histograms of joint position diferences (HJPD) and histogram 
of oriented displacements. Each method is implemented in its own python script in the project/scripts 
directory and can be ran using 
$ /usr/bin/python3 PATH/TO/project/scripts/script.py Train 
where script is "rad.py" for example. Ensure the the directory structure under /project is not 
altered to maintain functionality. Each script takes a command line argument "Train" or "Test" and 
defaults to "Test" when no argument is passed. The script will generate the coresponding test or 
train file under the project/data directory.      

## Implementation details
For the RAD implementation the five joimts that form a star skeleton were selected. A normalized 
histogram of 10 bins for both the reletive distances and angles are computed by for each of the five 
distances and angles of the star skeleton. the histograms are then concatenated as the feature 
vector for each frame. The HJPD implementation is similar exept the distances are stored for all 20 
joints and a normalized histogram of 10 bins is computed for each x,y and z component of the 
distances which are concatenated together for each frame as the feature vector. Lastley the HOD 
implementation computes a normalized histogram of 10 bins where the counst are the length of the 
trajectory from the previous frame and the bin is defined by in which fraction division of bin size
between 0 and 360 degrees the trajectorys angle is reletive to the x axis. Three histograms for each
2d projection are concatenated for each of the 20 joint trajectories as a feature vector for each
frame.    

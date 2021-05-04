# CSCI573_project3

## Running scripts
This repositiory contains the following three implementations of skeleton based representations
relative angles and displacments (RAD), histograms of joint position diferences (HJPD) and histogram 
of oriented displacements. Each method is implemented in its own python script in the project/scripts 
directory. these scripts can no longer be ran individually, the predict.py script will invoke a given representation with the specified number of bins passed as a command line arguments a prediction is 
ran as follows 
$ /usr/bin/python3 PATH/TO/project/scripts/predict.py hjpd 25
This will train and test the model for the hjpd representation using 25 bins and output accuracy and 
confusion matrix. The plot.py script can be ran to generate a plot of accuracy vs number of bins.
Plots have already been generated for grid search and accuracy vs bin number and can be viewed under 
the plots directory. Ensure the directory structure under /project is not altered to maintain 
functionality.      

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

## Best c and gamma
For the RAD representation grid search returned 8.0 for the best C and 2.0 for the best gamma

For the HJPD representation grid search returned 2.0 for the best C and 0.125 for the best gamma

For the HOD representation grid search returned 128.0 for the best C and 0.0 for the best gamma

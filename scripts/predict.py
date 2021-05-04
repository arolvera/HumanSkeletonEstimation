from sklearn.metrics import confusion_matrix 
from libsvm.svmutil import *
import os
import sys
import hjpd
import hod
import rad

def main():
    bins = 10
    n_args = len(sys.argv) - 1
    if(n_args == 0):
        print("Error please specify representation")
        return 
    if(sys.argv[1] != "rad" and sys.argv[1] != "hjpd" and sys.argv[1] != "hod"):
        print("Error invalid representation")
        return
    representation = sys.argv[1]
    if(n_args != 1 and n_args != 2):
        print("Error incorrect arguments")
        return 
    for arg in range(1, n_args+1):
        if sys.argv[arg].isdigit():
            bins = int(sys.argv[arg])
    if(representation == "rad"):
        rad.main(True, bins)
        rad.main(False, bins)
    elif(representation == "hjpd"):
        hjpd.main(True, bins)
        hjpd.main(False, bins)
    elif(representation == "hod"):
        hod.main(True, bins)
        hod.main(False, bins)
    else:
        print("Error unhandled condition")
        return

    file = os.getcwd() + "/data/" + representation + "_d2"
    file_t = os.getcwd() + "/data/" + representation + "_d2.t"

    labels, x = svm_read_problem(file)
    labelst, xt = svm_read_problem(file_t)

    if(representation == "rad"):
        m = svm_train(labels, x, '-c 8 -g 2')
    elif(representation == "hjpd"):
        m = svm_train(labels, x, '-c 2 -g 0.125')
    elif(representation == "hod"):
        m = svm_train(labels, x, '-c 128 -g 0')

    p_label, p_acc, p_val = svm_predict(labelst, xt, m)
    accuracy = p_acc[0]
    with open(file_t) as f:
        y_true = [int(line.split()[0]) for line in f]
    
    matrix = confusion_matrix(y_true, p_label)
    
    print("Accuracy is: ", accuracy)
    print("Confusion Matrix is: ", "\n", matrix)
      

if __name__ == '__main__':
    main()
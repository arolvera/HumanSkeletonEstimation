from libsvm.svmutil import *
import matplotlib.pyplot as plt
import os
import sys
import hjpd
import hod
import rad

def main():
    bins = 10
    accuracies = []
    bin_nums = []
    n_args = len(sys.argv) - 1
    if(n_args == 0):
        print("Error please specify representation")
        return 
    if(sys.argv[1] != "rad" and sys.argv[1] != "hjpd" and sys.argv[1] != "hod"):
        print("Error invalid representation")
        return
    representation = sys.argv[1]
    file = os.getcwd() + "/data/" + representation + "_d2"
    file_t = os.getcwd() + "/data/" + representation + "_d2.t"
    for bins in range(3, 99, 3):
        print("Bins = ", bins)
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
        labels, x = svm_read_problem(file)
        labelst, xt = svm_read_problem(file_t)
        m = svm_train(labels, x)
        p_label, p_acc, p_val = svm_predict(labelst, xt, m)
        accuracy = p_acc[0]
        bin_nums.append(bins)
        accuracies.append(accuracy)
    
    plt.plot(bin_nums, accuracies)
    plt.ylabel("Accuracy")
    plt.xlabel("Number of Bins")
    plt.title(representation + " accuracy vs number of bins")
    plt.savefig(os.getcwd() + "/plots/" + representation + ".jpg")
    plt.show()
        




    
    

if __name__ == '__main__':
    main()
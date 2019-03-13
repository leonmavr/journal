import numpy as np
import csv
import matplotlib.pyplot as plt
# Setting the random seed, feel free to change it and see different solutions.
np.random.seed(42)


def stepFunction(t):
    if t >= 0:
        return 1
    return 0


def prediction(X, W, b):
    return stepFunction((np.matmul(X,W)+b)[0])


# TODO: Fill in the code below to implement the perceptron trick.
# The function should receive as inputs the data X, the labels y,
# the weights W (as an array), and the bias b,
# update the weights and bias W, b, according to the perceptron algorithm,
# and return W and b.
def perceptronStep(X, y, W, b, learn_rate = 0.01):
    for i, XX in enumerate(X):
        y_pred = prediction(X[i], W, b)
        #print(y_pred, y[i])
        if y[i] == 1 and y_pred == 0:
            W[0] += X[i][0] * learn_rate
            W[1] += X[i][1] * learn_rate
            b += 1 * learn_rate
        elif y[i] == 0 and y_pred == 1:
            W[0] -= X[i][0] * learn_rate
            W[1] -= X[i][1] * learn_rate
            b -= 1 * learn_rate
    return W, b
    

# This function runs the perceptron algorithm repeatedly on the dataset,
# and returns a few of the boundary lines obtained in the iterations,
# for plotting purposes.
# Feel free to play with the learning rate and the num_epochs,
# and see your results plotted below.
def trainPerceptronAlgorithm(X, y, learn_rate = 0.01, num_epochs = 25):
    x_min, x_max = min(X.T[0]), max(X.T[0])
    y_min, y_max = min(X.T[1]), max(X.T[1])
    W = np.array(np.random.rand(2,1))
    b = np.random.rand(1)[0] + x_max
    # These are the solution lines that get plotted below.
    boundary_lines = []
    for i in range(num_epochs):
        # In each epoch, we apply the perceptron step.
        W, b = perceptronStep(X, y, W, b, learn_rate)
        boundary_lines.append((-W[0]/W[1], -b/W[1]))
    return boundary_lines


def readData(fpath = 'data.csv'):
    """
        Reads input data, each line is of the form:
        x1, x2, y
        Note that y = 0 or 1
    """
    with open(fpath) as csvf:
        X = []
        y = []
        csv_data= csv.reader(csvf, delimiter = ',')
        for row in  csv_data:
            X.append([float(row[0]), float(row[1])])
            y.append(float(row[2]))
    X = np.array(X, np.float32)
    y = np.array(y, np.float32)
    return X, y


def plotData(X, y):
    """
        Plots what is returned by readData 
    """
    for i in  range(len(X)):
        if y[i] == 1:
            plt.plot(X[i][0], X[i][1], "o", color = 'blue')
        elif y[i] == 0:
            plt.plot(X[i][0], X[i][1], "o", color = 'red')


def plotBoundaries(bound_coeffs):
    """
        Plots the straight lines returned by trainPerceptronAlgorithm 
    """
    plt.xlim((-0.2,1.2))
    plt.ylim((-0.2,1.2))
    # boundary_lines.append((-W[0]/W[1], -b/W[1]))
    for i in  range(len(bound_coeffs)):
        x = np.linspace(0, 1, 50)
        y = bound_coeffs[i][0]*x +  bound_coeffs[i][1] 
        if i != len(bound_coeffs) - 1:
            plt.plot(x, y, 'g--', lw=1)
        else:
            plt.plot(x, y, 'g-', lw=2)


def main():
    X, y = readData()
    plotData(X,y) 
    boundaries = trainPerceptronAlgorithm(X,y)
    plotBoundaries(boundaries)
    plt.xlabel('x1')
    plt.ylabel('x2')
    plt.show()


main()



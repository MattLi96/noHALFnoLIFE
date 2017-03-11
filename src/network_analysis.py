import networkx as nx
from collections import Counter
import matplotlib.pyplot as plt
import math

class NetworkAnalysis:
    def __init__(self, G): #TODO any settings for the network analysis
        self.G = G
        self.outputPath = "../output/"
    
    def generateDegreeDistribution(self):
        output = open(self.outputPath + "raw/degreeDistribution.txt", "w")

        degree = nx.degree(self.G)
        C = Counter(degree.values())

        maxDegree = degree[max(degree, key=lambda i: degree[i])]

        logx, logy = ([] for i in range(2))

        for i in range(0, maxDegree+1):
            freq = C[i]
            output.write(str(i) + " " + str(freq) + "\n")
            if i > 0 and freq > 0:
                logx.append(math.log(i))
                logy.append(math.log(freq))
        
        output.close()

        self.makePlot('Log Histogram of Degree Frequencies', 'log j', 'log n_j', logx, logy, self.outputPath + "graphs/degreeDistribution.png")

    def makePlot(self, title, xaxis, yaxis, xdata, ydata, path):
        fig = plt.figure()
        fig.suptitle(title, fontsize=14, fontweight='bold')

        ax = fig.add_subplot(111)
        fig.subplots_adjust(top=0.85)

        ax.set_xlabel(xaxis)
        ax.set_ylabel(yaxis)

        ax.scatter(x = xdata, y = ydata)
        plt.scatter(x = xdata, y = ydata)
        
        plt.savefig(path)
        plt.close()

if __name__ == '__main__':
    pass



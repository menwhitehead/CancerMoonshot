import sys
import string
import csv
import random
from sklearn.manifold import TSNE
from sklearn import random_projection
import numpy as np
import matplotlib.pyplot as plt
from metadata import *
import FeatureDataset

graph_color = (31 / 255., 119 / 255., 180 / 255.)

def getCleanedTitleWords(title):
    result = []
    title_words = title.split()
    for title_word in title_words:
        cleaned = ''
        for c in title_word.lower():
            if c in string.ascii_lowercase:
                cleaned += c
            else:
                cleaned += ' '
        result += cleaned.split()
    return result

def loadCancerTitleWords(filename):
    all_words = {}
    f = open(filename, 'r')
    csvf = csv.reader(f, delimiter=',', quotechar='"')
    for line in csvf:
        title_words = getCleanedTitleWords(line[-18])
        tokens = line[1].split()
        if len(tokens) > 1:
            doc_id = '0' + tokens[1]
        else:
            doc_id = -1

        if doc_id in cp.doc_centroids:
            for title_word in title_words:
                if title_word not in all_words:
                    all_words[title_word] = []
                all_words[title_word].append(doc_id)
    return all_words

class ClusterPlotter:

    def __init__(self, centroids_filename):
        self.centroid_size = 300
        self.doc_limit = 200
        self.meta = Metadata()
        self.doc_ids = []
        self.doc_centroids = FeatureDataset.loadFeatures(centroids_filename)

    def loadRelevantCentroids(self, doc_list):
        dataset = []
        self.dataset_docids = []
        for doc_id in doc_list:
            if doc_id in self.doc_centroids:
                dataset.append(self.doc_centroids[doc_id])
                self.dataset_docids.append(doc_id)
                if len(dataset) >= self.doc_limit:
                    break
        self.X = np.array(dataset)

    #TSNE
    def clusterDocs(self):
        model = TSNE(n_components=2, random_state=0)
        np.set_printoptions(suppress=True)
        self.Y = model.fit_transform(self.X)

    def storeDotCoordinates(self, filename):
        o = open(filename, 'w')
        for i in range(len(self.coordinates)):
            o.write("%s, %.2f, %.2f\n" % (self.dataset_docids[i], self.coordinates[i][0], self.coordinates[i][1]))
        o.close()

    def plotCluster(self, filename="test.png", dot_size=50):
        plt.figure(2, figsize=(8, 6))
        plt.clf()
        fig, ax = plt.subplots(figsize=(8, 6), dpi=100)#(111)

        ax.spines["top"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
        plt.tick_params(axis="both", which="both", bottom="off", top="off",
                      labelbottom="off", left="off", right="off", labelleft="off")

        ax.scatter(self.Y[:, 0], self.Y[:, 1], color=graph_color, s=dot_size)

        # Get the x and y data and transform it into pixel coordinates
        x, y = self.Y[:, 0], self.Y[:, 1]
        xy_pixels = ax.transData.transform(np.vstack([x, y]).T)
        xpix, ypix = xy_pixels.T
        width, height = fig.canvas.get_width_height()
        ypix = height - ypix

        self.coordinates = zip(xpix, ypix)
        plt.savefig(filename)

    def plotAllClusters(self, all_words, min_threshold=10):
        for word, doc_list in all_words.items():
            print "Working on...", word, doc_list
            count = len(doc_list)
            if count >= min_threshold:
                img_filename = "cancer_viz/%s.png" % word
                dat_filename = "cancer_viz/%s.dat" % word
                self.loadRelevantCentroids(doc_list)
                print "\tFound %d relevant docs" % len(cp.X)
                self.clusterDocs()
                self.plotCluster(filename=img_filename)
                self.storeDotCoordinates(filename=dat_filename)



if __name__=="__main__"

    # Document embeddings file
    # Word embeddings obtained using skip-gram algorithm
    # in word2vec
    # Doc embeddings are centroids of word embeddings
    # for all words in the document
    centroids_filename = sys.argv[1]

    cp = ClusterPlotter(centroids_filename)

    filename = "cancer.csv"   # CSV dataset from USPTO
    all_words = loadCancerTitleWords(filename)
    print "Found %d words" % len(all_words)
    cp.plotAllClusters(all_words)







#

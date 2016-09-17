import sys
from sklearn.feature_extraction.text import TfidfVectorizer
import FeatureDataset

corpus_filename = sys.argv[1]
features_filename = "" # Filepath to your word embeddings file
size_limit = 10
corpus = []
f = open(corpus_filename, 'r')
line_count = 0
for line in f:
    line_count += 1
    patent_id = line.split()[0]
    corpus.append(line)
    if len(corpus) >= size_limit:
       break
f.close()

#print "calculating tfidf..."
vectorizer = TfidfVectorizer(min_df=0.002, max_df=0.2)
tfidf = vectorizer.fit_transform(corpus)
tfidf_words = vectorizer.get_feature_names()

#print "loading word features..."
features = FeatureDataset.loadFeatures(features_filename)

#print "calculating vecs..."
f = open(corpus_filename, 'r')
line_count = 0
for line in f:
    line_count += 1
    curr_tfidf = vectorizer.transform([line]).toarray()[0]
    running_sum = [0.0] * len(features.values()[0])
    for i in range(len(curr_tfidf)):
        if abs(curr_tfidf[i]) != 0:
            word = tfidf_words[i]
            if word in features:
                running_sum = FeatureDataset.add(running_sum, features[word])
    print line.split()[0],
    num_words = len(line.split())
    for val in running_sum:
       print "%.8f" % (val / num_words),
    print

f.close()

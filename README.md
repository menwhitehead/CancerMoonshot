# A Tool for Visualizing and Analyzing Relationships among Cancer-Related Patents

This repository contains supporting code for our USPTO Cancer Moonshot Challenge entry.

The backend code performs the clusterings and generates the corresponding images.  To use the code:

  1. You must download bulk patent texts from the USPTO.  
  2. You can extract individual patents from their XML using the "dump_all_patent_documents.py" script. This generates a large, cleaned text file of patents with one patent on each line.  
  3. You must run word2vec on the dataset to generate word embeddings.
  4. Run create_doc_centroids.py to generate all the patent embeddings
  5. Run cluster_cancer_documents.py to generate all t-SNE clustering images

Visualization code is in the Javascript (js) directory.  This code just loads the pre-generated t-SNE clustering images and adds interactivity.

The viz_images directory shows a few example images along with their data files used to provide interactivity with mouse clicks.

Reference-style: 
![alt text][logo]

[logo]: http://cs.coloradocollege.edu/~mwhitehead/CancerMoonshot/viz_images/cell.png "Visualization for Patents matching CELL"

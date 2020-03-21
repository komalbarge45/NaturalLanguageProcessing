# NaturalLanguageProcessing
Natural Language Processing assignments at Lakehead University.

For Assignment 1,

The california dataset that has been used to work on this assignment 1 can be found at this below link:
https://github.com/ageron/handson-ml/tree/master/datasets/housing


Steps to run the code:
1. Open '1095709_Assignment1.ipynb' file in python notebook platform like jupyter notebook or Google colab platform.
2. A trained model can be found in '1095709_1dconv_reg' file.
3. You can have a look at the proposed model in provided report or in 'DesignedModel.png' image file.

For Assignment 2,

The Rotten Tomatoes Movie Reviews dataset that has been used to work on this assignment 2 can be found at this below link:
https://raw.githubusercontent.com/cacoderquan/Sentiment-Analysis-on-the-Rotten-Tomatoes-movie-review-dataset/master/train.tsv

Steps to run the code:
1. Open '1095709_Assignment2.ipynb' file in python notebook platform like jupyter notebook or Google colab platform.
2. You will need GloVe word embeddings file which can be downloaded from https://www.kaggle.com/terenceliu4444/glove6b100dtxt .
3. A trained model with the weights can be found in '1095709_1dconv_reg.json' and '1095709_1dconv_reg.h5' files.
4. You can load the trained model with the help of json file, but you will also need to load the weights for the trained model through h5 format file.
You can find the code for loading the trained model and running it in last cell of the notebook. It will give you the validation accuracy on testing dataset.
5. To get the processed testing dataset, you need to run till the cell where we have performed padding of the sequences just before importing GloVe word embeddings.
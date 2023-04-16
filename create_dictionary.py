# 1.2 Creating a dictionary of Positive and Negative words
# This script uses words found in master_dictionary directory to create a dictionary before analyzing data
# Creates dictionary file in "dictionary" folder
import os
import re
import json

cwd = os.getcwd()
dictionary_path = os.path.join(cwd, 'master_dictionary')

pattern = r'([\wī\'\*-]*)'

word_dictionary = {
    'negative_words': [],
    'positive_words': []
}

os.chdir(dictionary_path)
word_files = os.listdir()

for file in word_files:

    if file == 'negative_words.txt':
        with open(file, 'r') as neg_words_file:

            # Changes directory to loop over stopwords files
            search_path = os.path.join(cwd, 'stopwords')
            os.chdir(search_path)
            stopwords_files = os.listdir()

            # Checks individual words in negative_words.txt
            for line in neg_words_file:
                line = line.rstrip('\n')
                # Boolean switch that triggers if the word is in any of the files
                isFound = False
                # checks if word/line exists in any stopwords file first
                for s_file in stopwords_files:
                    with open(s_file, 'r') as current_file:
                        data = current_file.read()
                        if line in data:
                            isFound = True
                            continue
                if isFound == False and line not in word_dictionary['negative_words']:
                    word_dictionary['negative_words'].append(line)

        os.chdir(dictionary_path)    
            
    if file == 'positive_words.txt':
        with open(file, 'r') as pos_words_file:

            search_path = os.path.join(cwd, 'stopwords')
            os.chdir(search_path)
            stopwords_files = os.listdir()

            for line in pos_words_file:

                line = line.rstrip('\n')
                isFound = False

                for s_file in stopwords_files:
                    with open(s_file, 'r') as current_file:
                        data = current_file.read()
                        if line in data:
                            isFound = True
                            continue
                if isFound == False and line not in word_dictionary['positive_words']:
                    word_dictionary['positive_words'].append(line)

        os.chdir(dictionary_path)

with open('dictionary.json', 'w') as dic:
    json.dump(word_dictionary, dic)

print("Dictionary available in directory 'master_dictionary/dictionary.json'.")
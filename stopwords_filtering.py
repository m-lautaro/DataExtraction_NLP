# Cleaning using Stop Words Lists - this script filters out words from stopwords guidelines
import os
import re
import nltk
nltk.download('stopwords')
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords

cwd = os.getcwd()

stopwords = []
stopwords_path = os.path.join(cwd, 'stopwords')

stopwords_files = os.listdir(stopwords_path)
for sw_file in stopwords_files:
    sw_filepath = os.path.join(stopwords_path, sw_file)
    with open(sw_filepath, 'r', encoding='utf-8') as f:
        for line in f:
            pattern = r'([\w\'%/.]*)'
            match = re.search(pattern, line)
            if match:
                word = match.group(1)
                stopwords.append(word)

# excluded_values = [',', '.', ':', '%', '(', ')', '"', '“', '”', '’', '?', '!', '#']
# for val in excluded_values: 
#     stopwords.append(val)

src_file_directory = os.path.join(cwd, 'source_files')
modified_files_path = os.path.join(cwd, 'clean_files')

# pattern = r'([\w\'%/.]+)'

if not os.path.exists(modified_files_path):
    os.makedirs(modified_files_path)

source_files = os.listdir(src_file_directory)

# Loops through all files
for file in source_files:
    
    src_filepath = os.path.join(src_file_directory, file)
    clean_filepath = os.path.join(modified_files_path, file)
    
    with open(src_filepath, 'r', encoding='utf-8') as source_file:
        
        fileName = file
         
        srcText = source_file.read()

        wordTokens = word_tokenize(srcText)

        clean_words = [word for word in wordTokens if word.lower() not in stopwords]
        clean_text = ' '.join(clean_words)
        
        with open(clean_filepath, 'w', encoding='utf-8') as clean_file:
            clean_file.write(clean_text)
            
print('Removed stopwords from source files. Clean files available in new directory.')        
# DataExtraction_NLP
Project Breakdown
Given a ".xlsx" file, takes all information from websites in the file and extracts its data. Then, data is filtered by removing all words contained in the files in "stopwords" directory. After that, text analysis is performed for each of the files in the original spreadsheet. The final output is a series of calculations that are written to the corresponding output in a .xlsx file.

How to run this project:
1. Run "create_source_files.py" to get data from websites that are in the given "Input.xlsx" file. Each website generates a file in "source_files" directory with the required data extracted.
2. Run "stopwords_filtering.py" to remove specific words from source files. Words that are removed are contained in each of the files in the "stopwords" directory. This program creates a "clean_files" directory with the new data already filtered.
3. Run "create_dictionary.py". This script uses words found in "master_dictionary" directory to create a dictionary with words that are not found in stopwords list before analyzing data.
4. Run "text_analysis.py" to perform calculations. This script uses functions from "derived_variables_extractor.py" over files in "clean_files" directory and prints the result in the spreadsheet found in "output" directory.

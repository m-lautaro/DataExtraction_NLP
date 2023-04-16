import os
import json
import nltk
from nltk import word_tokenize, sent_tokenize
import string
import re

dic_data = {}

# Loads dictionary data
with open('master_dictionary/dictionary.json', 'r') as dic:
    dic_data = json.load(dic)
#

# Computes Positive Score, Negative Score, Subjectivity Score, Polarity Score

# Positive Score: This score is calculated by assigning the value of +1 for each word if found
# in the Positive Dictionary and then adding up all the values.
#
def calculatePositiveScore(data):
    
    totalScore = 0
    dic = dic_data['positive_words']
    count_list = []

    for item in set(data):
        if item in dic:
            count = data.count(item)
            count_list.append((item, count))
    
    for i, element in enumerate(count_list):
        totalScore += count_list[i][1]

    return totalScore
#

# Negative Score: This score is calculated by assigning the value of -1 for each word if found
# in the Negative Dictionary and then adding up all the values. We multiply the score with -1
# so that the score is a positive number.
#
def calculateNegativeScore(data):
    
    totalScore = 0
    dic = dic_data['negative_words']
    count_list = []

    for item in set(data):
        if item in dic:
            count = data.count(item)
            count_list.append((item, count))
    
    for i, element in enumerate(count_list):
        totalScore += count_list[i][1]

    return totalScore
#

# Polarity Score: This is the score that determines if a given text is positive or negative in
# nature. It is calculated by using the formula:
# Polarity Score = (Positive Score – Negative Score) / ((Positive Score + Negative Score) +
# 0.000001)
# Range is from -1 to +1
#
def calculatePolarityScore(data):

    positiveScore = calculatePositiveScore(data)
    negativeScore = calculateNegativeScore(data)

    polarityScore = (
        (positiveScore - negativeScore) / (
            (positiveScore + negativeScore) + 0.000001
        )
    ) 

    print('Polarity Score: ', polarityScore)
    return polarityScore
#

# Subjectivity Score: This is the score that determines if a given text is objective or subjective.
# It is calculated by using the formula:
# Subjectivity Score = (Positive Score + Negative Score)/ ((Total Words after cleaning) +
# 0.000001)
# Range is from 0 to +1
#
def calculateSubjectivityScore(data):

    positiveScore = calculatePositiveScore(data)
    negativeScore = calculateNegativeScore(data)

    totalWords = len(data)
    subjectivityScore = (
        (positiveScore + negativeScore) / (
            (totalWords) + 0.000001
        )
    )

    print('Subjectivity Score: ', subjectivityScore)
    return subjectivityScore

# 2 Analysis of Readability
# Analysis of Readability is calculated using the Gunning Fox index formula described below.

# Average Sentence Length = the number of words / the number of sentences
#
def calculateAverageSentenceLength(tokens, sentences):
    num_words = len(tokens)
    num_sentences = len(sentences)

    averageSentenceLength = ( num_words / num_sentences )

    print('Average Sentence Length: ', averageSentenceLength)
    return averageSentenceLength    
#

# Percentage of Complex words = the number of complex words / the number of words
# 
def calculateComplexWords(tokens):
    
    vowels = set("aeiouy")

    # Define a function to count the number of syllables in a word
    def count_syllables(word):
        count = 0
        prev_char_was_vowel = False
        for char in word.lower():
            if char in vowels:
                if not prev_char_was_vowel:
                    count += 1
                prev_char_was_vowel = True
            else:
                prev_char_was_vowel = False
        return count
    
    # Count the number of complex words in the text
    complex_word_count = 0
    for word in tokens:
        # Remove any punctuation from the word
        word = word.translate(str.maketrans("", "", string.punctuation))
        syllable_count = count_syllables(word)
        if syllable_count > 2:
            complex_word_count += 1

    percentage_complex_words = ( complex_word_count / len(tokens) )

    print('Number of complex words: ', complex_word_count)
    print(f'Percentage of complex words: {percentage_complex_words} %')

    complexWords = {
        "count": complex_word_count,
        "percentage": percentage_complex_words
    }

    json_string = json.dumps(complexWords)
    return json_string
#

# Fog Index = 0.4 * (Average Sentence Length + Percentage of Complex words)
def calculateFogIndex(tokens, sentences):
    
    avgSentenceLength = calculateAverageSentenceLength(tokens, sentences)
    json_string = calculateComplexWords(tokens)
    json_obj = json.loads(json_string)
    complexWordsPercent = json_obj['percentage']
    
    fogIndex = (
        0.4 * ( avgSentenceLength +  complexWordsPercent)
    )

    print('Fog Index: ', fogIndex)
    return fogIndex

# Average Number of Words Per Sentence
# Average Number of Words Per Sentence = the total number of words / the total number of
# sentences
def calculateAverageWordPerSentence(tokens, sentences):
    print('Number of words: ', len(tokens))
    print('Number of sentences: ', len(sentences))
    avgWordPerSentence = (len(tokens) / len(sentences))
    print(f'Avg. Number of Words Per Sentence: {avgWordPerSentence}')
    return avgWordPerSentence

def is_complex(word):
    syllables = nltk.tokenize.word_tokenize(word)
    return len(syllables) > 2
#

# Syllable Count Per Word
#
def count_syllables(words):
    syllables_per_word = {}

    for word in words:
        # Convert the word to lowercase to simplify the logic
        word = word.lower()

        # If the word ends with "es" or "ed", remove them as they don't count as syllables
        if word.endswith("es") or word.endswith("ed"):
            word = word[:-2]

        # Count the vowels in the word
        num_vowels = len([c for c in word if c in "aeiouy"])

        # If the word ends with "e", subtract one vowel as it's often silent
        if word.endswith("e"):
            num_vowels -= 1

        # Add the word and its syllable count to the dictionary
        syllables_per_word[word] = num_vowels

    totalSyllables = sum(syllables_per_word.values())
    totalPerWord = (totalSyllables / len(words))
    print('Total Syllables per Word: ', totalPerWord)
    return totalPerWord
#

# Personal Pronouns
# To calculate Personal Pronouns mentioned in the text, we use regex to find the counts of the
# words - “I,” “we,” “my,” “ours,” and “us”. Special care is taken so that the country name US
# is not included in the list.
#
def calculatePersonalPronouns(text):
    # Define regular expression for personal pronouns
    pronoun_pattern = r'\b(I|we|my|ours|us)\b'

    # Use regular expression to find all personal pronouns in the text
    personal_pronouns = re.findall(pronoun_pattern, text)

    # Filter out "US" from the list of personal pronouns
    personal_pronouns = [p for p in personal_pronouns if p != 'US']

    # Count the number of personal pronouns found
    num_personal_pronouns = len(personal_pronouns)

    # Print the number of personal pronouns found
    print("Number of personal pronouns found:", num_personal_pronouns)
    return num_personal_pronouns
#

# Average Word Length
# Sum of the total number of characters in each word/Total number of words
# 
def calculateAverageWordLength(text):
    
    totalNumberOfWords = len(text)
    word_counts = []
    totalCharacters = 0

    for word in text:
        count = len(word)
        word_counts.append((word, count))

    for word in word_counts:
        totalCharacters += word[1]

    avgWordLength = ( totalCharacters / totalNumberOfWords )

    print('Total Characters: ', totalCharacters)
    print('Average Word Length: ', avgWordLength)
    return avgWordLength
#
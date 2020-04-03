import os 

# sorts the given dict by the name and removes duplicates.
# writes the result to sorted_dict.txt
def sort_dict():
    with open('source/dict.txt', 'r') as f:
        words = f.readlines()

    sorted_words = sorted(words, key=lambda v: v.lower())

    with open('source/sorted_dict.txt', 'w') as f:
        last = ''
        for word in sorted_words:
           if last != word:
              print(word[:-1], file=f)
           last = word 


# reads the result of the spell checking (make spelling), counts for every misspelled words its amount
# and returns a sorted list of word and amount to the shell and creates a new_words.txt just with the 
# words found in the analysis. 
def read_terms_from_errors():
    if os.path.isfile('build/spelling/output.txt'):
        with open('build/spelling/output.txt', 'r') as f:
            lines = f.readlines()

        new_words = {}

        for line in lines:
           word = line.split("(")[1][:-3]
           if word not in new_words:
               new_words[word] = 1
           else:
               new_words[word] += 1

        with open('new_words.txt', 'w') as f:
           for word in sorted(new_words, key=lambda w: new_words[w], reverse=True):
               print(word, file=f)
               print(word, new_words[word])

        print('\nFound %d unique words in a total of %d misspelled words' % (len(new_words), len(lines)))


read_terms_from_errors()
sort_dict()

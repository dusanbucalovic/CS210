import re
from math import log
from collections import OrderedDict

# Part 1-1
def clean_documents(list_of_docs):
    cleaned_documents = {}
    
    for document in list_of_docs:
        cleaned_documents[document] = []

        try:
            with open(document, "r") as file:
                word_count = 0

                for line in file:
                    line = line.strip()
                    cleaned_line = []
                    
                    # Remove links, punctuation and extra whitespace
                    words = re.split(r'\s+',line)

                    for word in words:
                        new_word = ''

                        if word.startswith('http://') or word.startswith('https://'):
                            continue
                        
                        for c in word:
                            if c.isalpha():
                                new_word = new_word + c.lower()
                            elif c.isnumeric() or c == '_':
                                new_word = new_word + c

                        cleaned_line.append(new_word)

                    cleaned_documents[document].append(cleaned_line)
                
        except IOError:
            print(document, "not found. Exiting program.")
            return
    
    return cleaned_documents

def main():
    # Part 1-1
    docs_file = open('tfidf_docs.txt', "r")
    list_of_docs = []

    for line in docs_file:
        doc = line.strip()
        list_of_docs.append(doc)
    
    docs_file.close()

    cleaned_documents = clean_documents(list_of_docs)

    # Part 1-2
    stop_words_set = set()

    try:
        with open('stopwords.txt', "r") as file:
            for word in file:
                stop_words_set.add(word.strip())
    except IOError:
        print("stopwords.txt not found. Exiting program.")
        return

    for document in cleaned_documents:
        sentences = cleaned_documents[document]

        for sentence in sentences:
            sentence_copy = sentence.copy()
            for word in sentence:
                if word in stop_words_set:
                    sentence_copy.remove(word)
            
            index = sentences.index(sentence)
            sentences[index] = sentence_copy
    
    # Part 1-3
    for document in cleaned_documents:
        sentences = cleaned_documents[document]

        for sentence in sentences:
            for word in sentence:
                original_word = word
                if word.endswith('ing'):
                    word = word[:-3]
                elif word.endswith('ly'):
                    word = word[:-2]
                elif word.endswith('ment'):
                    word = word[:-4]

                index = sentence.index(original_word)
                sentence[index] = word
    
    # Create document from modified data
    for document in cleaned_documents:
        sentences = cleaned_documents[document]
        amount = len(sentences)
        counter = 1

        with open('preproc_' + document, "w") as file:
            for sentence in sentences:
                file.write(" ".join(sentence))
                if counter < amount:
                    file.write("\n")
                
                counter += 1
    
    # Part 2-1
    documents_words_frequencies = {}
    documents_word_count = {}

    for document in list_of_docs:
        with open('preproc_' + document, "r") as file:
            word_frequency = {}
            word_count = 0

            for line in file:
                line = line.strip()
                words = line.split(' ')
                word_count += len(words)

                for word in words:
                    if word not in word_frequency:
                        word_frequency[word] = 1
                        continue

                    word_frequency[word] = word_frequency[word] + 1
            
            documents_word_count[document] = word_count
            documents_words_frequencies[document] = word_frequency

    documents_TF = {}
    documents_IDF = {}

    # Part 2-2
    for document in list_of_docs:
        word_TF = {}
        total_word_count = documents_word_count[document]
        word_frequency = documents_words_frequencies[document]

        for word in word_frequency:
            frequency = word_frequency[word]
            tf = frequency / total_word_count
            word_TF[word] = tf
        
        documents_TF[document] = word_TF
    
    # Part 2-3
    for document in list_of_docs:
        word_IDF = {}
        total_document_count = len(list_of_docs)
        word_frequency = documents_words_frequencies[document]

        for word in word_frequency:
            word_appearances = 0
            for document_check in list_of_docs:
                if word in documents_words_frequencies[document_check]:
                    word_appearances += 1
            
            idf = log((total_document_count) / (word_appearances)) + 1
            word_IDF[word] = idf
        
        documents_IDF[document] = word_IDF
    
    # Part 2-4
    documents_TFIDF = {}
    
    for document in list_of_docs:
        word_TFIDF = {}
        word_frequency = documents_words_frequencies[document]
        word_TF = documents_TF[document]
        word_IDF = documents_IDF[document]

        for word in word_frequency:
            tfidf = round(word_TF[word] * word_IDF[word], 2)
            word_TFIDF[word] = tfidf
        
        documents_TFIDF[document] = word_TFIDF
    
    # Part 2-5
    for document in documents_TFIDF:
        tfidf_dictionary = documents_TFIDF[document]
        ordered_tfidf = sorted(tfidf_dictionary.items(), key = lambda x:(-x[1], x[0]))
        
        with open('tfidf_' + document, "w") as file:
            file.write('[')
            counter = 0
            for tuple in ordered_tfidf[:5]:
                file.write('(' + tuple[0] + ', ' + str(tuple[1]) + ')')
                if counter < 4:
                    file.write(', ')
                
                counter += 1
                
            file.write(']')

main()
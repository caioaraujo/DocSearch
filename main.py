import json
import string

import nltk
import unidecode
from os import listdir


class DocSearch:

    def __init__(self):
        nltk.download('rslp')
        nltk.download('stopwords')

    def clear_pontuaction(self, str_content):
        translator = str.maketrans('', '', string.punctuation)
        clean_result = str_content.translate(translator)
        return clean_result

    def replace_stop_words(self, content):
        words = content.split(' ')

        stopwords = nltk.corpus.stopwords.words('portuguese')

        result = nltk.FreqDist(w.lower() for w in words if w not in stopwords)

        return sorted(list(result))

    def stemming_text(self, sorted_file_content):
        stemmer = nltk.stem.RSLPStemmer()
        result = [stemmer.stem(x) for x in sorted_file_content if x != '']

        return set(result)

    def apply_thesaurus(self, term):

        term_as_list = term.split(' ')
        term_result = term_as_list.copy()

        with open('thesaurus.json', 'r') as thesaurus_json:
            thesaurus = json.loads(thesaurus_json.read())

        for word in term_as_list:
            self.find_in_thesaurus_section(word, thesaurus, term_result)

        return ' '.join(set(term_result))

    def find_in_thesaurus_section(self, word, thesaurus_section, result):
        for k in thesaurus_section.keys():

            if k == 'concepts':
                concepts = thesaurus_section.get('concepts')
                if concepts:
                    if word in concepts:
                        result.extend([concept for concept in concepts if concept != word])

            else:
                subtypes = thesaurus_section.get('subtypes')
                if subtypes:
                    if type(subtypes) == dict:
                        self.find_in_thesaurus_section(word, subtypes, result)
                    elif word in subtypes:
                        result.extend([subtype for subtype in subtypes if subtype != word])

    def search(self, term_to_find):
        # clean pontuaction from term
        term_to_find = self.clear_pontuaction(term_to_find)

        # lower term
        term = term_to_find.lower()

        # apply thesaurus on term
        term = self.apply_thesaurus(term)

        # remove all accents from term
        term = unidecode.unidecode(term)

        # remove all stopwords from term
        term = self.replace_stop_words(term)

        # apply stemmer on term
        term_stemmed = self.stemming_text(term)

        # Read all files in evaluation-news-txt folder
        dir_name = 'evaluation-news-txt'
        files = listdir(dir_name)

        for file in files:
            with open(dir_name + '/' + file, 'r') as my_file:

                file_content = my_file.read()

            # clean pontuaction from file content
            file_content = self.clear_pontuaction(file_content)

            # lower file content
            file_content = file_content.lower()

            # remove all accents from file content
            file_content = unidecode.unidecode(file_content)

            # remove all stopwords from file content
            file_content = self.replace_stop_words(file_content)

            # apply stemmer on file content
            file_content_stemmed = self.stemming_text(file_content)

            for text in term_stemmed:
                if text in file_content_stemmed:
                    result[my_file.name] = file_content

        return result


if __name__ == '__main__':

    result = dict()
    term = input('Digite o termo: ')

    doc_search = DocSearch().search(term)

    print(f'Encontrado em: {result}')

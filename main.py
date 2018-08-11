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
        return [stemmer.stem(x) for x in sorted_file_content if x != '']

    def apply_thesaurus(self, term):

        term_as_list = term.split(' ')
        term_result = term_as_list.copy()

        with open('thesaurus.json', 'r') as thesaurus_json:
            thesaurus = json.loads(thesaurus_json.read())

        # FIXME: Apply recursivity on thesaurus search
        for word in term_as_list:
            word = word.lower()
            concepts = thesaurus.get('concepts')
            if concepts:
                if word in concepts:
                    term_result.append([concept for concept in concepts if concept != word])

        return ' '.join(set(term_result))

    def search(self, term_to_find):
        dir_name = 'evaluation-news-txt'
        files = listdir(dir_name)

        for file in files:
            with open(dir_name + '/' + file, 'r') as my_file:

                file_content = my_file.read()

            # clean pontuaction from both term and file content
            file_content = self.clear_pontuaction(file_content)
            term_to_find = self.clear_pontuaction(term_to_find)

            # lower both term and file content
            file_content = file_content.lower()
            term = term_to_find.lower()

            # apply thesaurus on term
            term = self.apply_thesaurus(term)

            # remove all accents from both term and file content
            file_content = unidecode.unidecode(file_content)
            term = unidecode.unidecode(term)

            # remove all stopwords from both term and file content
            file_content = self.replace_stop_words(file_content)
            term = self.replace_stop_words(term)

            # apply stemmer
            file_content_stemmed = self.stemming_text(file_content)
            term_stemmed = self.stemming_text(term)

            if set(term_stemmed).issubset(file_content_stemmed):
                result[my_file.name] = file_content

        return result


if __name__ == '__main__':

    result = dict()
    term = input('Digite o termo: ')

    doc_search = DocSearch().search(term)

    print(f'Encontrado em: {result}')

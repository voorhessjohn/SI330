import re
frequent_word_threshold = 5000

WORD_RE = re.compile(r'\b[\w]+\b')

def convert_dict_to_tuples(d):
    text = d['text']
    rating = d['stars']
    tokens = WORD_RE.findall(text)
    tuples = []
    for w in tokens:
        tuples.append((rating, w))
    return tuples


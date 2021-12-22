import random

import requests
from urllib.parse import quote
import json


def get_context(lemma):
    quoted_lemma = quote(lemma)
    seed = random.randint(0, 100000)

    url = 'https://processing.ruscorpora.ru/search.xml?' \
          'dpp=1&' \
          'spd=1&' \
          'p=0&' \
          'lang=ru&' \
          'level1=0&' \
          f'lex1={quoted_lemma}&' \
          'mode=main&' \
          'nodia=1&' \
          'out=normal&' \
          f'seed={seed}&' \
          'sem-mod1=sem&sort=random&' \
          'text=lexgramm&' \
          'format=json'

    r = requests.get(url)

    data = json.loads(r.text)

    if not data.get('document_groups'):
        return None, None

    source_title = data['document_groups'][0][0]['document_info']['title']

    snippet_words = data['document_groups'][0][0]['snippets'][0]['words']

    return ''.join([x['text'] for x in snippet_words]).strip().replace('\\t', '\t'), source_title


if __name__ == "__main__":
    print(get_context('слово'))

import json
import urllib.request
import pandas as pd
import string

url = 'https://raw.githubusercontent.com/meettaraviya/Letter-jam-hints/main/word_counts.json'
word_counts = json.loads(urllib.request.urlopen(url).read().decode('utf-8'))
count_values = sorted(word_counts.values())
lj_letters = set(string.ascii_lowercase) - set('jqvzx')

def get_ambiguity(word):
    ambiguity_score = 0
    for l in set(word):
        for l_ in lj_letters:
            if l != l_ and (word_ := word.replace(l, l_)) in word_counts:
                ambiguity_score += word.count(l)
    return ambiguity_score / len(word)

def lambda_handler(event, context):

    available_letters = set(event['availableLetters'].lower())
    max_diff_count = 1 if '*' in available_letters else 0
    available_letters.discard('*')
    possible_word_counts = [(word, count) for word, count in word_counts.items() if len(set(word)-available_letters) <= max_diff_count]
    
    word_info_df = pd.DataFrame([{
        'word': word,
        'frequency': count_values.index(count) / len(count_values),
        'ambiguity':get_ambiguity(word),
        'helpfulness': len(set(word))
        } for (word, count) in possible_word_counts])
    
    word_info_df = word_info_df.sort_values(["helpfulness", "ambiguity", "frequency"], ascending=[False, True, False]).head(25)

    return {
    'statusCode': 200,
    'body': word_info_df.to_html()
    }
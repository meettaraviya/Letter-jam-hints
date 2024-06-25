import json
import urllib.request

url = 'https://raw.githubusercontent.com/meettaraviya/Letter-jam-hints/main/word_counts.json'
word_counts = json.loads(urllib.request.urlopen(url).read().decode('utf-8'))

def lambda_handler(event, context):

    available_letters = set(event['availableLetters'].lower())
    max_diff_count = 1 if '*' in available_letters else 0        
    possible_words = [word for word, _ in word_counts.items() if len(set(word)-available_letters) <= max_diff_count]

    return {
    'statusCode': 200,
    'body': json.dumps(f'Following words are available: {" | ".join(possible_words)}')
    }
import random
import requests
import string

def get_theme_word():

    popular_words_list = []
    while popular_words_list == []:

        random_letter = random.choice(string.ascii_uppercase)
        random_word_length = random.randint(4, 7) - 1
        number_of_questionmarks = "?" * random_word_length
        response = requests.get("https://api.datamuse.com/words?sp=" + random_letter + number_of_questionmarks + "&md=f")
        response_list = response.json()
        
        
        for item in response_list:
            tag_string = item["tags"][0]

            frequency_score = float(tag_string[2:])

            if frequency_score >= 8.8 and " " not in item["word"]: # make sure that this isnt too high, otherwise you just get repeated words for some letters
                popular_words_list.append(item)
        
    theme_dict = random.choice(popular_words_list)
    
    theme_word = theme_dict["word"].upper()
    
    return theme_word

print(get_theme_word())
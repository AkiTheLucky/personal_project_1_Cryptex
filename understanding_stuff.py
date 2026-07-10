import random
import requests
import string

def get_theme_word():




        random_letter = random.choice(string.ascii_uppercase)
        response = requests.get("https://api.datamuse.com/words?sp=" + random_letter + "?????&md=f")
        response_list = response.json()
        
    
        return response_list

print(get_theme_word())
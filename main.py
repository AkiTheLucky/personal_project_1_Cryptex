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



def get_thematic_bucket(theme_word):
    datamuse_request_url = "https://api.datamuse.com/words?ml=" + theme_word + "&md=f"
    response = requests.get(datamuse_request_url)
    response_list = response.json()

    unfiltered_thematic_bucket_list = []
    
    for item in response_list:
        item_text = item["word"]
        if " " not in item_text and "-" not in item_text:
            unfiltered_thematic_bucket_list.append(item_text.upper())
    
    



    return unfiltered_thematic_bucket_list 


#new function for the word matching
def arrange_column_words(theme_word, unfiltered_thematic_bucket_list):
    thematic_bucket_list = []
    #to get from the unfiltered list to the filtered list, i need to get len(theme_word) amount of words that share the right letters
    #do i do this in here or in a seperate function? i guess i do it here
    #maybe in regards to re-usability, i want to have it seperate? considering that i need to re-use the thematic bucket list again in the puzzle logic? im not sure
    
    for column_index, letter in enumerate(theme_word):
        found_match = False

        for word in unfiltered_thematic_bucket_list:
            for letter_index, word_char in enumerate(word):

                if word_char == letter:
                    
                    column_dict = {
                        "word": word,
                        "theme_index": column_index,
                        "word_index": letter_index
                    }

                    thematic_bucket_list.append(column_dict)
                    unfiltered_thematic_bucket_list.remove(word)
                    found_match = True
                    break
            if found_match:
                break
        if not found_match :
            raise ValueError("no fitting word found, try again")
            #implement logic later to re-run the file for another theme word(?)

    return thematic_bucket_list

# print it for now, so i can see whats happening! 
theme_word = get_theme_word() 
thematic_bucket = get_thematic_bucket(theme_word) 
print(theme_word)
print(thematic_bucket)
print(arrange_column_words(theme_word, thematic_bucket))
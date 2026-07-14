import random
import requests
import string
from blessed import Terminal

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


#time to build the matrix that will get printed on the screen later
def build_cryptex_matrix(theme_word, thematic_bucket_list):
    #1. Find the height of the tallest column / longest aux word
    max_height_matrix = max(len(item["word"]) for item in thematic_bucket_list) +1 
    
    matrix_width= len(theme_word)

    cryptex_matrix = []

    for i in range(matrix_width):
        column_list = [" "] * max_height_matrix
        cryptex_matrix.append(column_list)
       
    
    #2nd loop to drop in the words
    for column_index in range(matrix_width):
        current_word = thematic_bucket_list[column_index]["word"]

        for char_index, char in enumerate(current_word):
            cryptex_matrix[column_index][char_index] = char
            
        



    return cryptex_matrix


#remote control?
term = Terminal()

#draw matrix to screen logic here:
def draw_cryptex_board(cryptex_matrix, term, active_column_index):
    #print clear screen to the terminal
    print(term.clear)


    #draw a box around my game
    
    box_width = (len(cryptex_matrix) * 4) + 12
    box_height = (len(cryptex_matrix[0])) + 4
    box_start_x = (term.width - box_width) // 2
    box_start_y = (term.height - box_height) // 2


    for current_x in range(box_start_x, box_start_x + box_width):
        print(term.move_xy(current_x, box_start_y) + term.blue("─")) #top edge

        print(term.move_xy(current_x, box_start_y + box_height) + term.blue("─")) # bottom edge
    

    
    for current_y in range(box_start_y, box_start_y + box_height):
        print(term.move_xy(box_start_x, current_y) + term.blue("|")) #left edge

        print(term.move_xy(box_start_x + box_width, current_y) + term.blue("|")) #right edge
    #corners
    print(term.move_xy(box_start_x,box_start_y)+ term.blue("+"))
    print(term.move_xy(box_start_x + box_width ,box_start_y)+ term.blue("+"))
    print(term.move_xy(box_start_x,box_start_y + box_height)+ term.blue("+"))
    print(term.move_xy(box_start_x + box_width ,box_start_y + box_height)+ term.blue("+"))


    #draw the letters
    #set the x pos for the rows (how far to the right)
    starting_x_pos = (term.width - box_width) // 2 + 4

    for column_index, column_data in enumerate(cryptex_matrix):
        #reset the Y position for each new column so they all start at the top
        current_y_pos = box_start_y + 2
        
        # Check if the column we are about to draw is the active one!
        is_active = (column_index == active_column_index)

        # loop through each char in column x
        for char in column_data:
            if is_active:
                #use blessed to print active column in reverse
                print(term.move_xy(starting_x_pos, current_y_pos) + term.reverse(term.green(char)))

            else:
                #use blessed to teleport cursor to the desired location
                print(term.move_xy(starting_x_pos, current_y_pos) + term.green(char))

            #move one row down:
            current_y_pos += 1

        #outside the inner loop, move the cursor over to the next column. lets see how much to the right
        starting_x_pos += 4 






# print it for now, so i can see whats happening! 
theme_word = get_theme_word() 
unfiltered_thematic_bucket = get_thematic_bucket(theme_word) 
thematic_bucket_list = arrange_column_words(theme_word, unfiltered_thematic_bucket)
cryptex_matrix = build_cryptex_matrix(theme_word, thematic_bucket_list)

print(theme_word)
print("\n")
print(arrange_column_words(theme_word, unfiltered_thematic_bucket))
print("\n")
print(build_cryptex_matrix(theme_word, thematic_bucket_list))

# 1. Calculate minimum required size to draw the game
required_width = (len(cryptex_matrix) * 4) + 12 
required_height = (len(cryptex_matrix[0])) + 8
if term.width < required_width or term.height < required_height:
    print("Your terminal is too small!")
    print(f"Please resize it to at least {required_width}x{required_height} characters.")
    print(f"Current size: {term.width}x{term.height}")
    exit() # Stop the game immediately


cryptex_matrix = build_cryptex_matrix(theme_word, thematic_bucket_list)
#actually do the drawing in a while loop to handle issues with the terminal
#this is actually the main game loop??? wow oh lol, its not. its further down
with term.fullscreen(), term.cbreak(), term.hidden_cursor():
    
    #declare some variables needed later
    active_column_index = 0
    solve_row_index = -1 # Or whatever row I want them to align on. lets see what feels best
    #solve_row_index = len(cryptex_matrix[0])

    
    #call the func from earlier that does the printing and drawing logic
    draw_cryptex_board(cryptex_matrix, term, active_column_index)
    
    #actual game loop here:
    while True:
        key = term.inkey()
        #exit key
        if key.lower() == "q":
            break

        elif key.name == "KEY_LEFT":
            if active_column_index == 0:
                pass
            else:
                active_column_index -= 1
             
        elif key.name == "KEY_RIGHT":
            if active_column_index == len(cryptex_matrix) - 1 : #lol, index off by one because 0,1,2,3,4 != 5 
                pass
            else:
                active_column_index += 1
        
        elif key.name == "KEY_UP":
            # Rotate the data in cryptex_matrix[active_column_index] "up"
            active_column = cryptex_matrix[active_column_index]

            #move topblock to bottom
            top_block = active_column.pop(0)
            active_column.append(top_block)
             
            
        elif key.name == "KEY_DOWN":
            # Rotate the data in cryptex_matrix[active_column_index] "down"
            active_column = cryptex_matrix[active_column_index]

            #move bottom block to top
            bottom_block = active_column.pop()
            active_column.insert(0, bottom_block)
            

        #all further keys here!!

        draw_cryptex_board(cryptex_matrix, term, active_column_index)
            
        # ==========================================
        # 5. CHECK FOR WIN CONDITION
        # ==========================================
        current_guess = ""
        for column in cryptex_matrix:
            letter = column[solve_row_index]

            current_guess += letter
        if current_guess == theme_word:
            #insert cool winning animation here!
            break 
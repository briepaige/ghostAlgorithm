ghost.py contains code for an online adaptation of the word game Ghost, in which players alternate playing letters that could follow the existing string, while avoiding playing the final letter of a legal dictionary word. 

the program allows for computerized players; the computer algorithm finds the proportion of words that would force another player to play the final letter of a word out of all possible words that could follow if the player were to make a certain choice. It then uses the list of proportions to randomly select a play to make, weighted by how high the proportion is. 
        
all_words_helper.py is a program created to process the original list of words, removing words that contain fewer than 4 letters (as those are not valid ghost words!). The program also contains functionality to remove any words that are superstrings of other words, although the final version of ghost.py no longer requires the removal of superstrings. 

that's all, enjoy!

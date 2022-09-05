ghost.py contains code for an online adaptation of the word game Ghost, in which players alternate playing letters that could follow the existing string, while avoiding playing the final letter of a legal dictionary word. 

the program allows for computerized players; the computer algorithm finds the proportion of words that would force another player to play the final letter of a word out of all possible words that could follow if the player were to make a certain choice. It then uses the list of proportions to randomly select a play to make, weighted by how high the proportion is. 
        

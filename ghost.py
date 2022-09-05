import random
import time

# class to store and update game data such as player counts and names and execute gameplay functions such as turn-taking and calculating of scores
class Game():

    def __init__(self, numPlayers, names, numHumans, wordList):
        self.numPlayers = numPlayers
        self.names = names
        self.numHumans = numHumans
        self.wordList = wordList

    #create player objects for each player
    def initializePlayers(self):
        self.players = []
        for i in range(self.numPlayers):
            if i < self.numHumans:
                self.players.append(Player(True, self.names[i], self.wordList))
            else:
                self.players.append(Player(False, self.names[i], self.wordList))
        random.shuffle(self.players)

    # plays the game by initializing players, playing rounds, and eliminating players as appropriate
    def playGame(self):
        print("Welcome to ghost!\n\nOn your turn, enter a letter that could legally follow the existing string of letters, while avoiding placing the final letter of a legal word.\n\nIf you believe the player before you spelled a legal word, press [enter] to check it in the scrabble dictionary. Be careful, though, if the word is not legal, you will take the penalty in lieu of your competitor.\n\nIf you do not believe that the existing string can begin any legal words, you may challenge your competitor's play by inputting \"1\".\n\nWords must be four or more letters!")
        self.initializePlayers()
        self.playerOrder = []
        for player in self.players:
            self.playerOrder.append(player)

        #outer loop plays a round and then checks to see if any players reached ghost, eliminating players who have
        while True:
            self.playerOrder.append(self.playerOrder[0])
            self.playerOrder.remove(self.playerOrder[0])
            self.playRound()
            print('Current Scores:')
            for player in self.players:
                print(player.name + ': ' + player.score)
            for player in self.players:
                if player.score == "GHOST":
                    print(player.name + " has been eliminated!")
                    self.numPlayers -= 1
                    self.players.remove(player)
                    self.playerOrder.remove(player)
            if self.numPlayers == 1:
                print(self.players[0].name + " wins!")
                exit()

    # plays a round, alternating between players until a word is is spelled (and caught!) or a phrase is challenged
    def playRound(self):
        running = True
        word = ""
        print('\n***\n')
        time.sleep(1)
        while running:
            for i in range(self.numPlayers):
                currPlayer = self.playerOrder[i]
                letter = currPlayer.takeTurn(word, self.numPlayers)
                if letter == '':
                    if word in self.wordList:
                        print(word + " found in dictionary.")
                        self.playerOrder[i-1].incrementScore()
                    else:
                        print(word + " not found in dictionary.")
                        self.playerOrder[i].incrementScore()
                    running = False
                    break

                elif letter == "1":
                    if self.playerOrder[i-1].human:
                        keyWord = input(self.playerOrder[i-1].name + ", what word were you thinking of? ")
                    else:
                        keyWord = self.playerOrder[i-1].getKeyword(word)
                        print(self.playerOrder[i-1].name + ", what word were you thinking of? " + keyWord)
                    if not keyWord.startswith(word):
                        print(word)
                        print(keyWord + " does not contain the existing word")
                        self.playerOrder[i-1].incrementScore()
                    elif keyWord in self.wordList:
                        print(keyWord + " found in dictionary.")
                        self.playerOrder[i].incrementScore()
                    else:
                        print(keyWord + " not found in dictionary.")
                        self.playerOrder[i-1].incrementScore()
                    running = False
                    break

                else: 
                    word += letter



# class to store player information such as name, score, and whether they are human or computer
# also contains the wordList put into a dictionary tree-like structure for more efficient traversal during computer turns
class Player():
    
    def __init__(self, human, name, wordList):
        self.human = human
        self.score = ""
        self.name = name
        self.wordList = wordList
        self.dictionary = self.constructDict()
        

    #increments the player's score
    def incrementScore(self):
        ghost = "GHOST"
        self.score += ghost[len(self.score)]


    #checks to see if the player is a human or computer, and calls a helper function accordingly
    def takeTurn(self, currWord, numPlayers):
        self.numPlayers = numPlayers
        self.currWord = currWord
        if self.human == True:
            return self.playHuman()
        else:
            letter = self.cpu(currWord)
            print(self.name + "'s turn: ", end = "")
            time.sleep(0.5)
            print(letter)
            return letter
    
    # prompts the user to enter a valid letter or challenge a play
    # returns a string containing the user's play
    def playHuman(self):
        letter = input(self.name + ", enter a letter: ")
        if letter == "":
            if len(self.currWord) < 4:
                input("Word too short. Please enter a valid letter: ")
            else:
                return letter
        while (len(letter) != 1 or not ((97 <= ord(letter) <= 122) or (65 <= ord(letter) <= 90))) and letter != "1":
            letter = input("Please enter a valid letter: ")
        try:
            letter = letter.lower()
        except:
            return letter
        return letter

    #returns a valid word beginning with the current substring
    #called in response to computerized player being challenged
    def getKeyword(self, currWord):
        time.sleep(0.5)
        for word in self.wordList:
            if word.startswith(currWord):
                return word
        return currWord + self.getLetter(random.randrange(26))

    # gets and returns a valid play letter from a list of possible plays
    def getPlayLetter(self):
        word = self.currWord

        # construct a list of legal next plays
        possiblePlays = self.dictionary.get(word)
        playValues = []

        # for each potential play, find ratio of safe words to total words
        # total words refers to the number of paths leading to valid ending words in the dictionary (e.g. the total words for "koal" would be 1 as the only path that could legally follow is "koala". we disregard "koalas" as that occurs on the same path as "koala" which is an ending word)
        # safe words refers to the number of paths whose first end word lands on another player
        for play in possiblePlays:
            result = self.searchDict(play, 0, 0)
            ratio = result[1]/result[0]
            playValues.append(ratio)
        # using the ratio of safe words to total words, assign proportional frequencies that letters should be chosen
        chooseFrequencies = []
        ratioSum = 0
        for value in playValues:
            ratioSum += value
        if ratioSum == 0:
            return "1"
        for i in range(len(playValues)):
            chooseFrequencies.append(playValues[i]/ratioSum)
        position = random.random()
        currPosition = 0
        # iterates through frequencies keeping a running sum
        # position is a random value between 0 and 1; when the running frequency sum surpasses the goal position, return that play
        for i in range(len(playValues)):
            value = chooseFrequencies[i]
            currPosition += value
            if currPosition >= position:
                letter = possiblePlays[i][-1]
                return letter
        return '1'
    
    # recursively searches the dictionary to find the total number of paths to end words found in the dictionary
    # also tracks 
    def searchDict(self, currWord, totalCount, safeCount):
        if self.dictionary.get(currWord)[0] == "":
            totalCount += 1
            turnsAway = len(currWord) - len(self.currWord)
            if turnsAway % self.numPlayers != 1:
                safeCount += 1
            return (totalCount, safeCount)
        else:
            nextPlayList = self.dictionary.get(currWord)
            for play in nextPlayList:
                result = self.searchDict(play, totalCount, safeCount)
                totalCount += result[0]
                safeCount += result[1]
            return (totalCount, safeCount)


    def cpu(self, word):
        if word == "":
            return self.getLetter(random.randrange(26))
        elif self.dictionary.get(word) == None:
            return "1"
        elif self.dictionary.get(word)[0] == "":
            return ""
        else:
            return self.getPlayLetter()


    def constructDict(self):
        dictionary = {}
        for word in self.wordList:
            for i in range(len(word)):
                if dictionary.get(word[:i+1]) == None:
                    dictionary[word[:i+1]] = []
                if word[:i+1] != word:
                    if word[:i+2] not in dictionary[word[:i+1]]:
                        dictionary[word[:i+1]].append(word[:i+2])
                else:
                    dictionary[word[:i+1]].insert(0, "")
        return dictionary



    def getIndex(self, letter):
        return ord(letter) - 97

    def getLetter(self, index):
        return chr(index + 97)

        
def constructWordList():
    inp = open("all_4+_letter_words.txt", "r")
    wordList = []
    for line in inp:
        wordList.append(line[:-1])
    inp.close()
    return wordList


def main():
    wordList = constructWordList()
    print('Welcome to Ghost!')
    numHumans = ''
    while numHumans == "":
        numHumans = input('How many human players will be participating? ')
        try:
            numHumans = int(numHumans)
        except:
            numHumans = ""
    names = []
    for i in range(numHumans):
        names.append(input('Enter player ' + str(i+1) + '\'s name: '))
    numCPUs = ''
    while numCPUs == "":
        numCPUs = input('How many CPU players will be participating? ')
        try:
            numCPUs = int(numCPUs)
        except:
            numCPUs = ""
    for i in range(numCPUs):
        names.append('CPU' + str(i+1))
    numPlayers = numHumans + numCPUs

    game = Game(numPlayers, names, numHumans, wordList)
    game.playGame()


if __name__ == "__main__":
    main()

import random
import threading

#Read input
def readFile():
    file_path = (r"words_test.txt")
    f = open(file_path)
    word_dict = f.read().split('\n')
    f.close()
    return word_dict

#Convert a list to a string
def convertToString(list):
    newString = ""
    for i in list:
        newString += i
    return newString

#Runs that players turn
def playerTurn(p,g,name):
    fail = False
    solvedPlayer = False
    while not fail and not solvedPlayer:
        print(f"\n{name.capitalize()}: You have ${p[g]}")
        if p[g] >= 250:
            option = input("Press 1 to spin the wheel and guess. Press 2 to buy a vowel. Press 3 to solve: ")
        else:
            option = input("Press 1 to spin the wheel and guess. Press 3 to solve: ")
        if not len(vowels) == 0 and not len(consonants) == 0:
            if p[g] >= 250:
                while option != '1' and option != '2' and option != '3':
                    option = input("Error: Press 1 to spin the wheel and guess. Press 2 to buy a vowel. Press 3 to solve: ")
            else:
                while option != '1' and option != '3':
                    option = input("Error: Press 1 to spin the wheel and guess. Press 3 to solve: ")
        elif len(consonants) == 0:
            if p[g] >= 250:
                while option != '2' and option != '3':
                    option = input("Error: Press 2 to buy a vowel. Press 3 to solve: ")
            else:
                while option != '3':
                    option = input("Press 3 to solve: ")
        elif len(vowels) == 0:
            while option != '1' and option != '3':
                option = input("Error: Press 1 to buy a consonant. Press 3 to solve: ")
        else:
            while option != '3':
                option = input("Press 3 to solve: ")        
        if option == '1':
            land = random.randint(0,len(wheel)-1)
            if wheel[land] == 'Bankrupt':
                print("The wheel landed on Bankrupt. You have lost your turn and money.")
                p[g] = 0
                fail = True
            elif wheel[land] == 'Lose a Turn':
                print("The wheel landed on Lose a Turn.")
                fail = True
            elif wheel[land] == 'Free Spin':
                print("The wheel landed on Free Spin.")
            else:
                print(f"The wheel landed on ${wheel[land]}")
                fail= guessConsonant(p,g,wheel[land])
        elif option == '2':
            fail = guessVowel(p,g)
        else:
            fail = solve()
            if not fail:
                solvedPlayer = True
                return solvedPlayer
        wordAsString = convertToString(blankWord)
        print(f"You progress is {wordAsString}")
        if wordAsString == word:
            print("The word has been solved!")
            solvedPlayer = True
    return solvedPlayer

#If player wants to spin wheel and guess a consonant
def guessConsonant(p,g,land):
    user_input = input("Enter a consonant: ")
    user_input = user_input.lower()
    while user_input not in consonants:
        user_input = input("Error: Enter a consonant that has not been guessed yet: ")
    check = user_input in wordList
    consonants.remove(user_input)
    if check == True:
        for i in range(0,len(word)):
            if  wordList[i] == user_input:
                blankWord[i] = user_input
                p[g] += land
        fail = False
    else:
        fail = True
    return fail

#If player wants to guess a vowel
def guessVowel(p,g):
    user_input = input("Enter a vowel: ")
    user_input = user_input.lower()
    while user_input not in vowels:
        user_input = input("Error: Enter a vowel that has not been guessed yet: ")
    check = user_input in wordList
    vowels.remove(user_input)
    if check == True:
        for i in range(0,len(word)):
            if  wordList[i] == user_input:
                blankWord[i] = user_input
        fail = False
    else:
        fail = True
    p[g] -= 250
    return fail

#If player wants to attempt to solve
def solve():
    user_input = input("Enter a word: ")
    user_input = user_input.lower()
    while not user_input.isalpha:
        user_input = input("Error: Enter a word: ")
    check = user_input == word
    if check == True:
        fail = False
        print("That is correct!")
    else:
        fail=True
    return fail

#Final Round Block
def finalRound():
    consonant1 = input("Enter a consonant: ")
    while consonant1 not in finalConsonants:
        consonant1 = input("Error: Enter a valid consonant: ")
    finalConsonants.remove(consonant1)
    consonant2 = input("Enter a consonant: ")
    while consonant2 not in finalConsonants:
        consonant2 = input("Error: Enter a valid consonant: ")
    finalConsonants.remove(consonant2)
    consonant3 = input("Enter a consonant: ")
    while consonant3 not in finalConsonants:
        consonant2 = input("Error: Enter a valid consonant: ")
    v = input("Enter a vowel: ")
    while v not in finalVowels:
        v = input("Error: Enter a valid vowel: ")
    guesses = [consonant1, consonant2,consonant3,v]
    for i in range(0,len(word)):
        if  wordList[i] == consonant1:
                blankWord[i] = consonant1
    for i in range(0,len(word)):
        if  wordList[i] == consonant2:
                blankWord[i] = consonant2
    for i in range(0,len(word)):
        if  wordList[i] == consonant3:
                blankWord[i] = consonant3
    for i in range(0,len(word)):
        if  wordList[i] == v:
                blankWord[i] = v
    wordAsString = convertToString(blankWord)
    print(f"After your guesses, you have {wordAsString}")
    print("\nYou have 10 seconds. Good Luck!")
    time = threading.Timer(10, time_expired)
    time.start()
    g = input("\nGuess: ")
    if not timeFail:
        print("You answered the question in time!")
        time.cancel()
    else:
        print("You did not answer the question in time!")
        time.cancel()
    return g == word

#Timer
def time_expired():
    global timeFail
    timeFail = True
    return True

#Global Variable Delarations
timeFail = False
lines = readFile()
print(lines)
wordsUsed = list()
vowels = {'a','e','i','o','u'}
consonants = {'b','c','d','f','g','h','j','k','l','m','n','p','q','r','s','t','v','w','x','y','z'}
lettersGuessed = []
player1 = {'game1':0,'game2':0}
player2 = {'game1':0,'game2':0}
player3 = {'game1':0,'game2':0}
wheel = ['Bankrupt',750,800,300,200,1000,500,400,300,200,'Free Spin',700,200,150,450,'Lose a Turn',200,400,250,150,400,600,250,350]
solved = False

#Game 1
rand = random.randint(0,len(lines))
wordList = list(lines[rand])
word = lines[rand]
while word in wordsUsed:
    rand = random.randint(0,len(lines))
    wordList = list(lines[rand])
    word = lines[rand]
wordsUsed.append(word)
blankWord = list('_'*len(word))
print(f"There is {len(blankWord)} letters. Good Luck!")
check = False
while not solved:
    char_loaction = list()
    if '_' not in blankWord:
        print("You win! The word was: ", word)
        break
    solved = playerTurn(player1,'game1','Player 1')
    if not solved:
        solved = playerTurn(player2,'game1', 'Player 2')
    if not solved:
        solved = playerTurn(player3,'game1','Player 3')

#On to Game 2
lettersGuessed = []
vowels = {'a','e','i','o','u'}
consonants = {'b','c','d','f','g','h','j','k','l','m','n','p','q','r','s','t','v','w','x','y','z'}
rand = random.randint(0,len(lines)-1)
wordList = list(lines[rand])
word = lines[rand]
while word in wordsUsed:
    rand = random.randint(0,len(lines)-1)
    wordList = list(lines[rand])
    word = lines[rand]
wordsUsed.append(word)
blankWord = list('_'*len(word))
print(f"There is {len(blankWord)} letters. Good Luck!")
check = False
solved = False
while not solved:
    char_loaction = list()
    if '_' not in blankWord:
        print("You win! The word was: ", word)
        break
    solved = playerTurn(player1,'game2','Player 1')
    if not solved:
        solved = playerTurn(player2,'game2', 'Player 2')
    if not solved:
        solved = playerTurn(player3,'game2','Player 3')

player1Total = player1['game1'] + player1['game2']
player2Total = player2['game1'] + player2['game2']
player3Total = player3['game1'] + player3['game2']
if player1Total > player2Total and player1Total > player3Total:
    winner = 'Player 1'
    print(f"Player 1 won ${player1Total} and was the winner and will move on to the final round")
    print(f"Player 2 won ${player2Total}")
    print(f"Player 3 won ${player3Total}")
    winnerTotal = player1Total
elif player2Total > player3Total:
    winner = 'Player 2'
    print(f"Player 2 won ${player2Total} and was the winner and will move on to the final round")
    print(f"Player 1 won ${player1Total}")
    print(f"Player 3 won ${player3Total}")
    winnerTotal = player2Total
else:
    winner = 'Player 3'
    print(f"Player 3 won ${player3Total} and was the winner and will move on to the final round")
    print(f"Player 1 won ${player1Total}")
    print(f"Player 2 won ${player2Total}")
    winnerTotal = player3Total

#Final Round
print("Moving on to the Final Round\n============================\n")
print(f"Congratulations {winner}")
r = random.randint(3,10)*10000
finalVowels = {'a','i','o','u'}
finalConsonants = {'b','c','d','f','g','h','j','k','m','p','q','v','w','x','y','z'}
given = ['r','s','t','l','n','e']
rand = random.randint(0,len(lines)-1)
wordList = list(lines[rand])
word = lines[rand]
while word in wordsUsed:
    rand = random.randint(0,len(lines)-1)
    wordList = list(lines[rand])
    word = lines[rand]
wordsUsed.append(word)
blankWord = list('_'*len(word))
print(f"There is {len(blankWord)} letters. Good Luck!")
print("You are given R, S, T, L, N and E!")
for j in range(0,len(given)):
    for i in range(0,len(word)):
            if  wordList[i] == given[j]:
                blankWord[i] = given[j]
wordAsString = convertToString(blankWord)
print(f"After R, S, T, L, N and E, you have {wordAsString}")
solved = finalRound()
if solved and not timeFail:
    print(f"Winnner! Congratulations! You have won ${r}, bringing your total to ${r+winnerTotal}!")
elif solved:
    print(f"That was correct, but too slow. You win ${winnerTotal}.")
else:
    print(f"Unfortuneately you did not win. The word was {word}. You  win ${winnerTotal}.")
playGame = False
from asyncore import read
from curses.ascii import isalpha
import random
from re import S

def readFile():
    file_path = (r"C:\Users\nickk\repo\WheelOfFortune\words_alpha.txt")
    f = open(file_path)
    word_dict = f.read().split('\n')
    f.close()
    return word_dict

def convertToString(list):
    newString = ""
    for i in list:
        newString += i
    return newString


def playerTurn(p,g,name):
    fail = False
    solvedPlayer = False
    while not fail and not solvedPlayer:
        print(f"\n{name.capitalize()}: You have ${p[g]}")
        if p[g] >= 250:
            option = input("Press 1 to spin the wheel and guess. Press 2 to buy a vowel. Press 3 to solve: ")
        else:
            option = input("Press 1 to spin the wheel and guess. Press 3 to solve: ")
        if p[g] >= 250:
            while option != '1' and option != '2' and option != '3':
                option = input("Error: Press 1 to spin the wheel and guess. Press 2 to buy a vowel. Press 3 to solve: ")
        else:
            while option != '1' and option != '3':
                option = input("Error: Press 1 to spin the wheel and guess. Press 3 to solve: ")
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
        wordAsString = convertToString(blankWord)
        print(f"You progress is {wordAsString}")
        if wordAsString == word:
            print("The word has been solved!")
            solvedPlayer = True
    return solvedPlayer

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

lines = readFile()
check = False
playGame = True
wordsUsed = list()
vowels = {'a','e','i','o','u'}
consonants = {'b','c','d','f','g','h','j','k','l','m','n','p','q','r','s','t','v','w','x','y','z'}
lettersGuessed = []
player1 = {'game1':0,'game2':0}
player2 = {'game1':0,'game2':0}
player3 = {'game1':0,'game2':0}
wheel = ['Bankrupt',750,800,300,200,1000,500,400,300,200,'Free Spin',700,200,150,450,'Lose a Turn',200,400,250,150,400,600,250,350]
solved = False
while playGame:
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
    if player1Total > player2Total and player1Total > player2Total:
        winner = 'Player 1'
        print("Player 1 won ${player1Total} and was the winner and will move on to the final round")
        print(f"Player 2 won ${player2Total}")
        print(f"Player 3 won ${player3Total}")
    elif player2Total > player3Total:
        winner = 'Player 2'
        print("Player 2 won ${player2Total} and was the winner and will move on to the final round")
        print(f"Player 1 won ${player1Total}")
        print(f"Player 3 won ${player3Total}")
    else:
        winner = 'Player 3'
        print("Player 3 won ${player3Total} and was the winner and will move on to the final round")
        print(f"Player 1 won ${player1Total}")
        print(f"Player 2 won ${player2Total}")
    playGame = False
    

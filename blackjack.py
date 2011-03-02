import random

def main():
    stillPlaying = True
    while (stillPlaying):
        answer = raw_input("Start a new game? (y/n): ")
        print
        if answer == 'y' or answer == 'Y':
            name = raw_input("What... is your name?\n> ")
            if name == "":
                name = 'Player1'
            print
            print("Type 'q' at a prompt to quit.")
            print
            startGame(name)
        elif answer == 'n' or answer == 'N':
            stillPlaying = False
        else:
            print("Please type 'y' or 'n'.")

    print("Thanks for playing loser!")

def get_cards():
    suits = ('Spade', 'Heart', 'Club', 'Diamond')
    values = (2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A')

    cards = []
    for suit in suits:
        for value in values:
            card = (value, suit)
            cards.append(card)
    return cards

def get_random_index():
    #get a random index between 0 and 51
    return random.randrange(0, 52)

def get_deck():
    '''
        Gets a shuffled deck.
    '''
    random.seed()
    unshuffled_deck = get_cards()
    shuffled_deck = []
    while len(shuffled_deck) < 52:
        card = unshuffled_deck[get_random_index()]
        if card not in shuffled_deck:
            shuffled_deck.append(card)
    print '----------------------------------------'
    print

    return shuffled_deck

def evaluateHand(cards):
    sum = 0
    aces = []
    for card in cards:
        faceValue = card[0]
        if faceValue == 'J' or faceValue == 'Q' or faceValue == 'K':
            sum += 10
        elif faceValue == 'A':
            aces.append(card)
        else:
            sum += faceValue
    if len(aces) > 0:
        while len(aces) > 0:
            ace = aces.pop()
            #if the current sum + the rest of the aces valued at 1 + this ace valued at 10
            #   will still keep the sum at or below 21, use 10 as the value
            if sum + len(aces) + 10 <= 21:
                sum += 10
            else:
                sum += 1
    return sum

#TODO: i think the dealer still gets cards if the player 'hit' up to 21
def reshuffleIfNecessary(deck):
    if len(deck) < 1:
        print("Reshuffling the deck")
        newDeck = get_deck()
        for card in newDeck:
            deck.append(card)

def hit(hand, deck, name, initialDeal):
    reshuffleIfNecessary(deck)
    hand.append(deck.pop())
    if initialDeal:
        reshuffleIfNecessary(deck)
        hand.append(deck.pop())

    print('%s\'s Hand:' % name)
    for card in hand:
        print(card)

    playerScore = evaluateHand(hand)
    print('TotalScore: %s' % playerScore)
    print
    return playerScore

def dealersTurn(hand, deck, name):
    score = evaluateHand(hand)
    while score < 17:
        score = hit(hand, deck, name, False)

def getTotalStr(playerScore, dealerScore):
    return "You=%d Dealer=%d" % (playerScore, dealerScore)

def determineWinner(playerHand, dealerHand, cash, betAmount):
    playerScore = evaluateHand(playerHand)
    dealerScore = evaluateHand(dealerHand)
    
    totalStr = getTotalStr(playerScore, dealerScore)
    if playerScore > 21:
        print("Nice fucking job, you busted. %s" % totalStr)
        cash = updateCash(cash, betAmount, 0)
    elif dealerScore > 21:
        print("Dealer's on crack. You win! %s" % totalStr)
        cash = updateCash(cash, betAmount, 1)
    elif playerScore == dealerScore:
        print("You almost didn't fucking suck. Draw. %s" % totalStr)
        cash = updateCash(cash, betAmount, 2)
    elif playerScore > dealerScore:
        print("You are so fucking amazing. %s" % totalStr)
        cash = updateCash(cash, betAmount, 1)
    else:
        print("What a fucking loser. I'm ashamed. %s" % totalStr)
        cash = updateCash(cash, betAmount, 0)

    raw_input("Hit enter to continue.")
    print
    return cash

def updateCash(cash, betAmount, result):
    if result == 0:
        cash -= betAmount
    elif result == 1:
        cash += betAmount
    #else it was a draw, cash stays the same
    print
    print("$%d" % cash)
    print
    return cash

def finishRound(playerHand, dealerHand, deck, dealerName, cash, betAmount):
    dealersTurn(dealerHand, deck, dealerName)
    cash = determineWinner(playerHand, dealerHand, cash, betAmount)
    return cash

def startGame(name):
    stillPlaying = True
    deck = get_deck()
    cash = 100
    print("You have $%d" % cash)
    print
    while stillPlaying and cash > 0:
        playerHand = []
        playerScore = hit(playerHand, deck, name, True)

        dealerName = 'Dealer'
        dealerHand = []
        dealerScore = hit(dealerHand, deck, dealerName, True)

        totalStr = getTotalStr(playerScore, dealerScore)
        print(totalStr)
        print

        getPlayerDecision = True
        betAmount = 5
        if (playerScore == 21):
            cash = determineWinner(playerHand, dealerHand, cash, betAmount)
            getPlayerDecision = False

        while getPlayerDecision:
            answer = raw_input('(H)it or (S)tay? ')
            print
            if answer == 'H' or answer == 'h':
                #TODO: this is a mess right here. needs overhaul. logic spread in too many
                #   places for determining if we're still playing.
                result = handlePlayerHit(playerHand, dealerHand, deck, name, dealerName, cash, betAmount)
                getPlayerDecision = not result[0]
                cash = result[1]
            elif answer == 'S' or answer == 's':
                cash = finishRound(playerHand, dealerHand, deck, dealerName, cash, betAmount)
                getPlayerDecision = False
            elif answer == 'Q' or answer == 'q':
                print('Fine, fuck you too then.')
                getPlayerDecision = False
                stillPlaying = False
            else:
                print("Please type 'h' or 's', or 'q' to (Q)uit")

def handlePlayerHit(playerHand, dealerHand, deck, name, dealerName, cash, betAmount):
    roundComplete = False
    playerScore = hit(playerHand, deck, name, False)
    if playerScore > 21:
        cash = determineWinner(playerHand, dealerHand, cash, betAmount)
        roundComplete = True
    elif playerScore == 21:
        cash = finishRound(playerHand, dealerHand, deck, dealerName, cash, betAmount)
        roundComplete = True
    else:
        print(getTotalStr(playerScore, evaluateHand(dealerHand)))
        print
        roundComplete = False
    return (roundComplete, cash)

if __name__ == '__main__':
    main()

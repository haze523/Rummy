
####################################################################################################################################################
#                                                               CLASSES
####################################################################################################################################################

class Board:
    def __init__(self, deck, table, discard, hands, turn, sturn, players):
        self.deck = deck
        self.table = table
        self.discard = discard
        self.hands = hands
        self.turn = turn
        self.sturn = sturn
        self.players = players

    # Changes the turn
    def turnchange(self):
        if self.turn == self.players:
            self.turn = 1
        else:
            self.turn +=1

    def sturnchange(self):
        if self.sturn == self.players:
            self.sturn == 1
        else:
            self.sturn +=1



# Class for the cards
class Card:
    def __init__(self, card, value, suit, name):
        self.value = value
        self.card = card
        self.suit = suit
        self.name = name

# Class for the players
class Player:

    def __init__(self, hand, score, selected, selindex, cscore, nscore, mancard, turnstage, name):
        self.hand = hand
        self.score = score
        self.selected = selected
        self.selindex = selindex
        self.cscore = cscore
        self.nscore = nscore
        self.mancard = mancard
        self.turnstage = turnstage
        self.name = name

    def selCards(self):
        self.selindex = []
        buffer=[]
        buffer2=[]
        imp = input("Which cards would you like to play? (enter index of cards) (end each index with a . please) ")
        for i in imp:
            if i ==("."):
                joinedbuffer=''.join(buffer)
                buffer2.append(joinedbuffer)
                for j in buffer2:
                    self.selindex.append(int(j))
                buffer.clear()
                buffer2.clear()
            else:
                buffer.append(i)
        count = 0
        for i in self.selindex:
            for j in range(0, int(len(self.hand))):
                if int(i) == j:
                    count += 1
        if count == len(self.selindex):
            self.MoveSelCard(self.selindex)
        else:
            print("Your input isn't cards in your hand")
            self.selCards()

    def playCards(self):
        self.selCards()
        count=0
        if checkplayable(self.selected):
            MainBoard.table.append(self.selected.copy())
            for i in self.selected:
                self.cscore+=i.value
            self.selindex.sort()
            for i in self.selindex:
                self.hand.pop(i-count)
                count+=1
        else:
            print("These cards aren't playable")
        self.selected.clear()
        self.selindex.clear()
        return 0

    def manplayCards(self):
        count1=0
        count2=0
        self.selCards()
        for i in self.selected:
            if i==self.mancard:
                count1+=1
        if count1==1:
            if checkplayable(self.selected):
                MainBoard.table.append(self.selected.copy())
                for i in self.selected:
                    self.cscore += i.value
                self.selindex.sort()
                for i in self.selindex:
                    self.hand.pop(i - count2)
                    count2 += 1
                self.turnstage=2
                return 0
            else:
                print("These cards aren't playable")
        else:
            print("YOU MUST PLAY THE CARD")
            self.manplayCards()

    def drawdeck(self):
        if len(MainBoard.deck)>0:
            self.hand.append(MainBoard.deck.pop())
        else:
            return print("There are no more cards in the deck")

    def drawdiscard(self):
        if len(MainBoard.discard)>0:
            numcount=0
            topstrtcount=0
            midstrtcount=0
            botstrtcount=0
            numpossible=False
            strtpossible=False
            hc=None
            ha=[]
            hh=self.hand.copy()
            hhs=[]
            tempdiscard=MainBoard.discard.copy()
            print("Discard=" + str(fulltranslate(MainBoard.discard)))
            imp=input("Which card are you drawing from?")
            hc=MainBoard.discard[int(imp)]
            if int(imp)==len(MainBoard.discard):
                self.hand.append(MainBoard.discard.pop(int(imp)))
                print(fulltranslate(MainBoard.discard))
                return False
            while len(tempdiscard)>int(imp):
                ha.append(tempdiscard.pop(int(imp)))
            for i in ha:
                hh.append(i)
            for i in hh:
                if i.card==hc.card:
                    numcount+=1
            if numcount>=3:
                numpossible=True
            for i in hh:
                if i.suit==hc.suit:
                    hhs.append(i)
            for i in hhs:
                if hc.card==1:
                    if i.card==2 or 3:
                        botstrtcount+=1
                    elif i.card==12 or 13:
                        topstrtcount+=1
                elif hc.card==13:
                    if i.card==1 or 12:
                        midstrtcount+=1
                    elif i.card==11 or 12:
                        topstrtcount+=1
                else:
                    if i.card==hc.card+1 or hc.card-1:
                        topstrtcount+=1
                    elif i.card==hc.card+1 or hc.card+2:
                        botstrtcount+=1
                    elif i.card == hc.card - 1 or hc.card - 2:
                        topstrtcount += 1
            if topstrtcount>=3 or midstrtcount>=3 or botstrtcount>=3:
                strtpossible=True
            if strtpossible or numpossible:
                while len(MainBoard.discard)>int(imp):
                    self.hand.append(MainBoard.discard.pop(int(imp)))
                self.mancard=hc
                return True
            else:
                return print("You can't play the card you are trying to draw from")
        else:
            return print("The discard pile is empty")

    def discard(self):
        imp = input("Which cards would you like to discard? (enter index of card)")
        if int(imp) <= len(self.hand)-1:
            MainBoard.discard.append(self.hand.pop(int(imp)))
            if len(self.hand)==0:
                print("The round is over")
                MainBoard.turn=5
                return 0
        else:
            print("That isn't a valid discard")
            self.discard()

    def MoveSelCard(self, x):
        for i in x:
            self.selected.append(self.hand[i])

    def playontable(self):
        hypocard=None
        playablesets=[]
        hyposet=[]
        playablesetsindex=[]
        print(fulltranslate(self.hand))
        inp=input("Which card would you like to play?")
        if int(inp)<=len(self.hand)-1 and int(inp)>0:
            if int(inp) <= len(self.hand) - 1:
                hypocard = self.hand[int(inp)]
            else:
                print("That isn't a valid card")
                self.playontable()
            for st in MainBoard.table:
                hyposet = st.copy()
                hyposet.append(hypocard)
                print(fulltranslate(hyposet), "217")
                print(checkplayable(hyposet))
                if checkplayable(hyposet):
                    playablesets.append(hyposet.copy())
                hyposet.clear()
                playablesetsindex.append(MainBoard.table.index(st))
            if len(playablesets) > 1:
                print(fulltranslatelist(playablesets))
                print("The index of each is: ", end="")
                print(playablesetsindex)
                inp2 = input("Where would you like to play the card?")
                MainBoard.table[playablesetsindex[int(inp2)]].append(hypocard)
                self.hand.pop(int(inp))
                self.cscore += hypocard.value
            elif len(playablesets) == 1:
                MainBoard.table[playablesetsindex[0]].append(hypocard)
                self.hand.pop(int(inp))
                self.cscore += hypocard.value

        else:
            print("That index is invalid")
            self.playontable()

    def addcard(self):
        inp=input("add:")
        for i in MainBoard.deck:
            if i.name==inp:
                self.hand.append(MainBoard.deck.pop(MainBoard.deck.index(i)))
                return print("card added")
        return print("Not in deck")

    def changescore(self):
        inp=input("score:")
        self.score=int(inp)




####################################################################################################################################################
#                                                               DECK
####################################################################################################################################################

# Instantiation of every card
S1 = Card(1, 15, "spades", "s1")
S2 = Card(2, 5, "spades", "s2")
S3 = Card(3, 5, "spades", "s3")
S4 = Card(4, 5, "spades", "s4")
S5 = Card(5, 5, "spades", "s5")
S6 = Card(6, 5, "spades", "s6")
S7 = Card(7, 5, "spades", "s7")
S8 = Card(8, 5, "spades", "s8")
S9 = Card(9, 5, "spades", "s9")
S10 = Card(10, 10, "spades", "s10")
S11 = Card(11, 10, "spades", "s11")
S12 = Card(12, 45, "spades", "s12")
S13 = Card(13, 10, "spades", "s13")
C1 = Card(1, 15, "clubs", "c1")
C2 = Card(2, 5, "clubs", "c2")
C3 = Card(3, 5, "clubs", "c3")
C4 = Card(4, 5, "clubs", "c4")
C5 = Card(5, 5, "clubs", "c5")
C6 = Card(6, 5, "clubs", "c6")
C7 = Card(7, 5, "clubs", "c7")
C8 = Card(8, 5, "clubs", "c8")
C9 = Card(9, 5, "clubs", "c9")
C10 = Card(10, 10, "clubs", "c10")
C11 = Card(11, 10, "clubs", "c11")
C12 = Card(12, 10, "clubs", "c12")
C13 = Card(13, 10, "clubs", "c13")
D1 = Card(1, 15, "diamonds", "d1")
D2 = Card(2, 5, "diamonds", "d2")
D3 = Card(3, 5, "diamonds", "d3")
D4 = Card(4, 5, "diamonds", "d4")
D5 = Card(5, 5, "diamonds", "d5")
D6 = Card(6, 5, "diamonds", "d6")
D7 = Card(7, 5, "diamonds", "d7")
D8 = Card(8, 5, "diamonds", "d8")
D9 = Card(9, 5, "diamonds", "d9")
D10 = Card(10, 10, "diamonds", "d10")
D11 = Card(11, 10, "diamonds", "d11")
D12 = Card(12, 10, "diamonds", "d12")
D13 = Card(13, 10, "diamonds", "d13")
H1 = Card(1, 15, "hearts", "h1")
H2 = Card(2, 5, "hearts", "h2")
H3 = Card(3, 5, "hearts", "h3")
H4 = Card(4, 5, "hearts", "h4")
H5 = Card(5, 5, "hearts", "h5")
H6 = Card(6, 5, "hearts", "h6")
H7 = Card(7, 5, "hearts", "h7")
H8 = Card(8, 5, "hearts", "h8")
H9 = Card(9, 5, "hearts", "h9")
H10 = Card(10, 10, "hearts", "h10")
H11 = Card(11, 10, "hearts", "h11")
H12 = Card(12, 10, "hearts", "h12")
H13 = Card(13, 10, "hearts", "h13")

# Instantiation of players
player1 = Player([], 0, [], [], 0, 0, None, 0, "player 1")
player2 = Player([], 0, [], [], 0, 0, None, 0, "player 2")
player3 = Player([], 0, [], [], 0, 0, None, 0, "player 3")
player4 = Player([], 0, [], [], 0, 0, None, 0, "player 4")

# Deck of cards
Deck = [S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12, S13,
        C1, C2, C3, C4, C5, C6, C7, C8, C9, C10, C11, C12, C13,
        D1, D2, D3, D4, D5, D6, D7, D8, D9, D10, D11, D12, D13,
        H1, H2, H3, H4, H5, H6, H7, H8, H9, H10, H11, H12, H13]

# Instantiation of Board
MainBoard=Board(Deck.copy(), [], [], [], None, 0, None)
####################################################################################################################################################
#                                                            FUNCTIONS
####################################################################################################################################################



# Shuffle the deck and deal the cards
def ShuffleDeal(players, sturn):
    random.shuffle(MainBoard.deck)
    if players==1:
        MainBoard.hands.append(player1)
    elif players == 2:
        MainBoard.hands.append(player1)
        MainBoard.hands.append(player2)
    elif players == 3:
        MainBoard.hands.append(player1)
        MainBoard.hands.append(player2)
        MainBoard.hands.append(player3)
    elif players == 4:
        MainBoard.hands.append(player1)
        MainBoard.hands.append(player2)
        MainBoard.hands.append(player3)
        MainBoard.hands.append(player4)

    if sturn==1:
        for i in range(7):
            if players==1:
                player1.hand.append(MainBoard.deck.pop())
            elif players == 2:
                player1.hand.append(MainBoard.deck.pop())
                player2.hand.append(MainBoard.deck.pop())
            elif players == 3:
                player1.hand.append(MainBoard.deck.pop())
                player2.hand.append(MainBoard.deck.pop())
                player3.hand.append(MainBoard.deck.pop())
            elif players == 4:
                player1.hand.append(MainBoard.deck.pop())
                player2.hand.append(MainBoard.deck.pop())
                player3.hand.append(MainBoard.deck.pop())
                player4.hand.append(MainBoard.deck.pop())
    elif sturn==2:
        for i in range(7):
            if players == 2:
                player2.hand.append(MainBoard.deck.pop())
                player1.hand.append(MainBoard.deck.pop())
            elif players == 3:
                player2.hand.append(MainBoard.deck.pop())
                player3.hand.append(MainBoard.deck.pop())
                player1.hand.append(MainBoard.deck.pop())
            elif players == 4:
                player2.hand.append(MainBoard.deck.pop())
                player3.hand.append(MainBoard.deck.pop())
                player4.hand.append(MainBoard.deck.pop())
                player1.hand.append(MainBoard.deck.pop())
    elif sturn==3:
        for i in range(7):
            if players == 3:
                player3.hand.append(MainBoard.deck.pop())
                player1.hand.append(MainBoard.deck.pop())
                player2.hand.append(MainBoard.deck.pop())
            elif players == 4:
                player3.hand.append(MainBoard.deck.pop())
                player4.hand.append(MainBoard.deck.pop())
                player1.hand.append(MainBoard.deck.pop())
                player2.hand.append(MainBoard.deck.pop())
    elif sturn==4:
        for i in range(7):
            player4.hand.append(MainBoard.deck.pop())
            player1.hand.append(MainBoard.deck.pop())
            player2.hand.append(MainBoard.deck.pop())
            player3.hand.append(MainBoard.deck.pop())





# Checks to see if cards are playable by books
def check_num(lst):
    count = 0
    card=lst[0].card
    for i in lst:
        if i.card == card:
            count += 1
    if count == len(lst):
        return True

# checks to see if every card is in the same suit
def check_suit(lst):
    count = 0
    suit=lst[0].suit
    for i in lst:
        if i.suit==suit:
            count +=1
    if count == len(lst):
        return True


# Checks to see if card are playable by straight
def check_strt(x):
    ace=False
    sort(x)
    if len(x)>=3:
        for i in x:
            if i.card==1:
                ace=True
        if check_suit(x):
            if ace:
                if x[0].card+len(x)-1==x[-1].card or x[1].card+len(x)-2==13:
                    return True
            elif ace==False:
                if x[0].card+len(x)-1==x[-1].card:
                    return True
            else:
                return False
        else:
            return False


def sort(x):
    for i in range(len(x)):
        for j in range(len(x)):
            if x[i].card<x[j].card:
                x[i],x[j]=x[j],x[i]

# Translates the card objects into readable names
def CardTranslate(x):
    return (str(x.card) + " of " + x.suit)

def fulltranslate(x):
    newlist=[]
    for i in x:
        newlist.append(CardTranslate(i))
    return newlist

def checkplayable(x):
    if check_strt(x) or check_num(x):
        return True

def fulltranslatelist(x):
    nl=[]
    for i in x:
        nl.append(fulltranslate(i))
    return nl

def taketurn(player):
    if player.turnstage == 0:
        print("It is player "+str(MainBoard.turn) +"'s turn")
        print("Your hand=" + str(fulltranslate(player.hand)))
        print("There are " + str(len(Deck)) + " cards left in the deck.")
        print("The table=" + str(fulltranslate(MainBoard.table)))
        print("Discard=" + str(fulltranslate(MainBoard.discard)))
        print("Helpful commands: score:shows current total score / hand:shows hand / dpile:shows discard pile / deck:prints # of cards in the deck")
        player.turnstage += 1

    if player.turnstage == 1:
        inp = input("It is your turn, what would you like to do? (dfd: draw from deck / dfdis: draw from discard)")

    if player.turnstage == 2:
        inp = input("Would you like to play cards or dicard? (pc:play cards / dis: discard / pot:play on table)")

    if player.turnstage == 3:
        print("You must play your card from discard")
        print("Your hand=" + str(fulltranslate(player.hand)))
        player.manplayCards()

    if inp == ("dfd") and player.turnstage == 1:
        player.drawdeck()
        player.turnstage = 2

    elif inp == ("dfdis") and player.turnstage == 1:
        if len(MainBoard.discard) > 0:
            if player.drawdiscard():
                player.turnstage = 3
            else:
                player.turnstage = 2
        else:
            print("There are no cards in the discard pile")

    elif inp == ("tbl"):
        print("The table=" + str(fulltranslatelist(MainBoard.table)))

    elif inp == ("deck"):
        print("There are " + str(len(Deck)) + " cards left in the deck.")

    elif inp == ("dpile"):
        print("Discard=" + str(fulltranslate(MainBoard.discard)))

    elif inp == ("hand"):
        print("Your hand=" + str(fulltranslate(player.hand)))

    elif inp == ("score"):
        print("Your current score is " + str(player.score))

   # elif inp == ("ac"):
    #    player.addcard()
    # both for testing purposes
    # elif inp == ("cs"):
     #   player.changescore()

    elif inp == ("pc") and player.turnstage == 2:
        player.playCards()

    elif inp == ("pot") and player.turnstage == 2:
        player.playontable()

    elif inp == ("dis") and player.turnstage == 2:
        if player.discard()==0:
            return 0
        print("Discard=" + str(fulltranslate(MainBoard.discard)))
        # player.turnstage = 1 (For testing purposes)
        MainBoard.turnchange()

    else:
        print("That isn't an option")

def mainloop():
    ShuffleDeal(MainBoard.players, MainBoard.sturn)
    while True:
        while MainBoard.turn == 1:
            taketurn(player1)
        while MainBoard.turn == 2:
            taketurn(player2)
        while MainBoard.turn == 3:
            taketurn(player3)
        while MainBoard.turn == 4:
            taketurn(player4)
        if MainBoard.turn == 5:
            for i in MainBoard.hands:
                if len(i.hand) > 0:
                    for j in i.hand:
                        i.nscore += j.value
                    i.score += i.cscore - i.nscore
            for i in MainBoard.hands:
                if i.score >= 500:
                    print("The game is over")
                    print("The winner is " + i.name)
                    print("Scores:")
                    for j in MainBoard.hands:
                        print(j.name+ ": " +str(j.score))
                    return 0
            MainBoard.sturnchange()
            MainBoard.deck=Deck.copy
            mainloop()
####################################################################################################################################################
#                                                           GAME LOOP
####################################################################################################################################################

def main():
    minp=input("Would you like to play rummy? (y/n)")
    if minp=="y":
        ninp = input("How many players?")
        if int(ninp)==2 or int(ninp)==3 or int(ninp)==4:
            MainBoard.players=int(ninp)
            if MainBoard.sturn==0:
                # MainBoard.sturn=1 (For testing purposes)
                MainBoard.sturn=random.randint(1, int(ninp))
                print("Player "+str(MainBoard.sturn)+" starts")
            MainBoard.turn=MainBoard.sturn
            mainloop()
        else:
            print("You can only choose 2, 3, or 4")
    elif minp=="n":
        print("ok :(")
    else:
        print("That isn't an option >:(")
        main()

main()

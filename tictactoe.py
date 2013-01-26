import pickle
import random
table = []

#generate a table of all possible states and their prob of winning
#everything is .5 except terminal states
#0 for loss/tie, 1 for win


#in abstract:
#play as X
#90% of time, choose best move
#otherwise, explore
#do until you reach terminal
#drag each visited node towards terminal score

#repeat process per game
try:
    table = pickle.load(open('table','r'))
except:

    c = 0

    while c < 262144:
        valid = (c & 3) < 3
        valid &= ((c >> 2) & 3) < 3
        valid &= ((c >> 4) & 3) < 3
        valid &= ((c >> 6) & 3) < 3
        valid &= ((c >> 8) & 3) < 3
        valid &= ((c >> 10) & 3) < 3
        valid &= ((c >> 12) & 3) < 3
        valid &= ((c >> 14) & 3) < 3
        valid &= ((c >> 16) & 3) < 3

        if valid:
            i = c
            j = 0
            tblslot = []
            while j < 9:
                tblslot.append(i&3)
                i >>= 2
                j += 1
            prob = .5 
            for i in range(0,9,3):
                if tblslot[i] == tblslot[i+1] and tblslot[i] == tblslot[i+2]:
                    if tblslot[i] == 1:
                        prob = 1.0
                    elif tblslot[i] == 2:
                        prob = 0.0
            for i in range(3):
                if tblslot[i] == tblslot[i+3] and tblslot[i] == tblslot[i+6]:
                    if tblslot[i] == 1:
                        prob = 1.0
                    elif tblslot[i] == 2:
                        prob = 0.0
            if tblslot[0] == tblslot[4] and tblslot[0] == tblslot[8]:
                    if tblslot[0] == 1:
                        prob = 1.0
                    elif tblslot[0] == 2:
                        prob = 0.0
            if tblslot[2] == tblslot[4] and tblslot[2] == tblslot[6]:
                    if tblslot[2] == 1:
                        prob = 1.0
                    elif tblslot[2] == 2:
                        prob = 0.0

            table.append([tblslot,prob])
        
        c += 1

#table is generated

#find all the potential moves
#create new boards with each potential played, find within the table
#90% choose best one, otherwise explore new option
#repeat process for game until terminal
#drag each visited node towards terminal score
def play(board,p):
    potentials = []
    for i in range(9):
        tempboard = [spot for spot in board]
        if tempboard[i] == 0:
            tempboard[i] = p 
            potentials.append(tempboard)

    #for each potential board
    #find its prob of winning
    #biased randomly choose move

    probs = []
    for potential in potentials:
        for tblslot in table:
            if potential == tblslot[0]: #this may not work because of addressing and shit
                probs.append(tblslot[1])
                break
    if p == 1:
        best = max(probs)
    else:
        best = min(probs)
    bestidxs = []
    otheridxs = []
    for i in range(len(probs)):
        prob = probs[i]
        #print prob,'prob being tested'
        if p == 1:
            if prob >= best:
                bestidxs.append(i)
            else:
                otheridxs.append(i)
        else:
            if prob <= best:
                bestidxs.append(i)
            else:
                otheridxs.append(i)

    bandit = random.random()
    if len(bestidxs) == len(probs):
        #print 'everything option is equally good'
        choiceidx = random.choice(bestidxs)
        choice = potentials[choiceidx]
    else:
        if bandit <= .60: #raise to 1 when playing to win and not learn
            #print 'greedy'
            choiceidx = random.choice(bestidxs)
            choice = potentials[choiceidx]

        elif best == 1 or best == 0:
            choiceidx = random.choice(bestidxs)
            choice = potentials[choiceidx]

        else:
            #print 'exploring'
            choiceidx = random.choice(otheridxs)
            choice = potentials[choiceidx]

    for i in range(len(board)):
        if board[i] != choice[i]:
            board[i] = choice[i]
            break

    return choice


        

def done(board):
    for i in range(0,9,3):
        if board[i] == board[i+1] and board[i] == board[i+2]:
            if board[i] != 0:
                return True
    for i in range(3):
        if board[i] == board[i+3] and board[i] == board[i+6]:
            if board[i] != 0:
                return True
    if board[0] == board[4] and board[0] == board[8]:
            if board[0] != 0:
                return True
    if board[2] == board[4] and board[2] == board[6]:
            if board[2] != 0:
                return True
    return False


def playme():
    nodes = []
    board = [0,0,0, 0,0,0, 0,0,0]
    for i in range(9):
        if i % 2 == 0:
            node = play(board,1)
            nodes.append(node)
            if done(board):
                print 'win for computer'
        else:
            myplay = int(raw_input('play a move:'))-1
            while board[myplay] != 0:
                myplay = int(raw_input('play a move:'))-1
            board[myplay] = 2
            if done(board):
                print 'draw or loss for computer'
                nodes.append(board)

        for i in range(3):
            print board[i],
        print
        for i in range(3,6):
            print board[i],
        print
        for i in range(6,9):
            print board[i],
        print

        if done(board):
            print 'done'
            break

def playmeas2():
    nodes = []
    board = [0,0,0, 0,0,0, 0,0,0]
    for i in range(9):
        if i % 2 == 1:
            node = play(board,2)
            nodes.append(node)
            if done(board):
                print 'win for computer'
        else:
            myplay = int(raw_input('play a move:'))-1
            while board[myplay] != 0:
                myplay = int(raw_input('play a move:'))-1
            board[myplay] = 1 
            if done(board):
                print 'draw or loss for computer'
                nodes.append(board)

        for i in range(3):
            print board[i],
        print
        for i in range(3,6):
            print board[i],
        print
        for i in range(6,9):
            print board[i],
        print

        if done(board):
            print 'done'
            break

def selfplay(rounds):
    for x in range(rounds):
        nodes = []
        node2s = []
        board = [0,0,0, 0,0,0, 0,0,0]
        for i in range(9):
            if i % 2 == 0:
#                print 'Player 1 Moving:'
                node = play(board,1)
                nodes.append(node)
                if done(board):
                    node2s.append(board)
                    if i < 8:
                        #print 'definitely loss for player2'
                        pass
                    else:
                        #print 'draw or loss for player2'
                        pass
            else:
#                print 'Player 2 Moving:'
                #myplay = random.randint(0,8)#int(raw_input('play a move:'))-1
                #while board[myplay] != 0:
                #    myplay = random.randint(0,8)#int(raw_input('play a move:'))-1
                #board[myplay] = 2
                node2 = play(board,2)
                node2s.append(node2)
                if done(board):
                    #print 'loss for player1'
                    nodes.append(board)

            """for i in range(3):
                print board[i],
            print
            for i in range(3,6):
                print board[i],
            print
            for i in range(6,9):
                print board[i],
            print
            """
            if done(board):
#                print 'done'
                break

        nodes = nodes[::-1]
        node2s = node2s[::-1]
        #print node2s,'nodes'
        probs = []
        probs2 = []

        alpha = .4 #+ (1/(x+2))

        for node in nodes:
            for tblslot in table:
                if node == tblslot[0]: #this may not work because of addressing and shit
                    probs.append(tblslot[1])
                    break
        for i in range(1,len(probs)):
            probs[i] = probs[i] + alpha*(probs[i-1] - probs[i])

        for i in range(len(nodes)):
            for tblslot in table:
                if nodes[i] == tblslot[0]:
                    tblslot[1] = probs[i]
                    break
        for node2 in node2s:
            for tblslot in table:
                if node2 == tblslot[0]:
                    probs2.append(tblslot[1])
                    break
        for i in range(1,len(probs2)):
            probs2[i] = probs2[i] + alpha*(probs2[i-1] - probs2[i])
        #print probs2,'new probs'
        for i in range(len(node2s)):
            for tblslot in table:
                if node2s[i] == tblslot[0]:
                    tblslot[1] = probs2[i]
                    break

#selfplay(50000)
playme()
playmeas2()
pickle.dump(table,open('table','w'))


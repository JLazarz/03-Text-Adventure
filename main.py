import sys, logging, json

#check to make sure we are running the right version of Python
version = (3,7)
assert sys.version_info >= version, "This script requires at least Python {0}.{1}".format(version[0],version[1])

#turn on logging, in case we have to leave ourselves debugging messages
logging.basicConfig(format='[%(filename)s:%(lineno)d] %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

def render(game,current,rooms,moves):
    '''Displays the current room, and moves'''
    r = game['rooms']
    c = r[current]

    print('\n\nMoves: {moves}'.format(moves=moves))
    print('\n\nYou are in {name}'.format(name=c['name']))
    print(c['desc'])

print('Welcome to Continental Explorer! Your goal is to reach the Capital of the USA in as few move as possible! Good Luck!')
def getInput(game,current,verbs):
    ''' Asks the user for input and normalizes the inputted value. Returns a list of commands '''    
    toReturn = input('\nWhat would you like to do? ').strip().upper().split()   
    if (len(toReturn)):        
        toReturn[0] = normalizeVerb(toReturn[0],verbs)
    return toReturn

def update(selection,game,current):
    ''' Process the input and update the state of the world '''   
    s = list(selection)[0]  #We assume the verb is the first thing typed    
    if s == "":
        print("\nSorry, I don't understand.")        
        return current    
    elif s == 'EXITS':        
        printExits(game,current)        
        return current  
    else:        
        for e in game['rooms'][current]['exits']:            
            if s == e['verb'] and e['target'] != 'NoExit':                
                return e['target']    
    print("\nYou can't go that way!")    
    return current


def printExits(game,current):    
    e = ", ".join(str(x['verb']) for x in game['rooms'][current]['exits'])    
    print('\nYou can go the following directions: {directions}'.format(directions =e))


def normalizeVerb(selection,verbs):    
    for v in verbs:        
        if selection == v['v']:            
            return v['map']   
    return ""


def end_game(winning,points,moves):    
    if winning:        
        print('You have won! Congratulations')        
        print('You scored {points} points in {moves} moves! Nicely done!'.format(moves=moves, points=points))    
    else:        
        print('Thanks for playing!')        
        print('You scored {points} points in {moves} moves. See you next time!'.format(moves=moves, points=points))


def main():
   
    game = {}
    with open('zork.json') as json_file:
        game = json.load(json_file)
    
    current = 'WHOUS'

    quit = False
    moves = 0
    points = 0
    inventory = []
    while not quit:
        
        render(game,current,game['rooms'],moves)

        selection = getInput(game,current,game['verbs'])

        current = update(selection,game,current)
        moves = moves+1
    return True



#if we are running this from the command line, run main
if __name__ == '__main__':
	main()
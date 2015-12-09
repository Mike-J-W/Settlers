from pieces import *
import random
import pygame
import math
import time
import sys


def main():
    # Initialize all the game pieces
    
    # Set the colors
    oceanBlue = (0, 0, 120)
    forestGreen = (34, 139, 34)
    oceanBlue = (0, 0, 120)
    wheatYellow = (244, 233, 19)
    woolGreen = (144, 238, 144)
    clayColor = (173, 77, 8)
    rockGray = (128, 128, 128)
    sandyDesert = (211, 208, 143)
    black = (0,0,0)
    red = (255, 0, 242)
    playerRed = (213, 5, 46)
    playerBlue = (102, 207, 245)
    playerGreen = (90, 206, 48)
    playerPurple = (149, 58, 172)
    playerWhite = (255, 255, 255)
    playerOrange = (255, 182, 71)
    playerColors = {"red": playerRed, "blue": playerBlue, "green": playerGreen, "purple": playerPurple, "white": playerWhite, "orange": playerOrange}
    
    # Set the piece and image sizes
    hexEdgeLength = 60                                                      # The length of a side of a hex
    hexRadius = int(round(hexEdgeLength * math.sqrt(3) / 2.0))              # The distance from a hex's center to the midpoint of an edge
    settlementEdgeLength = int(round(hexEdgeLength / 4))                    # The width of a town
    roadWidth = int(round(settlementEdgeLength / 3))                        # The width of a road
    robberRadius = int(settlementEdgeLength)                                # The radius of the circle denoting the Robber
    screenSize = (hexRadius * 10 + hexEdgeLength * 4, hexEdgeLength * 12)   # The size of the window that is opened

    # The resource and card variables
    lumber = "Wood"
    grain = "Wheat"
    wool = "Wool"
    clay = "Clay"
    ore = "Ore"
    desert = "Desert"
    resourceTypes = [lumber, grain, wool, clay, ore]    # A list of the resources in the game
    resourceToColor = {lumber: forestGreen, grain: wheatYellow, wool: woolGreen, clay: clayColor, ore: rockGray, desert: sandyDesert}    # A dictionary relating resouces to colors
    developmentDeck = Card_Deck(["Knight"] * 14 + ["Monopoly", "Year of Plenty", "Road Building"] * 2 + ["Victory Point"] * 5)    # A list with one element per development card
    resourceDecks = {lumber: 19, grain: 19, wool: 19, clay: 19, ore: 19}    # A dictionary to hold the decks of resources, keyed to their resource name
    resourcesForHexes = [lumber] * 4 + [grain] * 4 + [wool] * 4 + [clay] * 3 + [ore] * 3    # A list representing the number of hexes per resource
    random.shuffle(resourcesForHexes) # Shuffle the list of hex resources

    # Making the odds tiles placed on top of the hexes
    odds = [6,6,8,8,2,3,3,4,4,5,5,9,9,10,10,11,11,12]   # A list of the numbered, circular tiles denoting times of harvest
    indices = [i for i in range(19)]    # A list of the indices of the odds tiles
    # A list of hexes adjacent to the hex represented by the index of the larger list (e.g. hex 0 is adjacent to hexes [1,3,4])
    adjacents = [[1,3,4],[0,2,4,5],[1,5,6],[0,4,7,8],[0,1,3,5,8,9],[1,2,4,6,9,10],[2,5,10,11],[3,8,12],[3,4,7,9,12,13],[4,5,8,10,13,14],[5,6,9,11,14,15],[6,10,15],[7,8,13,16],[8,9,12,14,16,17],[9,10,13,15,17,18],[10,11,14,18],[12,13,17],[13,14,16,18],[14,15,17]]
    oddsOrdered = [0] * 19    # A list to hold the odds tiles placed in random order
    # Loop through the odds to place each in oddsOrdered
    for o in odds:
        oddPlaced = False   # A flag to determine if a place was found for the odd
        # Keep trying to place the odd until successful
        while not oddPlaced:
            newIndex = random.choice(indices)   # Pick an index from those still available
            goodIndex = True                    # Start by assuming the index is valid
            # If the odd is 6 or 8, check that it would not be placed on a hex adjacent to another 6 or 8
            if o == 6 or o == 8:
                # Look at the hexes adjacent to the hex of the currently chosen index
                for i in adjacents[newIndex]:
                    # Check if that hex has a 6 or 8
                    if oddsOrdered[i] == 6 or oddsOrdered[i] == 8:
                        # If so, don't use that index
                        goodIndex = False
                        break
            # If the index is valid, assign the odd to that index in the ordered odds list and remove the index from the list as seen by later iterations of the loop
            if goodIndex:
                oddsOrdered[newIndex] = o
                indices.remove(newIndex)
                oddPlaced = True
    # Get the index of the 0-odd tile and insert "Desert" at that index in the resources list
    desertIndex = oddsOrdered.index(0)
    resourcesForHexes.insert(desertIndex, "Desert")
    
    # The unadjusted coordinates of the centers of the hexes
    baseHexCenters = [(3,1),(5,1),(7,1),(2,2.5),(4,2.5),(6,2.5),(8,2.5),(1,4),(3,4),(5,4),(7,4),(9,4),(2,5.5),(4,5.5),(6,5.5),(8,5.5),(3,7),(5,7),(7,7)]
    # The centers of the hexes adjusted for the length of their sides
    hexCenters = [(int(2 * hexEdgeLength + baseHexCenters[i][0] * hexRadius), int((baseHexCenters[i][1] + 2) * hexEdgeLength)) for i in range(len(baseHexCenters))]
    # A list of the hexes, assigned a resource and a numbered tile using the lists above
    hexes = [Hex(resourcesForHexes[x], oddsOrdered[x], resourceToColor[resourcesForHexes[x]], hexCenters[x], hexEdgeLength) for x in range(19)]
    # Iterate over the hexes and create Vertex objects using the coordinates of their vertices
    vertices = []
    vertexCoordsSeen = []
    # Loop over the top 3 rows of hexes
    for hex in hexes[:12]:
        # Loop over the coordinates of the upper 3 vertices
        for index, coord in enumerate(hex.vertexCoordinates[:3]):
            # Check that this is a new vertex coordinate
            if coord not in vertexCoordsSeen:
                vertexCoordsSeen.append(coord)  # Record this vertex position
                newVertex = Vertex(coord)       # Create a new Vertex object at these coordinates
                # Check that the vertex is not the upper-left vertex of the hex
                # If not, record that this vertex is adjacent to the previous vertex
                if index != 0:
                    vertices[-1].adjacentVertices.append(newVertex)
                    newVertex.adjacentVertices.append(vertices[-1])
                # Add the vertex to the list of vertices
                vertices.append(newVertex)
    # Repeat the loop above for the bottom three rows of hexes
    for hex in hexes[7:]:
        # Use the lower 3 coordinates here
        for index, coord in enumerate(hex.vertexCoordinates[3:][::-1]):
            if coord not in vertexCoordsSeen:
                vertexCoordsSeen.append(coord)
                newVertex = Vertex(coord)
                if index != 0:
                    vertices[-1].adjacentVertices.append(newVertex)
                    newVertex.adjacentVertices.append(vertices[-1])
                vertices.append(newVertex)
    # Loop through the vertices and relate them to the hexes they touch
    for vertex in vertices:
        # For each vertex, look at hex
        for hex in hexes:
            # Check that the vertex and hex aren't already related but the coordinates match
            if vertex not in hex.vertices and vertex.coordinates in hex.vertexCoordinates:
                verIndex = hex.vertexCoordinates.index(vertex.coordinates)  # Record the position of the vertex according to the hex's coordinate list
                hex.vertices[verIndex] = vertex     # Place the vertex into the hex's vertex list at the same position
                vertex.hexes.append(hex)            # Add the hex to the vertex's hex list
                # If the vertex has 3 hexes in its hex list, no more hexes need to be examined
                if len(vertex.hexes) == 3:
                    break
    # Loop through the hexes and relate vertices that are vertically adjacent
    for hex in hexes:
        if hex.vertices[0] not in hex.vertices[5].adjacentVertices:
            hex.vertices[0].adjacentVertices.append(hex.vertices[5])
            hex.vertices[5].adjacentVertices.append(hex.vertices[0])
        if hex.vertices[2] not in hex.vertices[3].adjacentVertices:
            hex.vertices[2].adjacentVertices.append(hex.vertices[3])
            hex.vertices[3].adjacentVertices.append(hex.vertices[2])

    # A list of the ports on the map
    ports = [Port(resource, 2) for resource in resourceTypes]
    ports += [Port("All", 3)] * 4
    # Assign the ports to the appropriate vertices
    vertices[0].port = ports[5]
    vertices[1].port = ports[5]
    ports[5].vertices = [vertices[0], vertices[1]]
    vertices[3].port = ports[2]
    vertices[4].port = ports[2]
    ports[2].vertices = [vertices[3], vertices[4]]
    vertices[7].port = ports[4]
    vertices[14].port = ports[6]
    vertices[15].port = ports[6]
    ports[6].vertices = [vertices[14], vertices[15]]
    vertices[17].port = ports[4]
    ports[4].vertices = [vertices[7], vertices[17]]
    vertices[26].port = ports[7]
    vertices[28].port = ports[1]
    vertices[37].port = ports[7]
    vertices[38].port = ports[1]
    ports[7].vertices = [vertices[26], vertices[37]]
    ports[1].vertices = [vertices[28], vertices[38]]
    vertices[45].port = ports[3]
    vertices[46].port = ports[3]
    ports[3].vertices = [vertices[45], vertices[46]]
    vertices[47].port = ports[8]
    vertices[48].port = ports[8]
    ports[8].vertices = [vertices[47], vertices[48]]
    vertices[50].port = ports[0]
    vertices[51].port = ports[0]
    ports[0].vertices = [vertices[50], vertices[51]]

    # Create the Robber
    robber = Robber(hexes[desertIndex], robberRadius)

    # Instaniate the players
    # The game expects 4 players and a name, a color, and an AI status (True or False) for each
    if len(sys.argv) != 13:
        print("Wrong number of arguments (name, color, isAI four times)")
        sys.exit()
    # Check that the colors given are in the player-color dictionary
    for inputColor in sys.argv[2::3]:
        if inputColor not in playerColors:
            print("\"{}\" is not a valid color.  The options are: {}".format(inputColor, ", ".join(playerColors.keys())))
            sys.exit()
    # Default AI status for each player is False - assumes the players are human
    p1AI = False
    p2AI = False
    p3AI = False
    p4AI = False
    trueOpts = ["True", "true", "T", "t"]   # The options that signify the player is an AI
    # Check if the player is an AI
    if sys.argv[3] in trueOpts:
        p1AI = True
    # Instantiate a player with their name, color, AI status, and the sizes of their pieces
    player1 = Player(sys.argv[1], playerColors[sys.argv[2]], p1AI, settlementEdgeLength, roadWidth)
    if sys.argv[6] in trueOpts:
        p2AI = True
    player2 = Player(sys.argv[4], playerColors[sys.argv[5]], p2AI, settlementEdgeLength, roadWidth)
    if sys.argv[9] in trueOpts:
        p3AI = True
    player3 = Player(sys.argv[7], playerColors[sys.argv[8]], p3AI, settlementEdgeLength, roadWidth)
    if sys.argv[12] in trueOpts:
        p4AI = True
    player4 = Player(sys.argv[10], playerColors[sys.argv[11]], p4AI, settlementEdgeLength, roadWidth)
    # Construct a list of the players
    playerList = [player1, player2, player3, player4]
    # Give the players enough cards to build their first settlements and roads
    startingHand = [grain, wool] * 2 + [clay, lumber] * 4
    for player in playerList:
        player.draw_cards(startingHand, resourceDecks)
    # Shuffle the players to set the turn order
    random.shuffle(playerList)

    # Set up the award placards
    largestArmy = Largest_Army(playerList)
    longestRoad = Longest_Road(playerList)


    ## Pygame initialization
    pygame.init()
    screen = pygame.display.set_mode(screenSize)    # opens the window with the size specifications given
    screen.fill(oceanBlue)                          # sets the background color
    myfont = pygame.font.SysFont("comicsansms", 25) # sets the font and size

    # The pygame loop
    boardDrawn = False                  # A flag to track if the board has been drawn
    initialSettlementsBuilt = False     # A flag to track if the players have built their starting settlements and roads
    while 1:
        # Draw the hexes, odds tiles, and Robber
        if not boardDrawn:
            # Loop through the hexes, so that they can be drawn
            for hex in hexes:
                pygame.draw.polygon(screen, hex.color, hex.vertexCoordinates, 0)    # Draw the hex
                # Check that the hex is not the desert hex
                if hex.resource != desert:
                    resourceOdds = str(hex.odds)    # Record the hex's odds tile
                    # Set the color of the odds number's text based on the value
                    if resourceOdds == "6" or resourceOdds == "8":
                        label = myfont.render(resourceOdds, 1, red)
                    else:
                        label = myfont.render(resourceOdds, 1, black)
                    screen.blit(label, (hex.coordinates))   # Place the number on the screen
                # If the hex is the desert, place the Robber on it
                else:
                    robber.move(hex, screen)
            pygame.display.flip()   # Update the whole screen in order to show the newly drawn board
            boardDrawn = True       # Record that the board has been drawn

        # Set up the initial settlements and roads for each player
        if not initialSettlementsBuilt:
            print("Each player must build their first settlements and roads.")
            # Loop through the shuffled player list forwards once and then backwards once
            for player in playerList + playerList[::-1]:
                validAction = False     # A flag to track whether the player has completed a valid action
                print("")               # Give a line break
                # Repeat until the player successfully builds a settlement
                while not validAction:
                    print("For the settlement, ")
                    settlementVertex = get_vertex_from_player(player, vertices) # Ask the player for the vertex on which to build their settlement
                    buildResult = player.build_town(settlementVertex, screen)   # Attempt to build and draw the settlement
                    # If unsuccessful, print the error message and loop again
                    if buildResult[0] != 0:
                        print(buildResult[1] + "  Please try again")
                    # If successful, update the screen to show the settlement and end the loop
                    else:
                        validAction = True      # Set the tracker so that the loop doesn't repeat
                        pygame.display.update() # Update the screen to show the new settlement
                validAction = False     # Reset the valid action tracker
                # Repeat until the player successfully builds a road
                while not validAction:
                    print("For the heading of the road from that settlement, ")
                    roadDestinationVertex = get_vertex_from_player(player, vertices)    # Ask the player for the vertex to which their road goes
                    buildResult = player.build_road(settlementVertex, roadDestinationVertex, longestRoad, screen)   # Attempt to build and draw the road
                    # If unsuccessful, print the error message and loop again
                    if buildResult[0] != 0:
                        print(buildResult[1] + "  Please try again")
                    # If successful, update the screen and end the loop
                    else:
                        validAction = True
                        pygame.display.update()
            initialSettlementsBuilt = True  # Record that the players have built the initial 2 settlements and roads
        
        # Loop through the players to let each take their game turns
        for player in playerList:
            player.developmentCards.append("Knight")
            # Let the player play a knight before roll if they choose
            validAction = False     # A flag to track whether the player has completed a valid action
            # Repeat until the player successfully plays a Knight or decides to roll
            while not validAction:
                playKnightFirst = get_knight_choice_from_player(player) # Ask the player if they'd like to play a Knight before the roll
                # If the player wants to play a Knight, begin that proceess
                if playKnightFirst == "k":
                    robberPlay = get_robber_play_from_player(player, robber, hexes) # Ask the player how they'd like to use the Robber
                    knightResult = player.play_knight(robber, robberPlay[0], robberPlay[1], largestArmy, screen)    # Attempt to make that play
                    # If unsuccessful, print the error message and repeat the loop
                    if knightResult[0] != 0:
                        print(knightResult[1])
                    # If successful, print the result of the move and end the loop
                    else:
                        validAction = True      # Set the tracker so that the loop doesn't repeat
                        print(knightResult[1])  # Print the result of the player stealing from someone
                        pygame.display.update() # Update the screen to show the new location of the Robber
                else:
                    validAction = True
        
            # Roll the dice and print the result
            diceResult = random.randint(1,6) + random.randint(1,6)
            print("\n{} rolled a {}.".format(player.name, diceResult))

            # Check if the roll was a 7, and have the players discards cards and play the Robber if so
            if diceResult == 7:
                # Discard cards for players with more than 7
                for playerToCheck in playerList:
                    if sum(playerToCheck.cardsInHand.values()) > 7:
                        validAction = False
                        while not validAction:
                            discardDict = get_cards_to_discard_from_player(playerToCheck, resourceTypes)
                            discardResult = playerToCheck.discard_cards(discardDict, resourceDecks)
                            if discardResult[0] != 0:
                                print(discardResult[1] + " Please try again.")
                            else:
                                validAction = True
                robberPlay = get_robber_play_from_player(player, robber, hexes) # Ask the player how they'd like to play the Robber
                robberResult = robber.play(screen, robberPlay[0], player, robberPlay[1])    # Attempt to make that play
                pygame.display.update() # Update the screen to show the new location of the Robber
                print(robberResult) # Print the result of the player stealing from someone
            else:
                # Have the players draw their resource cards
                for playerDrawing in playerList:
                    for settlement in playerDrawing.builtSettlements:
                        playerDrawing.draw_cards(settlement.find_yield(diceResult), resourceDecks)
                    print("{} has {}".format(playerDrawing.name, playerDrawing.cardsInHand))
            
            # build and/or trade and/or play Dev Card
            turnIsOver = False
#            while not turnIsOver:
#               turnAction = get_turn_action_from_player(player)
    

        # waits ten seconds and then starts the whole process over again
        time.sleep(1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()


def get_cards_to_discard_from_player(player, resourceTypes):
    if player.isAI:
        pass
    else:
        handSize = sum(player.cardsInHand.values())
        numberToDiscard = int(round(handSize / 2, -0))
        correctNumberChosen = False
        cardsToDiscard = dict(zip(resourceTypes, [0,0,0,0,0]))
        while not correctNumberChosen:
            print("{}, you have {} cards and must discard {}.".format(player.name, handSize, numberToDiscard))
            print("Your cards are: {}".format(player.cardsInHand))
            for resource in resourceTypes:
                if player.cardsInHand[resource] != 0:
                    validInput = False
                    while not validInput:
                        resourceInput = input("You have {} {} cards. How many will you dicard? ".format(player.cardsInHand[resource], resource))
                        try:
                            resourceCount = int(resourceInput)
                            if 0 <= resourceCount <= player.cardsInHand[resource]:
                                cardsToDiscard[resource] = resourceCount
                                validInput = True
                            else:
                                print("Not within the valid range.")
                        except ValueError:
                            print("That was not an integer.")
            if sum(cardsToDiscard.values()) > numberToDiscard or sum(cardsToDiscard.values()) < numberToDiscard:
                print ("Incorrect number of cards chosen.")
                cardsToDiscard = dict(zip(resourceTypes, [0,0,0,0,0]))
            else:
                correctNumberChosen = True
        return cardsToDiscard


def get_turn_action_from_player(player):
    if player.isAI:
        pass
    else:
        print("The options are: build road, build town, build city, buy development card, play Knight, play Monoply, play Year of Plenty, play Road Building, trade, end turn")
        actionName = input("{} please give the 0-based index of the turn action to take.".format(player.name))


# A function to get the new hex for the Robber and the player from whom the player wants to steal
# Takes the player moving the Robber, the Robber, and the list of hexes
def get_robber_play_from_player(player, robber, hexes):
    # Check if the player is an AI or human
    if player.isAI:
        pass
    else:
        destinationHex = robber.currentHex  # Get the current hex of the Robber to use as a metric to determine when the player has successfully picked a new hex
        while destinationHex == robber.currentHex:
            print("\nChoose a new hex for the Robber.")
            destinationHex = get_hex_from_player(player, hexes) # Ask the player to which hex they want to move the Robber
        playersAvailableToRob = []  # A list to hold the players from whom the player can steal
        # Loop through the vertices that surround the Robber's new hex
        for vertex in destinationHex.vertices:
            # Check whether each vertex has a settlement built on it
            if vertex.settlement != None:
                # If so, check that the owner of that settlement is not the player
                if vertex.settlement.owner != player and vertex.settlement.owner not in playersAvailableToRob:
                    # If that's the case, the owner of that vertex is a player from whom the player can steal
                    playersAvailableToRob.append(vertex.settlement.owner)
        playerToRob = None  # The default value for the player from whom the player will steal
        # If the player has multiple players from whom they can steal, ask them to choose their target
        if len(playersAvailableToRob) > 1:
            print("Choose the player from whom you wish to steal.")
            playerToRob = get_player_from_player(player, playersAvailableToRob)
        # If there is only one player from the player can steal, use that player as their target
        elif len(playersAvailableToRob) == 1:
            playerToRob = playersAvailableToRob[0]
        # Return the hex to which the Robber will be moved and the player who will be robbed
        return (destinationHex, playerToRob)

# A function to get the player's decision on whether to play a knight before their roll
# Takes the player to be queried
def get_knight_choice_from_player(player):
    # Check if the player is an AI or human
    if player.isAI:
        pass
    else:
        # Get the player's input on the decision
        choice = input("\n{} enter k to play a Knight before the roll or enter r to roll now: ".format(player.name))
        # Check that it was a valid input - if not, call the function again to repeat the query
        if choice != "r" and choice != "k":
            print("That was not a valid option.")
            choice = get_knight_choice_from_player(player)
        # Return either "r' or "k" based on whether the player wants to roll the dice or play a Knight
        return choice

# A function to get the player's choice from among multiple players
# Takes the player choosing and the list of players from which the player is choosing
def get_player_from_player(player, playerList):
    # Check if the player is an AI or human
    if player.isAI:
        pass
    else:
        playerNames = [p.name for p in playerList]  # Make a list of the player names
        print("The players are: " + ", ".join(playerNames)) # Show the players to the player
        playerIndex = input("{} please give a 0-based index to choose a player: ".format(player.name))  # Get the player's choice
        # Attempt to convert the input string to an integer and reference the player object corresponding to the name
        try:
            chosenPlayer = playerList[int(playerIndex)]
        # If the input was not an integer, print an error message and call the fuction again to repeat the query
        except ValueError:
            print("That entry was not an integer.")
            chosenPlayer = get_player_from_player(player, playerList)
        # If the input was not a valid index for the player list, print an error message and call the function again to repeat the query
        except IndexError:
            print("That index is out of the range of valid players")
            chosenPlayer = get_player_from_player(player, playerList)
        # Return the player object corresponding to the name entered by the player
        return chosenPlayer

# A function to get a hex chosen by the player
# Takes the player choosing and the list of board hexes
def get_hex_from_player(player, hexList):
    # Check if the player is an AI or human
    if player.isAI:
        pass
    else:
        hexIndex = input("{} please give a hex index: ".format(player.name))    # Get the player's hex choice
        # Attempt to convert the input string to an integer and reference the hex object corresponding to the index
        try:
            hex = hexList[int(hexIndex)]
        # If the input was not an integer, print an error message and call the fuction again to repeat the query
        except ValueError:
            print("That entry was not an integer.")
            hex = get_hex_from_player(player, hexList)
        # If the input was not a valid index for the hex list, print an error message and call the function again to repeat the query
        except IndexError:
            print("That index is out of the range of valid hexes")
            hex = get_hex_from_player(player, hexList)
        # Return the hex object corresponding to the index chosen by the player
        return hex

# A function to get a vertex chosen by the player
# Takes the player choosing and the list of vertices
def get_vertex_from_player(player, vertexList):
    # Check if the player is an AI or human
    if player.isAI:
       pass
    else:
        vertexIndex = input("{} please give a vertex index: ".format(player.name))  # Get the player's vertex index choice
        # Attempt to convert the input string to an integer and reference the vertex object corresponding to the index
        try:
            vertex = vertexList[int(vertexIndex)]
        # If the input was not an integer, print an error message and call the fuction again to repeat the query
        except ValueError:
            print("That entry was not an integer.")
            vertex = get_vertex_from_player(player, vertexList)
        #  If the input was not a valid index for the vertex list, print an error message and call the function again to repeat the query
        except IndexError:
            print("That index is out of the range of valid vertices")
            vertex = get_vertex_from_player(player, vertexList)
        # Return the vertex object corresponding to the index chosen by the player
        return vertex



if __name__ == "__main__":
    main()

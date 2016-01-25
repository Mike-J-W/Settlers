from pieces import *
import random
import pygame
import math
import time
import sys
import os
import geometricfunctions as gf
from constants import * #TODO holds all the game constants e.g. colors, menu_dicts, etc


def main():
    # Initialize all the game pieces

    random.shuffle(resourcesForHexes) # Shuffle the list of hex resources

    # Making the odds tiles placed on top of the he7]]
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
    ports = [Port([resource], 2) for resource in resourceTypes]
    ports += [Port(list(resourceTypes), 3) for i in range(4)]
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

    # Instantiate the players
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
    startingHand = {grain: 2, wool: 2, clay: 4, lumber: 4}
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
    myfont = pygame.font.SysFont("comicsansms", 25) # sets the font and size
    keyFont = pygame.font.SysFont("Arial", 15)
    pygame.event.set_allowed(None)
    pygame.event.set_allowed([pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN, pygame.QUIT])

    # The pygame loop
    boardDrawn = False                  # A flag to track if the board has been drawn
    initialSettlementsBuilt = False     # A flag to track if the players have built their starting settlements and roads
    gameOver = False                    # A flag to track if a player has won the game
    while 1:
        # Draw the key, hexes, odds tiles, and Robber
        if not boardDrawn:
            # Set the background color
            screen.fill(oceanBlue)
            # Draw the player key
            pygame.draw.rect(screen, (255,255,255), (int(round(hexEdgeLength/2)), int(round(hexEdgeLength/2)), 120, 120), 0)
            keyTitle = keyFont.render("Player Key", 1, black)
            screen.blit(keyTitle, (int(round(hexEdgeLength/2)) + 5, int(round(hexEdgeLength/2))))
            for count, player in enumerate(playerList):
                pygame.draw.rect(screen, player.color, (int(round(hexEdgeLength/2)) + 5, int(round(hexEdgeLength/2)) + 25 + (count * 25), 12, 12), 0)
                playerLabel = keyFont.render(player.name, 1, black)
                screen.blit(playerLabel, (int(round(hexEdgeLength/2)) + 27, int(round(hexEdgeLength/2)) + 22 + (count * 25)))
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
            # Draw the Robber
            robber.draw_robber(screen)
            # Draw the ports, colored according to their resource
            for port in ports:
                portColor = (0,0,0)
                if port.resources != resourceTypes:
                    portColor = resourceToColor[port.resources[0]]
                port.draw_port(screen, portColor)
            # Draw any existing player objects
            for player in playerList:
                if player.builtRoads != []:
                    for road in player.builtRoads:
                        road.draw_road(screen)
                if player.builtSettlements != []:
                    for settlement in player.builtSettlements:
                        settlement.draw_settlement(screen)
            pygame.display.flip()   # Update the whole screen in order to show the newly drawn board
            boardDrawn = True       # Record that the board has been drawn

        # Set up the initial settlements and roads for each player
        if not initialSettlementsBuilt:
            print("Each player must build their first settlements and roads.")
            # Loop through the shuffled player list forwards once and then backwards once
            for player in playerList: #+ playerList[::-1]:  #########TODO NEEED TO CHANGE BACK!!!
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
                    print("For the heading of the road from that settlement:")
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

        if not gameOver:
            # Loop through the players to let each take their game turns
            for player in playerList:
                print("\n{}, it is now your turn.".format(player.name))

                # Initiate the pre-harvest menu
                actionChoice = present_menu(player, preHarvestMenu)
                result = eval(actionChoice)
                if not isinstance(result, int):
                    result = roll_dice(player)
                diceResult = result

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

                turnOver = False
                while not turnOver:
                    actionChoice2 = present_menu(player, postHarvestMenu)
                    result = eval(actionChoice2)
                    if result[1] == "Turn is over.":
                        turnOver = True
                        if result[2] >= 10:
                            print("\n{} has won the game with {} points!!".format(player.name, result[3]))
                            gameOver = True
                if gameOver:
                    break

            screen.fill(black)
            pygame.display.update()
            boardDrawn = False

        # waits ten seconds and then starts the whole process over again
        time.sleep(2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()


# A function to take the player's input and build a road
def build_road(player, vertexList, longestRoad, screen):
    successfulBuild = False
    while not successfulBuild:
        print("Pick the first vertex.")
        vertex1 = get_vertex_from_player(player, vertexList)
        print("Pick the second vertex.")
        vertex2 = get_vertex_from_player(player, vertex1.adjacentVertices)
        result = player.build_road(vertex1, vertex2, longestRoad, screen)
        print(result[1])
        if result[0] == 0:
            successfulBuild = True
    pygame.display.update()
    return (0, "Road built!")

# A function to take the player's input and build a settlement
def build_settlement(player, vertexList, screen):
    successfulBuild = False
    while not successfulBuild:
        print("Pick the vertex desired for the settlement.")
        vertexToSettle = get_vertex_from_player(player, vertexList)
        result = player.build_town(vertexToSettle, screen)
        print(result[1])
        if result[0] == 0:
            successfulBuild = True
    pygame.display.update()
    return (0, "Settlement built!")


# A function to take the player's input and upgrade a settlement
def upgrade_settlement():
    pass

# A function to buy a devlopment card for a player
def buy_development_card():
    pass

# A function to take the player's input and play a monopoly card
def play_monopoly_card():
    pass

# A function to take the player's input and play a year of plenty card
def play_yop_card():
    pass

# A function to take the player's input and play a road building card
def play_road_building():
    pass

# A function to take the player's input and make a maritime trade
def maritime_trade():
    pass

# A function to take th player's input and offer a trade to other players
def offer_trade():
    pass

# A function to complete end-of-turn checks and move to the next player
def end_turn(player):
    # Count the player's point
    pointTotal = player.count_points()
    player.points = pointTotal
    # Clear the screen
    os.system('cls' if os.name == 'nt' else 'clear')
    return (0, "Turn is over.", pointTotal)

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


# A function to get the new hex for the Robber and the player from whom the player wants to steal
# Takes the player moving the Robber, the Robber, and the list of hexes
def get_robber_play_from_player(player, robber, hexes):
    # Check if the player is an AI or human
    if player.isAI:
        pass
    else:
        destinationHex = robber.currentHex  # Get the current hex of the Robber to use as a metric to determine when the player has successfully picked a new hex
        while destinationHex == robber.currentHex:
            print("Choose a new hex for the Robber.")
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
        # Create a list of names
        playerNames = []
        for p in playerList:
            if p != None:
                playerNames.append(p.name)
            else:
                playerNames.append("Nobody")
        # Make a dictionary of the player names the player objects
        playerMenu = dict(zip(playerNames, playerList))
        # Get the choice
        print("Please choose a player.")
        chosenPlayer = present_menu(player, playerMenu)
        # Return the player object corresponding to the name entered by the player
        return chosenPlayer

# A function to get a hex chosen by the player
# Takes the player choosing and the list of board hexes
def get_hex_from_player(player, hexList):
    # Check if the player is an AI or human
    if player.isAI:
        pass
    else:
        # Loop until the user clicks on a vertex
        validClick = False
        while not validClick:
            # Make sure no other events are on the queue
            pygame.event.clear()
            # Prompt the user for a click and wait for two events
            print("{} please click a hex.".format(player.name))
            chosenHex = None
            eventA = pygame.event.wait()
            eventB = pygame.event.wait()
            # If the next two events are the mouse being pressed down and then released, move forward
            if eventA.type == pygame.MOUSEBUTTONDOWN and eventB.type == pygame.MOUSEBUTTONUP:
                posA = eventA.__dict__['pos']
                posB = eventB.__dict__['pos']
                # If the mouse actions (pressed down, released) were no more than 10 pixels apart, move forward
                if gf.pp_distance(posA, posB) < 10:
                    # Loop through the hexes to see if the click ocurred inside one
                    for hex in hexList:
                        # If both mouse actions ocurred inside the current hex, move forward
                        if gf.is_within_hex(hex, posA) and gf.is_within_hex(hex, posB):
                            # Record the hex, switch the boolean to end the while loop, and break the hex loop
                            chosenHex = hex
                            validClick = True
                            break
                    if validClick == False:
                        print("That click was not inside a hex. Please try again.")
                else:
                    print("The mouse moved while pressed down. Please try again.")
        return chosenHex

# A function to get a vertex chosen by the player
# Takes the player choosing and the list of vertices
def get_vertex_from_player(player, vertexList):
    # Check if the player is an AI or human
    if player.isAI:
       pass
    else:
        # Loop until the user clicks on a vertex
        validClick = False
        while not validClick:
            # Make sure no other events are on the queue
            pygame.event.clear()
            # Prompt the user for a click and wait for two events
            print("{} please click a vertex.".format(player.name))
            eventA = pygame.event.wait()
            eventB = pygame.event.wait()
            # If the next two events are the mouse being pressed down and then released, move forward
            if eventA.type == pygame.MOUSEBUTTONDOWN and eventB.type == pygame.MOUSEBUTTONUP:
                # Get the coordinates of each vertex on the board
                vertexCoords = [v.coordinates for v in vertexList]
                # Get the coordinates of the vetices closes to where the mouse was pressed down and where it was released
                verCoordA = gf.get_closest_point(vertexCoords, eventA.__dict__['pos'])
                verCoordB = gf.get_closest_point(vertexCoords, eventB.__dict__['pos'])
                # If the two coordinates are the same and both events happened within 10 pixels each other, move forward
                if verCoordA[0] == verCoordB[0] and abs(verCoordA[1] - verCoordB[1]) < 10:
                    # If the mouse action (pressed down, released) happened within 10 pixels of the closest vertex, move forward
                    if verCoordA[1] <= 10 and verCoordB[1] <= 10:
                        # With all condiitions satisfied, find the vertex corresponding to the coordinates found
                        closestVertex = vertexList[vertexCoords.index(verCoordA[0])]
                        validClick = True
                    else:
                        print("That click was not close enough to a vertex. Please try again.")
                else:
                    print("The mouse moved while pressed down. Please try again.")
        return closestVertex

def present_menu(player, menuDict):
    if player.isAI == True:
        pass
    else:
        print("The available options are:")
        menuOpts = sorted(list(menuDict.keys()))
        for i, e in enumerate(menuOpts):
            print("\t{}\t{}".format(i, e))

        validOptionFound = False
        while not validOptionFound:
            option = input("Please choose an option: ")
            try:
                optIndex = int(option)
            except:
                print("not an integer.  try again")
                continue
            try:
                optKey = menuOpts[optIndex]
            except:
                print("not a valid option.  try again")
                continue
            action = menuDict[optKey]
            validOptionFound = True
        return action

# Function that simply rolls the dice and returns the result
def roll_dice(player):
    # Roll the dice and print the result
    diceResult = random.randint(1,6) + random.randint(1,6)

    print("Rolling Dice now...")
    print("{} rolled a(n) {}.\n".format(player.name, diceResult))

    return diceResult

# Function that deals with the choice to play the knight first
# Takes the player in question
def play_knight(player,robber,hexes,largestArmy, screen):
    player.developmentCards.append("Knight")
    robberPlay = get_robber_play_from_player(player, robber, hexes) # Ask the player how they'd like to use the Robber
    knightResult = player.play_knight(robber, robberPlay[0], robberPlay[1], largestArmy, screen)    # Attempt to make that play
    pygame.display.update()
    print(knightResult[1])
    print()
    return knightResult



if __name__ == "__main__":
    main()

import random
import pygame
import time
import sys
import os
import collections
import geometricfunctions as gf
import constants as c
import pieces as p


def main():

    # A dictionary to hold the decks of resources, keyed to their resource name
    resourceDecks = {c.lumber: 19, c.grain: 19, c.wool: 19, c.clay: 19, c.ore: 19}
    developmentDeck = collections.deque(c.developmentDeckList)

    # A list of the hexes, assigned a resource and a numbered tile using the lists above
    hexes = [p.Hex(c.resourcesForHexes[x], c.oddsOrdered[x], c.resourceToColor[c.resourcesForHexes[x]], c.hexCenters[x])
             for x in range(19)]
    # Iterate over the hexes and create Vertex objects using the coordinates of their vertices
    vertices = []
    vertexCoordsSeen = []
    # Loop over the top 3 rows of hexes
    for hexTile in hexes[:12]:
        # Loop over the coordinates of the upper 3 vertices
        for index, coord in enumerate(hexTile.vertexCoordinates[:3]):
            # Check that this is a new vertex coordinate
            if coord not in vertexCoordsSeen:
                # Record this vertex position
                vertexCoordsSeen.append(coord)
                # Create a new Vertex object at these coordinates
                newVertex = p.Vertex(coord)
                # Check that the vertex is not the upper-left vertex of the hex
                # If not, record that this vertex is adjacent to the previous vertex
                if index != 0:
                    vertices[-1].adjacentVertices.append(newVertex)
                    newVertex.adjacentVertices.append(vertices[-1])
                # Add the vertex to the list of vertices
                vertices.append(newVertex)
    # Repeat the loop above for the bottom three rows of hexes
    for hexTile in hexes[7:]:
        # Use the lower 3 coordinates here
        for index, coord in enumerate(hexTile.vertexCoordinates[3:][::-1]):
            if coord not in vertexCoordsSeen:
                vertexCoordsSeen.append(coord)
                newVertex = p.Vertex(coord)
                if index != 0:
                    vertices[-1].adjacentVertices.append(newVertex)
                    newVertex.adjacentVertices.append(vertices[-1])
                vertices.append(newVertex)
    # Loop through the vertices and relate them to the hexes they touch
    for vertex in vertices:
        # For each vertex, look at hex
        for hexTile in hexes:
            # Check that the vertex and hex aren't already related but the coordinates match
            if vertex not in hexTile.vertices and vertex.coordinates in hexTile.vertexCoordinates:
                # Record the position of the vertex according to the hex's coordinate list
                verIndex = hexTile.vertexCoordinates.index(vertex.coordinates)
                # Place the vertex into the hex's vertex list at the same position
                hexTile.vertices[verIndex] = vertex
                # Add the hex to the vertex's hex list
                vertex.hexes.append(hexTile)
                # If the vertex has 3 hexes in its hex list, no more hexes need to be examined
                if len(vertex.hexes) == 3:
                    break
    # Loop through the hexes and relate vertices that are vertically adjacent
    for hexTile in hexes:
        if hexTile.vertices[0] not in hexTile.vertices[5].adjacentVertices:
            hexTile.vertices[0].adjacentVertices.append(hexTile.vertices[5])
            hexTile.vertices[5].adjacentVertices.append(hexTile.vertices[0])
        if hexTile.vertices[2] not in hexTile.vertices[3].adjacentVertices:
            hexTile.vertices[2].adjacentVertices.append(hexTile.vertices[3])
            hexTile.vertices[3].adjacentVertices.append(hexTile.vertices[2])

    # A list of the ports on the map
    ports = [p.Port([resource], 2) for resource in c.resourceTypes]
    ports += [p.Port(list(c.resourceTypes), 3) for i in range(4)]
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
    robber = p.Robber(hexes[c.desertIndex])

    # Instantiate the players
    # The game expects 4 players and a name, a color, and an AI status (True or False) for each
    if len(sys.argv) != 13:
        print("Wrong number of arguments (name, color, isAI four times)")
        sys.exit()
    # Check that the colors given are in the player-color dictionary
    for inputColor in sys.argv[2::3]:
        if inputColor not in c.playerColors:
            print("\"{}\" is not a valid color.  The options are: {}".format(
                inputColor, ", ".join(c.playerColors.keys())))
            sys.exit()
    # Default AI status for each player is False - assumes the players are human
    p1AI = False
    p2AI = False
    p3AI = False
    p4AI = False
    # The options that signify the player is an AI
    trueOpts = ["True", "true", "T", "t"]
    # Check if the player is an AI
    if sys.argv[3] in trueOpts:
        p1AI = True
    # Instantiate a player with their name, color, AI status, and the sizes of their pieces
    player1 = p.Player(sys.argv[1], c.playerColors[sys.argv[2]], p1AI)
    if sys.argv[6] in trueOpts:
        p2AI = True
    player2 = p.Player(sys.argv[4], c.playerColors[sys.argv[5]], p2AI)
    if sys.argv[9] in trueOpts:
        p3AI = True
    player3 = p.Player(sys.argv[7], c.playerColors[sys.argv[8]], p3AI)
    if sys.argv[12] in trueOpts:
        p4AI = True
    player4 = p.Player(sys.argv[10], c.playerColors[sys.argv[11]], p4AI)
    # Construct a list of the players
    playerList = [player1, player2, player3, player4]
    # Give the players enough cards to build their first settlements and roads
    # TODO EDITED THIS TO TEST MARITIME TRADING & BUILDING
    startingHand = {c.grain: 4, c.wool: 2, c.clay: 4, c.lumber: 4, c.ore: 3}
    for player in playerList:
        player.draw_cards(startingHand, resourceDecks)
    # Shuffle the players to set the turn order
    random.shuffle(playerList)

    # Set up the award placards
    largestArmy = p.LargestArmy(playerList)
    longestRoad = p.LongestRoad(playerList)

    # Pygame initialization
    pygame.init()
    # opens the window with the size specifications given
    screen = pygame.display.set_mode(c.screenSize)
    # sets the font and size
    comicsansLargeFont = pygame.font.SysFont("comicsansms", 25)
    # set the font and size for the player key
    arialSmallFont = pygame.font.SysFont("Arial", 15)
    pygame.event.set_allowed(None)
    pygame.event.set_allowed([pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN, pygame.QUIT])
    # Create the Player Key
    playerKey = p.PlayerKey(arialSmallFont, playerList)
    boardSurface = screen.subsurface((0, 0), c.oceanSize)
    playerHandSurface = screen.subsurface((c.oceanWidth, 0), (c.gameMenuWidth, 100))
    playerHandSurface.fill(c.white)
    menuSurface = screen.subsurface((c.oceanWidth, 100), (c.gameMenuWidth, c.oceanHeight-100))
    menuSurface.fill(c.white)
    logSurface = screen.subsurface((c.oceanWidth + c.gameMenuWidth + 1, 0), (c.gameEventLogWidth - 1, c.oceanHeight))
    logSurface.fill(c.white)

    # The pygame loop
    # A flag to track if the board has been drawn
    boardDrawn = False
    # A flag to track if the players have built their starting settlements and roads
    initialSettlementsBuilt = False
    # A flag to track if a player has won the game
    gameOver = False
    while 1:
        # Draw the key, hexes, odds tiles, and Robber
        if not boardDrawn:
            # Set the background color
            boardSurface.fill(c.oceanBlue)
            # Draw the player key
            playerKey.draw(boardSurface)
            # Loop through the hexes, so that they can be drawn
            for hexTile in hexes:
                # Draw the hex
                pygame.draw.polygon(boardSurface, hexTile.color, hexTile.vertexCoordinates, 0)
                # Check that the hex is not the desert hex
                if hexTile.resource != c.desert:
                    # Record the hex's odds tile
                    resourceOdds = str(hexTile.odds)
                    # Set the color of the odds number's text based on the value
                    if resourceOdds == "6" or resourceOdds == "8":
                        label = comicsansLargeFont.render(resourceOdds, 1, c.red)
                    else:
                        label = comicsansLargeFont.render(resourceOdds, 1, c.black)
                    # Place the number on the screen
                    boardSurface.blit(label, hexTile.coordinates)
            # Draw the Robber
            robber.draw_robber(boardSurface)
            # Draw the ports, colored according to their resource
            for port in ports:
                portColor = (0, 0, 0)
                if port.resources != c.resourceTypes:
                    portColor = c.resourceToColor[port.resources[0]]
                port.draw_port(boardSurface, portColor)
            # Draw any existing player objects
            for player in playerList:
                if player.builtRoads:
                    for road in player.builtRoads:
                        road.draw_road(boardSurface)
                if player.builtSettlements:
                    for settlement in player.builtSettlements:
                        settlement.draw_settlement(boardSurface)
            # Update the whole screen in order to show the newly drawn board
            pygame.display.flip()
            # Record that the board has been drawn
            boardDrawn = True

        # Set up the initial settlements and roads for each player
        if not initialSettlementsBuilt:
            print("Each player must build their first settlements and roads.")
            # Loop through the shuffled player list forwards once and then backwards once
            # playerList[::-1]:  TODO NEEED TO CHANGE BACK!!!
            for player in playerList:
                # A flag to track whether the player has completed a valid action
                validAction = False
                # Give a line break
                print("")
                while not validAction:
                    print("For the settlement:")
                    buildResult = build_settlement(player, vertices, resourceDecks, boardSurface, playerKey)
                    if buildResult[0] == 0:
                        validAction = True
                        pygame.display.update()
                validAction = False
                # Repeat until the player successfully builds a road
                while not validAction:
                    print("For the road from that settlement:")
                    buildResult = build_road(player, vertices, longestRoad, resourceDecks, boardSurface, playerKey)
                    if buildResult[0] == 0:
                        validAction = True
                        pygame.display.update()
            # Record that the players have built the initial 2 settlements and roads
            initialSettlementsBuilt = True

        if not gameOver:
            # Loop through the players to let each take their game turns
            for player in playerList:
                print("\n{}, it is now your turn.".format(player.name))

                draw_player_hand(player, playerHandSurface, comicsansLargeFont, arialSmallFont)
                pygame.display.update(playerHandSurface.get_rect())

                # Initiate the pre-harvest menu
                actionChoice = present_menu(player, c.preHarvestMenu, "Pre-Harvest", menuSurface, comicsansLargeFont, arialSmallFont)
                result = eval(actionChoice)
                if not isinstance(result, int):
                    result = roll_dice(player)
                diceResult = result

                # Check if the roll was a 7, and have the players discards cards and play the Robber if so
                if diceResult == 7:
                    # Discard cards for players with more than 7
                    for playerToCheck in playerList:
                        if sum(playerToCheck.cardsInHand.values()) > 7:
                            halve_player_hand(playerToCheck, resourceDecks, playerHandSurface, menuSurface,
                                              comicsansLargeFont, arialSmallFont)
                    playChosen = False
                    while not playChosen:
                        # Ask the player how they'd like to play the Robber
                        robberPlay = get_robber_play_from_player(player, robber, hexes, playerKey)
                        if robberPlay[0] == 0:
                            playChosen = True
                    # Attempt to make that play
                    robberResult = robber.play(boardSurface, robberPlay[1], player, robberPlay[2])
                    # Update the screen to show the new location of the Robber
                    pygame.display.update()
                    # Print the result of the player stealing from someone
                    print(robberResult)
                else:
                    # Have the players draw their resource cards
                    for playerDrawing in playerList:
                        for settlement in playerDrawing.builtSettlements:
                            playerDrawing.draw_cards(settlement.find_yield(diceResult), resourceDecks)
                        print("{} has {}".format(playerDrawing.name, playerDrawing.cardsInHand))
                    print("The decks have {}".format(resourceDecks))

                turnOver = False
                while not turnOver:
                    draw_player_hand(player, playerHandSurface, comicsansLargeFont, arialSmallFont)
                    pygame.display.update(playerHandSurface.get_rect())
#                    present_graphical_menu(player, postHarvestMenu, menuSurface, comicsansLargeFont, arialSmallFont)
#                    pygame.display.update(menuSurface.get_rect())
                    actionChoice2 = present_menu(player, c.postHarvestMenu, "Post-Harvest", menuSurface, comicsansLargeFont,
                                                 arialSmallFont)
                    result = eval(actionChoice2)
                    print(result[1])
                    if result[1] == "Turn is over.":
                        turnOver = True
                        if result[2] >= 10:
                            print("\n{} has won the game with {} points!!".format(player.name, result[3]))
                            gameOver = True
                if gameOver:
                    break

            boardSurface.fill(c.black)
            pygame.display.update()
            boardDrawn = False

        # waits ten seconds and then starts the whole process over again
        time.sleep(2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()


def halve_player_hand(player, resourceDecks, handSurface, menuSurface, titleFont, infoFont):
    draw_player_hand(player, handSurface, titleFont, infoFont)
    pygame.display.update(handSurface.get_rect())
    numToDiscard = int(round(sum(player.cardsInHand.values()) / 2, -0))
    while numToDiscard > 0:
        resourcesInHand = sorted([resource for resource in player.cardsInHand.keys()
                                  if player.cardsInHand[resource] > 0])
        resourceMenu = dict(zip(resourcesInHand, resourcesInHand))
        cardToDiscard = present_menu(player, resourceMenu, "Discard {}".format(numToDiscard), menuSurface, titleFont,
                                     infoFont)
        player.discard_cards({cardToDiscard: 1}, resourceDecks)
        draw_player_hand(player, handSurface, titleFont, infoFont)
        pygame.display.update(handSurface.get_rect())
        numToDiscard -= 1
    return (0, "{} successfully discarded cards.".format(player.name))


# A function to take the player's input and build a road
def build_road(player, vertexList, longestRoad, resourceDecks, surface, playerKey):
    successfulBuild = False
    while not successfulBuild:
        print("Pick the first vertex.")
        vertex1 = get_vertex_from_player(player, vertexList, playerKey)
        if vertex1 is None:
            return (1, "No vertex picked. Returning.")
        print("Pick the second vertex.")
        vertex2 = get_vertex_from_player(player, vertex1.adjacentVertices, playerKey)
        if vertex2 is None:
            return (1, "No vertex picked. Returning")
        result = player.build_road(vertex1, vertex2, longestRoad, resourceDecks, surface)
        print(result[1])
        if result[0] == 0:
            successfulBuild = True
    pygame.display.update()
    return (0, "Road built!")


# A function to take the player's input and build a settlement
def build_settlement(player, vertexList, resourceDecks, surface, playerKey):
    successfulBuild = False
    while not successfulBuild:
        print("{}, pick the vertex desired for the settlement.".format(player.name))
        vertexToSettle = get_vertex_from_player(player, vertexList, playerKey)
        if vertexToSettle is None:
            return (1, "No vertex selected. Returning.")
        result = player.build_town(vertexToSettle, resourceDecks, surface)
        print(result[1])
        if result[0] == 0:
            successfulBuild = True
    pygame.display.update()
    return (0, "Settlement built!")


# A function to take the player's input and upgrade a settlement
def upgrade_settlement(player, vertexList, resourceDecks, surface, playerKey):
    successfulUpgrade = False
    while not successfulUpgrade:
        print("{}, pick the town you wish to upgrade.".format(player.name))
        vertexToUpgrade = get_vertex_from_player(player, vertexList, playerKey)
        if vertexToUpgrade is None:
            return(1, "No vertex selected. Returning.")
        result = player.build_city(vertexToUpgrade, resourceDecks, surface)
        print(result[1])
        if result[0] == 0:
            successfulUpgrade = True
    pygame.display.update()
    return (0, "Settlement upgraded!")


# A function to buy a devlopment card for a player
def buy_development_card(player, resourceDecks, developmentDeck):
    buyResult = player.buy_development_card(developmentDeck, resourceDecks)
    return buyResult


# A function to take the player's input and play a monopoly card
def play_monopoly_card(player, playerList, surface, titleFont, infoFont):
    print("{}, which resource do you want to monopolize?".format(player.name))
    resourceMenu = dict(zip(c.resourceTypes, c.resourceTypes))
    resourceMenu["Cancel and return to main menu"] = None
    choice = present_menu(player, dict(zip(c.resourceTypes, c.resourceTypes)), "Take Which?", surface, titleFont, infoFont)
    if choice is None:
        return (2, "{} cancelled the play. Returning.")
    monopolyResult = player.play_monopoly(playerList, choice)
    return monopolyResult


# A function to take the player's input and play a year of plenty card
def play_yop_card(player, resourceDecks, surface, titleFont, infoFont):
    if "Year of Plenty" not in player.developmentCards:
        return (1, "{} does not have a Year of Plenty to play.".format(player.name))
    availableResources = [resource for resource in resourceDecks.keys() if resourceDecks[resource] > 0]
    resourceMenu = dict(zip(availableResources, availableResources))
    resourceMenu["Cancel and return to main menu"] = None
    print("{}, choose the first resource to draw.".format(player.name))
    resource1 = present_menu(player, resourceMenu, "Draw Which?", surface, titleFont, infoFont)
    if resource1 is None:
        return (2, "{} chose to not play a Year of Plenty.".format(player.name))
    player.draw_cards({resource1: 1}, resourceDecks)
    player.developmentCards.remove("Year of Plenty")
    availableResources = [resource for resource in resourceDecks.keys() if resourceDecks[resource] > 0]
    resourceMenu = dict(zip(availableResources, availableResources))
    resourceMenu["Don't draw a 2nd card"] = None
    print("{}, choose the second resource to draw.".format(player.name))
    resource2 = present_menu(player, resourceMenu, "Draw Which?", surface, titleFont, infoFont)
    if resource2 is None:
        return (0, "{} used Year of Plenty to draw {}".format(player.name, resource1))
    player.draw_cards({resource2: 1}, resourceDecks)
    return (0, "{} used Year of Plenty to draw {} and {}".format(player.name, resource1, resource2))


# A function to take the player's input and play a road building card
def play_road_building(player, vertexList, longestRoad, resourceDecks, surface, playerKey):
    if "Road Building" not in player.developmentCards:
        return (1, "{} does not have a Road Building to play.".format(player.name))
    buildResult = build_road(player, vertexList, longestRoad, resourceDecks, surface, playerKey)
    if buildResult[0] == 1:
        return (2, "{} chose not to use Road Building.".format(player.name))
    player.draw_cards(c.roadCost, resourceDecks)
    player.developmentCards.remove("Road Building")
    buildResult = build_road(player, vertextList, longestRoad, resourceDecks, surface, playerKey)
    if buildResult[0] == 1:
        return (0, "{} built 1 road with Road Building.".format(player.name))
    player.draw_cards(c.roadCost, resourceDecks)
    return (0, "{} built 2 roads with Road Building.".format(player.name))


# A function to take the player's input and make a maritime trade
def maritime_trade(player, maritimeTradeMenu, resourceDecks):
    print("Please select the resource you would like to maritime trade: ")
    resourceTrading = present_menu(player, maritimeTradeMenu)

    validOptionFound = False
    while not validOptionFound:
        quantCardsTrading = input("How many {} resource cards would you like to trade in? ".format(resourceTrading[1]))
        try:
            quantCardsTrading = int(quantCardsTrading)
        except:
            print("not an integer.  try again")
            continue
        action = quantCardsTrading
        validOptionFound = True

    print("Please select the resource type you would like to receive: ")
    resourceReceiving = present_menu(player, maritimeTradeMenu)

    validOptionFound = False
    while not validOptionFound:
        quantCardsReceiving = input("How many {} resource cards would you like to receive? ".format(
            resourceReceiving[1]))
        try:
            quantCardsReceiving = int(quantCardsReceiving)
        except:
            print("not an integer.  try again")
            continue
        validOptionFound = True

    result = player.make_maritime_trade(resourceTrading[0], quantCardsTrading, resourceReceiving[0],
                                        quantCardsReceiving, resourceDecks)

    return (0, "Cards successfully maritime traded!")


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


# A function to get the new hex for the Robber and the player from whom the player wants to steal
# Takes the player moving the Robber, the Robber, and the list of hexes
def get_robber_play_from_player(player, robber, hexes, playerKey, surface, titleFont, infoFont):
    # Check if the player is an AI or human
    if player.isAI:
        pass
    else:
        # Get the current hex of the Robber to use as a metric to know when the player has successfully picked a new hex
        destinationHex = robber.currentHex
        while destinationHex == robber.currentHex:
            print("Choose a new hex for the Robber.")
            # Ask the player to which hex they want to move the Robber
            destinationHex = get_hex_from_player(player, hexes, playerKey)
        if destinationHex is None:
            return (1, "No hex selected. Returning.")
        # A list to hold the players from whom the player can steal
        playersAvailableToRob = []
        # Loop through the vertices that surround the Robber's new hex
        for vertex in destinationHex.vertices:
            # Check whether each vertex has a settlement built on it
            if vertex.settlement is not None:
                # If so, check that the owner of that settlement is not the player
                if vertex.settlement.owner != player and vertex.settlement.owner not in playersAvailableToRob:
                    # If that's the case, the owner of that vertex is a player from whom the player can steal
                    playersAvailableToRob.append(vertex.settlement.owner)
        # The default value for the player from whom the player will steal
        playerToRob = None
        # If the player has multiple players from whom they can steal, ask them to choose their target
        if len(playersAvailableToRob) > 0:
            print("Choose the player from whom you wish to steal.")
            playerToRob = get_player_from_player(player, playersAvailableToRob, surface, titleFont, infoFont)
        # Return the hex to which the Robber will be moved and the player who will be robbed
        return (0, destinationHex, playerToRob)


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
def get_player_from_player(player, listOfPlayers, surface, titleFont, infoFont):
    # Check if the player is an AI or human
    if player.isAI:
        pass
    else:
        # Create a list of names
        playerNames = []
        for plyr in listOfPlayers:
            if plyr is not None:
                playerNames.append(plyr.name)
            else:
                playerNames.append("Nobody")
        # Make a dictionary of the player names the player objects
        playerMenu = dict(zip(playerNames, listOfPlayers))
        # Get the choice
        print("Please choose a player.")
        chosenPlayer = present_menu(player, playerMenu, "Steal from:", surface, titleFont, infoFont)
        # Return the player object corresponding to the name entered by the player
        return chosenPlayer


# A function to get a hex chosen by the player
# Takes the player choosing and the list of board hexes
def get_hex_from_player(player, hexList, playerKey):
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
            print("{} please click a hex. Or click the Player Key to select nothing.".format(player.name))
            chosenHex = None
            eventA = pygame.event.wait()
            eventB = pygame.event.wait()
            # If the next two events are the mouse being pressed down and then released, move forward
            if eventA.type == pygame.MOUSEBUTTONDOWN and eventB.type == pygame.MOUSEBUTTONUP:
                posA = eventA.__dict__['pos']
                posB = eventB.__dict__['pos']
                # If the mouse actions (pressed down, released) were no more than 10 pixels apart, move forward
                if gf.pp_distance(posA, posB) < 10:
                    # If the click was inside the Player Key, return to the previous menu without a selection
                    if gf.is_within_rect(playerKey.box, posA) and gf.is_within_rect(playerKey.box, posB):
                        chosenHex = None
                        validClick = True
                        print("{} did not choose a hex.".format(player.name))
                    else:
                        # Loop through the hexes to see if the click ocurred inside one
                        for hexTile in hexList:
                            # If both mouse actions ocurred inside the current hex, move forward
                            if gf.is_within_hex(hexTile, posA) and gf.is_within_hex(hexTile, posB):
                                # Record the hex, switch the boolean to end the while loop, and break the hex loop
                                chosenHex = hexTile
                                validClick = True
                                break
                        if not validClick:
                            print("That click was not inside a hex. Please try again.")
                else:
                    print("The mouse moved while pressed down. Please try again.")
        return chosenHex


# A function to get a vertex chosen by the player
# Takes the player choosing and the list of vertices
def get_vertex_from_player(player, vertexList, playerKey):
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
            print("{} please click a vertex. Or click the Player Key to select nothing.".format(player.name))
            eventA = pygame.event.wait()
            eventB = pygame.event.wait()
            # If the next two events are the mouse being pressed down and then released, move forward
            if eventA.type == pygame.MOUSEBUTTONDOWN and eventB.type == pygame.MOUSEBUTTONUP:
                # Get the coordinates of the clicks
                posA = eventA.__dict__['pos']
                posB = eventB.__dict__['pos']
                # Get the coordinates of each vertex on the board
                vertexCoords = [v.coordinates for v in vertexList]
                # Get coordinates of the vetices closest to where the mouse was pressed down and where it was released
                verCoordA = gf.get_closest_point(vertexCoords, posA)
                verCoordB = gf.get_closest_point(vertexCoords, posB)
                # If the two coordinates are the same and both events happened within 10 pixels each other, move forward
                if verCoordA[0] == verCoordB[0] and abs(verCoordA[1] - verCoordB[1]) < 10:
                    # If the click was inside the Player Key, return to the previous menu without a selection
                    if gf.is_within_rect(playerKey.box, posA) and gf.is_within_rect(playerKey.box, posB):
                        closestVertex = None
                        validClick = True
                        print("{} did not choose a vertex.".format(player.name))
                    else:
                        # If the mouse action (pressed down, released) happened within 10 pixels of
                        # the closest vertex, move forward
                        if verCoordA[1] <= 10 and verCoordB[1] <= 10:
                            # With all condiitions satisfied, find the vertex corresponding to the coordinates found
                            closestVertex = vertexList[vertexCoords.index(verCoordA[0])]
                            validClick = True
                        else:
                            print("That click was not close enough to a vertex. Please try again.")
                else:
                    print("The mouse moved while pressed down. Please try again.")
        return closestVertex


def present_menu(player, menuDict, titleContent, surface, titleFont, infoFont):
    if player.isAI:
        pass
    else:
        chosenOpt = present_graphical_menu(player, menuDict, titleContent, surface, titleFont, infoFont)
        choice = menuDict[chosenOpt]
        surface.fill(c.white)
        pygame.display.update(surface.get_rect())
        '''
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
            choice = menuDict[optKey]
            validOptionFound = True
        '''
        return choice


def present_graphical_menu(player, menuDict, titleContent, surface, titleFont, infoFont):
    surface.fill(c.white)
    pygame.display.update(surface.get_rect())
    surfaceWidth = surface.get_width()
    titleLabel = titleFont.render(titleContent, 1, c.black)
    surface.blit(titleLabel, (25, 7))
    menuOpts = sorted(list(menuDict.keys()))
    menuOptSurfaces = [surface.subsurface(pygame.Rect((0, 47 + i*25), (surfaceWidth, 25)))
                       for i in range(len(menuOpts))]
    for i, optSurface in enumerate(menuOptSurfaces):
        optLabel = infoFont.render(menuOpts[i], 1, c.black)
        optSurface.blit(optLabel, (10, 2))
    pygame.display.update(surface.get_rect())
    rectList = [pygame.Rect(oS.get_abs_offset(), (oS.get_rect().width, oS.get_rect().height)) for oS in menuOptSurfaces]
    chosenRect = get_rect_from_player(player, rectList)
    chosenOpt = menuOpts[rectList.index(chosenRect)]
    return chosenOpt


def get_rect_from_player(player, rectList):
    # Loop until the user clicks on a vertex
    validClick = False
    while not validClick:
        # Make sure no other events are on the queue
        pygame.event.clear()
        # Prompt the user for a click and wait for two events
        print("{} please click a option.".format(player.name))
        chosenRect = None
        eventA = pygame.event.wait()
        eventB = pygame.event.wait()
        # If the next two events are the mouse being pressed down and then released, move forward
        if eventA.type == pygame.MOUSEBUTTONDOWN and eventB.type == pygame.MOUSEBUTTONUP:
            posA = eventA.__dict__['pos']
            posB = eventB.__dict__['pos']
            # If the mouse actions (pressed down, released) were no more than 10 pixels apart, move forward
            if gf.pp_distance(posA, posB) < 10:
                # Loop through the rects to see if the click ocurred inside one
                for rect in rectList:
                    # If both mouse actions ocurred inside the current hex, move forward
                    if gf.is_within_rect(rect, posA) and gf.is_within_rect(rect, posB):
                        # Record the rect, switch the boolean to end the while loop, and break the rect loop
                        chosenRect = rect
                        validClick = True
                        break
                if not validClick:
                    print("That click was not inside a rect. Please try again.")
            else:
                print("The mouse moved while pressed down. Please try again.")
    return chosenRect


# Function that simply rolls the dice and returns the result
def roll_dice(player):
    # Roll the dice and print the result
    diceResult = random.randint(1, 6) + random.randint(1, 6)

    print("Rolling Dice now...")
    print("{} rolled a(n) {}.\n".format(player.name, diceResult))

    return diceResult


# Function that deals with the choice to play the knight first
# Takes the player in question
def play_knight(player, robber, hexes, largestArmy, surface, playerKey):
    player.developmentCards.append("Knight")
    # Ask the player how they'd like to use the Robber
    robberPlay = get_robber_play_from_player(player, robber, hexes, playerKey)
    if robberPlay[0] == 1:
        return (1, "{} chose not to play the Knight.".format(player.name))
    # Attempt to make that play
    knightResult = player.play_knight(robber, robberPlay[1], robberPlay[2], largestArmy, surface)
    pygame.display.update()
    print(knightResult[1])
    print()
    return knightResult


def draw_player_hand(player, surface, titleFont, infoFont):
    surface.fill(c.white)
    titleColorBox = pygame.Rect((25, 12), (25, 25))
    titleLabel = titleFont.render("'s Hand", 1, c.black)
    pygame.draw.rect(surface, player.color, titleColorBox)
    surface.blit(titleLabel, (50, 7))
    boxEdgeLength = 15
    for i, resource in enumerate(c.resourceTypes):
        x = ((i % 3) * 55) + 20
        if i < 3:
            y = 47
        else:
            y = 72
        box = pygame.Rect((x, y), (boxEdgeLength, boxEdgeLength))
        pygame.draw.rect(surface, c.resourceToColor[resource], box)
        label = infoFont.render(" - {}".format(player.cardsInHand[resource]), 1, c.black)
        surface.blit(label, (x+16, y))


if __name__ == "__main__":
    main()

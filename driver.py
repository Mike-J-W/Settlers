import random
import pygame
import time
import sys
import os
import collections
import constants as c
import pieces as p
import userinput as ui


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
    playerHandSurface = screen.subsurface((c.oceanWidth, 0), (c.gameMenuWidth, 225))
    playerHandSurface.fill(c.white)
    menuSurface = screen.subsurface((c.oceanWidth, 226), (c.gameMenuWidth, c.oceanHeight-226))
    menuSurface.fill(c.white)
    enemyInfoSurface = screen.subsurface((c.oceanWidth + c.gameMenuWidth + 1, 0), (c.gameEventLogWidth -1, 225))
    enemyInfoSurface.fill(c.white)
    logSurface = screen.subsurface((c.oceanWidth + c.gameMenuWidth + 1, 226), (c.gameEventLogWidth - 1,
                                                                               c.oceanHeight - 226))
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
                actionChoice = ui.present_menu(player, c.preHarvestMenu, "Pre-Harvest", menuSurface, comicsansLargeFont,
                                            arialSmallFont)
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
                    playMade = False
                    while not playMade:
                        # Have the player make a play with the Robber
                        robberPlay = use_robber(player, robber, hexes, boardSurface, playerKey, menuSurface,
                                                                 comicsansLargeFont, arialSmallFont)
                        if robberPlay[0] == 0:
                            playMade = True
                    # Update the screen to show the new location of the Robber
                    pygame.display.update()
                    # Print the result of the player stealing from someone
                    print(robberPlay[1])
                else:
                    # Have the players draw their resource cards
                    for playerDrawing in playerList:
                        for settlement in playerDrawing.builtSettlements:
                            playerDrawing.draw_cards(settlement.find_yield(diceResult), resourceDecks)
                        print("{} has {}".format(playerDrawing.name, playerDrawing.cardsInHand))
                    print("The decks have {}".format(resourceDecks))

                turnOver = False
                while not turnOver:
                    draw_enemy_info(player, playerList, enemyInfoSurface, arialSmallFont)
                    pygame.display.update(enemyInfoSurface.get_rect())
                    draw_player_hand(player, playerHandSurface, comicsansLargeFont, arialSmallFont)
                    pygame.display.update(playerHandSurface.get_rect())
#                    present_graphical_menu(player, postHarvestMenu, menuSurface, comicsansLargeFont, arialSmallFont)
#                    pygame.display.update(menuSurface.get_rect())
                    actionChoice2 = ui.present_menu(player, c.postHarvestMenu, "Post-Harvest", menuSurface,
                                                 comicsansLargeFont, arialSmallFont)
                    result = eval(actionChoice2)
                    print(result[1])
                    if result[1] == "Turn is over.":
                        turnOver = True
                        if result[2] >= 10:
                            print("\n{} has won the game with {} points!!".format(player.name, result[3]))
                            gameOver = True
                if gameOver:
                    break

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
        cardToDiscard = ui.present_menu(player, resourceMenu, "Discard {}".format(numToDiscard), menuSurface, titleFont,
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
        vertex1 = ui.get_vertex_from_player(player, vertexList, playerKey)
        if vertex1 is None:
            return (1, "No vertex picked. Returning.")
        print("Pick the second vertex.")
        vertex2 = ui.get_vertex_from_player(player, vertex1.adjacentVertices, playerKey)
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
        vertexToSettle = ui.get_vertex_from_player(player, vertexList, playerKey)
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
        vertexToUpgrade = ui.get_vertex_from_player(player, vertexList, playerKey)
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
    choice = ui.present_menu(player, dict(zip(c.resourceTypes, c.resourceTypes)), "Take Which?", surface, titleFont,
                          infoFont)
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
    resource1 = ui.present_menu(player, resourceMenu, "Draw Which?", surface, titleFont, infoFont)
    if resource1 is None:
        return (2, "{} chose to not play a Year of Plenty.".format(player.name))
    player.draw_cards({resource1: 1}, resourceDecks)
    player.developmentCards.remove("Year of Plenty")
    availableResources = [resource for resource in resourceDecks.keys() if resourceDecks[resource] > 0]
    resourceMenu = dict(zip(availableResources, availableResources))
    resourceMenu["Don't draw a 2nd card"] = None
    print("{}, choose the second resource to draw.".format(player.name))
    resource2 = ui.present_menu(player, resourceMenu, "Draw Which?", surface, titleFont, infoFont)
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
    buildResult = build_road(player, vertexList, longestRoad, resourceDecks, surface, playerKey)
    if buildResult[0] == 1:
        return (0, "{} built 1 road with Road Building.".format(player.name))
    player.draw_cards(c.roadCost, resourceDecks)
    return (0, "{} built 2 roads with Road Building.".format(player.name))


# A function to take the player's input and make a maritime trade
def maritime_trade(player, resourceDecks, surface, titleFont, infoFont):
    tradeAwayMenu = {"Cancel and return to main menu": None}
    for resource in c.resourceTypes:
        ratio = player.tradeRatios[resource]
        if player.cardsInHand[resource] >= ratio:
            tradeAwayMenu["{} at {} to 1".format(resource, ratio)] = resource

    print("Please select the resource you would like to maritime trade: ")
    resourceTrading = ui.present_menu(player, tradeAwayMenu, "Trade Away", surface, titleFont, infoFont)
    if resourceTrading is None:
        return (1, "{} chose not to trade.".format(player.name))
    tradeRatio = player.tradeRatios[resourceTrading]
    tradeForMenu = {"Cancel and return to main menu": None}
    for resource in c.resourceTypes:
        if resource is not resourceTrading and resourceDecks[resource] > 0:
            tradeForMenu[resource] = resource
    resourceGetting = ui.present_menu(player, tradeForMenu, "Trade For", surface, titleFont, infoFont)
    if resourceGetting is None:
        return (1, "{} chose not to trade.".format(player.name))
    tradeAmountMenu = {"Cancel and return to main menu": None}
    counter = 1
    while counter * tradeRatio <= player.cardsInHand[resourceTrading] and counter <= resourceDecks[resourceGetting]:
        tradeAmountMenu["{} {} for {} {}".format(counter * tradeRatio, resourceTrading, counter, resourceGetting)] = \
            counter
        counter += 1
    tradeQuantity = ui.present_menu(player, tradeAmountMenu, "Trade", surface, titleFont, infoFont)
    if tradeQuantity is None:
        return (1, "{} chose not to trade.".format(player.name))
    player.discard_cards({resourceTrading: tradeQuantity * tradeRatio}, resourceDecks)
    player.draw_cards({resourceGetting: tradeQuantity}, resourceDecks)
    return (0, "{} traded {} {} for {} {}".format(player.name, tradeQuantity * tradeRatio, resourceTrading,
                                                  tradeQuantity, resourceGetting))


# A function to take th player's input and offer a trade to other players
def offer_trade():
    pass


# A function to complete end-of-turn checks and move to the next player
def end_turn(player):
    # Count the player's points
    pointTotal = player.count_points()
    # Clear the screen
    os.system('cls' if os.name == 'nt' else 'clear')
    return (0, "Turn is over.", pointTotal)


# A function to get the new hex for the Robber and the player from whom the player wants to steal
# Takes the player moving the Robber, the Robber, and the list of hexes
def use_robber(player, robber, hexes, boardSurface, playerKey, menuSurface, titleFont, infoFont):
    # Get the current hex of the Robber to use as a metric to know when the player has successfully picked a new hex
    destinationHex = robber.currentHex
    print("Choose a new hex for the Robber.")
    # Ask the player to which hex they want to move the Robber
    destinationHex = ui.get_hex_from_player(player, hexes, playerKey)
    if destinationHex is None:
        return (1, "{} did not choose a hex.".format(player.name))
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
        playerMenu = {"Cancel and return to main menu": None}
        for plyr in playersAvailableToRob:
            playerMenu["{} ({} cards)".format(plyr.name, sum(plyr.cardsInHand.values()))] = plyr
        playerToRob = ui.present_menu(player, playerMenu, "Steal from", menuSurface, titleFont, infoFont)
    if playerToRob is None:
        return (2, "{} did not choose a player.".format(player.name))
    robberResult = robber.play(boardSurface, destinationHex, player, playerToRob)
    return (0, robberResult)


# Function that simply rolls the dice and returns the result
def roll_dice(player):
    # Roll the dice and print the result
    diceResult = random.randint(1, 6) + random.randint(1, 6)

    print("Rolling Dice now...")
    print("{} rolled a(n) {}.\n".format(player.name, diceResult))

    return diceResult


# Function that deals with the choice to play the knight first
# Takes the player in question
def play_knight(player, robber, hexes, largestArmy, boardSurface, playerKey, menuSurface, titleFont, infoFont):
    if "Knight" not in player.developmentCards:
        return (1, "{} does not have a Knight to play.".format(player.name))
    # Ask the player how they'd like to use the Robber
    robberPlay = use_robber(player, robber, hexes, boardSurface, playerKey, menuSurface, titleFont, infoFont)
    if robberPlay[0] != 0:
        return (2, "{} chose not to play the Knight.".format(player.name))
    # Attempt to make that play
    knightResult = player.play_knight(largestArmy)
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
    for i, card in enumerate(["Road Building", "Year of Plenty", "Victory Point"]):
        cardLabel = infoFont.render("{}: {}".format(card, player.developmentCards.count(card)), 1, c.black)
        surface.blit(cardLabel, (15,100 + 20 * i))
    for i, card in enumerate(["Monopoly", "Knight"]):
        cardLabel = infoFont.render("{}: {}".format(card, player.developmentCards.count(card)), 1, c.black)
        surface.blit(cardLabel, (135,100 + 20 * i))
    armyLabel = infoFont.render("Army: {}".format(player.armySize), 1, c.black)
    surface.blit(armyLabel, (135, 140))
    largestArmyLabel = infoFont.render("Largest Army: {}".format(player.hasLargestArmy), 1, c.black)
    surface.blit(largestArmyLabel, (15, 160))
    longestRaodLabel = infoFont.render("Longest Road: {}".format(player.hasLongestRoad), 1, c.black)
    surface.blit(longestRaodLabel, (15, 180))
    pointsLabel = infoFont.render("Total Points: {}".format(player.points), 1, c.black)
    surface.blit(pointsLabel, (15, 200))


def draw_enemy_info(player, playerList, surface, infoFont):
    surface.fill(c.white)
    enemyList = [person for person in playerList if person is not player]
    for i, enemy in enumerate(enemyList):
        colorBox = pygame.Rect((15, 15 + i * 72), (15, 15))
        pygame.draw.rect(surface, enemy.color, colorBox)
        resourceLabel = infoFont.render("Resources: {}".format(sum(enemy.cardsInHand.values())), 1, c.black)
        surface.blit(resourceLabel, (40, 15 + i * 72))
        armyLabel = infoFont.render("Army: {}".format(enemy.armySize), 1, c.black)
        surface.blit(armyLabel, (140, 15 + i * 72))
        laLabel = infoFont.render("LA: {}".format(enemy.hasLargestArmy), 1, c.black)
        surface.blit(laLabel, (15, 35 + i * 72))
        lrLabel = infoFont.render("LR: {}".format(enemy.hasLongestRoad), 1, c.black)
        surface.blit(lrLabel, (100, 35 + i * 72))
        cardsLabel = infoFont.render("Development Cards: {}".format(len(enemy.developmentCards)), 1, c.black)
        surface.blit(cardsLabel, (15, 55 + i * 72))


def append_public_log(message, playerList, publicLog):
    publicLog.append(message)
    for player in playerList:
        player.log.append(message)


if __name__ == "__main__":
    main()

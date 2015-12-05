from pieces import *
import random
import pygame
import math
import time
import sys


def main():
    # Initialize all the game pieces
    
    ## initalizes pygame
    pygame.init()
    ## sets the size of the window that is opened
    size = width, height = 900, 750
    oceanBlue = 0, 0, 120
    ## opens the window with the size specifications given
    screen = pygame.display.set_mode(size)
    ## sets the background color
    screen.fill(oceanBlue)
    ## sets the font and size
    myfont = pygame.font.SysFont("comicsansms", 25)
    ## defines certain colors
    forestGreen = 34, 139, 34
    oceanBlue = 0, 0, 120
    wheatYellow = 244, 233, 19
    woolGreen = 144, 238, 144
    clayColor = 173, 77, 8
    rockGray = 128, 128, 128
    sandyDesert = 211, 208, 143
    black = 0,0,0
    red = 255, 0,242
    playerRed = 213, 5, 46
    playerBlue = 102, 207, 245
    playerGreen = 90, 206, 48
    playerPurple = 149, 58, 172
    playerWhite = 255, 255, 255
    playerOrange = 255, 182, 71
    playerColors = {"red": playerRed, "blue": playerBlue, "green": playerGreen, "purple": playerPurple, "white": playerWhite, "orange": playerOrange}
    # The length of a side of a hex  PYGAME variable
    hexEdgeLength = 60
    # The width of a town
    settlementEdgeLength = int(round(hexEdgeLength / 4))
    # The width of a road
    roadWidth = int(round(settlementEdgeLength / 3))
    # The resource variables
    lumber = "Wood"
    grain = "Wheat"
    wool = "Wool"
    clay = "Clay"
    ore = "Ore"
    desert = "Desert"
    # A list of the resources in the game
    resourceTypes = [lumber, grain, wool, clay, ore]
    # A dictionary relating resouces to colors
    resourceToColor = {lumber: forestGreen, grain: wheatYellow, wool: woolGreen, clay: clayColor, ore: rockGray, desert: sandyDesert}
    # A list with one element per development card
    developmentDeck = Card_Deck(["Knight"] * 14 + ["Monopoly", "Year of Plenty", "Road Building"] * 2 + ["Victory Point"] * 5)
    # A dictionary to hold the decks of resources, keyed to their resource name
    resourceDecks = {}
    # Generate each resource deck and add it to the dictionary
    for resource in resourceTypes:
        resourceDecks[resource] = [resource] * 19
    
    # A list representing the number of hexes per resource
    resourcesForHexes = [lumber] * 4 + [grain] * 4 + [wool] * 4 + [clay] * 3 + [ore] * 3
    # Shuffle the list of resources so that they are accessed in random order when assigned to hexes
    random.shuffle(resourcesForHexes)
    # A list of the numbered, circular tiles denoting times of harvest
    odds = [6,6,8,8,2,3,3,4,4,5,5,9,9,10,10,11,11,12]
    # A list of the indices of the odds tiles
    indices = [i for i in range(19)]
    # A list of hexes adjacent to the hex represented by the index of the larger list (e.g. hex 0 is adjacent to hexes [1,3,4])
    adjacents = [[1,3,4],[0,2,4,5],[1,5,6],[0,4,7,8],[0,1,3,5,8,9],[1,2,4,6,9,10],[2,5,10,11],[3,8,12],[3,4,7,9,12,13],[4,5,8,10,13,14],[5,6,9,11,14,15],[6,10,15],[7,8,13,16],[8,9,12,14,16,17],[9,10,13,15,17,18],[10,11,14,18],[12,13,17],[13,14,16,18],[14,15,17]]
    # A list to hold the odds tiles placed in random order
    oddsOrdered = [0] * 19
    # Loop through the odds to place each in oddsOrdered
    for o in odds:
        # A flag to determine if a place was found for the odd
        oddPlaced = False
        # Keep trying to place the odd until successful
        while not oddPlaced:
            # Pick an index from those still available
            newIndex = random.choice(indices)
            # Start by assuming the index is valid
            goodIndex = True
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
    
    # The distance from the center of a hex to the middle of an edge
    radius = int(round(hexEdgeLength * math.sqrt(3) / 2.0))
    # The unadjusted coordinates of the centers of the hexes
    baseHexCenters = [(3,1),(5,1),(7,1),(2,2.5),(4,2.5),(6,2.5),(8,2.5),(1,4),(3,4),(5,4),(7,4),(9,4),(2,5.5),(4,5.5),(6,5.5),(8,5.5),(3,7),(5,7),(7,7)]
    # The centers of the hexes adjusted for the length of their sides
    hexCenters = [(2 * hexEdgeLength + baseHexCenters[i][0] * radius, (baseHexCenters[i][1] + 2) * hexEdgeLength) for i in range(len(baseHexCenters))]
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
        for hex in hexes:
            if vertex not in hex.vertices and vertex.coordinates in hex.vertexCoordinates:
                verIndex = hex.vertexCoordinates.index(vertex.coordinates)
                hex.vertices[verIndex] = vertex
                vertex.hexes.append(hex)
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
    robber = Robber(hexes[desertIndex])

    # Instaniate the players
    if len(sys.argv) != 13:
        print("Wrong number of arguments (name, color, isAI four times)")
        sys.exit()
    p1AI = False
    p2AI = False
    p3AI = False
    p4AI = False
    trueOpts = ["True", "true", "T", "t"]
    if sys.argv[3] in trueOpts:
        p1AI = True
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
    playerList = [player1, player2, player3, player4]
    # Give the players enough cards to build their first settlements and roads
    startingHand = [grain, wool] * 2 + [clay, lumber] * 4
    for player in playerList:
        player.draw_cards(startingHand)
    # Shuffle the players to set the turn order
    random.shuffle(playerList)
    # Set up award placards
    largestArmy = Largest_Army(playerList)
    longestRoad = Longest_Road(playerList)


    # The pygame loop
    boardBuilt = False
    initialSettlementsBuilt = False
    while 1:
        if not boardBuilt:
            # Loop through the hexes, so that they can be drawn
            for hex in hexes:
                pygame.draw.polygon(screen, hex.color, hex.vertexCoordinates, 0)
                if hex.resource != desert:
                    resourceOdds = str(hex.odds)
                    if resourceOdds == "6" or resourceOdds == "8":
                        label = myfont.render(resourceOdds, 1, red)
                    else:
                        label = myfont.render(resourceOdds, 1, black)
                    screen.blit(label, (hex.coordinates))
        
            pygame.display.flip()
            boardBuilt = True

        if not initialSettlementsBuilt:
            # Set up the initial settlements and roads for each player
            print("Each player must build their first settlements and roads.")
            for player in playerList + playerList[::-1]:
                validInput = False
                print("")
                while not validInput:
                    print("For the settlement, ")
                    settlementVertex = get_vertex_from_player(player, vertices)
                    buildResult = player.build_town(settlementVertex, screen)
                    if buildResult[0] != 0:
                        print(buildResult[1] + "  Please try again")
                    else:
                        validInput = True
                        pygame.display.update()
                validInput = False
                while not validInput:
                    print("For the heading of the road from that settlement, ")
                    roadDestinationVertex = get_vertex_from_player(player, vertices)
                    buildResult = player.build_road(settlementVertex, roadDestinationVertex, longestRoad, screen)
                    if buildResult[0] != 0:
                        print(buildResult[1] + "  Please try again")
                    else:
                        validInput = True
                        pygame.display.update()
            initialSettlementsBuilt = True
        
        for player in playerList:
            # play knight before roll if desired
            playKnightFirst = get_knight_choice_from_player(player)
            if playKnightFirst:
                knightResult = get_knight_play_from_player(player, robber, newHex, playerToRob, largestArmy)
            # roll dice
            if choice == "r":
                diceResult = roll_dice()

            # build and/or trade and/or play Dev Card

        # waits ten seconds and then starts the whole process over again
        time.sleep(1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()



def get_knight_play_from_player(player, robber, newHex, playerToRob, largestArmy):
    if player.isAI:
        pass
    else:
        s

def roll_dice():
    die1 = random.randint(1,6)
    die2 = random.randint(1,6)
    return die1 + die2

def get_knight_choice_from_player(player):
    if player.isAI:
        pass
    else:
        choice = input("%s enter k to play a Knight before the roll or enter r to roll now: " % player.name)
        if choice != "r" and choice != "k":
            choice = get_knight_choice_from_player(player)
        if choice == "r":
            return False
        else:
            return True

def get_vertex_from_player(player, vertexList):
    if player.isAI:
       pass
    else:
        vertexIndex = input("%s please give a vertex index: " % player.name)
        try:
            vertex = vertexList[int(vertexIndex)]
        except IndexError:
            print("That vertex is out of the range of valid vertices")
            vertex = get_vertex_from_player(player, vertexList)
        except ValueError:
            print("That entry was not an integer.")
            vertex = get_vertex_from_player(player, vertexList)
        return vertex


if __name__ == "__main__":
    main()

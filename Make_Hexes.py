from pieces import *
import random
import pygame
import math
import time
import sys


def main():
    # Initialize all the game pieces

    # initalizes pygame
    pygame.init()
    # sets the size of the window that is opened
    size = width, height = 900, 750
    oceanBlue = 0, 0, 120
    # opens the window with the size specifications given
    screen = pygame.display.set_mode(size)
    # sets the background color
    screen.fill(oceanBlue)
    # sets the font and size
    myfont = pygame.font.SysFont("comicsansms", 25)
    # defines certain colors
    forestGreen = (34, 139, 34)
    oceanBlue = (0, 0, 120)
    wheatYellow = (244, 233, 19)
    woolGreen = (144, 238, 144)
    clayColor = (173, 77, 8)
    rockGray = (128, 128, 128)
    sandyDesert = (211, 208, 143)
    black = (0, 0, 0)
    red = (255, 0, 242)

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
    resourceToColor = {lumber: forestGreen, grain: wheatYellow, wool: woolGreen, clay: clayColor,
                       ore: rockGray, desert: sandyDesert}
    # A list with one element per development card
    developmentDeck = Card_Deck(["Knight"] * 14 + ["Monopoly", "Year of Plenty", "Road Building"] * 2 +
                                ["Victory Point"] * 5)
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
    odds = [6, 6, 8, 8, 2, 3, 3, 4, 4, 5, 5, 9, 9, 10, 10, 11, 11, 12]
    # A list of the indices of the odds tiles
    indices = [i for i in range(19)]
    # A list of hexes next to the hex represented by the index of the larger list (hex 0 is adjacent to hexes [1,3,4])
    adjacents = [[1, 3, 4], [0, 2, 4, 5], [1, 5, 6], [0, 4, 7, 8], [0, 1, 3, 5, 8, 9], [1, 2, 4, 6, 9, 10],
                 [2, 5, 10, 11], [3, 8, 12], [3, 4, 7, 9, 12, 13], [4, 5, 8, 10, 13, 14], [5, 6, 9, 11, 14, 15],
                 [6, 10, 15], [7, 8, 13, 16], [8, 9, 12, 14, 16, 17], [9, 10, 13, 15, 17, 18], [10, 11, 14, 18],
                 [12, 13, 17], [13, 14, 16, 18], [14, 15, 17]]
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
            # If the index is valid, assign the odd to that index in the ordered odds list and remove the
            # index from the list as seen by later iterations of the loop
            if goodIndex:
                oddsOrdered[newIndex] = o
                indices.remove(newIndex)
                oddPlaced = True
    # Get the index of the 0-odd tile and insert "Desert" at that index in the resources list
    desertIndex = oddsOrdered.index(0)
    resourcesForHexes.insert(desertIndex, "Desert")
    # A list of the hexes, assigned a resource and a numbered tile using the lists above
    hexes = [Hex(resourcesForHexes[x], oddsOrdered[x], resourceToColor[resourcesForHexes[x]]) for x in range(19)]

    # The length of a side of a hex  PYGAME variable
    edgeLength = 60
    # The distance from the center of a hex to the middle of an edge
    radius = int(round(edgeLength * math.sqrt(3) / 2.0))
    # The unadjusted coordinates of the centers of the hexes
    baseHexCenters = [(3, 1), (5, 1), (7, 1), (2, 2.5), (4, 2.5), (6, 2.5), (8, 2.5), (1, 4), (3, 4), (5, 4), (7, 4),
                      (9, 4), (2, 5.5), (4, 5.5), (6, 5.5), (8, 5.5), (3, 7), (5, 7), (7, 7)]
    # The centers of the hexes adjusted for the length of their sides
    hexCenters = [(2 * edgeLength + baseHexCenters[i][0] * radius, (baseHexCenters[i][1] + 2) * edgeLength)
                  for i in range(len(baseHexCenters))]
    # "Place" the hexes by assigned the coordinates to the objects and generate list of the coordinates of
    # the vertices using the hex coordinates
    vertexCoords = []
    for index, coord in enumerate(hexCenters):
        hexes[index].coordinates = coord
    for coord in hexCenters[:12]:
        leftVertexCoord = (coord[0] - radius, coord[1] - int(round(edgeLength / 2.0)))
        if leftVertexCoord not in vertexCoords:
            vertexCoords.append(leftVertexCoord)
        vertexCoords.append((coord[0], coord[1] - edgeLength))
        vertexCoords.append((coord[0] + radius, coord[1] - int(round(edgeLength / 2.0))))
    for coord in hexCenters[7:]:
        leftVertexCoord = (coord[0] - radius, coord[1] + int(round(edgeLength / 2.0)))
        if leftVertexCoord not in vertexCoords:
            vertexCoords.append(leftVertexCoord)
        vertexCoords.append((coord[0], coord[1] + edgeLength))
        vertexCoords.append((coord[0] + radius, coord[1] + int(round(edgeLength / 2.0))))

    # A list to hold the vertices of the map
    vertices = []
    # There are 54 vertices on the map
    # this loop instantiates each one and relates it to the one preceding it when appropriate
    for newVertexIndex in range(54):
        newVertex = Vertex(vertexCoords[newVertexIndex])
        # The leftmost vertices of each row (vertices 0,7,16,27,38,47) do not have a preceding vertex adjacent to them
        if newVertexIndex != 0 and newVertexIndex != 7 and newVertexIndex != 16 and newVertexIndex != 27 and \
                        newVertexIndex != 38 and newVertexIndex != 47:
            newVertex.adjacentVertices.append(vertices[newVertexIndex - 1])
            vertices[newVertexIndex - 1].adjacentVertices.append(newVertex)
        vertices.append(newVertex)
    # The last vertex with a vertical relationship to define is vertex 45, so the loop must go that far
    for x in range(46):
        # Use x as an index for the vertices list
        # The if-elif-else structure represents the division of vertices by row on the board
        if x < 7:
            # The top row on the board has vertical relationships between even-numbered vertices
            if x % 2 == 0:
                # Use y as the index of the vertex vertically related to vertex x.
                # There are 3 hexes in row 1 and 4 in row 2, so the vertices are 8 apart
                y = x + 8
                vertices[x].adjacentVertices.append(vertices[y])
                vertices[y].adjacentVertices.append(vertices[x])
        elif x < 16:
            # The 2nd row on the board has vertical relationships between odd-numbered vertices.
            if x % 2 == 1:
                # There are 4 hexes in row 2 and 5 in row 3, so the vertices are 10 apart
                y = x + 10
                vertices[x].adjacentVertices.append(vertices[y])
                vertices[y].adjacentVertices.append(vertices[x])
        elif x < 28:
            # The 3rd row has vertical relationships between even-numbered vertices
            if x % 2 == 0:
                # There are 5 hexes in row 3 and 4 in row 4, so the vertices are 11 apart
                y = x + 11
                vertices[x].adjacentVertices.append(vertices[y])
                vertices[y].adjacentVertices.append(vertices[x])
        elif x < 39:
            if x % 2 == 0:
                # There are 4 hexes in 4 and 3 in row 5, so the vertices are 10 apart
                y = x + 10
                vertices[x].adjacentVertices.append(vertices[y])
                vertices[y].adjacentVertices.append(vertices[x])
        else:
            if x % 2 == 1:
                # There are 3 hexes in row 5 and no row 6, so the vertices are 8 apart
                y = x + 8
                vertices[x].adjacentVertices.append(vertices[y])
                vertices[y].adjacentVertices.append(vertices[x])
    # The if-elif structure represents the division of hexes by row on the board
    # For each hex, connect it to the vertices that surround it
    for hexIndex in range(19):
        if hexIndex < 3:
            # In row 1, the upper left vertex index (a) is twice the hex index
            a = hexIndex * 2
            # In row 1, the lower left vertex index (b) is 8 greater than the upper left vertex index
            b = a + 8
            # Loop over the three upper and three lower vertex indices and relate them to the hex
            for vertex in [vertices[a + i] for i in range(3)] + [vertices[b + j] for j in range(3)[::-1]]:
                vertex.hexes.append(hexes[hexIndex])
                hexes[hexIndex].vertices.append(vertex)
        elif hexIndex < 7:
            a = hexIndex * 2 + 1  # In row 2, the upper left vertex index (a) is twice the hex index plus 1
            b = a + 10  # In row 2, the lower left vertex index (b) is 10 greater than the upper left index
            # Loop over the three upper and three lower vertex indices and relate them to the hex
            for vertex in [vertices[a + i] for i in range(3)] + [vertices[b + j] for j in range(3)[::-1]]:
                vertex.hexes.append(hexes[hexIndex])
                hexes[hexIndex].vertices.append(vertex)
        elif hexIndex < 12:
            a = hexIndex * 2 + 2  # In row 3, the upper left vertex index (a) is twice the hex index plus 2
            b = a + 11  # In row 3, the lower left vertex index (b) is 11 greater than the upper left index
            for vertex in [vertices[a + i] for i in range(3)] + [vertices[b + j] for j in range(3)[::-1]]:
                vertex.hexes.append(hexes[hexIndex])
                hexes[hexIndex].vertices.append(vertex)
        elif hexIndex < 16:
            a = hexIndex * 2 + 4  # In row 4, the upper left vertex index (a) is twice the hex index plus 4
            b = a + 10  # In row 4, the lower left vertex index (b) is 10 greater than the upper left index
            for vertex in [vertices[a + i] for i in range(3)] + [vertices[b + j] for j in range(3)[::-1]]:
                vertex.hexes.append(hexes[hexIndex])
                hexes[hexIndex].vertices.append(vertex)
        else:
            a = hexIndex * 2 + 7
            b = a + 8
            for vertex in [vertices[a + i] for i in range(3)] + [vertices[b + j] for j in range(3)[::-1]]:
                vertex.hexes.append(hexes[hexIndex])
                hexes[hexIndex].vertices.append(vertex)
    for hexTile in hexes:
        hexTile.vertexCoordinates = [ver.coordinates for ver in hexTile.vertices]

    while 1:
        # Loop through the hexes, so that they can be drawn
        for hexTile in hexes:
            pygame.draw.polygon(screen, hexTile.color, hexTile.vertexCoordinates, 0)
            if hexTile.resource != desert:
                resourceOdds = str(hex.odds)
                if resourceOdds == "6" or resourceOdds == "8":
                    label = myfont.render(resourceOdds, 1, red)
                else:
                    label = myfont.render(resourceOdds, 1, black)
                screen.blit(label, (hex.coordinates))
        pygame.display.flip()

        # waits ten seconds and then starts the whole process over again
        time.sleep(1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()


if __name__ == "__main__":
    main()

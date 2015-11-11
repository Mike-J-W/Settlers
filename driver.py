from pieces import *
import random
import pygame


def make_map():
    edgeLength = 10
    angleSize = 120
    


def main():

    # Initialize all the game pieces
    # The resource variables
    lumber = "Wood"
    grain = "Wheat"
    wool = "Wool"
    clay = "Clay"
    ore = "Ore"
    # A list of the resources in the game
    resourceTypes = [lumber, grain, wool, clay, ore]
    # A list representing the number of hexes per resource
    resourcesForHexes = [lumber] * 4 + [grain] * 4 + [wool] * 4 + [clay] * 3 + [ore] * 3
    # A list of the numbered, circular tiles denoting times of harvest
    oddsTiles = [2,3,3,4,4,5,5,6,6,8,8,9,9,10,10,11,11,12]
    # Shuffle the order of the list of numbered tiles, so that they can be assigned to the hexes randomly
    random.shuffle(oddsTiles)
    # A list with one element per development card
    developmentDeck = Card_Deck(["Knight"] * 14 + ["Monopoly", "Year of Plenty", "Road Building"] * 2 + ["Victory Point"] * 5)
    # A dictionary to hold the decks of resources, keyed to their resource name
    resourceDecks = {}
    # Generate each resource deck and add it to the dictionary
    for resource in resourceTypes:
        resourceDecks[resource] = [resource] * 19
    # A list of the hexes, assigned a resource and a numbered tile using the lists above
    hexes = [Hex(resourcesForHexes[x], oddsTiles[x]) for x in range(18)]
    # Add the desert hex
    hexes.append(Hex("Desert", 0))
    # Shuffle the list of hexes so that they can be placed on the board in a random fashion
    random.shuffle(hexes)
    # A list of the ports on the map
    ports = [Port(resource, 2) for resource in resourceTypes]
    ports += [Port("All", 3)] * 4
    # A list to hold the vertices of the map
    vertices = []
    # There are 54 vertices on the map; this loop instantiates each one and relates it to the one preceding it when appropriate
    for x in range(54):
        newVertex = Vertex()
        # The leftmost vertices of each row (vertices 0,7,16,27,38,47) do not have a preceding vertex adjacent to them
        if x != 0 and x != 7 and x != 16 and x != 27 and x != 38 and x != 47:
            newVertex.adjacentVertices.append(vertices[x-1])
            vertices[x-1].adjacentVertices.append(newVertex)
        vertices.append(newVertex)
    # The last vertex with a vertical relationship to define is vertex 45, so the loop must go that far
    for x in range(46):
        # Use x as an index for the vertices list
        # The if-elif-else structure represents the division of vertices by row on the board
        if x < 7:
            # The top row on the board has vertical relationships between even-numbered vertices
            if x % 2 == 0:
                # Use y as the index of the vertex vertically related to vertex x. There are 3 hexes in row 1 and 4 in row 2, so the vertices are 8 apart
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
        # Here, use x as an index for the hexes list
        # The if-elif structure represents the division of hexes by row on the board
        # There are only 19 hexes, so the full range of the loop is not used
        if x < 3:
            a = x * 2       # In row 1, the upper left vertex index (a) is twice the hex index
            b = a + 8       # In row 1, the lower left vertex index (b) is 8 greater than the upper left vertex index
            # Loop over the three upper and three lower vertex indices and assign the hex to them
            for i in range(3):
                vertices[a+i].hexes.append(hexes[x])
                vertices[b+i].hexes.append(hexes[x])
        elif x < 7:
            a = x * 2 + 1   # In row 2, the upper left vertex index (a) is twice the hex index plus 1
            b = a + 10      # In row 2, the lower left vertex index (b) is 10 greater than the upper left index
            # Loop over the three upper and three lower vertex indices and assign the hex to them
            for i in range(3):
                vertices[a+i].hexes.append(hexes[x])
                vertices[b+i].hexes.append(hexes[x])
        elif x < 12:
            a = x * 2 + 2   # In row 3, the upper left vertex index (a) is twice the hex index plus 2
            b = a + 11      # In row 3, the lower left vertex index (b) is 11 greater than the upper left index
            for i in range(3):
                vertices[a+i].hexes.append(hexes[x])
                vertices[b+i].hexes.append(hexes[x])
        elif x < 16:
            a = x * 2 + 4   # In row 4, the upper left vertex index (a) is twice the hex index plus 4
            b = a + 10      # In row 4, the lower left vertex index (b) is 10 greater than the upper left index
            for i in range(3):
                vertices[a+i].hexes.append(hexes[x])
                vertices[b+i].hexes.append(hexes[x])
        elif x < 19:
            a = x * 2 + 7
            b = a + 8
            for i in range(3):
                vertices[a+i].hexes.append(hexes[x])
                vertices[b+i].hexes.append(hexes[x])
    # Assign the ports to the appropriate vertices
    vertices[0].port = ports[5]
    vertices[1].port = ports[5]
    vertices[3].port = ports[2]
    vertices[4].port = ports[2]
    vertices[7].port = ports[4]
    vertices[14].port = ports[6]
    vertices[15].port = ports[6]
    vertices[17].port = ports[4]
    vertices[26].port = ports[7]
    vertices[28].port = ports[1]
    vertices[37].port = ports[7]
    vertices[38].port = ports[1]
    vertices[45].port = ports[3]
    vertices[46].port = ports[3]
    vertices[47].port = ports[8]
    vertices[48].port = ports[8]
    vertices[50].port = ports[0]
    vertices[51].port = ports[0]




if __name__ == "__main__":
    main()
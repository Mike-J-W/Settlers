from pieces import *
import random

def main():

    lumber = "Wood"
    grain = "Wheat"
    wool = "Wool"
    clay = "Clay"
    ore = "Ore"
    resourceTypes = [lumber, grain, wool, clay, ore]
    resourcesForHexes = [lumber] * 4 + [grain] * 4 + [wool] * 4 + [clay] * 3 + [ore] * 3
    oddsTiles = [2,3,3,4,4,5,5,6,6,8,8,9,9,10,10,11,11,12]
    random.shuffle(oddsTiles)
    
    # Initialize all the game pieces
    developmentDeck = Card_Deck(["Knight"] * 14 + ["Monopoly", "Year of Plenty", "Road Building"] * 2 + ["Victory Point"] * 5)
    resourceDecks = {}
    for resource in resourceTypes:
        resourceDecks[resource] = [resource] * 19
    hexes = [Hex(resourcesForHexes[x], oddsTiles[x]) for x in range(18)]
    hexes.append(Hex("Desert", 0))
    random.shuffle(hexes)
    ports = [Port(resource, 2) for resource in resourceTypes]
    ports += [Port("All", 3)] * 4
    vertices = []
    for x in range(54):     # Set up the vertices, noting the sequential relationships
        newVertex = Vertex()
        if x != 0 and x != 7 and x != 16 and x != 27 and x != 38 and x != 47:
            newVertex.adjacentVertices.append(vertices[x-1])
            vertices[x-1].adjacentVertices.append(newVertex)
        vertices.append(newVertex)
    for x in range(46):     # Complete the adjacency relationships and "place" the hexes
        if x < 7:
            if x % 2 == 0:
                y = x + 8
                vertices[x].adjacentVertices.append(vertices[y])
                vertices[y].adjacentVertices.append(vertices[x])
        elif x < 16:
            if x % 2 == 1:
                y = x + 10
                vertices[x].adjacentVertices.append(vertices[y])
                vertices[y].adjacentVertices.append(vertices[x])
        elif x < 28:
            if x % 2 == 0:
                y = x + 11
                vertices[x].adjacentVertices.append(vertices[y])
                vertices[y].adjacentVertices.append(vertices[x])
        elif x < 39:
            if x % 2 == 0:
                y = x + 10
                vertices[x].adjacentVertices.append(vertices[y])
                vertices[y].adjacentVertices.append(vertices[x])
        else:
            if x % 2 == 1:
                y = x + 8
                vertices[x].adjacentVertices.append(vertices[y])
                vertices[y].adjacentVertices.append(vertices[x])
        if x < 3:
            a = x * 2
            b = a + 8
            for i in range(3):
                vertices[a+i].hexes.append(hexes[x])
                vertices[b+i].hexes.append(hexes[x])
        elif x < 7:
            a = x * 2 + 1
            b = a + 10
            for i in range(3):
                vertices[a+i].hexes.append(hexes[x])
                vertices[b+i].hexes.append(hexes[x])
        elif x < 12:
            a = x * 2 + 2
            b = x + 11
            for i in range(3):
                vertices[a+i].hexes.append(hexes[x])
                vertices[b+i].hexes.append(hexes[x])
        elif x < 16:
            a = x * 2 + 4
            b = x + 10
            for i in range(3):
                vertices[a+i].hexes.append(hexes[x])
                vertices[b+i].hexes.append(hexes[x])
        elif x < 19:
            a = x * 2 + 7
            b = x + 8
            for i in range(3):
                vertices[a+i].hexes.append(hexes[x])
                vertices[b+i].hexes.append(hexes[x])
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
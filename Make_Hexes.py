from pieces import *
import random
import pygame
import math
import time

## initalizes pygame
pygame.init()
## sets the size of the window that is opened
size = width, height = 900, 750
oceanBlue = 0, 0, 120
## opens the window with the size specifications given
screen = pygame.display.set_mode(size)
## sets the background color
screen.fill(oceanBlue)


##  This function checks to make sure that no 6 or 8 odds tiles are directly adjacent to one another.  If they are found to be adjacent, the hexes are reshuffled and a new combination is attempted
def reshuffle_hexes(hexes, adjacencyProblem):
    while adjacencyProblem == True:
        random.shuffle(hexes)
        for index in range(19):
            if index < 2:
                if hexes[index].odds == 6 or hexes[index].odds == 8:
                    if hexes[index+1].odds == 6 or hexes[index+1].odds == 8:
                        break
                    elif hexes[index+3].odds == 6 or hexes[index+3].odds == 8:
                        break
                    elif hexes[index+4].odds == 6 or hexes[index+4].odds == 8:
                            break
            elif index == 2:
                if hexes[index].odds == 6 or hexes[index].odds == 8:
                    if hexes[index+3].odds == 6 or hexes[index+3].odds == 8:
                        break
                    elif hexes[index+4].odds == 6 or hexes[index+4].odds == 8:
                        break
            elif index < 6:
                if hexes[index].odds == 6 or hexes[index].odds == 8:
                    if hexes[index+1].odds == 6 or hexes[index+1].odds == 8:
                        break
                    elif hexes[index+4].odds == 6 or hexes[index+4].odds == 8:
                        break
                    elif hexes[index+5].odds == 6 or hexes[index+5].odds == 8:
                        break
            elif index == 6:
                if hexes[index].odds == 6 or hexes[index].odds == 8:
                    if hexes[index+4].odds == 6 or hexes[index+4].odds == 8:
                        break
                    elif hexes[index+5].odds == 6 or hexes[index+5].odds == 8:
                        break
            elif index == 7:
                if hexes[index].odds == 6 or hexes[index].odds == 8:
                    if hexes[index+1].odds == 6 or hexes[index+1].odds == 8:
                        break
                    elif hexes[index+5].odds == 6 or hexes[index+5].odds == 8:
                        break
            elif index < 11:
                if hexes[index].odds == 6 or hexes[index].odds == 8:
                    if hexes[index+1].odds == 6 or hexes[index+1].odds == 8:
                        break
                    elif hexes[index+4].odds == 6 or hexes[index+4].odds == 8:
                        break
                    elif hexes[index+5].odds == 6 or hexes[index+5].odds == 8:
                        break
            elif index == 11:
                if hexes[index].odds == 6 or hexes[index].odds == 8:
                    if hexes[index+4].odds == 6 or hexes[index+4].odds == 8:
                        break
            elif index == 12:
                if hexes[index].odds == 6 or hexes[index].odds == 8:
                    if hexes[index+1].odds == 6 or hexes[index+1].odds == 8:
                        break
                    elif hexes[index+4].odds == 6 or hexes[index+4].odds == 8:
                        break
            elif index < 15:
                if hexes[index].odds == 6 or hexes[index].odds == 8:
                    if hexes[index+1].odds == 6 or hexes[index+1].odds == 8:
                        break
                    elif hexes[index+3].odds == 6 or hexes[index+3].odds == 8:
                        break
                    elif hexes[index+4].odds == 6 or hexes[index+4].odds == 8:
                        break
            elif index == 15:
                if hexes[index].odds == 6 or hexes[index].odds == 8:
                    if hexes[index+3].odds == 6 or hexes[index+3].odds == 8:
                        break
            elif index < 18:
                if hexes[index].odds == 6 or hexes[index].odds == 8:
                    if hexes[index+1].odds == 6 or hexes[index+1].odds == 8:
                        break
            elif index == 18:
                adjacencyProblem = False
                print("Succesful odds order!")
                return hexes


def main(screen):
    # Initialize all the game pieces
    
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
    
    # The resource variables
    lumber = "Wood"
    grain = "Wheat"
    wool = "Wool"
    clay = "Clay"
    ore = "Ore"
    desert = "Desert"
    # A list of the resources in the game
    resourceTypes = [lumber, grain, wool, clay, ore]
    # A list with one element per development card
    developmentDeck = Card_Deck(["Knight"] * 14 + ["Monopoly", "Year of Plenty", "Road Building"] * 2 + ["Victory Point"] * 5)
    # A dictionary to hold the decks of resources, keyed to their resource name
    resourceDecks = {}
    # Generate each resource deck and add it to the dictionary
    for resource in resourceTypes:
        resourceDecks[resource] = [resource] * 19

    # A list representing the number of hexes per resource
    resourcesForHexes = [lumber] * 4 + [grain] * 4 + [wool] * 4 + [clay] * 3 + [ore] * 3
    # A list of the numbered, circular tiles denoting times of harvest
    oddsTiles = [2,3,3,4,4,5,5,6,6,8,8,9,9,10,10,11,11,12]
    # Shuffle the order of the list of numbered tiles, so that they can be assigned to the hexes randomly
    random.shuffle(oddsTiles)
    # A list of the hexes, assigned a resource and a numbered tile using the lists above
    hexesPreAdjacencyCheck = [Hex(resourcesForHexes[x], oddsTiles[x]) for x in range(18)]
    # Add the desert hex
    hexesPreAdjacencyCheck.append(Hex("Desert", 0))
    # Shuffle the list of hexes so that they can be placed on the board in a random fashion

    # Runs the reshuffle_hexes function to ensure that no 8s or 6s are adjacent to each to other
    adjacencyProblem = True
    hexes = reshuffle_hexes(hexesPreAdjacencyCheck, adjacencyProblem)

    
    # The length of a side of a hex  PYGAME variable
    edgeLength = 60
    # The distance from the center of a hex to the middle of an edge
    radius = int(round(edgeLength * math.sqrt(3) / 2.0))
    # The unadjusted coordinates of the centers of the hexes
    baseHexCenters = [(3,1),(5,1),(7,1),(2,2.5),(4,2.5),(6,2.5),(8,2.5),(1,4),(3,4),(5,4),(7,4),(9,4),(2,5.5),(4,5.5),(6,5.5),(8,5.5),(3,7),(5,7),(7,7)]
    # The centers of the hexes adjusted for the length of their sides
    hexCenters = [(2 * edgeLength + baseHexCenters[i][0] * radius, (baseHexCenters[i][1] + 2) * edgeLength) for i in range(len(baseHexCenters))]
    # "Place" the hexes by assigned the coordinates to the objects and generate list of the coordinates of the vertices using the hex coordinates
    vertexCoords = []

    
    
    

    for index, coord in enumerate(hexCenters):
        
        hexes[index].coordinates = coord
        vertexCoords.append((coord[0] - radius, coord[1] - int(round(edgeLength / 2.0))))
        vertexCoords1 = (coord[0] - radius, coord[1] - int(round(edgeLength / 2.0)))
        vertexCoords.append((coord[0], coord[1] - edgeLength))
        vertexCoords2 = (coord[0], coord[1] - edgeLength)
        vertexCoords.append((coord[0] + radius, coord[1] - int(round(edgeLength / 2.0))))
        vertexCoords3 = (coord[0] + radius, coord[1] - int(round(edgeLength / 2.0)))

        # Populates list with top three coordinates of each hex
        drawHexPoints = [vertexCoords1,vertexCoords2, vertexCoords3]
        
        
        if hexes[index].resource == lumber:
            # Calculates the bottom three coordinates from the top three and the length of each side of the hexagon
            coordFour = (coord[0] + radius, (coord[1] - int(round(edgeLength / 2.0)))+ edgeLength)
            coordFive = ((coord[0], coord[1] + edgeLength))
            coordSix = ((coord[0] - radius, coord[1] + edgeLength - int(round(edgeLength / 2.0))))
            
            # Appends the bottom three coordinates in the proper order to the top three coordinates
            drawHexPoints.append(coordFour)
            drawHexPoints.append(coordFive)
            drawHexPoints.append(coordSix)
            #print("For lumber:")
            #print(drawHexPoints)
            
            # Draws the hexagon using the points specified with the proper color of the resource tile
            pygame.draw.polygon(screen, forestGreen, drawHexPoints, 0)
            # Creates the string for the resource odds that will be written on the gameboard
            resourceOdds = str(hexes[index].odds)
            #print(resourceOdds," = Resource Odds")
            
            # Writes the 6 and 8 resource odds tiles in a different color
            if str(resourceOdds) == "6" or str(resourceOdds) == "8":
                label = myfont.render(str(resourceOdds), 1, red)
            else:
                label = myfont.render(str(resourceOdds), 1, black)

            # Adds the label of the odds to each hex
            screen.blit(label, (hexes[index].coordinates))
            
            # Updates the screen
            pygame.display.update()
        
        
        elif hexes[index].resource == wool:
            coordFour = (coord[0] + radius, (coord[1] - int(round(edgeLength / 2.0)))+ edgeLength)
            coordFive = ((coord[0], coord[1] + edgeLength))
            coordSix = ((coord[0] - radius, coord[1] + edgeLength - int(round(edgeLength / 2.0))))
            drawHexPoints.append(coordFour)
            drawHexPoints.append(coordFive)
            drawHexPoints.append(coordSix)
            #print("For wool:")
            #print(drawHexPoints)
            pygame.draw.polygon(screen, woolGreen, drawHexPoints, 0)
            resourceOdds = hexes[index].odds
            #print(resourceOdds)
            if str(resourceOdds) == "6" or str(resourceOdds) == "8":
                label = myfont.render(str(resourceOdds), 1, red)
            else:
                label = myfont.render(str(resourceOdds), 1, black)
            screen.blit(label, (hexes[index].coordinates))
            pygame.display.update()
        
        elif hexes[index].resource == grain:
            coordFour = (coord[0] + radius, (coord[1] - int(round(edgeLength / 2.0)))+ edgeLength)
            coordFive = ((coord[0], coord[1] + edgeLength))
            coordSix = ((coord[0] - radius, coord[1] + edgeLength - int(round(edgeLength / 2.0))))
            drawHexPoints.append(coordFour)
            drawHexPoints.append(coordFive)
            drawHexPoints.append(coordSix)
            #print("For grain:")
            #print(drawHexPoints)
            pygame.draw.polygon(screen, wheatYellow, drawHexPoints, 0)
            resourceOdds = hexes[index].odds
            #print(resourceOdds)
            if str(resourceOdds) == "6" or str(resourceOdds) == "8":
                label = myfont.render(str(resourceOdds), 1, red)
            else:
                label = myfont.render(str(resourceOdds), 1, black)

            screen.blit(label, (hexes[index].coordinates))
            pygame.display.update()

        elif hexes[index].resource == clay:
            coordFour = (coord[0] + radius, (coord[1] - int(round(edgeLength / 2.0)))+ edgeLength)
            coordFive = ((coord[0], coord[1] + edgeLength))
            coordSix = ((coord[0] - radius, coord[1] + edgeLength - int(round(edgeLength / 2.0))))
            drawHexPoints.append(coordFour)
            drawHexPoints.append(coordFive)
            drawHexPoints.append(coordSix)
            #print("For clay:")
            #print(drawHexPoints)
            pygame.draw.polygon(screen, clayColor, drawHexPoints, 0)
            resourceOdds = hexes[index].odds
            #print(resourceOdds)
            if str(resourceOdds) == "6" or str(resourceOdds) == "8":
                label = myfont.render(str(resourceOdds), 1, red)
            else:
                label = myfont.render(str(resourceOdds), 1, black)
            screen.blit(label, (hexes[index].coordinates))
            pygame.display.update()


        elif hexes[index].resource == ore:
            coordFour = (coord[0] + radius, (coord[1] - int(round(edgeLength / 2.0)))+ edgeLength)
            coordFive = ((coord[0], coord[1] + edgeLength))
            coordSix = ((coord[0] - radius, coord[1] + edgeLength - int(round(edgeLength / 2.0))))
            drawHexPoints.append(coordFour)
            drawHexPoints.append(coordFive)
            drawHexPoints.append(coordSix)
            #print("For rock:")
            #print(drawHexPoints)
            pygame.draw.polygon(screen, rockGray, drawHexPoints, 0)
            resourceOdds = hexes[index].odds
            #print(resourceOdds)
            if str(resourceOdds) == "6" or str(resourceOdds) == "8":
                label = myfont.render(str(resourceOdds), 1, red)
            else:
                label = myfont.render(str(resourceOdds), 1, black)

            screen.blit(label, (hexes[index].coordinates))
            pygame.display.update()

        elif hexes[index].resource == desert:
            coordFour = (coord[0] + radius, (coord[1] - int(round(edgeLength / 2.0)))+ edgeLength)
            coordFive = ((coord[0], coord[1] + edgeLength))
            coordSix = ((coord[0] - radius, coord[1] + edgeLength - int(round(edgeLength / 2.0))))
            drawHexPoints.append(coordFour)
            drawHexPoints.append(coordFive)
            drawHexPoints.append(coordSix)
            #print(drawHexPoints)
            pygame.draw.polygon(screen, sandyDesert, drawHexPoints, 0)
            pygame.display.update()

    print("Finished cycling through all hexes!")
    
    # waits ten seconds and then starts the whole process over again
    time.sleep(10)


while 1:
    if __name__ == "__main__":
        main(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()






'''Contains the Class definitions for all persistent objects in the game'''

import math
import random
import pygame
import constants as c


# A hexagonal tile that composes the game board
class Hex(object):
    '''Defined by its location, owner, resource, and odds for harvest.
       Also knows its size and whether it has the Robber.'''
    def __init__(self, resource, odds, color, coordinates):
        self.resource = resource
        self.odds = odds
        self.color = color
        self.edgeLength = c.hexEdgeLength
        self.radius = int(round(self.edgeLength * math.sqrt(3) / 2.0))
        self.vertices = [None, None, None, None, None, None]
        self.hasRobber = False
        if resource == "Desert":
            self.hasRobber = True
        self.coordinates = coordinates
        # Set the coordinates of the vertices, starting with the upper left and moving in a clockwise direction
        self.vertexCoordinates = [(self.coordinates[0] - self.radius,
                                   self.coordinates[1] - int(round(self.edgeLength / 2.0))),
                                  (self.coordinates[0], self.coordinates[1] - self.edgeLength),
                                  (self.coordinates[0] + self.radius,
                                   self.coordinates[1] - int(round(self.edgeLength / 2.0))),
                                  (self.coordinates[0] + self.radius,
                                   self.coordinates[1] + int(round(self.edgeLength / 2.0))),
                                  (self.coordinates[0], self.coordinates[1] + self.edgeLength),
                                  (self.coordinates[0] - self.radius,
                                   self.coordinates[1] + int(round(self.edgeLength / 2.0)))]


# A vertex between hexagonal tiles and/or coasts
class Vertex(object):
    '''Defined by its location and relationship to hexes and other vertices.
       Also knows of ports, settlements, and roads on it.'''
    def __init__(self, coordinates):
        self.hexes = []
        self.port = None
        self.settlement = None
        self.roads = []
        self.canBeSettled = True
        self.adjacentVertices = []
        self.coordinates = coordinates


# A town or city able to be placed on a vertex
class Settlement(object):
    '''Defined by its size (town or city) and owner.
       Also knows if/where it's been built and its size'''
    def __init__(self, scale, player):
        self.scale = scale
        self.owner = player
        self.vertex = None
        self.edgeLength = c.settlementEdgeLength
        self.circumradius = int(round(math.sqrt(50 + 10 * math.sqrt(5)) * self.edgeLength / 10))
    
    def find_yield(self, roll):
        '''Checks surrounding hex tiles for odds that match the roll and returns resources accordingly.'''
        yieldedResources = dict(zip(c.resourceTypes, [0, 0, 0, 0, 0]))
        for hexTile in self.vertex.hexes:
            if hexTile.odds == roll and not hexTile.hasRobber and hexTile.resource != "Desert":
                yieldedResources[hexTile.resource] += self.scale
        return yieldedResources

    def draw_settlement(self, surface):
        '''Places image (square for town, pentagon for city) of settlement over its vertex, in the owner's color.'''
        if self.scale == 1:
            pygame.draw.rect(surface, self.owner.color, pygame.Rect(self.vertex.coordinates[0] - self.edgeLength / 2,
                                                                    self.vertex.coordinates[1] - self.edgeLength / 2,
                                                                    self.edgeLength, self.edgeLength))
        else:
            x1 = int(round(math.sqrt(10 + 2 * math.sqrt(5)) * self.circumradius / 4))
            y1 = int(round((math.sqrt(5) - 1) * self.circumradius / 4))
            x2 = int(round(math.sqrt(10 - 2 * math.sqrt(5)) * self.circumradius / 4))
            y2 = int(round((math.sqrt(5) + 1) * self.circumradius / 4))
            p1 = (self.vertex.coordinates[0], self.vertex.coordinates[1] - self.circumradius)
            p2 = (self.vertex.coordinates[0] + x1, self.vertex.coordinates[1] - y1)
            p3 = (self.vertex.coordinates[0] + x2, self.vertex.coordinates[1] + y2)
            p4 = (self.vertex.coordinates[0] - x2, self.vertex.coordinates[1] + y2)
            p5 = (self.vertex.coordinates[0] - x1, self.vertex.coordinates[1] - y1)
            pygame.draw.polygon(surface, self.owner.color, [p1, p2, p3, p4, p5])


# A road connecting settlements
class Road(object):
    '''Defined by its size, owner, and vertices it connects, if any.'''
    def __init__(self, player):
        self.owner = player
        self.vertex1 = None
        self.vertex2 = None
        self.width = c.roadWidth

    def draw_road(self, surface):
        '''Places image of road along the edge between its vertices in the owner's color.'''
        pygame.draw.line(surface, self.owner.color, self.vertex1.coordinates, self.vertex2.coordinates, self.width)


# A trading port along the coast
class Port(object):
    '''Defined by the resources it affects, the trade ratio for those resources, and the vertices that access it.'''
    def __init__(self, resources, rate):
        self.resources = resources
        self.rate = rate
        self.vertices = []

    def draw_port(self, surface, color):
        '''Places image of port (triangle) off the coast in between the two vertices that can access it and 
           colored according to the resources the port affects.'''
        neighborVertices = []
        for vertex in self.vertices:
            adjVerOptions = list(vertex.adjacentVertices)
            for ver in self.vertices:
                if ver in adjVerOptions:
                    adjVerOptions.remove(ver)
            if len(adjVerOptions) == 1:
                neighborVertices.append(adjVerOptions[0])
            else:
                for adjVer in adjVerOptions:
                    if len(adjVer.hexes) == 3:
                        neighborVertices.append(adjVer)
        rises = [self.vertices[i].coordinates[1] - neighborVertices[i].coordinates[1] for i in range(2)]
        runs = [self.vertices[i].coordinates[0] - neighborVertices[i].coordinates[0] for i in range(2)]
        indexA = 0
        indexB = 1
        outerCornerX = 0
        outerCornerY = 0
        if 0 in runs:
            indexA = runs.index(0)
            indexB = (indexA - 1) * -1
            outerCornerX = self.vertices[indexA].coordinates[0]
            outerCornerY = self.vertices[indexB].coordinates[1] - int(round(rises[indexB] /
                                                                            (runs[indexB] /
                                                                             (self.vertices[indexB].coordinates[0] -
                                                                              outerCornerX))))
        else:
            outerCornerY = int(round((self.vertices[0].coordinates[1] + self.vertices[1].coordinates[1])/2))
            outerCornerX = self.vertices[0].coordinates[0] + int(round((outerCornerY -
                                                                        self.vertices[0].coordinates[1]) *
                                                                       runs[0] / rises[0]))
        cornerA = (self.vertices[indexA].coordinates[0] + int(round(runs[indexA] * 0.25)),
                   self.vertices[indexA].coordinates[1] + int(round(rises[indexA] * 0.25)))
        cornerB = (self.vertices[indexB].coordinates[0] + int(round(runs[indexB] * 0.25)),
                   self.vertices[indexB].coordinates[1] + int(round(rises[indexB] * 0.25)))
        pygame.draw.polygon(surface, color, [(outerCornerX, outerCornerY), cornerA, cornerB])


# The Robber piece
class Robber(object):
    '''Defined by its size, color, location, and the hex tile it occupies.'''
    def __init__(self, desertHex):
        self.currentHex = desertHex
        self.radius = c.robberRadius
        self.color = (15, 15, 15)
        self.coordinates = (self.currentHex.coordinates[0] - int(round(self.radius / 2)),
                            self.currentHex.coordinates[1] - int(round(self.radius / 2)))
    
    def move(self, newHex, surface):
        '''Alters the board image and properties of the Robber such that it changes position.'''
        pygame.draw.circle(surface, self.currentHex.color, self.coordinates, self.radius)
        self.currentHex.hasRobber = False
        self.currentHex = newHex
        newHex.hasRobber = True
        self.coordinates = (self.currentHex.coordinates[0] - int(round(self.radius / 2)),
                            self.currentHex.coordinates[1] - int(round(self.radius / 2)))
        self.draw_robber(surface)

    def steal_from(self, playerToRob):
        '''Takes a random resource card from the targeted player.'''
        targetCards = playerToRob.cardsInHand
        targetHand = []
        for key in targetCards.keys():
            targetHand += [key] * targetCards[key]
        if not targetHand:
            return "Nothing"
        else:
            random.shuffle(targetHand)
            cardStolen = targetHand[0]
            playerToRob.cardsInHand[cardStolen] -= 1
            return cardStolen

    def play(self, surface, newHex, playerRobbing, playerToRob):
        '''Combines Robber functions into a complete game action.'''
        self.move(newHex, surface)
        if playerToRob is None:
            return "{} moved the Robber and drew nothing from Nobody.".format(playerRobbing.name)
        else:
            newCard = self.steal_from(playerToRob)
            if newCard != "Nothing":
                playerRobbing.cardsInHand[newCard] += 1
            return "{} moved the Robber and drew {} from {}.".format(playerRobbing.name, newCard, playerToRob.name)

    def draw_robber(self, surface):
        '''Draws image of the Robber (circle) at its location.'''
        pygame.draw.circle(surface, self.color, self.coordinates, self.radius)


# A player in the game
# Has identifying variables, point total, list of settlements built and count remaining, list of roads built and
#     count remaining, list of unplayed development cards, count of Knights played, status of owning Longest_Road and
#     Largest_Army, and list of resource cards in hand
# Functions for each action a player can take during their turn
class Player(object):
    '''Defined by name, color, human or AI, game points, resources, development cards, infrastructure, and trade ratios.'''
    def __init__(self, name, color, isAI):
        self.name = name
        self.color = color
        self.isAI = isAI
        self.points = 0
        self.builtSettlements = []
        self.unbuiltSettlements = [Settlement(1, self) for x in range(5)]
        self.unbuiltSettlements += [Settlement(2, self) for x in range(4)]
        self.builtRoads = []
        self.unbuiltRoads = [Road(self) for x in range(15)]
        self.developmentCards = []
        self.armySize = 0
        self.hasLongestRoad = False
        self.hasLargestArmy = False
        self.cardsInHand = {c.wool: 0, c.grain: 0, c.lumber: 0, c.clay: 0, c.ore: 0}
        self.tradeRatios = {c.wool: 4, c.grain: 4, c.lumber: 4, c.clay: 4, c.ore: 4}
    
    def build_town(self, vertexToSettle, resourceDecks, surface):
        '''After checks, places town on a vertex and changes player data accordingly, including discarding resources.'''
        for resource in c.townCost.keys():
            if self.cardsInHand[resource] < c.townCost[resource]:
                return (2, "{} does not have enough {} to build a town.".format(self.name, resource))
        if not vertexToSettle.canBeSettled:
            return (3, "That vertex cannot be built upon.")
        if not self.unbuiltSettlements:
            return (4, "{} does not have any towns to build.".format(self.name))
        if len(self.builtSettlements) >= 2:
            onRoad = False
            for road in self.builtRoads:
                if vertexToSettle == road.vertex1 or vertexToSettle == road.vertex2:
                    onRoad = True
                    break
            if not onRoad:
                return (5, "The proposed settlement does not connect to any of {}'s roads.".format(self.name))
        for settlement in self.unbuiltSettlements:
            if settlement.scale == 1:
                self.unbuiltSettlements.remove(settlement)
                self.builtSettlements.append(settlement)
                settlement.vertex = vertexToSettle
                vertexToSettle.settlement = settlement
                for vertex in [vertexToSettle] + vertexToSettle.adjacentVertices:
                    vertex.canBeSettled = False
                self.discard_cards(c.townCost, resourceDecks)
                settlement.draw_settlement(surface)
                if settlement.vertex.port is not None:
                    for rsc in settlement.vertex.port.resources:
                        if self.tradeRatios[rsc] > settlement.vertex.port.rate:
                            self.tradeRatios[rsc] = settlement.vertex.port.rate
                return (0, "Success!")
        return (1, "Failed to build the town for an unknown reason.")
    
    def build_city(self, vertexToUpgrade, resourceDecks, surface):
        '''After checks, puts city over a town and changes player data accordingly, including discarding resources.'''
        for resource in c.cityCost.keys():
            if self.cardsInHand[resource] < c.cityCost[resource]:
                return (2, "{} does not have enough {} to upgrade a settlement".format(self.name, resource))
        if 2 not in [s.scale for s in self.unbuiltSettlements]:
            return (3, "{} does not have any cities left to play.".format(self.name))
        if vertexToUpgrade.settlement not in self.builtSettlements:
            return (4, "{} does not have a settlement on that vertex.".format(self.name))
        if vertexToUpgrade.settlement.scale == 2:
            return (5, "That settlement has already been upgraded.")
        for settlement in self.unbuiltSettlements:
            if settlement.scale == 2:
                self.unbuiltSettlements.remove(settlement)
                self.builtSettlements.append(settlement)
                self.builtSettlements.remove(vertexToUpgrade.settlement)
                self.unbuiltSettlements.append(vertexToUpgrade.settlement)
                vertexToUpgrade.settlement = settlement
                settlement.vertex = vertexToUpgrade
                self.discard_cards(c.cityCost, resourceDecks)
                settlement.draw_settlement(surface)
                return (0, "Success!")
        return (1, "Failed to upgrade the settlement for an unknown reason")
    
    def build_road(self, vertex1, vertex2, longestRoad, resourceDecks, surface):
        '''After checks, places road between vertices and changes player data accordingly.'''
        if not self.unbuiltRoads:
            return (2, "{} does not have any roads to build".format(self.name))
        for resource in c.roadCost.keys():
            if self.cardsInHand[resource] < c.roadCost[resource]:
                return (3, "{} does not have enough {} to build a road.".format(self.name, resource))
        if vertex1 not in vertex2.adjacentVertices:
            return (4, "Those vertices are not adjacent.")
        if vertex1.roads:
            for road in vertex1.roads:
                if road.vertex1 == vertex2 or road.vertex2 == vertex2:
                    return (5, "A road already exists along that path.")
        contiguousRoad = False
        if self.builtRoads:
            for road in self.builtRoads:
                if vertex1 == road.vertex1 or vertex1 == road.vertex2 or vertex2 == road.vertex1 or \
                                vertex2 == road.vertex2:
                    contiguousRoad = True
                    break
        if not contiguousRoad:
            for settlement in self.builtSettlements:
                if vertex1 == settlement.vertex or vertex2 == settlement.vertex:
                    contiguousRoad = True
                    break
            if not contiguousRoad:
                return (6, "The proposed road does not connect with any "
                           "other part of {}'s infrastructure.".format(self.name))
        newRoad = self.unbuiltRoads[0]
        self.unbuiltRoads.remove(newRoad)
        self.builtRoads.append(newRoad)
        newRoad.vertex1 = vertex1
        vertex1.roads.append(newRoad)
        newRoad.vertex2 = vertex2
        vertex2.roads.append(newRoad)
        self.discard_cards(c.roadCost, resourceDecks)
        longestRoad.determine_owner()
        newRoad.draw_road(surface)
        return (0, "Success!")
    
    def buy_development_card(self, developmentDeck, resourceDecks):
        '''After checks, exchanges resources for development card and alters player data and card decks accordingly.'''
        for resource in c.developmentCardCost.keys():
            if self.cardsInHand[resource] < c.developmentCardCost[resource]:
                return (1, "{} does not have enough {} to buy a Development Card.".format(self.name, resource))
        if len(developmentDeck) == 0:
            return (2, "The deck of Development Cards is empty.")
        newCard = developmentDeck.popleft()
        self.developmentCards.append(newCard)
        self.discard_cards(c.developmentCardCost, resourceDecks)
        return (0, "Success! {} bought a {}.".format(self.name, newCard))

    def play_knight(self, robber, newHex, playerToRob, largestArmy, surface):
        '''Moves a knight from player's hand to their army, checks Largest Army, and plays the Robber.'''
        if "Knight" in self.developmentCards:
            self.armySize += 1
            self.developmentCards.remove("Knight")
            largestArmy.determine_owner()
            return (0, "Success! " + robber.play(surface, newHex, self, playerToRob))
        else:
            return (1, "{} does not have any Knights to play.".format(self.name))
                
    def play_monopoly(self, playerList, resourceWanted):
        '''Exchanges Monopoly from player's hand for all of 1 resource from other players' hands.'''
        if "Monopoly" not in self.developmentCards:
            return (1, "{} does not have a Monopoly Card to play.".format(self.name))
        self.developmentCards.remove("Monopoly")
        playerListCopy = playerList.copy()
        playerListCopy.remove(self)
        originalCount = self.cardsInHand[resourceWanted]
        for player in playerListCopy:
            self.cardsInHand[resourceWanted] += player.cardsInHand[resourceWanted]
            player.cardsInHand[resourceWanted] = 0
        takenCount = self.cardsInHand[resourceWanted] - originalCount
        return (0, "Success! {} gained {} {} cards.".format(self.name, takenCount, resourceWanted))

    def play_year_of_plenty(self, cardsDesired):
        '''Exchanges Year of Plenty from player's hand for any 2 resource cards from the decks.'''
        if "Year of Plenty" in self.developmentCards:
            self.developmentCards.remove("Year of Plenty")
            self.draw_cards(cardsDesired[:2])
            return 0
        else:
            return 1
                
    def play_road_building(self, vertexPair1, vertexPair2):
        '''Exchanges Road Building from player's hand for the free construction of 2 roads.'''
        if "Road Building" in self.developmentCards:
            for pair in [vertexPair1, vertexPair2]:
                if len(self.unbuiltRoads) > 0:
                    if len(pair) > 1:
                        self.build_road(pair[0], pair[1])
                    else:
                        return 1
            return 0
        else:
            return 1

    def offer_trade(self, cardsOffering, cardsRequesting, playersNotified):
        pass
    
    def make_player_trade(self, cardsGiving, cardsTaking, tradeAgent):
        pass

    def make_maritime_trade(self, resourceGiving, countGiving, resourceTaking, countTaking, resourceDecks):
        if self.tradeRatios[resourceGiving] * countTaking != countGiving:
            return (1, "{}'s trade ratio for {} does not allow that trade.".format(self.name, resourceGiving))
        if countGiving > self.cardsInHand[resourceGiving]:
            return (2, "{} does not have {} {} cards to discard.".format(self.name, countGiving, resourceGiving))
        if countTaking > resourceDecks[resourceTaking]:
            return (3, "There are not {} {} cards available.".format(countTaking, resourceTaking))
        self.cardsInHand[resourceGiving] -= countGiving
        resourceDecks[resourceGiving] += countGiving
        self.cardsInHand[resourceTaking] += countTaking
        resourceDecks[resourceTaking] -= countTaking
        return (0, "Success!")
    
    def discard_cards(self, cardsToDiscard, resourceDecks):
        for resource in cardsToDiscard.keys():
            if cardsToDiscard[resource] > self.cardsInHand[resource]:
                return (1, "{} does not have {} {} cards to discard.".format(self.name,
                                                                             cardsToDiscard[resource], resource))
        for resource in cardsToDiscard.keys():
            self.cardsInHand[resource] -= cardsToDiscard[resource]
            resourceDecks[resource] += cardsToDiscard[resource]
        return (0, "Success!")
    
    def draw_cards(self, cardsToDraw, resourceDecks):
        for resource in cardsToDraw.keys():
            if cardsToDraw[resource] > resourceDecks[resource]:
                return (1, "There are not {} {} cards available.".format(cardsToDraw[resource], resource))
        for resource in cardsToDraw.keys():
            self.cardsInHand[resource] += cardsToDraw[resource]
            resourceDecks[resource] -= cardsToDraw[resource]
        return(0, "Success!")

    def determine_harvest(self, roll):
        harvest = []
        if self.builtSettlements:
            for settlement in self.builtSettlements:
                harvest += settlement.find_yield(roll)
            if harvest:
                harvestDict = {c.grain: 0, c.ore: 0, c.wool: 0, c.clay: 0, c.lumber: 0}
                for resource in c.resourceTypes:
                    harvestDict[resource] = harvest.count(resource)
                self.draw_cards(harvestDict)
    
    def count_points(self):
        pointCounter = 0
        if self.builtSettlements:
            for settlement in self.builtSettlements:
                pointCounter += settlement.scale
        if self.developmentCards:
            for card in self.developmentCards:
                if card == "Victory Point":
                    pointCounter += 1
        if self.hasLargestArmy:
            pointCounter += 2
        if self.hasLongestRoad:
            pointCounter += 2
        return pointCounter


# The Largest Army placard
# Has owner of placard, size of the largest army, and list of players in the game
# Functions for determining the player with the largest army, and for reassigning the placard
class LargestArmy(object):
    def __init__(self, playerList):
        self.owner = None
        self.size = 2
        self.players = playerList
    
    def determine_owner(self):
        newSize = self.size
        newOwner = self.owner
        for player in self.players:
            if player.armySize > newSize:
                newSize = player.armySize
                newOwner = player
        if newOwner != self.owner:
            self.owner.hasLargestArmy = False
            self.owner = newOwner
            self.owner.hasLargestArmy = True
            self.size = newSize


# The Longest Road placard
# Has owner of placard and length of the longest road
# Functions for determining the player with the longest road, for determining the length of the longest
#     stretch connected to a given road (for a specific player), and for reassigning the placard
class LongestRoad(object):
    def __init__(self, playerList):
        self.owner = None
        self.size = 0
        self.players = playerList
    
    def determine_owner(self):
        newOwner = self.owner
        newSize = self.size
        for player in self.players:
            maxRoadLength = 0
            for road in player.builtRoads:
                roadLength = self.explore_players_roads(player, road, 0, [], "")
                if roadLength > maxRoadLength:
                    maxRoadLength = roadLength
            if maxRoadLength > 3 and maxRoadLength > newSize:
                newOwner = player
                newSize = maxRoadLength
        if newOwner != self.owner:
            self.owner.hasLongestRoad = False
            self.owner = newOwner
            self.owner.hasLongestRoad = True
            self.size = newSize
    
    def explore_players_roads(self, playerExploring, entryRoad, roadLength, countedRoads, lastVertex):
        countedRoads.append(entryRoad)
        roadLength += 1
        newLengths = []
        vertexList = [entryRoad.vertex1, entryRoad.vertex2]
        if lastVertex != "":
            vertexList.remove(lastVertex)
        for currentVertex in vertexList:
            if currentVertex.settlement is None or currentVertex.settlement.owner == playerExploring:
                roadList = [someRoad for someRoad in currentVertex.roads if someRoad not in countedRoads]
                if roadList:
                    for branchRoad in roadList:
                        newLengths.append(self.explore_players_roads(playerExploring, branchRoad,
                                                                     roadLength, countedRoads, currentVertex))
        return max([roadLength] + newLengths)


class PlayerKey(object):
    def __init__(self, keyFont, playerList):
        self.background = c.white
        self.box = pygame.Rect(int(round(c.hexEdgeLength/2)), int(round(c.hexEdgeLength/2)), 120, 120)
        self.keyFont = keyFont
        self.title = self.keyFont.render("Player Key", 1, c.black)
        self.titleCoordinates = (int(round(c.hexEdgeLength/2)) + 5, int(round(c.hexEdgeLength/2)))
        defaultColorBox = pygame.Rect(int(round(c.hexEdgeLength/2)) + 5, int(round(c.hexEdgeLength/2)) + 25,
                                      c.colorBoxEdgeLength, c.colorBoxEdgeLength)
        self.colorBoxes = [defaultColorBox.move(0, i * 25) for i in range(4)]
        self.playerColors = [p.color for p in playerList]
        self.playerLabels = [self.keyFont.render(p.name, 1, c.black) for p in playerList]
        self.playerLabelCoordinates = [(int(round(c.hexEdgeLength/2)) + 27,
                                        int(round(c.hexEdgeLength/2)) + 22 + (i * 25)) for i in range(4)]

    def draw(self, surface):
        pygame.draw.rect(surface, self.background, self.box, 0)
        surface.blit(self.title, self.titleCoordinates)
        for i in range(4):
            pygame.draw.rect(surface, self.playerColors[i], self.colorBoxes[i], 0)
            surface.blit(self.playerLabels[i], self.playerLabelCoordinates[i])

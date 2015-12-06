import math
import random
import pygame

lumber = "Wood"
grain = "Wheat"
wool = "Wool"
clay = "Clay"
ore = "Ore"


# A hex piece that defines the board
# Has resource type, number on the hex, whether the hex has the robber on it, and graphical position
class Hex(object):
    def __init__(self, resource, odds, color, coordinates, edgeLength):
        self.resource = resource
        self.odds = odds
        self.color = color
        self.edgeLength = edgeLength
        self.radius = int(round(self.edgeLength * math.sqrt(3) / 2.0))
        self.vertices = [None, None, None, None, None, None]
        self.hasRobber = False
        if resource == "Desert":
            self.hasRobber = True
        self.coordinates = coordinates
        # Set the coordinates of the vertices, starting with the upper left and moving in a clockwise direction
        self.vertexCoordinates = [(self.coordinates[0] - self.radius, self.coordinates[1] - int(round(self.edgeLength / 2.0))), (self.coordinates[0], self.coordinates[1] - self.edgeLength), (self.coordinates[0] + self.radius, self.coordinates[1] - int(round(self.edgeLength / 2.0))), (self.coordinates[0] + self.radius, self.coordinates[1] + int(round(self.edgeLength / 2.0))), (self.coordinates[0], self.coordinates[1] + self.edgeLength), (self.coordinates[0] - self.radius, self.coordinates[1] + int(round(self.edgeLength / 2.0)))]


# A vertex between hexes and/or coasts
# Has list of adjacent hexes, list of adjacent roads, town/city object, port info, and graphical position
class Vertex(object):
    def __init__(self, coordinates):
        self.hexes = []
        self.port = None
        self.settlement = None
        self.roads = []
        self.canBeSettled = True
        self.adjacentVertices = []
        self.coordinates = coordinates


# A town or citiy placed on the vertices
# Has scale (1 for town, 2 for city), owner of settlement, and location
# Function for determining the resources yieled by a dice roll
class Settlement(object):
    def __init__(self, scale, player, edgeLength):
        self.scale = scale
        self.owner = player
        self.vertex = None
        self.edgeLength = edgeLength
    
    def find_yield(self, roll):
        yieldedResources = []
        for hexElement in self.vertex.hexes:
            if hexElement.odds == roll and hexElement.hasRobber == False and hexElement.resource != "Desert":
                yieldedResources += self.scale * [hexElement.resource]
        return yieldedResources

    def draw_settlement(self, screen):
        if self.scale == 1:
#            pygame.draw.rect(screen, (0,0,0), pygame.Rect(self.vertex.coordinates[0] - self.edgeLength / 2 - 1, self.vertex.coordinates[1] - self.edgeLength / 2 - 1, self.edgeLength + 2, self.edgeLength + 2))
            pygame.draw.rect(screen, self.owner.color, pygame.Rect(self.vertex.coordinates[0] - self.edgeLength / 2, self.vertex.coordinates[1] - self.edgeLength / 2, self.edgeLength, self.edgeLength))
        else:
            pass


# A road connecting settlements
# Has owner of road, and the vertices on both ends of the road
class Road(object):
    def __init__(self, player, width):
        self.owner = player
        self.vertex1 = None
        self.vertex2 = None
        self.width = width

    def draw_road(self, screen):
#        pygame.draw.line(screen, (0,0,0), self.vertex1.coordinates, self.vertex2.coordinates, self.width + 1)
        pygame.draw.line(screen, self.owner.color, self.vertex1.coordinates, self.vertex2.coordinates, self.width)


# A port along the coast
# Has resource(s) that can be traded there, and the rate of trade
class Port(object):
    def __init__(self, resources, rate):
        self.resources = resources
        self.rate = rate
        self.cordinates = (0,0)
        self.vertices = []


# The Robber piece
# Has the current location of the Robber
# Functions for moving the Robber and stealing a resource card
class Robber(object):
    def __init__(self, desertHex, radius):
        self.currentHex = desertHex
        self.radius = radius
        self.color = (15,15,15)
        self.coordinates = (self.currentHex.coordinates[0] - int(round(self.radius / 2)), self.currentHex.coordinates[1] - int(round(self.radius / 2)))
    
    def move(self, newHex, screen):
        pygame.draw.circle(screen, self.currentHex.color, self.coordinates, self.radius)
        self.currentHex.hasRobber = False
        self.currentHex = newHex
        newHex.hasRobber = True
        self.coordinates = (self.currentHex.coordinates[0] - int(round(self.radius / 2)), self.currentHex.coordinates[1] - int(round(self.radius / 2)))
        pygame.draw.circle(screen, self.color, self.coordinates, self.radius)
    
    def steal_from(self, playerToRob):
        targetCards = playerToRob.cardsInHand
        targetHand = []
        for key in targetCards.keys():
            targetHand += [key] * targetCards[key]
        if targetHand == []:
            return "Nothing"
        else:
            random.shuffle(targetHand)
            return targetHand[0]

    def play(self, screen, newHex, playerRobbing, playerToRob):
        self.move(newHex, screen)
        if playerToRob == None:
            return "{} moved the Robber and drew nothing from Nobody.".format(playerRobbing.name)
        else:
            newCard = self.steal_from(playerToRob)
            if newCard != "Nothing":
                playerRobbing.cardsInHand.append(newCard)
            return "{} moved the Robber and drew {} from {}.".format(playerRobbing.name, newCard, playerToRob.name)


# A player in the game
# Has identifying variables, point total, list of settlements built and count remaing, list of roads built and
#     count remaining, list of unplayed development cards, count of Knights played, status of owning Longest_Road and
#     Largest_Army, and list of resource cards in hand
# Functions for each action a player can take during their turn
class Player(object):
    def __init__(self, name, color, isAI, settlementEdgeLength, roadWidth):
        self.name = name
        self.color = color
        self.isAI = isAI
        self.points = 0
        self.builtSettlements = []
        self.unbuiltSettlements = [Settlement(1, self, settlementEdgeLength) for x in range(5)]
        self.unbuiltSettlements += [Settlement(2, self, settlementEdgeLength) for x in range(4)]
        self.builtRoads = []
        self.unbuiltRoads = [Road(self, roadWidth) for x in range(15)]
        self.developmentCards = []
        self.armySize = 0
        self.hasLongestRoad = False
        self.hasLargestArmy = False
        self.cardsInHand = {wool: 0, grain: 0, lumber: 0, clay: 0, ore: 0}
    
    def build_town(self, vertexToSettle, screen):
        townCost = [grain, wool, clay, lumber]
        for resource in townCost:
            if self.cardsInHand[resource] == 0:
                return (2, "{} does not have enough resources to build a town.".format(self.name))
        if not vertexToSettle.canBeSettled:
            return (3, "That vertex cannot be built upon.")
        if self.unbuiltSettlements == []:
            return (4, "{} does not have any towns to build.".format(self.name))
        for settlement in self.unbuiltSettlements:
            if settlement.scale == 1:
                self.unbuiltSettlements.remove(settlement)
                self.builtSettlements.append(settlement)
                settlement.vertex = vertexToSettle
                vertexToSettle.settlement = settlement
                for vertex in [vertexToSettle] + vertexToSettle.adjacentVertices:
                    vertex.canBeSettled = False
                for resource in townCost:
                    self.cardsInHand[resource] -= 1
                settlement.draw_settlement(screen)
                return (0, "Success!")
        return (1, "Failed to build the town for an unknown reason.")
    
    def build_city(self, vertexToUpgrade):
        if self.cardsInHand[grain] < 2 or self.cardsInHand[ore] < 3:
            return 1
        if vertexToUpgrade.settlement not in builtSettlements or vertexToUpgrade.settlement.scale == 2:
            return 1
        for settlement in self.unbuiltSettlements:
            if settlement.scale == 2:
                self.unbuiltSettlements.remove(settlement)
                self.builtSettlements.append(settlement)
                self.builtSettlements.remove(vertex.settlement)
                self.unbuiltSettlements.append(vertex.settlement)
                vertex.settlement = settlement
                self.cardsInHand[grain] -= 2
                self.cardsInHand[ore] -= 3
                return 0
        return 1
    
    def build_road(self, vertex1, vertex2, longestRoad, screen):
        if self.cardsInHand[lumber] == 0 or self.cardsInHand[clay] == 0 or self.unbuiltRoads == []:
            return (2, "{} does not have enough resources to build a road.".format(self.name))
        if vertex1 not in vertex2.adjacentVertices:
            return (3, "Those vertices are not adjacent.")
        if vertex1.roads != []:
            for road in vertex1.roads:
                if road.vertex1 == vertex2 or road.vertex2 == vertex2:
                    return (4, "A road already exists along that path.")
        if self.unbuiltRoads == []:
            return (5, "{} does not have any roads to build".format(self.name))
        newRoad = self.unbuiltRoads[0]
        self.unbuiltRoads.remove(newRoad)
        self.builtRoads.append(newRoad)
        newRoad.vertex1 = vertex1
        vertex1.roads.append(newRoad)
        newRoad.vertex2 = vertex2
        vertex2.roads.append(newRoad)
        self.cardsInHand[lumber] -= 1
        self.cardsInHand[clay] -= 1
        longestRoad.determine_owner()
        newRoad.draw_road(screen)
        return (0, "Success!")
    
    def buy_development_card(self, deck):
        if ore in self.cardsInHand and grain in self.cardsInHand and wool in self.cardsInHand:
            newCard = deck.draw()
            if newCard == "Empty":
                return 1
            else:
                self.developmentCards.append(newCard)
                self.cardsInHand.remove(ore)
                self.cardsInHand.remove(grain)
                self.cardsInHand.remove(wool)
                return 0
        else:
            return 1

    def play_knight(self, robber, newHex, playerToRob, largestArmy, screen):
        if "Knight" in self.developmentCards:
            self.armySize += 1
            self.developmentCards.remove("Knight")
            largestArmy.determine_owner()
            return (0, "Success! " + robber.play(screen, newHex, self, playerToRob))
        else:
            return (1, "{} does not have any Knights to play.".format(self.name))
                
    def play_monopoly(self, playerList, resourceWanted):
        if "Monopoly" in self.developmentCards:
            self.developmentCards.remove("Monopoly")
            for player in playerList.remove(self):
                originalHandSize = len(player.cardsInHand)
                player.cardsInHand = [card for card in player.cardsInHand if card != resourceWanted]
                cardsRemoved = originalHandSize - len(player.cardsInHand)
                self.cardsInHand += cardsRemoved * [resourceWanted]
            return 0
        else:
            return 1

    def play_year_of_plenty(self, cardsDesired):
        if "Year of Plenty" in self.developmentCards:
            self.developmentCards.remove("Year of Plenty")
            self.draw_cards(cardsDesired[:2])
            return 0
        else:
            return 1
                
    def play_road_building(self, vertexPair1, vertexPair2):
        if "Road Building" in self.developmentCards:
            for pair in [vertexPair1, vertexPair2]:
                if self.roadsRemaining > 0:
                    if len(pair) > 1:
                        self.build_road(pair[0], pair[1])
                    else:
                        return 1
            return 0
        else:
            return 1

    def offer_trade(self, cardsOffering, cardsRequesting, playersNotified):
        pass
    
    def make_trade(self, cardsGiving, cardsTaking, tradeAgent):
        pass
    
    def discard_cards(self, cardsToDiscard):
        pass
    
    def draw_cards(self, cardsToDraw):
        for card in cardsToDraw:
            self.cardsInHand[card] += 1
    
    def determine_harvest(self, roll):
        harvest = []
        if self.builtSettlements != []:
            for settlement in self.builtSettlements:
                harvest += settlement.find_yield(roll)
            if harvest != []:
                self.draw_cards(harvest)
    
    def count_points(self):
        pass


# The Largest Army placard
# Has owner of placard, size of the largest army, and list of players in the game
# Functions for determining the player with the largest army, and for reassigning the placard
class Largest_Army(object):
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
#     strech connected to a given road (for a specific player), and for reassigning the placard
class Longest_Road(object):
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
            if currentVertex.settlement == None or currentVertex.settlement.owner == playerExploring:
                roadList = [someRoad for someRoad in currentVertex.roads if someRoad not in countedRoads]
                if roadList != []:
                    for branchRoad in roadList:
                        newLengths.append(self.explore_players_roads(playerExploring, branchRoad, roadLength, countedRoads, currentVertex))
        return max([roadLength] + newLengths)


# The deck of undrawn development cards
# Has the shuffled list of cards
# Function for drawing a card from the deck
class Card_Deck(object):
    def __init__(self, cardList):
        self.cardList = cardList
        # For development cards, should be: ["Knight"] * 14 + ["Monopoly", "Year of Plenty", "Road Building"] * 2 + ["Victory Point"] * 5
        # For resources cards, should be 19 of each resource
        random.shuffle(self.cardList)
    
    def draw(self):
        if len(cardList) > 0:
            card = cardList[0]
            if len(cardList) > 0:
                cardList = cardList[1:]
            return card
        else:
            return "Empty"

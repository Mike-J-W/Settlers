
import random

lumber = "Wood"
grain = "Wheat"
wool = "Wool"
clay = "Clay"
ore = "Ore"


# A hex piece that defines the board
# Has resource type, number on the hex, whether the hex has the robber on it, and graphical position
class Hex(object):
    def __init__(self, resource, odds):
        self.resource = resource
        self.odds = odds
        self.hasRobber = False
        if resource == "Desert":
            self.hasRobber = True
        self.coordinates = (0,0)


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
    def __init__(self, scale, player):
        self.scale = scale
        self.owner = player
        self.vertex = None
    
    def find_yield(self, roll):
        yieldedResources = []
        for hexElement in self.vertex.hexes:
            if hexElement.odds == roll and hexElement.hasRobber == False and hexElement.resource != "Desert":
                yieldedResources += self.scale * [hexElement.resource]
        return yieldedResources


# A road connecting settlements
# Has owner of road, and the vertices on both ends of the road
class Road(object):
    def __init__(self, player):
        self.owner = player
        self.vertex1 = None
        self.vertex2 = None


# A port along the coast
# Has resource(s) that can be traded there, and the rate of trade
class Port(object):
    def __init__(self, resources, rate):
        self.resources = resources
        self.rate = rate


# The Robber piece
# Has the current location of the Robber
# Functions for moving the Robber and stealing a resource card
class Robber(object):
    def __init__(self, desertHex):
        self.currentHex = desertHex
    
    def move(self, newHex):
        self.currentHex.hasRobber = False
        self.currentHex = newHex
        newHex.hasRobber = True
    
    def steal_from(self, playerToRob):
        targetCards = playerToRob.cardsInHand
        targetHand = []
        for key in targetCards.keys():
            targetHand += [key] * targetCards[key]
        if targetHand == []:
            return "Empty"
        else:
            random.shuffle(targetHand)
            return targetHand[0]


# A player in the game
# Has identifying variables, point total, list of settlements built and count remaing, list of roads built and
#     count remaining, list of unplayed development cards, count of Knights played, status of owning Longest_Road and
#     Largest_Army, and list of resource cards in hand
# Functions for each action a player can take during their turn
class Player(object):
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
        self.cardsInHand = {wool: 0, grain: 0, lumber: 0, clay: 0, ore: 0}
    
    def build_town(self, vertexToSettle):
        townCost = [grain, wool, clay, lumber]
        for resource in townCost:
            if self.cardsInHand[resource] == 0:
                return 2
        if not vertexToSettle.canBeSettled:
            return 3
        if self.unbuiltSettlements == []:
            return 4
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
                return 0
        return 1
    
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
    
    def build_road(self, vertex1, vertex2, longestRoad):
        if self.cardsInHand[lumber] == 0 or self.cardsInHand[clay] == 0 or self.unbuiltRoads == []:
            return 1
        if vertex1 not in vertex2.adjacentVertices:
            return 1
        if vertex1.roads != []:
            for road in vertex1.roads:
                if road.vertex1 == vertex2 or road.vertex2 == vertex2:
                    return 1
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
        return 0
    
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

    def play_knight(self, robber, newHex, playerToRob, largestArmy):
        if "Knight" in self.developmentCards:
            self.armySize += 1
            self.developmentCards.remove("Knight")
            robber.move(newHex)
            newCard = robber.steal_from(playerToRob)
            if newCard != "Empty":
                self.cardsInHand.append(newCard)
            largestArmy.determine_owner()
        else:
            return 1
                
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
        self.size = 0
        self.players = playerList
    
    def determine_owner(self):
        newSize = self.size
        newOwner = self.owner
        for player in self.players:
            if player.armySize > newSize:
                newSize = player.armySize
                newOwner = player
        if newOwner != self.Owner:
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

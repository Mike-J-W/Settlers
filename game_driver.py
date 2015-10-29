
import random

lumber = "Wood"
grain = "Wheat"
wool = "Wool"
clay = "Clay"
ore = "Ore"


# A hex piece that defines the board
# Has resource type, number on the hex, and whether the hex has the robber on it
class Hex(object):
    def __init__(self, resource, odds):
        self.resource = resource
        self.odds = odds
        self.hasRobber = False
        if resource == "Desert":
            self.hasRobber = True


# A vertice between hexes and/or coasts
# Has list of adjacent hexes, list of adjacent roads, town/city object, and port info
class Intersection(object):
    def __init__(self, hexList, port):
        self.hexes = hexList
        self.port = port
        self.settlement = None
        self.roads = []
        self.isEmpty = True


# A town or citiy placed on the intersections
# Has scale (1 for town, 2 for city), owner of settlement, and location
# Function for determining the resources yieled by a dice roll
class Settlement(object):
    def __init__(self, player, intersection):
        self.scale = 1
        self.owner = player
        self.intersection = None
    
    def find_yield(self, roll):
        yieldedResources = []
        for hexElement in self.intersection.hexes:
            if hexElement.odds == roll and hexElement.hasRobber == False and hexElement.resource != "Desert":
                yieldedResources += self.scale * [hexElement.resource]
        return yieldedResources


# A road connecting settlements
# Has owner of road, and the intersections on both ends of the road
class Road(object):
    def __init__(self, player, intersection1, intersection2):
        self.owner = player
        self.intersection1 = intersection1
        self.intersection2 = intersection2


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
        pass


# A player in the game
# Has identifying variables, point total, list of settlements built and count remaing, list of roads built and
#     count remaining, list of unplayed development cards, count of Knights played, status of owning Longest_Road and
#     Largest_Army, and list of resource cards in hand
# Functions for each action a player can take during their turn
class Player(object):
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.points = 0
        self.builtSettlements = []
        self.unbuiltSettlements = []
        self.builtRoads = []
        self.unbuiltRoads = []
        self.developmentCards = []
        self.armySize = 0
        self.hasLongestRoad = False
        self.hasLargestArmy = False
        self.cardsInHand = {wool: 0, grain: 0, lumber: 0, clay: 0, ore: 0}
    
    def build_town(self, intersection):
        townCost = [grain, wool, clay, lumber]
        for resource in townCost:
            if self.cardsInHand[resource] == 0:
                return 1
        if not intersection.isEmpty or self.unbuiltSettlements == []:
            return 1
        for settlement in self.unbuiltSettlements:
            if settlement.scale == 1:
                self.unbuiltSettlements.remove(settlement)
                self.builtSettlements.append(settlement)
                settlement.intersection = intersection
                intersection.settlement = settlement
                intersection.isEmpty = False
                for resource in townCost:
                    self.cardsInHand[resource] -= 1
                return 0
        return 1
    
    def build_city(self, intersectionToUpgrade):
        if self.cardsInHand[grain] < 2 or self.cardsInHand[ore] < 3:
            return 1
        if intersectionToUgrade.settlement not in builtSettlements or intersectionToUpgrade.settlement.scale == 2:
            return 1
        for settlement in self.unbuiltSettlements:
            if settlement.scale == 2:
                self.unbuiltSettlements.remove(settlement)
                self.builtSettlements.append(settlement)
                self.builtSettlements.remove(intersection.settlement)
                self.unbuiltSettlements.append(intersection.settlement)
                intersection.settlement = settlement
                self.cardsInHand[grain] -= 2
                self.cardsInHand[ore] -= 3
                return 0
        return 1
    
    def build_road(self, intersection1, intersection2):
        if self.cardsInHand[lumber] == 0 or self.cardsInHand[clay] == 0 or self.unbuiltRoads == []:
            return 1
        if intersection1.roads != []:
            for road in intersection1.roads:
                if road.intersection1 == intersection2 or road.intersection2 == intersection2:
                    return 1
        newRoad = self.unbuiltRoads[0]
        self.unbuiltRoads.remove(newRoad)
        self.builtRoads.append(newRoad)
        newRoad.intersection1 = intersection1
        intersection1.roads.append(newRoad)
        newRoad.intersection2 = intersection2
        intersection2.raods.append(newRoad)
        self.cardsInHand[lumber] -= 1
        self.cardsInHand[clay] -= 1
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
                
    def play_road_building(self, intersectionPair1, intersectionPair2):
        if "Road Building" in self.developmentCards:
            for pair in [intersectionPair1, intersectionPair2]:
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
        pass
    
    def determine_harvest(self, roll):
        pass
    
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
        pass
    
    def change_possession(self, newOwner):
        pass


# The Longest Road placard
# Has owner of placard and length of the longest road
# Functions for determining the player with the longest road, for determining the length of the longest
#     strech connected to a given road (for a specific player), and for reassigning the placard
class Longest_Road(object):
    def __init__(self):
        self.owner = None
        self.size = 0
    
    def determine_owner(self, players):
        pass
    
    def explore_players_roads(playerExploring, entryRoad, roadLength, countedRoads, lastIntersection):
        countedRoads.append(entryRoad)
        roadLength += 1
        newLengths = []
        intersectionList = [entryRoad.intersection1, entryRoad.intersection2]
        if lastIntersection != "":
            intersectionList.remove(lastIntersection)
        for currentIntersection in intersectionList:
            if currentIntersection.settlement.owner == playerExploring or currentIntersection.settlement.owner == None:
                roadList = [someRoad for someRoad in currentIntersection.roads if someRoad not in countedRoads]
                if roadList != []:
                    for branchRoad in roadList:
                        newLengths.append(explore_players_roads(playerExploring, branchRoad, roadLength, countedRoads, currentIntersection))
        return max([roadLength] + newLengths)
    
    def change_possession(self, newOwner):
        pass


# The deck of undrawn development cards
# Has the shuffled list of cards
# Function for drawing a card from the deck
class Development_Card_Deck(object):
    def __init__(self):
        self.cardList = ["Knight"] * 14 + ["Monopoly", "Year of Plenty", "Road Building"] * 2 + ["Victory Point"] * 5
        random.shuffle(self.cardList)
    
    def draw(self):
        if len(cardList) > 0:
            card = cardList[0]
            if len(cardList) > 0:
                cardList = cardList[1:]
            return card
        else:
            return "Empty"


import random

lumber = "Wood"
grain = "Wheat"
wool = "Wool"
clay = "Clay"
ore = "Ore"

class Hex(object):
    def __init__(self, resource, odds):
        self.resource = resource
        self.odds = odds
        self.hasRobber = False
        if resource == "Desert":
            self.hasRobber = True


class Intersection(object):
    def __init__(self, hexList, port):
        self.hexes = hexList
        self.port = port
        self.settlement = None
        self.roads = []
        self.buildable = True


class Settlement(object):
    def __init__(self, player, intersection):
        self.scale = 1
        self.owner = player
        self.intersection = intersection
    
    def upgrade(self):
        if self.scale == 1:
            self.scale = 2
            return 0
        else:
            return 1

def find_yield(self, roll):
    yieldedResources = []
        for hexElement in self.intersection.hexes:
            if hexElement.odds == roll and hexElement.hasRobber == False and hexElement.resource != "Desert":
                yieldedResources += self.scale * [hexElement.resource]
        return yieldedResources


class Road(object):
    def __init__(self, player, intersection1, intersection2):
        self.owner = player
        self.intersection1 = intersection1
        self.intersection2 = intersection2


class Port(object):
    def __init__(self, resources, rate):
        self.resources = resources
        self.rate = rate


class Robber(object):
    def __init__(self, desertHex):
        self.currentHex = desertHex
    
    def move(self, newHex):
        self.currentHex.hasRobber = False
        self.currentHex = newHex
        newHex.hasRobber = True
    
    def steal_from(self, playerToRob):
        pass


class Player(object):
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.points = 0
        self.settlements = []
        sef.townsRemaining = 5
        self.citiesRemaing = 4
        self.roads = []
        self.roadsRemaining = 15
        self.developmentCards = []
        self.armySize = 0
        self.hasLongestRoad = False
        self.hasLargestArmy = False
        self.cardsInHand = []
    
    def build_town(self, intersection):
        pass
    
    def build_city(self, townToUpgrade):
        pass
    
    def build_road(self, intersection1, intersection2):
        pass
    
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


class Largest_Army(object):
    def __init__(self, playerList):
        self.owner = None
        self.size = 0
        self.players = playerList
    
    def determine_owner(self):
        pass
    
    def change_possession(self, newOwner):
        pass


class Longest_Road(object):
    def __init__(self):
        self.owner = None
        self.size = 0
    
    def determine_owner(self, players):
        pass
    
    def explore_roads(length, road, countedRoads, lastIntersection):
        countedRoads.append(road)
        length += 1
        newLengths = []
        intersectionList = [road.intersection1, road.intersection2]
        if lastIntersection != "":
            intersectionList.remove(lastIntersection)
        for currentIntersection in intersectionList:
            if currentIntersection.settlement.owner == currentPlayer or currentIntersection.settlement.owner == None:
                roadList = [someRoad for someRoad in currentIntersection.roads if someRoad not in countedRoads]
                if roadList != []:
                    for branchRoad in roadList:
                        newLengths.append(explore_roads(length, branchRoad, countedRoads, currentIntersection))
        return max([length] + newLengths)
    
    def change_possession(self, newOwner):
        pass


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

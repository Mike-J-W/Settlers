"""Define the pieces and other persistent objects in the game"""

import math
import random
import pygame
import constants as c


class Hex(object):
    """A hexagonal tile piece that forms part of the game board.

    :param resource: The resource type yielded by the tile during harvest
    :param odds: The dice roll that triggers a harvest of this tile's resource
    :param color: The color of the tile
    :param coordinates: The graphical location of the tile
    :ivar edgeLength: The length of 1 side of the tile
    :ivar radius: The distance from the center of the tile to any vertex of the tile
    :ivar vertices: A list of the Vertex objects for the vertices of the tile
    :ivar hasRobber: True if the Robber is on the tile; False otherwise
    :ivar vertexCoordinates: A list of the graphical locations of the tile's vertices
    """

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


class Vertex(object):
    """A representation for the vertices of the tiles.

    :param coordinates: The graphical location of the vertex
    :ivar port: The trading port connected to this vertex, if applicable
    :ivar settlement: The player settlement on the vertex, if applicable
    :ivar roads: A list of the roads connected to the vertex
    :ivar canBeSettled: False if under or adjacent to a settlement; True otherwise
    :ivar adjacentVertices: The closest vertices in each direction
    """

    def __init__(self, coordinates):
        self.hexes = []
        self.port = None
        self.settlement = None
        self.roads = []
        self.canBeSettled = True
        self.adjacentVertices = []
        self.coordinates = coordinates


class Settlement(object):
    """A representation of the settlements built by the players.

    :param scale: The type of settlement - 1 for town, 2 for city
    :param player: The owner of the settlement
    :ivar vertex: The vertex on which the settlement is built, if applicable
    :ivar edgeLength: The length of 1 side of the square representing the settlement when scale = 1
    :ivar circumradius: The distance from the center of the pentagon (when scale = 2) to 1 of the pentagon's vertices
    """

    def __init__(self, scale, player):
        self.scale = scale
        self.owner = player
        self.vertex = None
        self.edgeLength = c.settlementEdgeLength
        self.circumradius = int(round(math.sqrt(50 + 10 * math.sqrt(5)) * self.edgeLength / 10))
    
    def find_yield(self, roll):
        """Check surrounding hex tiles for odds that match the roll and return resources accordingly."""
        yieldedResources = dict(zip(c.resourceTypes, [0, 0, 0, 0, 0]))
        for hexTile in self.vertex.hexes:
            if hexTile.odds == roll and not hexTile.hasRobber and hexTile.resource != "Desert":
                yieldedResources[hexTile.resource] += self.scale
        return yieldedResources

    def draw_settlement(self, surface):
        """Place image (square for town, pentagon for city) of settlement over its vertex, in the owner's color."""
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


class Road(object):
    """A representation of the roads built by the players.

    :param player: The owner of the road
    :ivar vertex1: The vertex at one of the road's endpoints, if applicable
    :ivar vertex2: The vertex at the other endpoint, if applicable
    :ivar width: The thickness of the line representing the road on the board
    """

    def __init__(self, player):
        self.owner = player
        self.vertex1 = None
        self.vertex2 = None
        self.width = c.roadWidth

    def draw_road(self, surface):
        """Place image of road along the edge between its vertices in the owner's color."""
        pygame.draw.line(surface, self.owner.color, self.vertex1.coordinates, self.vertex2.coordinates, self.width)


class Port(object):
    """A representation of the trading ports along the coast.

    :param resources: The resources affected the port
    :param rate: The trade ratio granted by the port
    :ivar vertices: The vertices affected by the port
    """

    def __init__(self, resources, rate):
        self.resources = resources
        self.rate = rate
        self.vertices = []

    def draw_port(self, surface, color):
        """Place image of port (triangle) off the coast in between the two vertices that can access it and
           color according to the resources the port affects."""
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


class Robber(object):
    """A representation of the Robber game piece.

    :param desertHex: The Hex of the desert tile
    :ivar radius: The radius of the circle used to represent the Robber on the board
    :ivar color: The color of the circle used to represent the Robber on the board
    :ivar coordinates: The graphical location of the center of the circle representing the Robber on the board
    """

    def __init__(self, desertHex):
        self.currentHex = desertHex
        self.radius = c.robberRadius
        self.color = (15, 15, 15)
        self.coordinates = (self.currentHex.coordinates[0] - int(round(self.radius / 2)),
                            self.currentHex.coordinates[1] - int(round(self.radius / 2)))
    
    def move(self, newHex, surface):
        """Alter the board image and properties of the Robber such that it changes position."""
        pygame.draw.circle(surface, self.currentHex.color, self.coordinates, self.radius)
        self.currentHex.hasRobber = False
        self.currentHex = newHex
        newHex.hasRobber = True
        self.coordinates = (self.currentHex.coordinates[0] - int(round(self.radius / 2)),
                            self.currentHex.coordinates[1] - int(round(self.radius / 2)))
        self.draw_robber(surface)

    def steal_from(self, playerToRob):
        """Take a random resource card from the targeted player."""
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
        """Combine Robber functions into a complete game action."""
        self.move(newHex, surface)
        if playerToRob is None:
            return "{} moved the Robber and drew nothing from Nobody.".format(playerRobbing.name)
        else:
            newCard = self.steal_from(playerToRob)
            if newCard != "Nothing":
                playerRobbing.cardsInHand[newCard] += 1
            return "{} moved the Robber and drew {} from {}.".format(playerRobbing.name, newCard, playerToRob.name)

    def draw_robber(self, surface):
        """Draws image of the Robber (circle) at its location."""
        pygame.draw.circle(surface, self.color, self.coordinates, self.radius)


class Player(object):
    """A representation of and the data for the players participating in the game.

    :param name: The identifier of the player
    :param color: The color to be used for the player's infrastructure and identification
    :param isAI: False if the player is a human; True if the player is a bot
    :ivar points: The game points accumulated by the player
    :ivar builtSettlements: A list of the settlements that the player has built
    :ivar unbuiltSettlements: A list of the settlements available to be built by the player
    :ivar builtRoads: A list of the roads that the player has built
    :ivar unbuiltRoads: A list of the roads available to be built by the player
    :ivar newDevelopmentCards: A list of the Development Cards bought by the player during the current turn
    :ivar developmentCards: A list of the Development Cards bought by the player before the current turn
    :ivar hasPlayedKnight: True if the player used a Knight in the current turn; False if not
    :ivar armySize: A count of the Knights played by the player
    :ivar hasLongestRoad: True if the player meets the game criteria for Longest Road; False otherwise
    :ivar hasLargestArmy: True if the player meets the game criteria for Largest Army; False otherwise
    :ivar cardsInHand: A dictionary tracking the number of each resource in the player's hand
    :ivar tradeRatios: A dictionary of the trade ratio available to the player for each resource
    :ivar log: A list of the log messages relevant to the player
    """

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
        self.newDevelopmentCards = []
        self.developmentCards = []
        self.hasPlayedKnight = False
        self.armySize = 0
        self.hasLongestRoad = False
        self.hasLargestArmy = False
        self.cardsInHand = {c.wool: 0, c.grain: 0, c.lumber: 0, c.clay: 0, c.ore: 0}
        self.tradeRatios = {c.wool: 4, c.grain: 4, c.lumber: 4, c.clay: 4, c.ore: 4}
        self.log = []

    def can_afford(self, cost):
        for resource in cost.keys():
            if self.cardsInHand[resource] < cost[resource]:
                return False
        return True

    def has_unbuilt_town(self):
        if self.unbuiltSettlements:
            towns = [settlement for settlement in self.unbuiltSettlements if settlement.scale == 1]
            if towns:
                return True
        return False

    def has_unbuilt_city(self):
        if self.unbuiltSettlements:
            cities = [settlement for settlement in self.unbuiltSettlements if settlement.scale == 2]
            if cities:
                return True
        return False

    def has_unbuilt_road(self):
        if self.unbuiltRoads:
            return True
        return False      

    def has_dev_card(self, card):
        if card in self.developmentCards:
            return True
        return False

    def has_new_dev_card(self, card):
        if card in self.newDevelopmentCards:
            return True
        return False

    def get_dev_card_count(self, card):
        return self.developmentCards.count(card) + self.newDevelopmentCards.count(card)
    
    def build_town(self, vertexToSettle, resourceDecks, surface):
        """After checks, place town on a vertex and change player data accordingly, including discarding resources."""
        if not self.can_afford(c.townCost):
                return (2, "{} cannot afford to build a town.".format(self.name))
        if not vertexToSettle.canBeSettled:
            return (3, "That vertex cannot be built upon.")
        if not self.has_unbuilt_town():
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
                self.discard_resources(c.townCost, resourceDecks)
                settlement.draw_settlement(surface)
                if settlement.vertex.port is not None:
                    for rsc in settlement.vertex.port.resources:
                        if self.tradeRatios[rsc] > settlement.vertex.port.rate:
                            self.tradeRatios[rsc] = settlement.vertex.port.rate
                return (0, "Success!")
        return (1, "Failed to build the town for an unknown reason.")
    
    def build_city(self, vertexToUpgrade, resourceDecks, surface):
        """After checks, put city over a town and change player data accordingly, including discarding resources."""
        if not self.can_afford(c.cityCost):
            return (2, "{} cannot afford to upgrade a settlement".format(self.name))
        if not self.has_unbuilt_city:
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
                self.discard_resources(c.cityCost, resourceDecks)
                settlement.draw_settlement(surface)
                return (0, "Success!")
        return (1, "Failed to upgrade the settlement for an unknown reason")
   
    def build_road(self, vertex1, vertex2, longestRoad, resourceDecks, surface):
        """After checks, places road between vertices and changes player data accordingly."""
        if not self.can_afford(c.roadCost):
            return (3, "{} cannot afford to build a road.".format(self.name))
        if not self.unbuiltRoads:
            return (2, "{} does not have any roads to build".format(self.name))
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
        self.discard_resources(c.roadCost, resourceDecks)
        longestRoad.determine_owner()
        newRoad.draw_road(surface)
        return (0, "Success!")
    
    def buy_development_card(self, developmentDeck, resourceDecks):
        """After checks, exchange resources for development card and alter player data and card decks accordingly."""
        if not self.can_afford(c.developmentCardCost):
            return (1, "{} cannot afford to buy a Development Card.".format(self.name))
        if len(developmentDeck) == 0:
            return (2, "The deck of Development Cards is empty.")
        newCard = developmentDeck.popleft()
        self.newDevelopmentCards.append(newCard)
        self.discard_resources(c.developmentCardCost, resourceDecks)
        return (0, "Success! {} bought a {}.".format(self.name, newCard))

    def consume_dev_card(self, card):
        if not self.has_dev_card(card):
            return (1, "{} does not have a {} card to consume.".format(self.name, card))
        self.developmentCards.remove(card)
        if card == "Knight":
            self.armySize += 1
            self.hasPlayedKnight = True
        return (0, "{} consumed a {} card.".format(self.name, card))

    def offer_trade(self, cardsOffering, cardsRequesting, playersNotified):
        pass
    
    def make_player_trade(self, cardsGiving, cardsTaking, tradeAgent):
        pass

    def discard_resources(self, cardsToDiscard, resourceDecks):
        for resource in cardsToDiscard.keys():
            if cardsToDiscard[resource] > self.cardsInHand[resource]:
                return (1, "{} does not have {} {} cards to discard.".format(self.name,
                                                                             cardsToDiscard[resource], resource))
        for resource in cardsToDiscard.keys():
            self.cardsInHand[resource] -= cardsToDiscard[resource]
            resourceDecks[resource] += cardsToDiscard[resource]
        return (0, "Success!")
    
    def draw_resources(self, cardsToDraw, resourceDecks):
        for resource in cardsToDraw.keys():
            if cardsToDraw[resource] > resourceDecks[resource]:
                return (1, "There are not {} {} cards available.".format(cardsToDraw[resource], resource))
        for resource in cardsToDraw.keys():
            self.cardsInHand[resource] += cardsToDraw[resource]
            resourceDecks[resource] -= cardsToDraw[resource]
        return(0, "Success!")

    def determine_harvest(self, roll, resourceDecks):
        harvest = []
        if self.builtSettlements:
            for settlement in self.builtSettlements:
                harvest += settlement.find_yield(roll)
            if harvest:
                harvestDict = {c.grain: 0, c.ore: 0, c.wool: 0, c.clay: 0, c.lumber: 0}
                for resource in c.resourceTypes:
                    harvestDict[resource] = harvest.count(resource)
                self.draw_resources(harvestDict, resourceDecks)
    
    def count_points(self):
        pointCounter = 0
        if self.builtSettlements:
            for settlement in self.builtSettlements:
                pointCounter += settlement.scale
        if self.developmentCards:
            pointCounter += self.developmentCards.count("Victory Point")
        if self.hasLargestArmy:
            pointCounter += 2
        if self.hasLongestRoad:
            pointCounter += 2
        self.points = pointCounter
        return pointCounter


class LargestArmy(object):
    """A manager for the Largest Army award.

    :param playerList: A list of the player objects active in the game
    :ivar owner: The player in possession of the Largest Army, if applicable
    :ivar size: The size of the largest army
    """

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


class LongestRoad(object):
    """A manager for the Longest Road award.

    :param playerList: A list of the player objects active in the game
    :ivar owner: The player in possession of the Longest Road, if applicable
    :ivar size: The length of the longest road
    """

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
            if maxRoadLength > 4 and maxRoadLength > newSize:
                newOwner = player
                newSize = maxRoadLength
        if newOwner != self.owner:
            if self.owner is not None:
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
    """A key to relate visually player names and player colors for the benefit of human players.

    :param keyFont: The font in which to write the player names
    :param playerList: A list of the player objects active in the game
    :ivar background: The background color of the key
    :ivar box: The pygame Rect defining the shape and location of the key
    :ivar title: The heading of the key
    :ivar titleCoordinates: The graphical location of the title
    :ivar colorBoxes: A list of the boxes used to show the player colors in the key
    :ivar playerColors: A list of the colors for each player
    :ivar playerLabelCoordinates: A list of the graphical locations for each player's name
    """

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

import math
import random

# Player Colors
forestGreen = (34, 139, 34)
oceanBlue = (0, 0, 120)
wheatYellow = (244, 233, 19)
woolGreen = (144, 238, 144)
clayColor = (173, 77, 8)
rockGray = (128, 128, 128)
sandyDesert = (211, 208, 143)
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 242)
playerRed = (213, 5, 46)
playerBlue = (102, 207, 245)
playerGreen = (90, 206, 48)
playerPurple = (149, 58, 172)
playerWhite = (255, 255, 255)
playerOrange = (255, 182, 71)

# Set the colors
playerColors = {"red": playerRed, "blue": playerBlue, "green": playerGreen, "purple": playerPurple,
                "white": playerWhite, "orange": playerOrange}

# The menus dictionary
preHarvestMenu = dict(
    zip(["Harvest your resources (AKA roll the dice)", "Play a Knight (if possible) and then harvest resources"],
        ["roll_dice(player)", "play_knight(player,robber,hexes,largestArmy,boardSurface,playerKey)"]))
postHarvestMenu = dict(
    zip(["Build a road", "Build a settlement", "Upgrade a settlement", "Buy a development card", "Play a knight",
         "Play a monopoly card", "Play a year of plenty card", "Play a road building card", "Make a maritime trade",
         "Offer a trade to players", "End turn"],
        ["build_road(player, vertices, longestRoad, resourceDecks, boardSurface, playerKey)",
         "build_settlement(player, vertices, resourceDecks, boardSurface, playerKey)",
         "upgrade_settlement(player, vertices, resourceDecks, boardSurface, playerKey)",
         "buy_development_card(player, resourceDecks, developmentDeck)", "play_knight()", "play_monopoly()",
         "play_yop_card(player, resourceDecks)", "play_road_building()", "maritime_trade()", "offer_trade()",
         "end_turn(player)"]))

# Set the piece and image sizes
# The length of a side of a hex
hexEdgeLength = 60
# The distance from a hex's center to the midpoint of an edge
hexRadius = int(round(hexEdgeLength * math.sqrt(3) / 2.0))
# The width of a town
settlementEdgeLength = int(round(hexEdgeLength / 4))
# The width of a road
roadWidth = int(round(settlementEdgeLength / 3))
# The radius of the circle denoting the Robber
robberRadius = int(settlementEdgeLength)
colorBoxEdgeLength = 12
oceanWidth = hexRadius * 10 + hexEdgeLength * 4
oceanHeight = hexEdgeLength * 12
oceanSize = (oceanWidth, oceanHeight)
gameMenuWidth = 240
gameEventLogWidth = 240
# The size of the window that is opened
screenSize = (oceanWidth + gameEventLogWidth + gameMenuWidth, oceanHeight)

# The resource and card variables
lumber = "Wood"
grain = "Wheat"
wool = "Wool"
clay = "Clay"
ore = "Ore"
desert = "Desert"
# A list of the resources in the game
resourceTypes = [lumber, grain, wool, clay, ore]
# A dictionary relating resources to colors
resourceToColor = {lumber: forestGreen, grain: wheatYellow, wool: woolGreen, clay: clayColor, ore: rockGray,
                   desert: sandyDesert}
# A list with one element per development card
developmentDeckList = ["Knight"] * 14 + ["Monopoly", "Year of Plenty", "Road Building"] * 2 + ["Victory Point"] * 5
random.shuffle(developmentDeckList)
# A list representing the number of hexes per resource
resourcesForHexes = [lumber] * 4 + [grain] * 4 + [wool] * 4 + [clay] * 3 + [ore] * 3
random.shuffle(resourcesForHexes)

townCost = {grain: 1, wool: 1, clay: 1, lumber: 1}
cityCost = {grain: 3, ore: 2}
roadCost = {clay: 1, lumber: 1}
developmentCardCost = {grain: 1, ore: 1, wool: 1}

# Making the odds tiles placed on top of the hexes
# A list of the numbered, circular tiles denoting times of harvest
odds = [6, 6, 8, 8, 2, 3, 3, 4, 4, 5, 5, 9, 9, 10, 10, 11, 11, 12]
# A list of the indices of the odds tiles
indices = [i for i in range(19)]
# A list of hexes next to the hex represented by the index of the larger list (e.g. hex 0 is adjacent to hexes [1,3,4])
adjacents = [[1, 3, 4], [0, 2, 4, 5], [1, 5, 6], [0, 4, 7, 8], [0, 1, 3, 5, 8, 9], [1, 2, 4, 6, 9, 10], [2, 5, 10, 11],
             [3, 8, 12], [3, 4, 7, 9, 12, 13], [4, 5, 8, 10, 13, 14], [5, 6, 9, 11, 14, 15], [6, 10, 15],
             [7, 8, 13, 16], [8, 9, 12, 14, 16, 17], [9, 10, 13, 15, 17, 18], [10, 11, 14, 18], [12, 13, 17],
             [13, 14, 16, 18], [14, 15, 17]]

# The unadjusted coordinates of the centers of the hexes
baseHexCenters = [(3, 1), (5, 1), (7, 1), (2, 2.5), (4, 2.5), (6, 2.5), (8, 2.5), (1, 4), (3, 4), (5, 4), (7, 4),
                  (9, 4), (2, 5.5), (4, 5.5), (6, 5.5), (8, 5.5), (3, 7), (5, 7), (7, 7)]
# The centers of the hexes adjusted for the length of their sides
hexCenters = [
    (int(2 * hexEdgeLength + baseHexCenters[i][0] * hexRadius), int((baseHexCenters[i][1] + 2) * hexEdgeLength)) for i
    in range(len(baseHexCenters))]

# Making the odds tiles placed on top of the hexes
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
        # If the index is valid, assign the odd to that index in the ordered odds list and
        # remove the index from the list as seen by later iterations of the loop
        if goodIndex:
            oddsOrdered[newIndex] = o
            indices.remove(newIndex)
            oddPlaced = True
# Get the index of the 0-odd tile and insert "Desert" at that index in the resources list
desertIndex = oddsOrdered.index(0)
resourcesForHexes.insert(desertIndex, "Desert")

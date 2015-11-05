from pieces import *

def main():

    lumber = "Wood"
    grain = "Wheat"
    wool = "Wool"
    clay = "Clay"
    ore = "Ore"
    resources = [lumber, grain, wool, clay, ore]
    
    # Initialize all the game pieces
    developmentDeck = Card_Deck(["Knight"] * 14 + ["Monopoly", "Year of Plenty", "Road Building"] * 2 + ["Victory Point"] * 5)
    resourceDecks = {}
    for resource in resources:
        resourceDecks[resource] = [resource] * 19
    




if __name__ == "__main__":
    main()
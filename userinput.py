import pygame
import constants as c
import geometricfunctions as gf


def get_rect_from_player(player, rectList):
    # Loop until the user clicks on a vertex
    validClick = False
    while not validClick:
        # Make sure no other events are on the queue
        pygame.event.clear()
        # Prompt the user for a click and wait for two events
        print("{} please click a option.".format(player.name))
        chosenRect = None
        eventA = pygame.event.wait()
        eventB = pygame.event.wait()
        # If the next two events are the mouse being pressed down and then released, move forward
        if eventA.type == pygame.MOUSEBUTTONDOWN and eventB.type == pygame.MOUSEBUTTONUP:
            posA = eventA.__dict__['pos']
            posB = eventB.__dict__['pos']
            # If the mouse actions (pressed down, released) were no more than 10 pixels apart, move forward
            if gf.pp_distance(posA, posB) < 10:
                # Loop through the rects to see if the click ocurred inside one
                for rect in rectList:
                    # If both mouse actions ocurred inside the current hex, move forward
                    if gf.is_within_rect(rect, posA) and gf.is_within_rect(rect, posB):
                        # Record the rect, switch the boolean to end the while loop, and break the rect loop
                        chosenRect = rect
                        validClick = True
                        break
                if not validClick:
                    print("That click was not inside a rect. Please try again.")
            else:
                print("The mouse moved while pressed down. Please try again.")
    return chosenRect


# A function to get a vertex chosen by the player
# Takes the player choosing and the list of vertices
def get_vertex_from_player(player, vertexList, playerKey):
    # Check if the player is an AI or human
    if player.isAI:
        pass
    else:
        # Loop until the user clicks on a vertex
        validClick = False
        while not validClick:
            # Make sure no other events are on the queue
            pygame.event.clear()
            # Prompt the user for a click and wait for two events
            print("{} please click a vertex. Or click the Player Key to select nothing.".format(player.name))
            eventA = pygame.event.wait()
            eventB = pygame.event.wait()
            # If the next two events are the mouse being pressed down and then released, move forward
            if eventA.type == pygame.MOUSEBUTTONDOWN and eventB.type == pygame.MOUSEBUTTONUP:
                # Get the coordinates of the clicks
                posA = eventA.__dict__['pos']
                posB = eventB.__dict__['pos']
                # Get the coordinates of each vertex on the board
                vertexCoords = [v.coordinates for v in vertexList]
                # Get coordinates of the vetices closest to where the mouse was pressed down and where it was released
                verCoordA = gf.get_closest_point(vertexCoords, posA)
                verCoordB = gf.get_closest_point(vertexCoords, posB)
                # If the two coordinates are the same and both events happened within 10 pixels each other, move forward
                if verCoordA[0] == verCoordB[0] and abs(verCoordA[1] - verCoordB[1]) < 10:
                    # If the click was inside the Player Key, return to the previous menu without a selection
                    if gf.is_within_rect(playerKey.box, posA) and gf.is_within_rect(playerKey.box, posB):
                        closestVertex = None
                        validClick = True
                        print("{} did not choose a vertex.".format(player.name))
                    else:
                        # If the mouse action (pressed down, released) happened within 10 pixels of
                        # the closest vertex, move forward
                        if verCoordA[1] <= 10 and verCoordB[1] <= 10:
                            # With all condiitions satisfied, find the vertex corresponding to the coordinates found
                            closestVertex = vertexList[vertexCoords.index(verCoordA[0])]
                            validClick = True
                        else:
                            print("That click was not close enough to a vertex. Please try again.")
                else:
                    print("The mouse moved while pressed down. Please try again.")
        return closestVertex


# A function to get a hex chosen by the player
# Takes the player choosing and the list of board hexes
def get_hex_from_player(player, hexList, playerKey):
    # Check if the player is an AI or human
    if player.isAI:
        pass
    else:
        # Loop until the user clicks on a vertex
        validClick = False
        while not validClick:
            # Make sure no other events are on the queue
            pygame.event.clear()
            # Prompt the user for a click and wait for two events
            print("{} please click a hex. Or click the Player Key to select nothing.".format(player.name))
            chosenHex = None
            eventA = pygame.event.wait()
            eventB = pygame.event.wait()
            # If the next two events are the mouse being pressed down and then released, move forward
            if eventA.type == pygame.MOUSEBUTTONDOWN and eventB.type == pygame.MOUSEBUTTONUP:
                posA = eventA.__dict__['pos']
                posB = eventB.__dict__['pos']
                # If the mouse actions (pressed down, released) were no more than 10 pixels apart, move forward
                if gf.pp_distance(posA, posB) < 10:
                    # If the click was inside the Player Key, return to the previous menu without a selection
                    if gf.is_within_rect(playerKey.box, posA) and gf.is_within_rect(playerKey.box, posB):
                        chosenHex = None
                        validClick = True
                        print("{} did not choose a hex.".format(player.name))
                    else:
                        # Loop through the hexes to see if the click ocurred inside one
                        for hexTile in hexList:
                            # If both mouse actions ocurred inside the current hex, move forward
                            if gf.is_within_hex(hexTile, posA) and gf.is_within_hex(hexTile, posB):
                                # Record the hex, switch the boolean to end the while loop, and break the hex loop
                                chosenHex = hexTile
                                validClick = True
                                break
                        if not validClick:
                            print("That click was not inside a hex. Please try again.")
                else:
                    print("The mouse moved while pressed down. Please try again.")
        return chosenHex


def present_menu(player, menuDict, titleContent, surface, titleFont, infoFont):
    if player.isAI:
        pass
    else:
        chosenOpt = present_graphical_menu(player, menuDict, titleContent, surface, titleFont, infoFont)
        choice = menuDict[chosenOpt]
        surface.fill(c.white)
        pygame.display.update(surface.get_rect())
        '''
        print("The available options are:")
        menuOpts = sorted(list(menuDict.keys()))
        for i, e in enumerate(menuOpts):
            print("\t{}\t{}".format(i, e))

        validOptionFound = False
        while not validOptionFound:
            option = input("Please choose an option: ")
            try:
                optIndex = int(option)
            except:
                print("not an integer.  try again")
                continue
            try:
                optKey = menuOpts[optIndex]
            except:
                print("not a valid option.  try again")
                continue
            choice = menuDict[optKey]
            validOptionFound = True
        '''
        return choice


def present_graphical_menu(player, menuDict, titleContent, surface, titleFont, infoFont):
    surface.fill(c.white)
    pygame.display.update(surface.get_rect())
    surfaceWidth = surface.get_width()
    titleLabel = titleFont.render(titleContent, 1, c.black)
    surface.blit(titleLabel, (25, 7))
    menuOpts = sorted(list(menuDict.keys()))
    menuOptSurfaces = [surface.subsurface(pygame.Rect((0, 47 + i*25), (surfaceWidth, 25)))
                       for i in range(len(menuOpts))]
    for i, optSurface in enumerate(menuOptSurfaces):
        optLabel = infoFont.render(menuOpts[i], 1, c.black)
        optSurface.blit(optLabel, (10, 2))
    pygame.display.update(surface.get_rect())
    rectList = [pygame.Rect(oS.get_abs_offset(), (oS.get_rect().width, oS.get_rect().height)) for oS in menuOptSurfaces]
    chosenRect = get_rect_from_player(player, rectList)
    chosenOpt = menuOpts[rectList.index(chosenRect)]
    return chosenOpt


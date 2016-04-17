import pygame
import constants as c
import pieces as p
import geometricfunctions as gf


def get_rect_from_player(player, rectList):
    # Loop until the user clicks on a vertex
    validClick = False
    while not validClick:
        # Make sure no other events are on the queue
        pygame.event.clear()
        # Prompt the user for a click and wait for two events
        if player:
            print("{} please click an option.".format(player.name))
        else:
            print("Please click an option.")
        chosenRect = None
        eventA = pygame.event.wait()
        eventB = pygame.event.wait()
        # If the next two events are the mouse being pressed down and then released, move forward
        if eventA.type == pygame.MOUSEBUTTONDOWN and eventB.type == pygame.MOUSEBUTTONUP:
            posA = eventA.__dict__['pos']
            posB = eventB.__dict__['pos']
            # If the mouse actions (pressed down, released) were no more than 10 pixels apart, move forward
            if gf.pp_distance(posA, posB) < 10:
                # Loop through the rects to see if the click occurred inside one
                for rect in rectList:
                    # If both mouse actions occurred inside the current hex, move forward
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
                # Get coordinates of the vertices closest to where the mouse was pressed down and where it was released
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
                            # With all conditions satisfied, find the vertex corresponding to the coordinates found
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
                        # Loop through the hexes to see if the click occurred inside one
                        for hexTile in hexList:
                            # If both mouse actions occurred inside the current hex, move forward
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
        return choice


def present_graphical_menu(player, menuDict, titleContent, surface, titleFont, infoFont):
    surface.fill(c.white)
    pygame.display.update(surface.get_rect())
    surfaceWidth = surface.get_width()
    titleLabel = titleFont.render(titleContent, 1, c.black)
    surface.blit(titleLabel, (25, 7))
    menuOpts = list(menuDict.keys())
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


def create_players():
    # Pygame initialization
    pygame.init()
    # opens the window with the size specifications given
    inputScreen = pygame.display.set_mode(c.screenSize)
    inputScreen.fill(c.white)
    subsurfaceHeight = c.oceanHeight / 5
    interiorSpacing = 4
    exteriorSpacing = 5
    baseY = 25
    typeX = 50
    typeSpacing = 30
    nameX = 250
    nameBoxSize = (150, 30)
    colorX = 500
    availableColors = list(c.playerColorsList)
    arialFont = pygame.font.SysFont("Arial", 15)
    pygame.event.set_allowed(None)
    pygame.event.set_allowed([pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN, pygame.KEYUP, pygame.QUIT])
    playerList = []

    for playerI in range(4):
        adjustedY = baseY + playerI * subsurfaceHeight

        '''
        typeMessage = arialFont.render("Choose the player type", 1, c.black)
        inputScreen.blit(typeMessage, (typeX, adjustedY))
        humanText = arialFont.render("Human", 1, c.black)
        humanButton = pygame.Rect((typeX, adjustedY + typeMessage.get_size()[1] + exteriorSpacing),
                                  (humanText.get_size()[0] + interiorSpacing * 2,
                                   humanText.get_size()[1] + interiorSpacing * 2))
        pygame.draw.rect(inputScreen, c.black, humanButton, 1)
        inputScreen.blit(humanText, (typeX + interiorSpacing,
                                       adjustedY + typeMessage.get_size()[1] + exteriorSpacing + interiorSpacing))
        aiText = arialFont.render("AI", 1, c.black)
        aiButton = pygame.Rect((typeX + humanText.get_size()[0] + typeSpacing,
                                adjustedY + typeMessage.get_size()[1] + exteriorSpacing),
                               (aiText.get_size()[0] + interiorSpacing * 2, aiText.get_size()[1] + interiorSpacing * 2))
        pygame.draw.rect(inputScreen, c.black, aiButton, 1)
        inputScreen.blit(aiText, (typeX + humanText.get_size()[0] + typeSpacing + interiorSpacing,
                                    adjustedY + typeMessage.get_size()[1] + exteriorSpacing + interiorSpacing))
        pygame.display.flip()
        chosenButton = get_rect_from_player(None, [humanButton, aiButton])
        if chosenButton == humanButton:
            playerIsAI = False
        else:
            playerIsAI = True
        '''
        playerIsAI = False

        nameMessage = arialFont.render("Enter a name", 1, c.black)
        inputScreen.blit(nameMessage, (nameX, adjustedY))
        textBox = pygame.Rect((nameX, adjustedY + nameMessage.get_size()[1] + exteriorSpacing), nameBoxSize)
        pygame.draw.rect(inputScreen, c.black, textBox, 1)
        arialFont.set_bold(True)
        okText = arialFont.render("OK", 1, c.forestGreen)
        okButton = pygame.Rect((nameX, adjustedY + nameMessage.get_size()[1] + nameBoxSize[1] + exteriorSpacing * 2),
                               (okText.get_size()[0] + interiorSpacing * 2, okText.get_size()[1] + interiorSpacing * 2))
        pygame.draw.rect(inputScreen, c.black, okButton, 1)
        inputScreen.blit(okText, (nameX + interiorSpacing,
                                  adjustedY + nameMessage.get_size()[1] + nameBoxSize[1] + exteriorSpacing * 2 +
                                  interiorSpacing))
        arialFont.set_bold(False)
        pygame.display.flip()
        playerName = ""
        clickedOK = False
        lastEvent = None
        pygame.event.clear()
        while not clickedOK:
            thisEvent = pygame.event.wait()
            if thisEvent.type == pygame.MOUSEBUTTONDOWN:
                pass
            elif thisEvent.type == pygame.MOUSEBUTTONUP and lastEvent and lastEvent.type == pygame.MOUSEBUTTONDOWN:
                downPosition = thisEvent.__dict__['pos']
                upPosition = lastEvent.__dict__['pos']
                if gf.is_within_rect(okButton, downPosition) and gf.is_within_rect(okButton, upPosition):
                    clickedOK = True
            elif thisEvent.type == pygame.KEYDOWN:
                pass
            elif thisEvent.type == pygame.KEYUP and lastEvent and lastEvent.type == pygame.KEYDOWN:
                if thisEvent.__dict__['key'] == lastEvent.__dict__['key']:
                    asciiValue = thisEvent.__dict__['key']
                    if 97 <= asciiValue <= 122:
                        modValue = thisEvent.__dict__['mod']
                        print(thisEvent.__dict__)
                        if modValue == 1 or modValue == 2 or modValue == 8192:
                            asciiValue -= 32
                        char = chr(asciiValue)
                        playerName += char
                        pygame.draw.rect(inputScreen, c.white, textBox, 0)
                        pygame.draw.rect(inputScreen, c.black, textBox, 1)
                        nameLabel = arialFont.render(playerName, 1, c.black)
                        inputScreen.blit(nameLabel, (nameX + interiorSpacing, adjustedY + nameMessage.get_size()[1] +
                                                     exteriorSpacing + interiorSpacing))
                        pygame.display.flip()
                    elif asciiValue == 8:
                        playerName = playerName[:-1]
                        pygame.draw.rect(inputScreen, c.white, textBox, 0)
                        pygame.draw.rect(inputScreen, c.black, textBox, 1)
                        nameLabel = arialFont.render(playerName, 1, c.black)
                        inputScreen.blit(nameLabel, (nameX + interiorSpacing, adjustedY + nameMessage.get_size()[1] +
                                                     exteriorSpacing + interiorSpacing))
                        pygame.display.flip()
                    elif asciiValue == 13:
                        clickedOK = True
            lastEvent = thisEvent

        colorMessage = arialFont.render("Choose a color", 1, c.black)
        inputScreen.blit(colorMessage, (colorX, adjustedY))
        defaultColorBox = pygame.Rect((colorX, adjustedY + colorMessage.get_size()[1] + exteriorSpacing),
                                      (c.colorBoxEdgeLength, c.colorBoxEdgeLength))
        colorBoxes = [defaultColorBox.move(i * 20, 0) for i in range(len(availableColors))]
        for i, color in enumerate(availableColors):
            if color == c.white:
                pygame.draw.rect(inputScreen, c.black, colorBoxes[i], 1)
            else:
                pygame.draw.rect(inputScreen, color, colorBoxes[i], 0)
        pygame.display.flip()
        chosenBox = get_rect_from_player(None, colorBoxes)
        playerColor = availableColors.pop(colorBoxes.index(chosenBox))

        playerList.append(p.Player(playerName, playerColor, playerIsAI))

    pygame.quit()
    return playerList



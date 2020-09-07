from graphics import *
from os import listdir
from time import sleep
from random import randint, random
from winsound import *

class Button:
    """A button is a labeled rectangle in a window. It is activated or
    deactivated with the activate() and deactivate() methods. The clicked(p)
    method returns true if the button is active and p is inside it."""

    def __init__(self, win, center, width, height, label):
        """ Creates a rectangular button, eg:qb = Button(myWin, centerPoint,
        width, height, 'Quit') """
        w,h = width/2.0, height/2.0
        x,y = center.getX(), center.getY()
        self.xmax, self.xmin = x+w, x-w
        self.ymax, self.ymin = y+h, y-h
        p1 = Point(self.xmin, self.ymin)
        p2 = Point(self.xmax, self.ymax)
        self.rect = Rectangle(p1,p2)
        self.rect.setFill('lightgray')
        self.rect.draw(win)
        self.label = Text(center, label)
        self.label.draw(win)
        self.deactivate()

    def clicked(self, p):
        """Returns true if button active and p is inside"""
        if not p == None:
            return (self.active and
            self.xmin <= p.getX() <= self.xmax and
            self.ymin <= p.getY() <= self.ymax)

    def getLabel(self):
        """Returns the label string of this button."""
        return self.label.getText()

    def activate(self):
        """Sets this button to 'active'."""
        self.label.setFill('black')
        self.rect.setWidth(1)
        self.active = True

    def deactivate(self):
        """Sets this button to 'inactive'."""
        self.label.setFill('darkgrey')
        self.rect.setWidth(0)
        self.active = False

    def delete(self):
        """Undraws the button"""
        self.deactivate()
        self.label.undraw()
        self.rect.undraw()

class Menu_Bckgnd:
    def __init__(self, win, fullscreen=False):
        """Creates and draw the background to the window"""
        self.rect = Rectangle(Point(100, 0), Point(400, 500))
        if fullscreen:
            self.rect = Rectangle(Point(0, 0), Point(500, 500))
        self.rect.setOutline("white")
        self.rect.setFill("white")
        self.rect.draw(win)

    def undraw(self):
        """Undraws the background"""
        self.rect.undraw()

class Menu:
    def __init__(self, win):
        """Creates the start menu"""

        # Creates the graphical objects and buttons used in the menu
        self.start = Button(win, Point(250, 450), 100, 50, "Start")
        self.exit = Button(win, Point(450, 450), 50, 50, "Exit")
        self.scores = Button(win, Point(90, 450), 120, 40, "Check Scores")
        self.title = Text(Point(250, 40), "Michael's Hangman")
        self.title.setSize(32)
        self.title.draw(win)

        # Activates the buttons used
        self.start.activate()
        self.scores.activate()
        self.exit.activate()

        # Loop that checks to see what button was pressed
        butclicked = False
        while butclicked == False:
            # Gets last mouse click
            pointclicked = win.checkMouse()

            # Starts game
            if self.start.clicked(pointclicked) == True:
                self.start.delete()
                self.exit.delete()
                butclicked = True

            # Displays past scores
            elif self.scores.clicked(pointclicked) == True:
                check_high_score(win)

            # Exits game
            elif self.exit.clicked(pointclicked) == True:
                self.exit.deactivate()
                PlaySound(None, SND_ASYNC)
                sleep(0.1)
                win.close()
                exit()
            else:
                pass

        # Undraws all menu items
        self.title.undraw()
        self.scores.delete()

    def choose_word(self, win):
        """Chooses a random word from the categories (within Word Lists/) and returns
        category"""

        # Menu header
        self.header = Text(Point(250, 40), "Choose an item from the category below")
        self.header.draw(win)

        # Creates list of category txt files and an empty list for the buttons
        a = listdir("Word Lists")
        ctgry_but = list()

        # y value of the first button
        y1 = 80

        # Creates button for each category and adds them to the button list
        for i in a:
            ctgry_but.append(Button(win, Point(250, y1), 200, 30, i[:-4]))
            y1 += 40

        # Activates all non-empty slot buttons
        for x in ctgry_but:
            if not "Empty Slot" in x.getLabel():
                x.activate()

        # Loop check what category was clicked
        ctgry_unchosen = True
        while ctgry_unchosen == True:
            pointclick = win.checkMouse()
            for x in ctgry_but:
                if x.clicked(pointclick) == True:
                    # Opens the category file and makes a list of the words in it
                    infilename = "Word Lists/" + x.getLabel() + ".txt"
                    infile = open(infilename, "r", newline=None)
                    list_of_words = infile.read().splitlines()
                    ctgry_unchosen = False

        # Undraws buttons and header
        for x in ctgry_but:
            x.delete()
        self.header.undraw()

        # Returns random word and the category it came from
        return list_of_words[randint(0, len(list_of_words) - 1)], infilename[11:-4]

    def choose_difficulty(self, win):
        """Chooses difficulty from 3 options: Easy, Medium, Hard"""

        # Creates the graphical objects and buttons for the menu
        header = Text(Point(250, 40), "Choose from the difficulties below")
        easy = Button(win, Point(250, 80), 200, 30, "Easy - 14 Fails")
        medium = Button(win, Point(250, 120), 200, 30, "Medium - 8 Fails")
        hard = Button(win, Point(250, 160), 200, 30, "Hard - 5 Fails")

        # Activates the used buttons
        easy.activate()
        medium.activate()
        hard.activate()

        # Loop check what difficulty was clicked, and assigns the number of
        # guesses correlated with that difficulty
        difclicked = False
        while difclicked == False:
            pointclick = win.checkMouse()
            if easy.clicked(pointclick) == True:
                buttonpressed = 14
                easy.deactivate()
                difclicked = True
            elif medium.clicked(pointclick) == True:
                buttonpressed = 8
                medium.deactivate()
                difclicked = True
            elif hard.clicked(pointclick) == True:
                buttonpressed = 5
                hard.deactivate()
                difclicked = True
            else:
                pass

        # Undraws menu buttons
        easy.delete()
        medium.delete()
        hard.delete()

        # Returns the number of guesses the player gets
        return buttonpressed

class PlayGame:
    def __init__(self, win, word, difficulty, isoboard, category):
        """Plays the actual Hangman game"""

        # Assigns the guessable word and makes an empty string
        self.word = word
        guessed_word = ""

        # Makes fillable list
        for i in word:
            if i.upper() in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                guessed_word += "-"
            else:
                guessed_word += i

        # Makes and draws labels for main game
        self.category = Text(Point(250, 50), "The word's category is " + category)
        self.category.draw(win)

        self.guessed_word_txt = Text(Point(250, 350), guessed_word)
        self.guessed_word_txt.draw(win)

        self.difficulty_label = Text(Point(430, 310), "Guesses Left")
        self.difficulty_label.draw(win)

        self.difficulty_txt = Text(Point(430, 330), str(difficulty))
        self.difficulty_txt.draw(win)

        # Change Music Button
        change_mus = Button(win, Point(50, 50), 50, 30, "Music")
        change_mus.activate()

        # Makes Keyboard class, number-of-guesses variable, and won boolean
        self.butlist = Keyboard_Buttons(win)
        self.butlist.keyboardactivate()
        self.num_left = difficulty
        self.num_wrong = difficulty
        self.won = None

        # Main game loop
        while self.won == None:
            click = win.checkMouse()
            keypressed = self.butlist.keyget(win, click)

            # Catches keypressed if it is None
            if keypressed == None:
                pass

            # Adds letters to word if keypressed is in word
            elif keypressed.upper() in word or keypressed in word:
                num_counter = 0
                for j in word:
                    if keypressed == j or keypressed.upper() == j:
                        self.guessed_word_txt.undraw()
                        guessed_word = guessed_word[:num_counter] + j + guessed_word[num_counter + 1:]
                        self.guessed_word_txt = Text(Point(250, 350), guessed_word)
                        self.guessed_word_txt.draw(win)
                    num_counter += 1
                isoboard.turn(win, True)

            # Removes one guess
            else:
                self.num_left -= 1
                isoboard.turn(win, False)
                self.difficulty_txt.undraw()
                self.difficulty_txt = Text(Point(430, 330), str(self.num_left))
                self.difficulty_txt.draw(win)

            # Opens change music screen if change music button is pressed
            if change_mus.clicked(click) == True:
                change_mus_scrn(win, self.butlist.key_lst[-1], change_mus)
                click = Point(0,0)

            # If the word is correct, the game is over and player won
            if word == guessed_word:
                self.won = True

            # If there are no more guesses left, the game is over and player lost
            elif self.num_left == 0:
                self.won = False

            sleep(0.01)

        # Undraws all unwanted objects after the game ends
        self.guessed_word_txt.undraw()
        self.difficulty_txt.undraw()
        self.butlist.keyboardkill()
        self.difficulty_label.undraw()
        self.category.undraw()
        change_mus.delete()

    def game_end(self, win, won, word, isoboard):
        """Game's Ending screen, allows user to enter score if they won"""

        # Allows you to record your score if you won, otherwise the button is greyed out
        if self.won == True:
            header = Text(Point(250, 40), "You have won")
            header.draw(win)
            isoboard.end_anim(win, True)
            self.record_high = Button(win, Point(250, 340), 200, 30, "Record Score")
            self.record_high.activate()
        else:
            header = Text(Point(250, 40), "You have lost")
            header.draw(win)
            isoboard.end_anim(win, False)
            self.record_high = Button(win, Point(250, 340), 200, 30, "No Recordable Score")

        # Shows the correct answer
        self.rightword = Text(Point(250, 470), "The right answer was " + word)
        self.rightword.draw(win)

        # Creates and activates the scores button
        self.scores = Button(win, Point(80, 420), 115, 25, "Check Scores")
        self.scores.activate()

        # Creates the play again and exit buttons and activates them
        self.play_again = Button(win, Point(250, 380), 200, 30, "Play Again")
        self.exit = Button(win, Point(250, 420), 200, 30, "Exit")
        self.play_again.activate()
        self.exit.activate()

        # Loop to see if exit, play again, or enter score was clicked
        keyclicked = False
        while keyclicked == False:
            pointclick = win.checkMouse()

            # Plays the game again
            if self.play_again.clicked(pointclick) == True:
                isoboard.undraw_vehicles(win)
                self.play_again.deactivate()
                sleep(0.1)
                keyclicked = True

            # Enters the record score menu
            elif self.record_high.clicked(pointclick) == True:
                self.record_high.delete()
                record_score(win, self.butlist.key_lst[-1], self.word, self.num_wrong - self.num_left)
                self.record_high.deactivate()

            # Displays past scores
            elif self.scores.clicked(pointclick) == True:
                check_high_score(win)

            # Exits the game
            elif self.exit.clicked(pointclick) == True:
                isoboard.undraw_vehicles(win)
                self.exit.deactivate()
                PlaySound(None, SND_ASYNC)
                sleep(0.1)
                win.close()
                exit()

        self.play_again.delete()
        self.exit.delete()
        header.undraw()
        self.rightword.undraw()
        self.record_high.delete()
        self.scores.delete()

        return True

class Keyboard_Buttons:
    def __init__(self, win):
        """Creates a graphical keyboard, using a similar method to the one used
        for the isometric board"""

        # The map of where all the keys and empty spaces go
        key_map = [
                   ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
                   ["K", "L", "M", "N", "O", "P", "Q", "R", "S", "T"],
                   ["_", "_","U", "V", "W", "X", "Y", "Z", "_", "_"]
                   ]

        # List of key buttons
        self.key_lst = []

        # Initial button x and y coords
        x_coord = 130
        y_coord = 400

        # Adds buttons to the key_lst if they are a letter
        for row in key_map:
            for key in row:
                if key in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                    self.key_lst.append(Button(win, Point(x_coord, y_coord), 20, 20, key))
                x_coord += 25
            x_coord = 130
            y_coord += 30

        # Adds the exit button
        self.key_lst.append(Button(win, Point(450, 450), 50, 50, "Exit"))

    def keyboardactivate(self):
        """Activates all of the buttons in the keyboard"""
        for key in self.key_lst:
            key.activate()

    def keyboardkill(self):
        """Undraws all of the buttons in the keyboard"""
        for key in self.key_lst:
            key.delete()

    def keyget(self, win, pointclick, deactive=True):
        """Checks to see if any keyboard buttons were clicked, and returns its
        letter if one was"""
        buttonpressed = None
        for key in self.key_lst:
            if key.getLabel() in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                if key.clicked(pointclick) == True:
                    buttonpressed = key.getLabel().lower()
                    if deactive:
                        key.deactivate()
                    keyclicked = True
            elif key.getLabel() == "Exit":
                if key.clicked(pointclick) == True:
                    key.deactivate()
                    PlaySound(None, SND_ASYNC)
                    sleep(0.1)
                    win.close()
                    exit()
            else:
                pass

        return buttonpressed

#===============================================================================
# Class Isotiles creates the "Hanging man" portion of the game
# Bus and cop vehicle sprites taken from https://opengameart.org/content/2d-car-pack-0, CC0 Liscensing
# Tiles taken from www.kenney.nl, CC0 Liscensing
# Code augmented from https://stackoverflow.com/questions/20629885/how-to-render-an-isometric-tile-based-world-in-python
#===============================================================================

class Isotiles:
    def __init__(self, win, num_of_guesses=5):
        """Creates the isographic map"""

        # List of tile Image objects
        self.tiles = []

        # 10 x 9 map of the tiles
        map = [
            [1, 4, 2, 3, 2, 3, 2, 5, 1, 1],
            [1, 4, 2, 3, 2, 3, 2, 5, 1, 1],
            [1, 4, 2, 3, 2, 3, 2, 5, 1, 1],
            [1, 4, 2, 3, 2, 3, 2, 5, 1, 1],
            [1, 4, 2, 3, 2, 3, 2, 5, 1, 1],
            [1, 4, 2, 3, 2, 3, 2, 5, 1, 1],
            [1, 4, 2, 3, 2, 3, 2, 5, 1, 1],
            [1, 4, 2, 3, 2, 3, 2, 5, 1, 1],
            [1, 4, 2, 3, 2, 3, 2, 5, 1, 1]
            ]


        # Tile width and height
        tileWidth = 22
        tileHeight = 22

        # Holds the current map row the tile is on (y)
        currentRow = 0

        # Holds the current tile (x)
        currentTile = 0

        # For every row of the map
        for row in map:
            # For every tile of each row
            for tile in row:
                # x is the index of the currentTile * the tile width
                cartx = currentTile * tileWidth

                # y is the index of the currentRow * the tile height
                carty = currentRow * tileHeight
                x = cartx - carty
                y = (cartx + carty) / 2

                if tile == 1:
                    tileImage = "Images/Tile.gif"
                elif tile == 2:
                    tileImage = "Images/wet.gif"
                    y += 2
                    x -= 2
                elif tile == 3:
                    tileImage = "Images/Wetroad.gif"
                elif tile == 4:
                    tileImage = "Images/Frontdam.gif"
                elif tile == 5:
                    tileImage = "Images/Backdam.gif"
                    y += 2
                    x -= 2

                # Display the tile
                self.tiles.append(Image(Point(x + 230, y + 100), tileImage))

                # Increase the tile we are working on
                currentTile += 1

            # Reset the current tile number
            currentTile = 0

            # Begin working on the next row
            currentRow += 1

        # Draw all tiles
        for tile in self.tiles:
            tile.draw(win)

    def start_game(self, win):
        """Executes the start of game animation"""

        # Creates and draws vehicles
        self.cop = Image(Point(472, -53), "Images/police.gif")
        self.bus = Image(Point(517, -31), "Images/bus.gif")
        self.cop.draw(win)
        self.bus.draw(win)

        # Moves the platforms back for the vehicles
        for i in range(176):
            self.tiles[5].move(1, -1)
            self.tiles[3].move(1, -1)
            sleep(0.01)

        # Moves the vehicles on the platforms back to the map
        for i in range(176):
            self.tiles[5].move(-1, 1)
            self.tiles[3].move(-1, 1)
            self.cop.move(-1, 1)
            self.bus.move(-1, 1)
            sleep(0.01)

        # Moves the vehicles forward for effect
        for i in range(33):
            self.bus.move(-0.5, 0.25)
            self.cop.move(-0.5, 0.25)
            sleep(0.04)

    def turn(self, win, correct):
        """Moves the bus forward if the player was correct, otherwise the moves
        the cop"""

        if correct == True:
            for i in range(11):
                self.bus.move(-0.5, 0.25)
                sleep(0.04)
        if correct == False:
            for i in range(11):
                self.cop.move(-0.5, 0.25)
                sleep(0.04)

    def end_anim(self, win, won):
        """Executes the end of game animation; Bus leaves if player wins, Cop
        leaves if the player loses"""

        if won == True:
            while self.bus.getAnchor().getX() > 164:
                self.bus.move(-0.5, 0.25)
                sleep(0.01)

            for i in range(400):
                self.bus.move(-0.5, 0.25)
                self.tiles[85].move(-0.5, 0.25)
                sleep(0.001)

            for i in range(400):
                self.tiles[85].move(0.5, -0.25)
                sleep(0.001)

        elif won == False:
            while self.cop.getAnchor().getX() > 120:
                self.cop.move(-0.5, 0.25)
                sleep(0.01)

            for i in range(400):
                self.cop.move(-0.5, 0.25)
                self.tiles[83].move(-0.5, 0.25)
                sleep(0.001)

            for i in range(400):
                self.tiles[83].move(0.5, -0.25)
                sleep(0.001)

    def undraw_vehicles(self, win):
        """Undraws the 2 vehicles"""
        self.bus.undraw()
        self.cop.undraw()

def record_score(win, exit_but, word, num_wrong):
    """Creates the Record Score menu"""

    # Creates the menu background
    Bckgrnd = Menu_Bckgnd(win)

    # Create the header
    header = Text(Point(250, 40), "Enter your name below")
    header.draw(win)

    # Creates the Text object of the entered username
    entered_word_str = ""
    entered_word = Text(Point(250, 200), entered_word_str)
    entered_word.draw(win)

    # Creates the enter and delete buttons
    enter_but = Button(win, Point(250, 250), 200, 30, "Enter")
    delete_but = Button(win, Point(250, 300), 200, 30, "Delete")
    enter_but.activate()
    delete_but.activate()

    # Opens highscores txt file with the append flag
    outfilename = "Highscores.txt"
    outfile = open(outfilename, "a")

    # Creates and activates the keyboard
    enter_name_keys = Keyboard_Buttons(win)
    enter_name_keys.keyboardactivate()

    # Loop that checks to see what buttons were clicked
    name_unchosen = True
    while name_unchosen == True:
        # Gets last mouse click
        pointclick = win.checkMouse()

        # Checks to see if a key was clickd, False makes the keys not deactivate
        # on click
        keypressed = enter_name_keys.keyget(win, pointclick, False)

        # If no key was clicked, pass
        if keypressed == None:
            pass

        # Appends the clicked letter to the username
        elif keypressed.upper() in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            entered_word.undraw()
            entered_word_str += keypressed
            entered_word = Text(Point(250, 200), entered_word_str)
            entered_word.draw(win)

        # Deactivates delete button if there is nothing to delete
        if entered_word_str == "":
            delete_but.deactivate()

        # Activates delete button if there is something to delete
        else:
            delete_but.activate()

        # Deletes the last letter in the username
        if delete_but.clicked(pointclick):
            entered_word.undraw()
            entered_word_str = entered_word_str[0:-1]
            entered_word = Text(Point(250, 200), entered_word_str)
            entered_word.draw(win)

        # Name has been entered, so loop ends
        elif enter_but.clicked(pointclick):
            name_unchosen = False

        # Exits game
        elif exit_but.clicked(pointclick):
            exit_but.deactivate()
            PlaySound(None, SND_ASYNC)
            sleep(0.1)
            win.close()
            exit()

        # Draws username
        entered_word.draw(win)

    # Writes the username, word guessed, and number of wrong guesses to the txt file
    outfile.write((entered_word_str + " got " + word + " with " + str(num_wrong) + " wrong guesses" + "\n"))

    # Undraws all unwanted objects
    Bckgrnd.undraw()
    header.undraw()
    entered_word.undraw()
    enter_but.delete()
    delete_but.delete()
    enter_name_keys.keyboardkill()

def change_mus_scrn(win, exit_but, menu_but):
    """Creates the Change Music Menu"""

    # Menu background
    Bckgrnd = Menu_Bckgnd(win)

    # Menu header
    header = Text(Point(250, 40), "Choose music from the list below")
    header.draw(win)

    # Makes a list of all sounds in Sounds folder and a list for the buttons to activate the music
    a = listdir("Sounds")
    mus_but = list()

    # Initial button y coord
    y1 = 80

    # Adds buttons to the button list
    for i in a:
        if not "desktop" in i.lower():
            mus_but.append(Button(win, Point(250, y1), 200, 30, i[:-4]))
            y1 += 40

    # Activates all music buttons
    for x in mus_but:
        x.activate()

    # Loop to see what button was clicked
    mus_unchosen = True
    while mus_unchosen == True:
        pointclick = win.checkMouse()

        # Plays music and exits menu when music button clicked
        for x in mus_but:
            if x.clicked(pointclick) == True:
                PlaySound("Sounds/" + x.getLabel() + ".wav", SND_ASYNC)
                for b in mus_but:
                    b.delete()
                header.undraw()
                Bckgrnd.undraw()
                mus_unchosen = False

        # Leaves menu if menu button clicked
        if menu_but.clicked(pointclick) == True:
            for x in mus_but:
                x.delete()
            header.undraw()
            Bckgrnd.undraw()
            mus_unchosen = False
            break

        # Exits game if exit clicked
        elif exit_but.clicked(pointclick) == True:
            exit_but.deactivate()
            PlaySound(None, SND_ASYNC)
            sleep(0.1)
            win.close()
            exit()

def check_high_score(win):
    """Creates the High Score Viewer menu"""

    # Menu background
    Bckgrnd = Menu_Bckgnd(win, True)

    # Button to leave scores
    leave_but = Button(win, Point(50, 450), 50, 20, "Leave")
    leave_but.activate()

    # Opens scores file
    infilename = "Highscores.txt"
    infile = open(infilename, "r")

    # Initial y value of the first score
    y = 500

    # List of the score graphical objects
    score_list = []

    # Adds the text objects to the list
    for i in infile.read().splitlines():
        score_list.append(Text(Point(250, y), i))
        y += 30

    # Draws objects in score_list
    for i in score_list:
        i.draw(win)

    # Loop that continues scrolling the scores up until the player clicks leave
    continue_scroll = True
    while continue_scroll:
        pointclick = win.checkMouse()

        # Moves the scores up by 2 pixels
        for i in score_list:
            i.move(0, -2)

        # Leaves the menu
        if leave_but.clicked(pointclick) == True:
            for i in score_list:
                i.undraw()
            Bckgrnd.undraw()
            continue_scroll = False
            leave_but.delete()
            break

        sleep(0.1)

def main():
    """The Full Loop"""
    # Creates the window
    win = GraphWin("Michael Janeway's Hangman Game", 500, 500)
    win.setBackground(color_rgb(205,249,255))

    # Main menu music
    PlaySound("Sounds/title3.wav", SND_ASYNC)

    # Isometric board creation
    isoboard = Isotiles(win)

    # Main menu creation
    mainscreen = Menu(win)

    # Switch music as you go into the game for effect
    PlaySound("Sounds/title1.wav", SND_ASYNC)

    # Hangman game loop
    game = True
    while game == True:
        word, category = mainscreen.choose_word(win)
        difficulty = mainscreen.choose_difficulty(win)
        isoboard.start_game(win)
        won = PlayGame(win, word, difficulty, isoboard, category)
        game = won.game_end(win, won, word, isoboard) # do the end anim

main()

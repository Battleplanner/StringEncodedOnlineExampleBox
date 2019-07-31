import pygame
from network import Network

width = 500
height = 500

#  Set's up the window
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

clientNumber = 0  # Holds the number of clients connected


class Player:
    """This will be our rectangle that will serve as the test for the server"""

    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x, y, width, height)
        self.vel = 3  # Velocity

    def draw(self, win):
        """Draws the rectangle that represents the character"""
        pygame.draw.rect(win, self.color, self.rect)  # Draws the rectangle on the screen

    def move(self):
        """Moves the character based on keyboard input"""

        # Note: The reason I have chosen not to check for each key individually is that collecting the keys pressed
        # like this allows me to run through multiple keys at a time, allowing the player to move diagonally.

        keys = pygame.key.get_pressed()  # Returns 1 if a key is being pressed, and returns 0 if not

        if keys[pygame.K_LEFT]:
            self.x -= self.vel  # Move left

        if keys[pygame.K_RIGHT]:
            self.x += self.vel  # Move right
        if keys[pygame.K_UP]:
            self.y -= self.vel  # Move up

        if keys[pygame.K_DOWN]:
            self.y += self.vel # Move down

        # Another note: the coordinates are based on the top left corner of the object, and so in order to go down
        # we need to "decrease" the y value.

        self.update()

    def update(self):
        """Updates the rectangle"""
        self.rect = (self.x, self.y, self.width, self.height)  # Updates the rectangle


def read_pos(str):
    """Receives a tuple in string form and returns it in int form"""
    str = str.split(",")  # Splits the text at every comma
    print(str)
    return int(str[0]), int(str[1])  # Returns the recreated tuple as integers


def make_pos(tup):
    """Takes a tuple and turns it into a string to be sent to server"""
    return str(tup[0]) + "," + str(tup[1])  # Returns the string tuple in the form (xx,yy)


def redrawWindow(win, player, player2):
    """Updates the window"""

    win.fill((255, 255, 255))  # Makes the window white
    player.draw(win)
    player2.draw(win)
    pygame.display.update()  # Updates the screen


def main():
    """The main loop: Constantly checks for collision, checks for events, constantly asking the server for info, etc"""

    run = True
    n = Network()
    startPos = read_pos(n.getPos())  # Gets the position of the other clients
    p = Player(startPos[0], startPos[1], 100, 100, (0, 255, 0)) # Makes the client player object
    p2 = Player(0, 0, 100, 100, (255, 0, 0))  # Makes the other player object
    clock = pygame.time.Clock()

    while run:

        clock.tick(60)  # Limits the game speed to a maximum of 60FPS

        p2Pos = read_pos(n.send(make_pos((p.x, p.y))))
        p2.x = p2Pos[0]
        p2.y = p2Pos[1]
        p2.update()

        # An important detail is that for each client object, 'p' represents themselves, while 'p2' represents
        # the other character. For this reason, in each client, we need to collect p2 from the server, because
        # as far as the client is aware, they're player one.

        # Checking for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If the event is QUIT
                run = False
                pygame.quit()

        p.move()
        redrawWindow(win, p, p2)  # Updates the screen


if __name__ == "__main__":
    main()
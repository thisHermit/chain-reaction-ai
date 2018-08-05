"""This is the current driver script to run the project."""
# TODO: later convert this to the game class.

from Board import Board
from Player import Player
import pygame
import time


class Game:

    def __init__(self, title="Chain Reaction", noOfPlayers=2):
        pygame.init()
        pygame.font.init()
        self.SCREEN_WIDTH = 350
        self.SCREEN_HEIGHT = 550
        self.size = [self.SCREEN_WIDTH, self.SCREEN_HEIGHT]
        self.title = title
        self.noOfPlayers = noOfPlayers

    def run(self):

        screen = pygame.display.set_mode(self.size)

        pygame.display.set_caption(self.title)

        clock = pygame.time.Clock()

        board = Board()

        gameOver = False
        firstRoundOver = False

        # noOfPlayers = int(input("Enter the number of players: "))

        players_list = [Player(i) for i in range(self.noOfPlayers)]
        currentPlayer = players_list[0]

        # ------------Main Game Loop----------------- #
        while not gameOver:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameOver = True
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()

                    # search the box handle the click
                    clicked_box = [y for x in board.board for y in x if y.collidepoint(pos)]
                    if clicked_box:
                        clicked_box = clicked_box[0]
                        # TODO: put this into a update function later
                        if clicked_box.balls == 0 or clicked_box.color == currentPlayer.color:
                            clicked_box.balls += 1
                            clicked_box.color = currentPlayer.color

                            if clicked_box.balls > clicked_box.unstability:
                                unstables = board.unstabilities()
                                while unstables:
                                    # for every unstability
                                    for unstable in unstables:
                                        # setting balls of unstable to zero
                                        unstable.balls = 0

                                        # finding the neighbours of the unstable element
                                        neighbours = [
                                            # up
                                            (unstable.coordinates[0] - 1, unstable.coordinates[1]),
                                            # down
                                            (unstable.coordinates[0] + 1, unstable.coordinates[1]),
                                            # left
                                            (unstable.coordinates[0], unstable.coordinates[1] - 1),
                                            # right
                                            (unstable.coordinates[0], unstable.coordinates[1] + 1)
                                        ]

                                        for row in board.board:
                                            for box in row:
                                                if box.coordinates in neighbours:
                                                    box.balls += 1
                                                    box.color = unstable.color

                                    unstables = board.unstabilities()

                            # player switching
                            for i, player in enumerate(players_list):
                                if player == currentPlayer:
                                    if not i == len(players_list) - 1:
                                        currentPlayer = players_list[i + 1]
                                    else:
                                        currentPlayer = players_list[0]
                                        firstRoundOver = True
                                    break

            # Update screen
            for row in board.board:
                for box in row:
                    # TODO: make white variable
                    pygame.draw.rect(screen, (255, 255, 255), box)
                    if box.balls:
                        for i in range(box.balls):
                            pygame.draw.circle(screen,
                                               box.color,
                                               (box.left + board.box_size // 3 + i * board.box_size // 4,
                                                box.top + board.box_size // 2),
                                               5)
            for i in range(board.columns + 1):
                pygame.draw.line(screen,
                                 board.board_lines_color,
                                 (board.epoch + i * board.box_size,
                                  board.epoch),
                                 (board.epoch + i * board.box_size,
                                  board.epoch + board.box_size * board.rows))
            for i in range(board.rows + 1):
                pygame.draw.line(screen,
                                 board.board_lines_color,
                                 (board.epoch,
                                  board.epoch + i * board.box_size),
                                 (board.epoch + board.box_size * board.columns,
                                  board.epoch + i * board.box_size))

            # Update players and check gameOver
            if firstRoundOver:
                remove_list = []
                for player in players_list:
                    flag = 0
                    for row in board.board:
                        for box in row:
                            if box.color == player.color:
                                flag = 1
                                break
                        else:
                            continue
                        break
                    if not flag:
                        remove_list.append(player)
                for remove in remove_list:
                    players_list.remove(remove)

                # Finally check for gameOver
                if len(players_list) == 1:
                    gameOver = True

            clock.tick(500)

            pygame.display.flip()

        screen.fill((0, 0, 0))
        myfont = pygame.font.SysFont("Comic Sans MS", 30)
        myfont2 = pygame.font.SysFont("Comic Sans MS", 15)
        textsurface = myfont.render("Game Over", False, (255, 0, 0))
        textsurface2 = myfont2.render("Click anywhere to continue...", False, (255, 255, 255))
        screen.blit(textsurface, (self.SCREEN_WIDTH // 3, self.SCREEN_HEIGHT // 2))
        screen.blit(textsurface2, (self.SCREEN_WIDTH // 3 - 15, self.SCREEN_HEIGHT // 2 + 30))
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.MOUSEBUTTONUP:
                    break
            else:
                continue
            break
        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()

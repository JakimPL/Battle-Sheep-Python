from game import Game


game = Game()
while True:
    try:
        game.frame()
    except KeyboardInterrupt:
        game.quit(save=False)

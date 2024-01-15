
def run():

    # MVC
    evManager = EventManager()
    gamemodel = GameEngine(evManager)
    
    controller = control(evManager, gamemodel)
    gamemodel.run()


if __name__ == "__main__":
    from MVC.Model import *
    from MVC.Controller import *
    from MVC.EventManager import *
    
    run()
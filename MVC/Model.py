from MVC.EventManager import *
import time
import pygame
from Components.Button.Button import Button

# State machine constants for the StateMachine class below
STATE_MAINPAGE = 1
STATE_STANDARDIZE = 2
STATE_GAME = 3
STATE_GAMEOVER = 4
STATE_OPTION = 5
STATE_PAUSE = 6

class GameEngine(object):
    def __init__(self, evManager):
        self.evManager = evManager
        evManager.RegisterListener(self)
        self.state = StateMachine_level_1()

        self.first_state = STATE_MAINPAGE

        self.load_settings_and_data()
        
    def load_settings_and_data(self):
        icon_path = "Resources/Images/icon.png"
        pygame_icon = pygame.image.load(icon_path)
        pygame.display.set_icon(pygame_icon)

        self.MainPage_BG_path = "Resources/Images/MainPageBG.png"

        self.MainPage_PlayerButton_path = "Resources/Images/Play Rect.png"
        self.MainPage_OptionButton_path = "Resources/Images/Options Rect.png"
        self.MainPage_QuitButton_path = "Resources/Images/Quit Rect.png"

    def get_font(self, size): # Returns Press-Start-2P in the desired size
        pygame.font.init()
        return pygame.font.Font("Resources/Fonts/font.ttf", size)

    def notify(self, event):
        """
        Called by an event in the message queue. 
        """

        if isinstance(event, QuitEvent):
            self.running = False

        if isinstance(event, StateChangeEvent):
            # pop request
            if not event.state:
                # false if no more states are left
                if not self.state.pop():
                    self.evManager.Post(QuitEvent())
            else:
                # push a new state on the stack
                self.state.push(event.state)

        if isinstance(event, StandardizeEvent):
            self.start_time = time.time()
            self.prev_time =self.start_time 

    def run(self):
        """
        Starts the game engine loop.

        This pumps a Tick event into the message queue for each loop.
        The loop ends when this object hears a QuitEvent in notify(). 
        """
        self.running = True
        self.evManager.Post(InitializeEvent())
        self.state.push(self.first_state)
        
        while self.running:
            newTick = TickEvent()
            self.evManager.Post(newTick)


class StateMachine_level_1(object):
    """
    Manages a stack based state machine.
    peek(), pop() and push() perform as traditionally expected.
    peeking and popping an empty stack returns None.
    """
    
    def __init__ (self):
        self.statestack = []
    
    def peek(self):
        """
        Returns the current state without altering the stack.
        Returns None if the stack is empty.
        """
        try:
            return self.statestack[-1]
        except IndexError:
            # empty stack
            return None
    
    def pop(self):
        """
        Returns the current state and remove it from the stack.
        Returns None if the stack is empty.
        """
        try:
            self.statestack.pop()
            print(self.statestack)
            return len(self.statestack) > 0
        except IndexError:
            # empty stack
            return None
    
    def push(self, state):
        """
        Push a new state onto the stack.
        Returns the pushed value.
        """
        self.statestack.append(state)
        print(self.statestack)
        return state
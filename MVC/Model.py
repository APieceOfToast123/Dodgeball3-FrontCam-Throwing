from MVC.EventManager import *
import time
import pygame
from Components.Button.Button import Button
import random

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

        self.random_number = None

        self.load_settings_and_data()
        # delete it later if finished the start_event
        self.start_time = None
        self.prev_time = self.start_time 
        self.total_score = 0
        self.hit_goal = False
    def load_settings_and_data(self):
        icon_path = "Resources/Images/icon.png"
        pygame_icon = pygame.image.load(icon_path)
        pygame.display.set_icon(pygame_icon)

        self.MainPage_BG_path = "Resources/Images/MainPage_BG.jpg"
        self.StandarizedPage_BG_path = "Resources/Images/StandardizedPage_BG.jpg"
        self.GamePage_BG_path = "Resources/Images/GamePage_BG.png"
        self.EndPage_BG_path = "Resources/Images/EndPage_BG.png"
        self.Monster_path = "Resources/Images/wizard.png"
        self.bun_sprite_path = "Resources/Images/Bun/wizard idle_"
        self.bun_sprite_time = 1.3

        self.processBar_path = "Resources/Images/ProcessBar/"
        self.iconBorder_path = self.processBar_path + "icon_border.png"
        self.centerBar_path = self.processBar_path + "center_bar.png"
        self.rightBar_path = self.processBar_path + "rightEdge.png"
        self.leftEnergy_path = self.processBar_path + "leftEnergy.png"
        self.reapetEnergy_path = self.processBar_path + "reapetEnergy.png"
        self.rightEnergy_path = self.processBar_path + "rightEnergy.png"
        self.borderLength = 8
        self.repeatLength = 9

        self.timer_path = "Resources/Images/timer.png"
        self.magic_path = "Resources/Images/magic.png"
        self.xp_path = "Resources/Images/xp.png"

        self.StandarizedPage_Outline_path = "Resources/Images/Outline.png"

        self.PlayerButton_path = "Resources/Images/Play Rect.png"
        self.OptionButton_path = "Resources/Images/Options Rect.png"
        self.QuitButton_path = "Resources/Images/Quit Rect.png"

        self.MainPage_BGM_path = "Resources/Musics/Title_Music.wav"
        self.StandarizedPage_BGM_path = "Resources/Musics/Standardized_Music.wav"
        self.GamePage_BGM_path = f"Resources/Musics/Game_Music1.ogg"

        self.GamePage_LeftVoice_path = "Resources/Musics/turn_left.mp3"
        self.GamePage_RightVoice_path = "Resources/Musics/turn_right.mp3"
        self.GamePage_StretchVoice_path = "Resources/Musics/Stretch arm.mp3"


    def get_font(self, size): # Returns Press-Start-2P in the desired size
        pygame.font.init()
        return pygame.font.Font("Resources/Fonts/font.ttf", size)
    
    def get_title_font(self, size): # Returns Press-Start-2P in the desired size
        pygame.font.init()
        return pygame.font.Font("Resources/Fonts/title_font.ttf", size)
    
    def random_music(self):
        self.random_number = random.randint(1, 11)
        self.GamePage_BGM_path = f"Resources/Musics/Game_Music{self.random_number}.ogg"

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

        # if isinstance(event, StandardizeEvent):
        #     self.start_time = time.time()
        #     self.prev_time =self.start_time 

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
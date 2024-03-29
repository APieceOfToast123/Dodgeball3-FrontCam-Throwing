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
STATE_RANKINGBOARD = 5
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
        self.guided = False
        self.applaused = False 
        self.beep = False
        self.game_record = []
        self.sorted_records = []

    def load_settings_and_data(self):
        icon_path = "./_internal/Resources/Images/icon.png"
        pygame_icon = pygame.image.load(icon_path)
        pygame.display.set_icon(pygame_icon)

        self.MainPage_BG_path = "./_internal/Resources/Images/MainPage_BG.jpg"
        self.StandarizedPage_BG_path = "./_internal/Resources/Images/StandardizedPage_BG.jpg"
        self.GamePage_BG_path = "./_internal/Resources/Images/GamePage_BG.png"
        self.EndPage_BG_path = "./_internal/Resources/Images/EndPage_BG.png"
        self.Monster_path = "./_internal/Resources/Images/wizard.png"
        self.bun_sprite_path = "./_internal/Resources/Images/Bun/wizard idle_"
        self.bun_sprite_time = 1.3

        self.processBar_path = "./_internal/Resources/Images/ProcessBar/"
        self.iconBorder_path = self.processBar_path + "icon_border.png"
        self.centerBar_path = self.processBar_path + "center_bar.png"
        self.rightBar_path = self.processBar_path + "rightEdge.png"
        self.leftEnergy_path = self.processBar_path + "leftEnergy.png"
        self.reapetEnergy_path = self.processBar_path + "reapetEnergy.png"
        self.rightEnergy_path = self.processBar_path + "rightEnergy.png"
        self.borderLength = 8
        self.repeatLength = 10

        self.timer_path = "./_internal/Resources/Images/timer.png"
        self.magic_path = "./_internal/Resources/Images/magic.png"
        self.xp_path = "./_internal/Resources/Images/xp.png"

        self.StandarizedPage_Outline_path = "./_internal/Resources/Images/Outline.png"

        self.PlayerButton_path = "./_internal/Resources/Images/Play Rect.png"
        self.OptionButton_path = "./_internal/Resources/Images/Options Rect.png"
        self.QuitButton_path = "./_internal/Resources/Images/Quit Rect.png"

        self.MainPage_BGM_path = "./_internal/Resources/Musics/Title_Music.wav"
        self.StandarizedPage_BGM_path = "./_internal/Resources/Musics/Standardized_Music.wav"
        self.GamePage_BGM_path = f"./_internal/Resources/Musics/Game_Music1.ogg"

        self.GamePage_LeftVoice_path = "./_internal/Resources/Musics/Left Voice.wav"
        self.GamePage_RightVoice_path = "./_internal/Resources/Musics/Right Voice.wav"
        self.GamePage_StretchVoice_path = "./_internal/Resources/Musics/Strench Your Arms.wav"

        self.ClickSound_path = "./_internal/Resources/Musics/Click Sound.wav"
        self.EnsureSound_path = "./_internal/Resources/Musics/Ensure Voice.wav"
        
        self.GamePage_guide_path = "./_internal/Resources/Musics/Guide.wav"
        self.GamePage_level0_path = "./_internal/Resources/Musics/level0.wav"
        self.GamePage_level1_path = "./_internal/Resources/Musics/level1.wav"
        self.GamePage_level2_path = "./_internal/Resources/Musics/level2.wav"
        self.GamePage_level3_path = "./_internal/Resources/Musics/level3.wav"

        self.Title_font_path = "./_internal/Resources/Fonts/title_font.ttf"
        self.Font_path = "./_internal/Resources/Fonts/font.ttf"


    def get_font(self, size): # Returns Press-Start-2P in the desired size
        pygame.font.init()
        return pygame.font.Font(self.Font_path, size)
    
    def get_title_font(self, size): # Returns Press-Start-2P in the desired size
        pygame.font.init()
        return pygame.font.Font(self.Title_font_path, size)
    
    def random_music(self):
        self.random_number = random.randint(1, 11)
        self.GamePage_BGM_path = f"./_internal/Resources/Musics/Game_Music{self.random_number}.ogg"

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
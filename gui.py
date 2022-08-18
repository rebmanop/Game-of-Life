import os
import pygame
import pygame_gui
from pygame_gui.core import ObjectID
from explanation import EXPLANATION_STR

BG_COLOR = (66, 133, 215)
EXPLANATION_WIN_COLOR = (56, 57, 60)

pygame.font.init()
EXPLANATION_TITLE_FONT = pygame.font.SysFont('Comic Sans MS', 20)
EXPLANATION_STR_FONT = pygame.font.SysFont('Comic Sans MS', 11)


class GUI:

    """GUI handler class"""

    def __init__(self, win, ui_manager, grid, width, height, animation_speed):
        self.win = win
        self.width = width
        self.height = height
        self.next_icon = pygame.image.load(os.path.join("assets", "next.png")).convert_alpha()
        self.population_icon = pygame.image.load(os.path.join("assets", "population.png")).convert_alpha()
        self.gui_elements_enabled = False
        self.explanation_title_surface = EXPLANATION_TITLE_FONT.render("Game of Life Explanation", True, pygame.Color("azure"))
        self.explanation_str_surface = EXPLANATION_STR_FONT.render(EXPLANATION_STR, True, pygame.Color("azure"))
        self.explanation_window_surf = pygame.Surface((self.width // 2, self.height // 2))
        self.gol_rules_example_pic = pygame.image.load(os.path.join("assets", "gol_rules_example.png")).convert_alpha()

        


        self.start_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((width / 2 - 50, height - 60), (100, 50)),
            text="START",
            manager=ui_manager,
            object_id=ObjectID(object_id=None, class_id="@button"),
        )


        self.clear_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
            (self.start_button.get_abs_rect().x + self.start_button.get_abs_rect().width + 100, 
            self.start_button.get_abs_rect().y + self.start_button.get_abs_rect().height / 2 - 20), 
            (100, 40)
            ),
            text="CLEAR",
            manager=ui_manager,
            object_id=ObjectID(object_id=None, class_id="@button"),
        )
         

        self.speed_slider = pygame_gui.elements.UIHorizontalSlider(
            start_value=animation_speed,
            value_range=(animation_speed * 2, 1),
            relative_rect=pygame.Rect((grid.x + 1050, height - 50), (200, grid.gap + 5)),
            manager=ui_manager,
            
            object_id=ObjectID(object_id=None, class_id="@button"),
        )
        
        self.speed_lable = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((grid.x + 1000, height - 50), (50, grid.gap + 5)),
            text="Speed:",
            manager=ui_manager,
            object_id=ObjectID(object_id=None, class_id="@button"),
        )


        self.default_speed_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((grid.x + 1250, height - 50), (35, grid.gap + 5)),
            text="",
            manager=ui_manager,
            object_id=ObjectID(object_id=None, class_id="@button"),
        )

        self.generation_counter_lable = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((30, height - 65), (50, grid.gap + 5)),
            text="0",
            manager=ui_manager,
            object_id=ObjectID(object_id=None, class_id="@button"),
        )


        self.population_counter_lable = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((30, height - 40), (50, grid.gap + 5)),
            text="0",
            manager=ui_manager,
            object_id=ObjectID(object_id=None, class_id="@button"),
            
        )

        
        self.explanation_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
            (self.start_button.get_abs_rect().x - self.start_button.get_abs_rect().width - 150, 
            self.start_button.get_abs_rect().y + self.start_button.get_abs_rect().height / 2 - 20), 
            (150, 40)
            ),
            text="EXPLANATION",
            manager=ui_manager,
            object_id=ObjectID(object_id=None, class_id="@button"),
        )

        self.gui_elements = [self.clear_button, self.start_button, self.speed_slider, self.default_speed_button]

        self.disable_gui_elements()


    def disable_gui_elements(self):
        for element in self.gui_elements:
            element.disable()
        self.gui_elements_enabled = False

        
    def enable_gui_elements(self):
        for element in self.gui_elements:
            element.enable()
        self.gui_elements_enabled = True
        

    def draw_explanation_window(self):
        self.win.blit(self.explanation_window_surf, (self.width / 2 - self.width / 2 / 2 , self.height / 2 -  self.height / 2 / 2  ))
        self.explanation_window_surf.fill(EXPLANATION_WIN_COLOR)
        self.explanation_window_surf.blit(self.explanation_title_surface,(self.width / 2 - self.width / 2 + 5, self.height / 2 -  self.height / 2 ))
        GUI.blit_text(self.explanation_window_surf, EXPLANATION_STR, (self.width / 2 - self.width / 2 + 5 , self.height / 2 -  self.height / 2  + 30), EXPLANATION_STR_FONT, pygame.Color("azure"))
        pygame.Surface.blit(self.explanation_window_surf, self.gol_rules_example_pic, (self.width / 2 - self.width / 2 / 2 - 275, self.height / 2 -  self.height / 2  + 125))


    @staticmethod
    def blit_text(surface, text, pos, font, color=pygame.Color('black')):
        words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
        space = font.size(' ')[0]  # The width of a space.
        max_width, max_height = surface.get_size()
        x, y = pos
        for line in words:
            for word in line:
                word_surface = font.render(word, True, color)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    x = pos[0]  # Reset the x.
                    y += word_height  # Start on new row.
                surface.blit(word_surface, (x, y))
                x += word_width + space
            x = pos[0]  # Reset the x.
            y += word_height  # Start on new row.



    def draw_ui_icons(self):
        pygame.Surface.blit(self.win, self.next_icon, (10, self.height - 65))
        pygame.Surface.blit(self.win, self.population_icon, (10, self.height - 40))



        

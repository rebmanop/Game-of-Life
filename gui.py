import os
import pygame
import pygame_gui
from pygame_gui.core import ObjectID



class GUI:

    """GUI handler class"""

    def __init__(self, win, ui_manager, grid, width, height, animation_speed):
        self.win = win
        self.width = width
        self.height = height
        self.next_icon = pygame.image.load(os.path.join("assets", "next.png")).convert_alpha()

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
            relative_rect=pygame.Rect((30, height - 50), (50, grid.gap + 5)),
            text="0",
            manager=ui_manager,
            object_id=ObjectID(object_id=None, class_id="@button"),
        )



    def draw_ui_icons(self):
        pygame.Surface.blit(self.win, self.next_icon, (10, self.height - 50))

        

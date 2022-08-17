import os
import pygame
import pygame_gui
from gui import GUI
from grid import Grid, GRID_FRAME_WIDTH


WIDTH, HEIGHT = 1291, 765
GRID_WIDTH, GRID_HEIGHT = 1280, 680
GRID_SIZE = (34, 64)  # (rows, columns)
GRID_POSITION = ((WIDTH - GRID_WIDTH) / 2, GRID_FRAME_WIDTH)

BG_COLOR = (66, 133, 215) 

pygame.init()
FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
UI_MANAGER = pygame_gui.UIManager((WIDTH, HEIGHT), "gui_theme.json")
ICON = pygame.transform.scale(pygame.image.load(os.path.join("assets", "icon.png")).convert_alpha(), (35, 35))
pygame.display.set_caption("Game of life")
pygame.display.set_icon(ICON)

DEFAULT_EVOLUTION_SPEED = 15

def draw(
    win: pygame.surface.Surface, 
    grid: Grid, 
    ui_manager: pygame_gui.UIManager,
    gui: GUI, 
    time_delta: float, 
) -> None:
    
    """Draws stuff to the screen every frame"""

    win.fill(BG_COLOR)
    grid.draw_all_cells()
    grid.draw_grid_lines()
    ui_manager.update(time_delta)
    grid.draw_grid_frame()

    ui_manager.draw_ui(WIN)
    gui.draw_ui_icons()

    pygame.display.update()


def main() -> None:
   
    evolution_speed = DEFAULT_EVOLUTION_SPEED
    generation_counter = 0

    clock = pygame.time.Clock()
    grid = Grid(WIN, GRID_SIZE, (GRID_WIDTH, GRID_HEIGHT), GRID_POSITION)
    gui = GUI(WIN, UI_MANAGER, grid, WIDTH, HEIGHT, evolution_speed)

    running = True
    simulation_is_running = False
    frame_counter = 0

    while running:
        
        if simulation_is_running:
            frame_counter += 1

        time_delta = clock.tick(FPS) / 1000.0
        draw(WIN, grid, UI_MANAGER, gui, time_delta)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            UI_MANAGER.process_events(event)

            # if left mouse button clicked
            if (pygame.mouse.get_pressed()[0] and grid.mouse_on_the_grid()):
                mpos = pygame.mouse.get_pos()
                row, col = grid.get_rc_of_under_mouse_cell(mpos)
                clicked_cell = grid[row][col]
                clicked_cell.resurrect()

            # if right mouse button clicked
            elif pygame.mouse.get_pressed()[2] and grid.mouse_on_the_grid():
                mpos = pygame.mouse.get_pos()
                row, col = grid.get_rc_of_under_mouse_cell(mpos)
                clicked_cell = grid[row][col]
                clicked_cell.kill()


            if event.type == pygame_gui.UI_BUTTON_START_PRESS:
              
                if event.ui_element == gui.start_button:
                    if simulation_is_running:
                       simulation_is_running = False
                       gui.start_button.set_text("START")
                       generation_counter = 0
                       gui.generation_counter_lable.set_text(str(generation_counter))
                    else:
                        simulation_is_running = True 
                        gui.start_button.set_text("STOP")
                        frame_counter = 0
                        

                if event.ui_element == gui.clear_button:
                    grid.clear()

                if event.ui_element == gui.default_speed_button:
                    evolution_speed = DEFAULT_EVOLUTION_SPEED
                    gui.speed_slider.set_current_value(DEFAULT_EVOLUTION_SPEED)
                    frame_counter = 0


            if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == gui.speed_slider:
                    frame_counter = 0
                    evolution_speed = gui.speed_slider.current_value
        
        #GAME LOGIC
        if simulation_is_running and frame_counter == evolution_speed:
            frame_counter = 0
            generation_counter += 1
            gui.generation_counter_lable.set_text(str(generation_counter))
            grid.update_alive_neighbors_list_for_every_cell()
            
            for i in range(grid.total_rows):
                for j in range(grid.total_columns):
                    current_cell = grid[i][j]
                    number_of_alive_neighbors = current_cell.number_of_alive_neighbors()
                    
                    if current_cell.is_alive() and number_of_alive_neighbors < 2:
                        current_cell.kill()

                    elif current_cell.is_alive() and number_of_alive_neighbors > 3:
                        current_cell.kill()
                    
                    elif current_cell.is_dead() and number_of_alive_neighbors == 3:
                        current_cell.resurrect()


    pygame.quit()


if __name__ == "__main__":
    main()


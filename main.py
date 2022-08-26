import os
import pygame
import pygame_gui
from gui import GUI, BG_COLOR
from grid import Grid, GRID_FRAME_WIDTH


WIDTH, HEIGHT = 1291, 765
GRID_WIDTH, GRID_HEIGHT = 1280, 680
GRID_SIZE = (100, 100)  # (rows, columns)
GRID_POSITION = ((WIDTH - GRID_WIDTH) / 2, GRID_FRAME_WIDTH)


pygame.init()
FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
UI_MANAGER = pygame_gui.UIManager((WIDTH, HEIGHT), "gui_theme.json")
ICON = pygame.image.load(os.path.join("assets", "icon.png")).convert_alpha()

pygame.display.set_caption("Game Of Life")
pygame.display.set_icon(ICON)

DEFAULT_EVOLUTION_SPEED = 15

def draw(
    win: pygame.surface.Surface, 
    grid: Grid, 
    ui_manager: pygame_gui.UIManager,
    gui: GUI, 
    time_delta: float,
    explanation_window_is_open: bool 
) -> None:
    
    """Draws stuff to the screen every frame"""

    win.fill(BG_COLOR)
    #grid.draw_all_cells()
    grid.draw_grid_lines()
    ui_manager.update(time_delta)
    gui.draw_footer()
    grid.draw_grid_frame()

    gui.draw_ui_icons()

    if explanation_window_is_open:
        gui.draw_explanation_window()


    ui_manager.draw_ui(WIN)

    
    pygame.display.update()


def main() -> None:
   
    evolution_speed = DEFAULT_EVOLUTION_SPEED
    generation_counter = 0

    clock = pygame.time.Clock()
    grid = Grid(WIN, GRID_SIZE, (GRID_WIDTH, GRID_HEIGHT), GRID_POSITION)
    gui = GUI(WIN, UI_MANAGER, grid, WIDTH, HEIGHT, evolution_speed)

    running = True
    simulation_is_running = False
    explanation_window_is_open = False
    frame_counter = 0
    mouse_button_down = False
    

    while running:
        
        if simulation_is_running:
            frame_counter += 1

        time_delta = clock.tick(FPS) / 1000.0        

        if grid.number_of_alive_cells == 0 and gui.gui_elements_enabled:
                gui.disable_gui_elements()
        elif grid.number_of_alive_cells > 0 and not gui.gui_elements_enabled and not explanation_window_is_open:
                gui.enable_gui_elements()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            UI_MANAGER.process_events(event)

            mouse_x, mouse_y = pygame.mouse.get_pos()
            keys = pygame.key.get_pressed()

            if event.type == pygame.MOUSEBUTTONDOWN and keys[pygame.K_LCTRL]:
                if pygame.mouse.get_pressed()[0]:
                    grid.start_pan_x, grid.start_pan_y = mouse_x, mouse_y
                    mouse_button_down = True
            
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_button_down = False
            
            if event.type == pygame.MOUSEMOTION and mouse_button_down:
                grid.offset_x -= (mouse_x - grid.start_pan_x) / grid.scale_x
                grid.offset_y -= (mouse_y - grid.start_pan_y) / grid.scale_y
                
                grid.start_pan_x = mouse_x
                grid.start_pan_y = mouse_y

            mouse_world_x_before_zoom, mouse_world_y_before_zoom = grid.screen_to_world(mouse_x, mouse_y)

            if event.type == pygame.MOUSEWHEEL:
                if event.y == 1:
                    grid.scale_x *= 1.1
                    grid.scale_y *= 1.1
                elif event.y == -1:
                    grid.scale_x *= 0.9
                    grid.scale_y *= 0.9

            mouse_world_x_after_zoom, mouse_world_y_after_zoom = grid.screen_to_world(mouse_x, mouse_y)

            grid.offset_x += mouse_world_x_before_zoom - mouse_world_x_after_zoom
            grid.offset_y += mouse_world_y_before_zoom - mouse_world_y_after_zoom

            # if not explanation_window_is_open and not simulation_is_running:        
            #     # if left mouse button clicked
            #     if (pygame.mouse.get_pressed()[0] and grid.mouse_on_the_grid()):
            #         mpos = pygame.mouse.get_pos()
            #         row, col = grid.get_rc_of_under_mouse_cell(mpos)
            #         clicked_cell = grid[row][col]
            #         if clicked_cell.is_dead():
            #             clicked_cell.resurrect()
            #             grid.number_of_alive_cells += 1

            #     # if right mouse button clicked
            #     elif pygame.mouse.get_pressed()[2] and grid.mouse_on_the_grid():
            #         mpos = pygame.mouse.get_pos()
            #         row, col = grid.get_rc_of_under_mouse_cell(mpos)
            #         clicked_cell = grid[row][col]
            #         if clicked_cell.is_alive():
            #             clicked_cell.kill()
            #             grid.number_of_alive_cells -= 1


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
                

                # if event.ui_element == gui.default_speed_button:
                #     evolution_speed = DEFAULT_EVOLUTION_SPEED
                #     gui.speed_slider.set_current_value(DEFAULT_EVOLUTION_SPEED)
                #     frame_counter = 0


                if event.ui_element == gui.explanation_button:
                    if explanation_window_is_open: 
                        explanation_window_is_open = False
                        if grid.number_of_alive_cells > 0:
                            gui.enable_gui_elements()
                    else:
                        explanation_window_is_open = True
                        gui.disable_gui_elements()

            # if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            #     if event.ui_element == gui.speed_slider:
            #         frame_counter = 0
            #         evolution_speed = gui.speed_slider.current_value
            draw(WIN, grid, UI_MANAGER, gui, time_delta, explanation_window_is_open)


        
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
                        grid.number_of_alive_cells -= 1

                    elif current_cell.is_alive() and number_of_alive_neighbors > 3:
                        current_cell.kill()
                        grid.number_of_alive_cells -= 1
                    
                    elif current_cell.is_dead() and number_of_alive_neighbors == 3:
                        current_cell.resurrect()
                        grid.number_of_alive_cells += 1
        
        if simulation_is_running and grid.number_of_alive_cells == 0:
            simulation_is_running = False
            generation_counter = 0
            gui.generation_counter_lable.set_text(str(generation_counter))
            gui.start_button.set_text("START")
            
            

       # gui.population_counter_lable.set_text(str(grid.number_of_alive_cells))


    pygame.quit()


if __name__ == "__main__":
    main()


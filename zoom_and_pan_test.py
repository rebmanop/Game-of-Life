import pygame

WIDTH, HEIGHT = 1291, 765

pygame.init()

FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))


def world_to_screen(world_x, world_y, offset_x, offset_y, scale_x, scale_y):
    screen_x = int((world_x - offset_x) * scale_x)
    screen_y = int((world_y - offset_y) * scale_y)
    return (screen_x, screen_y)


def screen_to_world(screen_x, screen_y, offset_x, offset_y, scale_x, scale_y):
    world_x = float(screen_x) / scale_x + offset_x
    world_y = float(screen_y) / scale_y + offset_y
    return (world_x, world_y)


def main() -> None:

    mouse_button_down = False
    running = True
    start_pan_x = 0.0
    start_pan_y = 0.0
    
    scale_x = 20.0
    scale_y = 20.0

    offset_x = (-WIDTH / 2 / scale_x + (1000) / 2)
    offset_y = (-HEIGHT / 2 / scale_y + (1000) / 2) 

    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
            mouse_x, mouse_y = pygame.mouse.get_pos()
            keys = pygame.key.get_pressed()

            if event.type == pygame.MOUSEBUTTONDOWN and keys[pygame.K_LCTRL]:
                if pygame.mouse.get_pressed()[0]:
                    start_pan_x, start_pan_y = mouse_x, mouse_y
                    mouse_button_down = True
            
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_button_down = False
            
            if event.type == pygame.MOUSEMOTION and mouse_button_down:
                offset_x -= (mouse_x - start_pan_x) / scale_x
                offset_y -= (mouse_y - start_pan_y) / scale_y
                
                start_pan_x = mouse_x
                start_pan_y = mouse_y

            mouse_world_x_before_zoom, mouse_world_y_before_zoom = screen_to_world(mouse_x, mouse_y, offset_x, offset_y, scale_x, scale_y)

            if event.type == pygame.MOUSEWHEEL:
                if event.y == 1:
                    scale_x *= 1.1
                    scale_y *= 1.1
                elif event.y == -1:
                    scale_x *= 0.9
                    scale_y *= 0.9

            mouse_world_x_after_zoom, mouse_world_y_after_zoom = screen_to_world(mouse_x, mouse_y, offset_x, offset_y, scale_x, scale_y)

            offset_x += mouse_world_x_before_zoom - mouse_world_x_after_zoom
            offset_y += mouse_world_y_before_zoom - mouse_world_y_after_zoom
            
        WIN.fill(pygame.Color("black"))
           
        for y in range(1000 + 1):
            sx = 0
            sy = y
            ex  = 1000
            ey = y
            
            pixel_sx, pixel_sy = world_to_screen(sx, sy, offset_x, offset_y, scale_x, scale_y)
            pixel_ex, pixel_ey = world_to_screen(ex, ey, offset_x, offset_y, scale_x, scale_y)
            pygame.draw.line(WIN, pygame.Color("white"), (pixel_sx, pixel_sy), (pixel_ex, pixel_ey))

        
        for x in range(1000  + 1):
            sx = x
            sy = 0
            ex  = x
            ey = 1000

            pixel_sx, pixel_sy = world_to_screen(sx, sy, offset_x, offset_y, scale_x, scale_y)
            pixel_ex, pixel_ey = world_to_screen(ex, ey, offset_x, offset_y, scale_x, scale_y)
            pygame.draw.line(WIN, pygame.Color("white"), (pixel_sx, pixel_sy), (pixel_ex, pixel_ey))
        

        pygame.display.update()


    pygame.quit()


if __name__ == "__main__":
    main()
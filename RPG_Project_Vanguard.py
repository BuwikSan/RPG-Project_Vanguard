import pygame
import os


# pygame setup
pygame.init()


screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
delta_time = 0


# asset loading
dirname = os.path.dirname(__file__)

camp_background_dir = os.path.join(dirname, fr"Assets\pics\Mapa_RPG-P.V._v1.0.0.png")
camp_background = pygame.Surface.convert(pygame.image.load(camp_background_dir))

slime_plains_background_dir = os.path.join(dirname, fr"Assets\pics\slimeplains.png")
slime_plaind_background = pygame.Surface.convert(pygame.image.load(slime_plains_background_dir))

player_image_dir = os.path.join(dirname, fr"Assets\pics\tucnak_warm.png")
player_image = pygame.Surface.convert(pygame.image.load(player_image_dir))




# vars and constants for menu

buttons = {}

buttons["back to game"] = pygame.Rect(540, 310, 100, 50)





# vars and constants for movement screen
## maps
map_border = pygame.Rect(5, 5, 1270, 710)

## camp
camp_wall_hitboxes = []

wall_1 = pygame.Rect(200, 260, 30, 200)
camp_wall_hitboxes.append(wall_1)

wall_2 = pygame.Rect(200, 260, 200, 30)
camp_wall_hitboxes.append(wall_2)


camp_interactable_hitboxes = {}

class portal_rect(pygame.Rect):
    
    def __init__(self, left, top):
        self.left = left
        self.top = top
        self.width = 10
        self.height = 100

PORTAL_DISPLACEMENT_Y = 64
camp_interactable_hitboxes["slime_plains_portal"] = portal_rect(1270, PORTAL_DISPLACEMENT_Y)
camp_interactable_hitboxes["golem_ruins_portal"] = portal_rect(1270, 2*PORTAL_DISPLACEMENT_Y + camp_interactable_hitboxes["slime_plains_portal"].height)
camp_interactable_hitboxes["wivern_mountains_portal"] = portal_rect(1270, 3*PORTAL_DISPLACEMENT_Y + camp_interactable_hitboxes["slime_plains_portal"].height + camp_interactable_hitboxes["golem_ruins_portal"].height)
camp_interactable_hitboxes["dragons_lair_portal"] = portal_rect(1270, 4* PORTAL_DISPLACEMENT_Y + camp_interactable_hitboxes["slime_plains_portal"].height + camp_interactable_hitboxes["golem_ruins_portal"].height + camp_interactable_hitboxes["wivern_mountains_portal"].height)





## slime plains


## golem ruins


## wivern montains


## dragon's lair




# player
BASE_PLAYER_SPEED = 200

player_hitbox = pygame.Rect(screen.get_width()/2, screen.get_height()/2, player_image.get_width(), player_image.get_height())
player_hitbox_perdiction = player_hitbox.copy()


# custom functions

def quit_game():
    global running
    running = False

def update_screen():
    global delta_time, clock
    pygame.display.flip()
    delta_time = clock.tick(60) / 1000

def speed_normalization(movement_keys, player_speed, delta_time):
    number_of_pressed_keys = 0
    speed_normalizer = 1

    for key in movement_keys:
        if key == True : number_of_pressed_keys += 1

        if number_of_pressed_keys > 1:
            speed_normalizer = 1.4;
            break

    distance_coefitient = player_speed * delta_time / speed_normalizer
    return distance_coefitient


def colision_detection(player_hitbox: pygame.Rect, stationary_hitboxes: list, old_x: int, old_y: int, tempx, tempy):
    disable_x, disable_y = False, False
    for wall in stationary_hitboxes:

        if  tempx <= wall.x + wall.width and tempx + player_hitbox.width >= wall.x and old_y <= wall.y + wall.height and old_y + player_hitbox.height >= wall.y:
            disable_x = True
        if  old_x <= wall.x + wall.width and old_x + player_hitbox.width >= wall.x and tempy <= wall.y + wall.height and tempy + player_hitbox.height >= wall.y:
            disable_y = True

    if disable_x and disable_y:
        print("2way colision")
        final_x, final_y = old_x, old_y
    elif disable_x and not disable_y:
        final_x, final_y = old_x, tempy
        print("x would cause colision")
    elif not disable_x and disable_y:
        final_x, final_y = tempx, old_y
        print("y would cause colision")
    else:
        final_x, final_y = tempx, tempy
    return (final_x, final_y)


def move(movement_keys, player, screen, stationary_hitboxes, player_speed, delta_time):
    old_x = player.x
    old_y = player.y
    tempx = player.x
    tempy = player.y

    distance_coefitient = speed_normalization(movement_keys, player_speed, delta_time)

    if movement_keys[0]:
        tempy = pygame.math.clamp(tempy - round(distance_coefitient), 0, screen.get_height() - player.height)

    if movement_keys[1]:
        tempy = pygame.math.clamp(tempy + round(distance_coefitient), 0, screen.get_height() - player.height)

    if movement_keys[2]:
        tempx = pygame.math.clamp(tempx - round(distance_coefitient), 0, screen.get_width() - player.width)

    if movement_keys[3]:
        tempx = pygame.math.clamp(tempx + round(distance_coefitient), 0, screen.get_width() - player.width)


    output_coords = colision_detection(player, stationary_hitboxes, old_x, old_y, tempx, tempy)

    return output_coords

# variables for game navigation
current_screen = "camp"
previous_screen  = None



# the game

while running:

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    keys_pressed = pygame.key.get_pressed()
    keys_down = pygame.key.get_just_pressed()

    if keys_down[pygame.K_ESCAPE] == True:
        if current_screen == "menu":
            current_screen = previous_screen
        else:
            previous_screen = current_screen
            current_screen = "menu"

        print(current_screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game()


    if current_screen == "menu":
        movement = False
        screen.fill("black")
        for button in buttons.values():
            pygame.draw.rect(screen, "white", button)
        for name, button in buttons.items():
            if pygame.mouse.get_pressed()[0] and (button.left < pygame.mouse.get_pos()[0] < (button.left + button.width)) and (button.top < pygame.mouse.get_pos()[1] < (button.top + button.height)):
                if name == "back to game":
                    previous_screen = current_screen
                    current_screen = "camp"
        
        

    if current_screen == "camp":
        movement = True
        screen.blit(camp_background, (0, 0))
        for i_stationary_hitbox in range(len(camp_wall_hitboxes)):
            pygame.draw.rect(screen, "black", camp_wall_hitboxes[i_stationary_hitbox])

        for interactable_hitbox in camp_interactable_hitboxes.values():
            pygame.draw.rect(screen, "red", interactable_hitbox)
    

    if current_screen == "slime plains":
        movement = True
        screen.blit(slime_plaind_background, (0, 0))



    if movement:
        movement_keys = [keys_pressed[pygame.K_w], keys_pressed[pygame.K_s], keys_pressed[pygame.K_a], keys_pressed[pygame.K_d]]


        player_coords = move(movement_keys, player_hitbox, screen, camp_wall_hitboxes, BASE_PLAYER_SPEED, delta_time)
        player_hitbox.x, player_hitbox.y = player_coords[0], player_coords[1]


        screen.blit(player_image, player_hitbox)
    



    update_screen()

pygame.quit()


## dodělej pozici hráče jako vektor a až pak zaokrouhluj a nastavuj reálné souřadnice
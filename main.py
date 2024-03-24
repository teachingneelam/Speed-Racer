import pygame
import random
import sys
import time




pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 700, 680
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Speed Racer - Take a Ride")

clock = pygame.time.Clock()


font_big = pygame.font.Font(r"font\monsterRacing.otf", 50)
font_small = pygame.font.Font(r"font\monsterRacing.otf", 30)
font_button = pygame.font.Font(r"font\monsterRacing.otf", 20)


RED = (255, 0, 0)
LIGHT_RED = (200, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
WHITE = (255, 255, 255)
LIGHT_GRAY = (220, 220, 220)


# Loading images
road_img = pygame.image.load("img\\road.png")
road_img = pygame.transform.scale(road_img, (150, HEIGHT)).convert_alpha()

grass_img = pygame.image.load("img\\grass2.jpg")
grass_img = pygame.transform.scale(grass_img, (60, HEIGHT)).convert_alpha()


player_img = pygame.image.load("img\\car_orange2.png")
player_img = pygame.transform.rotate(player_img, 180)
player_img = pygame.transform.scale(player_img, (120, 250)).convert_alpha()

home_img = pygame.image.load("img\\home.jpg")
home_img = pygame.transform.scale(home_img, (WIDTH, HEIGHT)).convert_alpha()


player_rect = player_img.get_rect()

bg_music = pygame.mixer.Sound("audio\\bgm1.mp3")
fast_sound = pygame.mixer.Sound("audio\\fast_car.mp3")
slow_sound = pygame.mixer.Sound("audio\\slow_car.mp3")
horn_sound = pygame.mixer.Sound("audio\\horn3.wav")
brake_sound = pygame.mixer.Sound("audio\\brake.mp3")
crash_sound = pygame.mixer.Sound("audio\\crash.mp3")



fast_sound.set_volume(0.3) 
slow_sound.set_volume(0.3) 
horn_sound.set_volume(1) 
brake_sound.set_volume(0.3) 
bg_music.set_volume(0.3)
crash_sound.set_volume(1)

music_list = [fast_sound, slow_sound, horn_sound, brake_sound]


background_y = 0
player_rect.x = (WIDTH - player_img.get_width()) // 2
player_rect.y = (HEIGHT - player_img.get_height())

car_colors = ["red", "yellow"]
cars = []

score = 0

#timer event for increasing score every second
timer_event = pygame.USEREVENT + 1
pygame.time.set_timer(timer_event, 100) 

start_time = time.time()

speed = 0
max_speed = 20
acceleration_rate = 0.2
deceleration_rate = 0.3
min_brakeing_speed = 7
player_x_vel = 5
player_fast_x_vel = 10

bg_music.play(-1)


class Car:
    def __init__(self, image, x, y, speed):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def move(self, speed=None):
        if self.rect.y > HEIGHT:
            cars.remove(self)
        if speed == None:
            self.rect.y += self.speed
        else:
            self.rect.y += speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)


    def check_collision(self, other_cars):
        for car in other_cars:
            if self.rect.colliderect(car.rect):
                return True
        return False
    


class Button:
    def __init__(self, x, y, width, height, color, hover_color, border_color, text_color, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.border_color = border_color
        self.text_color = text_color
        self.text = text
        self.action = action

    def draw(self, surface):
        # Draw background
        if self.is_mouse_over():
            pygame.draw.rect(surface, self.hover_color, self.rect, border_radius=10)
        else:
            pygame.draw.rect(surface, self.color, self.rect, border_radius=10)
        
        # Draw border
        pygame.draw.rect(surface, self.border_color, self.rect, 2, border_radius=10)

        # Draw text
        text_surface = font_button.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect()
        text_rect.center = self.rect.center
        surface.blit(text_surface, text_rect)

    def is_mouse_over(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return self.rect.collidepoint(mouse_x, mouse_y)



def check_collision_with_player():
    for car in cars:
        player_margin_rect = player_rect.inflate(-20, -20)
        car_margin_rect = car.rect.inflate(-20, -20)
        if car_margin_rect.colliderect(player_margin_rect):
            if speed and speed >= min_brakeing_speed:
                return True, None
            else:
                if player_rect.centerx > car.rect.centerx:
                    return car, "right"  # Collision on the right side of the player's car
                else:
                    return car, "left"  # Collision on the left side of the player's car
     

    return False, None

 

    
def generate_cars():
    max_cars = 5  # Maximum number of cars on the screen
    if len(cars) < max_cars and random.randint(0, 100) < 1:  
        color = random.choice(car_colors)
        car_image = pygame.image.load("img\\car_{}.png".format(color))
        car_image = pygame.transform.scale(car_image, (120, 250)).convert_alpha()
        car_image = pygame.transform.rotate(car_image, 180)
        x = random.choice([58, 210, 358, 510])
        y = -200  # Start above the screen
        speed = random.randint(6, 10)  # Adjust speed range as needed
        new_car = Car(car_image, x, y, speed)
        # Check collision with existing cars
        if not new_car.check_collision(cars):
            cars.append(new_car)


def draw_cars():
    for car in cars:
        car.move()
        car.draw(screen)


def draw_background():
    screen.blit(road_img, (50,background_y))
    screen.blit(road_img, (50,background_y - HEIGHT + 10))
    screen.blit(road_img, (195,background_y))
    screen.blit(road_img, (195,background_y - HEIGHT + 10))
    screen.blit(road_img, (340,background_y))
    screen.blit(road_img, (340,background_y - HEIGHT + 10))
    screen.blit(road_img, (485,background_y))
    screen.blit(road_img, (485,background_y - HEIGHT + 10))

    screen.blit(grass_img, (-5, background_y))
    screen.blit(grass_img, (-5, background_y - HEIGHT))
    screen.blit(grass_img, (WIDTH - 65, background_y))
    screen.blit(grass_img, (WIDTH - 65, background_y - HEIGHT))


def draw_player():
    screen.blit(player_img, player_rect)




def stopwatch(start_time):
    elapsed_time = time.time() - start_time  # Calculate elapsed time
    minutes = int(elapsed_time // 60)  # Calculate minutes
    seconds = int(elapsed_time % 60)   # Calculate seconds
    milliseconds = int((elapsed_time % 1) * 1000)  # Calculate milliseconds
    return minutes, seconds, milliseconds


def handle_input(keys):
    global background_y, speed
    if keys[pygame.K_RSHIFT]:
        horn_sound.play()

    if keys[pygame.K_UP]:
        # Accelerate
        speed += acceleration_rate
        if speed > max_speed:
            speed = max_speed
        background_y += speed
        for car in cars:
            car.move()
    else:
        # Decelerate
            if speed > 0:
                speed -= deceleration_rate
                background_y += speed
                for car in cars:
                    car.move()

    if keys[pygame.K_DOWN] or keys[pygame.K_SPACE]:
        if speed > min_brakeing_speed:
            speed -= deceleration_rate * (speed/max_speed) 
        background_y -= speed
        brake_sound.play()

    if keys[pygame.K_RIGHT] and player_rect.x < 515:
        if speed >= 10:
            player_rect.x += player_fast_x_vel
        else:
            player_rect.x += player_x_vel

    if keys[pygame.K_LEFT] and player_rect.x > 50:
        if speed >= 10:
            player_rect.x -= player_fast_x_vel
        else:
            player_rect.x -= player_x_vel

    if keys[pygame.K_ESCAPE]:
        pause()



    

def restart_game():
    global cars, speed, score, start_time
    cars = []
    speed = 0
    score = 0
    start_time = time.time()
    player_rect.x = (WIDTH - player_img.get_width()) // 2
    player_rect.y = (HEIGHT - player_img.get_height())
    main()


def car_sound():
    if speed > 8:
        slow_sound.stop()
        fast_sound.play()
    else:
        fast_sound.stop()
        slow_sound.play()


def show_speed():
    speed_text = font_big.render(str(int(5 if speed <= 0 else speed * 10)), True, RED)
    screen.blit(speed_text, (500, 550))

def show_score():
    global score
    score_text = font_small.render(f"Score :{str(score)}", True, YELLOW)
    screen.blit(score_text, (10, 10))
    

def home():
    global start_time
    run = True
    buttons = [Button(150, 360, 150, 50, RED, LIGHT_RED, YELLOW, YELLOW, "Quit", pygame.quit),
            Button(400, 360, 150, 50, RED, LIGHT_RED, YELLOW, YELLOW, "Start", main)]
    title_text = font_big.render("Speed Racer", True, RED)
    home_time = time.time()
    while run:
        clock.tick(FPS)
        screen.blit(home_img, (0, 0))
        screen.blit(title_text, ((WIDTH - title_text.get_width()) // 2, (HEIGHT - title_text.get_height()) // 2 - 100))
        for button in buttons:
            button.draw(screen)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.is_mouse_over():
                        elapsed_pause_time = time.time() - home_time
                        start_time += elapsed_pause_time
                        button.action()




def pause():
    global start_time
    pause_time = time.time()
    game_pause_text = font_big.render("Pause", True, YELLOW)
    for sound in music_list:
        sound.stop()
    buttons = [Button(150, 360, 150, 50, RED, LIGHT_RED, YELLOW, YELLOW, "Restart", restart_game),
                Button(400, 360, 150, 50, RED, LIGHT_RED, YELLOW, YELLOW, "Resume", main),
                Button(275, 460, 150, 50, RED, LIGHT_RED, YELLOW, YELLOW, "Quit", pygame.quit)]

    while True:
        clock.tick(FPS)
        screen.blit(game_pause_text, ((WIDTH - game_pause_text.get_width()) // 2, (HEIGHT - game_pause_text.get_height()) // 2 - 100))
        for button in buttons:
            button.draw(screen)
        pygame.display.flip()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Calculate the elapsed time during pause
                    elapsed_pause_time = time.time() - pause_time
                    start_time += elapsed_pause_time
                    main()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.is_mouse_over():
                        elapsed_pause_time = time.time() - pause_time
                        start_time += elapsed_pause_time
                        button.action()

def game_over():
    game_over_text = font_big.render(f"Crashed", True, RED)
    for sound in music_list:
        sound.stop()
    crash_sound.play()
    buttons = [Button(150, 360, 150, 50, RED, LIGHT_RED, YELLOW, YELLOW, "Quit", pygame.quit),
            Button(400, 360, 150, 50, RED, LIGHT_RED, YELLOW, YELLOW, "Restart", restart_game)]
    while True:
        clock.tick(FPS)
        screen.blit(game_over_text, ((WIDTH - game_over_text.get_width()) // 2, (HEIGHT - game_over_text.get_height()) // 2 - 100))
        for button in buttons:
            button.draw(screen)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    restart_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.is_mouse_over():
                        button.action()



def main():
    global background_y, score, start_time
    pause_button = Button(590, 8, 100, 50, RED, LIGHT_RED, YELLOW, YELLOW, "Pause", pause)

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == timer_event:
                if speed > 15:
                    score += 10
                if speed > 10:
                    score += 5
                if speed > 5:
                    score += 2


            if event.type == pygame.MOUSEBUTTONDOWN:
                    if pause_button.is_mouse_over():
                        pause_button.action()

        keys = pygame.key.get_pressed()
        handle_input(keys) 
        # Update background positions
        background_y += 5


        # If the road or grass goes beyond the screen, reset their positions
        if background_y >= HEIGHT:
            background_y = 0


        screen.fill((0, 200, 0))  # Fill the screen with black background
        draw_background()
        draw_player()
        generate_cars()
        draw_cars()
        show_speed()
        car_sound()
        show_score()
        pause_button.draw(screen)
        # Update and display stopwatch
        minutes, seconds, milliseconds = stopwatch(start_time)
        stop_watch_text = font_small.render(f"{minutes:02}:{seconds:02}.{milliseconds:03}", True, YELLOW)
        screen.blit(stop_watch_text, (10, 50))

        collision, side = check_collision_with_player()
        if collision == True:
            run = False
            game_over()
        elif isinstance(collision, Car):

            if side == None:
                collision.rect.x -= 20
            if side == "right":
                collision.rect.x -= 20
            if side == "left":
                collision.rect.x += 20
        



        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    home()

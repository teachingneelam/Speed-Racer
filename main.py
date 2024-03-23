import pygame
import random
import sys

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 600, 600
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Speed Racer - Take a Ride")

clock = pygame.time.Clock()

# Loading images
road_img = pygame.image.load("img\\road.png")
road_img = pygame.transform.scale(road_img, (WIDTH, HEIGHT)).convert_alpha()

grass_img = pygame.image.load("img\\grass2.jpg")
grass_img = pygame.transform.scale(grass_img, (90, HEIGHT)).convert_alpha()


player_img = pygame.image.load("img\\car_red.png")
# player_img = pygame.transform.rotate(player_img, 90)
player_img = pygame.transform.scale(player_img, (150, 300)).convert_alpha()


cars = []



class Car:
    def __init__(self, image, x, y, speed):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = speed

    def move(self):
        self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)


def generate_cars():
    if random.randint(0, 100) < 5:  # Adjust the probability as needed
        car_image = pygame.image.load("img\\car_red.png")
        car_image = pygame.transform.scale(car_image, (150, 300)).convert_alpha()
        x = random.randint(50, WIDTH - 50)
        y = -150  # Start above the screen
        speed = random.randint(3, 8)  # Adjust speed range as needed
        cars.append(Car(car_image, x, y, speed))

def display_cars():
    for car in cars:
        car.move()
    for car in cars():
        car.draw(screen)

# Initial position of road and grass
background_y = 0
player_x = (WIDTH - player_img.get_width()) // 2

def draw_background():
    global road_y, grass_y
    screen.blit(road_img, (0,background_y))
    screen.blit(road_img, (0,background_y - HEIGHT + 10))
    screen.blit(road_img, (-140,background_y))
    screen.blit(road_img, (-140,background_y - HEIGHT + 10))
    screen.blit(road_img, (140,background_y))
    screen.blit(road_img, (140,background_y - HEIGHT + 10))
    screen.blit(grass_img, (0, background_y))
    screen.blit(grass_img, (0, background_y - HEIGHT))
    screen.blit(grass_img, (WIDTH - 90, background_y))
    screen.blit(grass_img, (WIDTH - 90, background_y - HEIGHT))
    screen.blit(player_img, ( player_x, HEIGHT - player_img.get_height()))

def handle_movement(keys):
    global background_y, player_x
    if keys[pygame.K_UP]:
        background_y += 8
    if keys[pygame.K_DOWN] or keys[pygame.K_SPACE]:
        background_y -= 3
    if keys[pygame.K_RIGHT] and player_x < 380:
        player_x += 3
    if keys[pygame.K_LEFT] and player_x > 73:
        player_x -= 3




def main():
    global background_y
    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        handle_movement(keys) 
        # Update background positions
        background_y += 5


        # If the road or grass goes beyond the screen, reset their positions
        if background_y >= HEIGHT:
            background_y = 0
        if background_y >= HEIGHT:
            background_y = 0

        screen.fill((0, 0, 0))  # Fill the screen with black background
        draw_background()
        
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()

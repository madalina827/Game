import pygame
import random
# Initializarea Pygame
pygame.init()
screen = pygame.display.set_mode((800, 700))
pygame.display.set_caption("Joc chrome")
clock = pygame.time.Clock()
# Incarcarea imaginii dinozaurului
try :
    dino = pygame.image.load("dino.png")
    dino_img = pygame.transform.scale(dino, (80, 80))
except:
    print("Nu s-a putut incarca imaginea dino.png")
    dino_img = None
# Setarile initiale ale dinozaurului
dino_position = pygame.Rect(50, 375, 90, 90)
viteza_dino = 0
inaltime_saritura = -18
gravity = 0.8
is_jumping = False
is_bending = False
number_of_jumps = 0
#Incarcarea imaginii cactusului
try :
    cactus = pygame.image.load("cactus.png")
    cactus_img = pygame.transform.scale(cactus, (50, 100))
except:
    print("Nu s-a putut incarca imaginea cactus.png")
    cactus_img = None
cactus_position = pygame.Rect(800, 350, 50, 100)
cactus_speed = 5
# Incarcarea imaginii pasarii
try:
    bird = pygame.image.load("bird.png")
    bird_img = pygame.transform.scale(bird, (80, 50))
except:
    print("Nu s-a putut incarca imaginea bird.png")
    bird_img = None
bird_position = pygame.Rect(800, 325, 80, 50)
bird_speed = 7
# Tipul initial de obstacol
distanta_intre_obstacole = 600
obstacole = []
def generate_obstacle():
    type = random.choice(['cactus', 'bird'])
    number_of_obstacles = random.randint(1, 2)
    for i in range(number_of_obstacles):
        if type == 'cactus':
            obs = pygame.Rect(800 + i* 50, 350, 50, 100)
        else:
            bird_y = random.randint(275, 375)
            obs = pygame.Rect(800 + i* 80, bird_y, 80, 50)
        obstacole.append({'type': type, 'obs': obs})
generate_obstacle()
# Bucla principala a jocului
max_score = 0
font_max_score = pygame.font.SysFont(None, 35)
score = 0
font_score = pygame.font.SysFont(None, 35)
game_over = False
font_game_over = pygame.font.SysFont(None, 55)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #Comenzi de la tastatura
        if event.type == pygame.KEYDOWN:
            # Saritura dinozaurului
            if event.key == pygame.K_UP and not is_bending and not game_over:
                if number_of_jumps < 2:
                    viteza_dino = inaltime_saritura
                    is_jumping = True
                    number_of_jumps += 1
            # Aplecarea dinozaurului
            if event.key == pygame.K_DOWN and not is_jumping and not game_over:
                is_bending = True
                dino_position = pygame.Rect(50, 415, 40, 40)
            # Resetare joc
            if event.key == pygame.K_r and game_over:
                game_over = False
                number_of_jumps = 0
                dino_position = pygame.Rect(50, 375, 90, 90)
                viteza_dino = 0
                score = 0
                is_jumping = False
                is_bending = False
                obstacole.clear()
                generate_obstacle()
                print("Joc restartat")
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                is_bending = False
                dino_position = pygame.Rect(50, dino_position.y, 40, 40)
                if not is_jumping:
                    dino_position.y = 375
    if not game_over:
        sol = 415 if is_bending else 375
        if is_jumping or dino_position.y < sol:
            viteza_dino += gravity
            dino_position.y += viteza_dino
        if dino_position.y >= sol:
            dino_position.y = sol
            is_jumping = False
            viteza_dino = 0
            number_of_jumps = 0
        if len(obstacole) == 0:
            generate_obstacle()
        else:
            last_obstacle = obstacole[-1]['obs']
            if last_obstacle.x < 800 - distanta_intre_obstacole:
                generate_obstacle()
        for obstacle in obstacole:
            if obstacle['type'] == 'cactus':
                obstacle['obs'].x -= cactus_speed
            else:
                obstacle['obs'].x -= bird_speed
            if dino_position.colliderect(obstacle['obs']):
                game_over = True
        new_obstacles = []
        for obstacle in obstacole:
            if obstacle['obs'].x > -100:
                new_obstacles.append(obstacle)
            else:
                score += 1
        obstacole = new_obstacles
    screen.fill((255, 255, 255))
    pygame.draw.line(screen, (0, 0, 0), (0, 445), (800, 445), 2)
    if dino_img:
        if is_bending:
            dino_bent_img = pygame.transform.scale(dino_img, (40, 40))
            screen.blit(dino_bent_img, (dino_position.x, dino_position.y))
        else:
            screen.blit(dino_img, (dino_position.x, dino_position.y))
    else:
        pygame.draw.rect(screen, (0, 0, 0), dino_position)
    for obstacle in obstacole:
        if obstacle['type'] == 'cactus':
            if cactus_img:
                screen.blit(cactus_img, (obstacle['obs'].x, obstacle['obs'].y))
            else:
                pygame.draw.rect(screen, (225, 0, 0), obstacle['obs'])
        else:
            if bird_img:
                screen.blit(bird_img, (obstacle['obs'].x, obstacle['obs'].y))
            else:
                pygame.draw.rect(screen, (0, 0, 225), obstacle['obs'])
    max_score_text = font_max_score.render(f"Scor Maxim: {max_score}", True, (0, 0, 0))
    screen.blit(max_score_text, (600, 10))
    score_text = font_score.render(f"Scor: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    if score > max_score:
        max_score = score
    if game_over:
        game_over_text = font_game_over.render("Game Over!", True, (225, 0, 0))
        screen.blit(game_over_text, (295, 150))
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
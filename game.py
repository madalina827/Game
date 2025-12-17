import pygame
import random

pygame.init()
screen = pygame.display.set_mode((800, 700))
pygame.display.set_caption("Joc chrome")
clock = pygame.time.Clock()
dino_img = None
dino_mask = None
dino_bent_img = None
dino_bent_mask = None
cactus_img = None
cactus_mask = None
bird_img = None
bird_mask = None
cloud_img = None
def incarca_imagini(mod):
    global dino_img, dino_mask, dino_bent_img, dino_bent_mask
    global cactus_img, cactus_mask, bird_img, bird_mask, cloud_img
    sufix = "" 
    if mod == "fun":
        sufix = "_fun" 
    # Dino
    try:
        dino = pygame.image.load(f"dino{sufix}.png")
        dino_img = pygame.transform.scale(dino, (80, 80))
        dino_mask = pygame.mask.from_surface(dino_img)
        dino_bent_img = pygame.transform.scale(dino_img, (40, 36))
        dino_bent_mask = pygame.mask.from_surface(dino_bent_img)
    except:
        print(f"Nu s-a putut incarca dino{sufix}.png")
        dino_img = None
    # Cactus
    try:
        cactus = pygame.image.load(f"cactus{sufix}.png")
        cactus_img = pygame.transform.scale(cactus, (50, 100))
        cactus_mask = pygame.mask.from_surface(cactus_img)
    except:
        print(f"Nu s-a putut incarca cactus{sufix}.png")
        cactus_img = None
    # Bird
    try:
        bird = pygame.image.load(f"bird{sufix}.png")
        bird_img = pygame.transform.scale(bird, (80, 50))
        bird_mask = pygame.mask.from_surface(bird_img)
    except:
        print(f"Nu s-a putut incarca bird{sufix}.png")
        bird_img = None
    # Cloud
    try:
        cloud_file = pygame.image.load(f"clouds{sufix}.png")
        cloud_img = pygame.transform.scale(cloud_file, (300, 150))
    except:
        print(f"Nu s-a putut incarca clouds{sufix}.png")
        cloud_img = None
cloud = []
obstacole = []
dino_position = pygame.Rect(50, 375, 90, 90)
viteza_dino = 0
inaltime_saritura = -18
gravity = 0.8
is_jumping = False
is_bending = False
number_of_jumps = 0
cactus_speed = 5
bird_speed = 7
distanta_intre_obstacole = 600
max_score = 0
score = 0
font_score = pygame.font.SysFont(None, 35)
font_max_score = pygame.font.SysFont(None, 35)
font_game_over = pygame.font.SysFont(None, 55)
game_state = "menu"
current_mode = "classic"
buton_classic = pygame.Rect(300, 300, 200, 60)
buton_fun = pygame.Rect(300, 400, 200, 60)
font_menu = pygame.font.SysFont(None, 40)
def reset_game(mode):
    global cactus_speed, bird_speed, distanta_intre_obstacole, score, viteza_dino
    global is_jumping, is_bending, number_of_jumps, dino_position, game_over
    incarca_imagini(mode)
    obstacole.clear()
    cloud.clear()
    dino_position = pygame.Rect(50, 375, 90, 90)
    viteza_dino = 0
    is_jumping = False
    is_bending = False
    number_of_jumps = 0
    score = 0
    game_over = False
    cactus_speed = 5
    bird_speed = 7
    distanta_intre_obstacole = 600
    generate_obstacle()
def generate_obstacle():
    type = random.choice(['cactus', 'bird'])
    number_of_obstacles = random.randint(1, 2)
    for i in range(number_of_obstacles):
        if type == 'cactus':
            obs = pygame.Rect(800 + i* 50, 350, 50, 100)
        else:
            bird_y = random.randint(275, 385)
            obs = pygame.Rect(800 + i* 80, bird_y, 80, 50)
        obstacole.append({'type': type, 'obs': obs})
#Joc
running = True
game_over = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_state == "menu":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = event.pos
                    if buton_classic.collidepoint(mouse_pos):
                        current_mode = "classic"
                        reset_game("classic")
                        game_state = "run"
                    elif buton_fun.collidepoint(mouse_pos):
                        current_mode = "fun"
                        reset_game("fun")
                        game_state = "run"
        elif game_state == "run":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and not is_bending and not game_over:
                    if number_of_jumps < 2:
                        viteza_dino = inaltime_saritura
                        is_jumping = True
                        number_of_jumps += 1
                if event.key == pygame.K_DOWN and not is_jumping and not game_over:
                    is_bending = True
                    dino_position = pygame.Rect(50, 415, 40, 40)
                if event.key == pygame.K_r and game_over:
                    reset_game(current_mode)
                if event.key == pygame.K_ESCAPE:
                    game_state = "menu"
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    is_bending = False
                    dino_position = pygame.Rect(50, dino_position.y, 40, 40)
                    if not is_jumping:
                        dino_position.y = 375
    if game_state == "menu":
        screen.fill((255, 255, 255))
        titlu = font_game_over.render("ALEGE MODUL", True, (0, 0, 0))
        screen.blit(titlu, (275, 200))
        pygame.draw.rect(screen, (100, 80, 80), buton_classic)
        text_classic = font_menu.render("CLASSIC", True, (255, 255, 255))
        screen.blit(text_classic, (buton_classic.x + 40, buton_classic.y + 15))
        pygame.draw.rect(screen, (200, 0, 200), buton_fun)
        text_fun = font_menu.render("FUN MODE", True, (255, 255, 255))
        screen.blit(text_fun, (buton_fun.x + 30, buton_fun.y + 15))
    elif game_state == "run":
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
            #Clouds
            dist_clouds = False
            if len(cloud) == 0:
                if random.randint(0, 100) < 1: dist_clouds = True
            else:
                if cloud[-1].x < 600 and random.randint(0, 100) < 1: dist_clouds = True
            if dist_clouds:
                y_cloud = random.randint(50, 200)
                cloud.append(pygame.Rect(800, y_cloud, 100, 60))
            for cl in cloud: cl.x -= 2
            cloud = [cl for cl in cloud if cl.x > -150]
            if len(obstacole) == 0:
                generate_obstacle()
            else:
                if obstacole[-1]['obs'].x < 800 - distanta_intre_obstacole:
                    generate_obstacle()
            #Miscare si coliziune
            for obstacle in obstacole:
                if obstacle['type'] == 'cactus':
                    obstacle['obs'].x -= cactus_speed
                else:
                    obstacle['obs'].x -= bird_speed
                #Coiziune
                dino_current_mask = dino_bent_mask if is_bending else dino_mask
                obstacle_mask = cactus_mask if obstacle['type'] == 'cactus' else bird_mask
                offset = (obstacle['obs'].x - dino_position.x, obstacle['obs'].y - dino_position.y)  
                if dino_current_mask and obstacle_mask:
                    if dino_current_mask.overlap(obstacle_mask, offset):
                        game_over = True
            #Scor
            new_obstacles = []
            for obstacle in obstacole:
                if obstacle['obs'].x > -100:
                    new_obstacles.append(obstacle)
                else:
                    score += 1
                    if score % 50 == 0:
                        cactus_speed += 0.5
                        bird_speed += 0.5
                    if score % 100 == 0:
                        if distanta_intre_obstacole > 300:
                            distanta_intre_obstacole -= 20
            obstacole = new_obstacles
        screen.fill((255, 255, 255))
        #Clouds
        if cloud_img:
            for c in cloud: screen.blit(cloud_img, (c.x, c.y))
        else:
            for c in cloud: pygame.draw.rect(screen, (200, 200, 200), c)
        pygame.draw.line(screen, (0, 0, 0), (0, 445), (800, 445), 2)
        # Dino
        if dino_img:
            if is_bending:
                screen.blit(dino_bent_img, (dino_position.x, dino_position.y))
            else:
                screen.blit(dino_img, (dino_position.x, dino_position.y))
        else:
            pygame.draw.rect(screen, (50, 50, 50), dino_position)
        #Obstacole
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
        if score > max_score:
            max_score = score
        max_score_text = font_max_score.render(f"Scor Maxim: {max_score}", True, (0, 0, 0))
        screen.blit(max_score_text, (600, 10))
        score_text = font_score.render(f"Scor: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))
        if game_over:
            game_over_text = font_game_over.render("Game Over!", True, (225, 0, 0))
            screen.blit(game_over_text, (290, 150))
            esc_text = font_score.render("Apasa R (Restart) sau ESC (Meniu)", True, (100, 100, 100))
            screen.blit(esc_text, (220, 200))
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
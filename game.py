import pygame
import time

pygame.init()

WIDTH, HEIGHT = 1080, 720
FPS = 60
GRAVITY = 0.8
Y_VEL = int(10)
SCOREPM = 10

run = True

font = pygame.font.Font(None, 36)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Geometry Dash recreated")

class Player:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
        self.col = (255, 125, 245)
        self.rect = pygame.Rect(self.x, self.y, 50, 50)
        self.rect.center = (self.x, self.y)
        self.jumping = False
        self.y_vel = Y_VEL
        self.jump_height = 50
        self.dead = False
        self.score = 0

    def update(self):
        pygame.draw.rect(screen, self.col, self.rect)
    
    def jump(self):
        if self.jumping:
            self.y -= self.y_vel
            self.y_vel -= GRAVITY
            if self.y >= int(HEIGHT/2+10):  # Vérifie si le cube a atteint le sol
                self.y = int(HEIGHT/2+10)
                self.y_vel = Y_VEL
                self.jumping = False

        # Mettez à jour la position du cube en dehors de la condition if
        self.rect = pygame.Rect(self.x, self.y, 50, 50)
        self.rect.center = (self.x, self.y)

    def check_collision(self):
        if self.y + 50 >= HEIGHT:  # Si le cube atteint le sol
            self.y = HEIGHT - 50  # Ajuster la position du cube pour éviter qu'il ne traverse le sol
            self.jumping = False  # Arrêter le saut
            self.y_vel = 0  # Réinitialiser la vitesse verticale

    def die(self):
        self.dead = True


class Map():
    def __init__(self, map):
        self.map = map
        self.x = int(10)
        self.y = int(HEIGHT/2+50)
        self.col = (255, 255, 255)
        self.rect = pygame.Rect(self.x, self.y, 50, 50)
        self.rect.center = (self.x, self.y)
        self.type = [0,
                     1,
                     2]
        self.spikes = []
        self.count = 0

        print(map)
        print("this map")

        self.rectl = []
    def update(self):
        self.rectl = []
        currTime = time.monotonic()
        self.score = int((currTime-startTime)*SCOREPM)
        for i in range(len(self.map)):
            if self.map[i] == 1:
                self.rect = pygame.Rect(int(self.x+i*50), int(self.y), 50, 50)
                self.rect.center = (int(self.x+i*50), int(self.y))
                self.rectl.append((self.rect, self.type[1]))
                pygame.draw.rect(screen, self.col, self.rect)
            elif self.map[i] == 2:
                rect_center_x = self.x + i * 50  # Coordonnée x du centre du rectangle
                rect_center_y = self.y  # Coordonnée y du centre du rectangle
                x1 = rect_center_x
                y1 = rect_center_y - 25
                x2 = rect_center_x - 25
                y2 = rect_center_y + 25
                x3 = rect_center_x + 25
                y3 = rect_center_y + 25
                """
                x1 = self.x + i * 50
                y1 = self.y - 25
                x2 = self.x + i * 50 - 25
                y2 = self.y + 25
                x3 = self.x + i * 50 + 25
                y3 = self.y + 25
                """
                triangle = [(x1, y1), (x2, y2), (x3, y3)]
                pygame.draw.polygon(screen, self.col, triangle)
                self.spikes.append((triangle, self.type[2]))

    
    def check_collision(self, player):
        for rect, shape_type in self.rectl:
            if shape_type == 1 and rect.colliderect(player.rect):
                print("Collision with square", self.count)
                self.count += 1
        for shape, shape_type in self.spikes:
            if shape_type == 2 and self.check_triangle_collision(shape, player.rect):
                print("Collision with spike", self.count)
                endTime = time.monotonic()
                print("You survived ", endTime-startTime, "s")
                player.die()
                print(self.score)

    def check_triangle_collision(self, triangle, player_rect):
        # Convertir les points du triangle en rectangles pour faciliter la détection de collision
        rect_center_x = triangle[0][0]  # Coordonnée x du centre du rectangle
        rect_center_y = triangle[0][1] + 25  # Coordonnée y du centre du rectangle
        triangle_rect = pygame.Rect(rect_center_x - 25, rect_center_y - 25, 50, 50)
        
        # Vérifier la collision entre le rectangle du joueur et le rectangle du triangle
        if triangle_rect.colliderect(player_rect):
            return True
        return False
    

#print(object1.colliderect(object2))

cube = Player(WIDTH/2-150, HEIGHT/2+10)
map = Map([1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])

cube.score = font.render("Score: " + str(cube.score), True, (255, 255, 255))

clock = pygame.time.Clock()

startTime = time.monotonic()
endTime = 0
while run == True:

    clock.tick(FPS)

    map.x -= 5

    print(map.rectl, " ------------------------\n")
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                cube.jumping = True
                print("jump")
            if event.key == pygame.K_RIGHT:
                cube.x += 20
            if event.key == pygame.K_LEFT:
                cube.x -= 20
            if event.key == pygame.K_DOWN:
                cube.y += 10
            if event.key == pygame.K_UP:
                cube.y -= 10

    cube.jump()
    cube.check_collision()
    map.check_collision(cube)
    screen.fill((0, 0, 0))
    map.update()
    
    cube.update()
    if cube.dead == True:
        run = False

    currTime = time.monotonic()
    cube.score = (currTime - startTime) * SCOREPM
    cube.score = font.render("Score: " + str(int(cube.score)), True, (255, 255, 255))
    screen.blit(cube.score, (10, 10))

    pygame.display.update()
pygame.quit()
import pygame
import os


pygame.init()


RUN = True

#WINDOW
pygame.display.set_caption("First game")
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

#BACKGROUD
SKY_RAW = pygame.image.load(os.path.join('Images','Sky.png'))
SKY = pygame.transform.scale(SKY_RAW,(WIDTH,HEIGHT))



#GAME-PHYSICS


#GAME-VARIABLES
x1 = 225
y1 = 250 - 15
x2, y2 = 675, 250 - 15

HP1num = 100
HP2num = 100

#GAME-CONSTANTS
VELOCITY = 5
BVELOCITY = 8
BLUE = ((0,0,255))
WHITE = ((255,255,255))
RESULT_COORDINATE = ((300,200))

#GAME OBJECTS
    #MOVABLES
J1RAW = pygame.image.load(os.path.join('Images','YellowJet.png'))
J2RAW = pygame.image.load(os.path.join('Images','BlueJet.png'))

J1RAW = pygame.transform.scale(J1RAW,(30,30))
J2RAW = pygame.transform.scale(J2RAW,(30,30))

J1 = pygame.transform.rotate(J1RAW, 270)
J2 = pygame.transform.rotate(J2RAW, 90)

J1BULLETS = []
J2BULLETS = []


    #NON-MOVABLE
barrier = pygame.Rect(WIDTH/2 - 2,0,4,HEIGHT)

#TEXTS
#all_fonts = pygame.font.get_fonts()
HP = pygame.font.SysFont(None, 20)
HP1 = HP.render("Health Points: "+ str(HP1num),1,WHITE)
HP2 = HP.render("Health Points: "+ str(HP2num),1,WHITE)

RESULT_FONT = pygame.font.SysFont(None, 75)
WINNER = RESULT_FONT.render("",1,WHITE)

#GAME_SOUND
FIRE = pygame.mixer.Sound(os.path.join('Sounds','Fire.wav'))
HIT = pygame.mixer.Sound(os.path.join('Sounds','Hit.wav'))


#UPDATE COORDINATES
def update_rect1(inputkey, rect1):
    if inputkey[pygame.K_w] and rect1.y>15:
        rect1.y = rect1.y - VELOCITY
    elif inputkey[pygame.K_s] and rect1.y < HEIGHT-15:
        rect1.y = rect1.y+VELOCITY
    elif inputkey[pygame.K_a] and rect1.x > 25:
        rect1.x = rect1.x - VELOCITY
    elif inputkey[pygame.K_d] and rect1.x < WIDTH/2 - 9:
        rect1.x =rect1.x + VELOCITY

def update_rect2(inputkey, rect2):
    if inputkey[pygame.K_UP] and rect2.y>15:
        rect2.y = rect2.y - VELOCITY
    elif inputkey[pygame.K_DOWN] and rect2.y < HEIGHT-15:
        rect2.y = rect2.y+VELOCITY
    elif inputkey[pygame.K_LEFT] and rect2.x > WIDTH/2 + 9:
        rect2.x = rect2.x - VELOCITY
    elif inputkey[pygame.K_RIGHT] and rect2.x < WIDTH - 25:
        rect2.x =rect2.x + VELOCITY

def update_bullet(rect1,rect2):
    global HP1
    global HP2
    global HP1num
    global HP2num

    for bullet in J1BULLETS:
        if bullet.x > WIDTH:
            J1BULLETS.remove(bullet)
        elif bullet.colliderect(rect2):
            J1BULLETS.remove(bullet)
            HIT.play()
            '''
            pygame.mixer.music.load(os.path.join('Sounds', 'Hit.mp3'))
            pygame.mixer.music.play()
            time.sleep(2)
            pygame.mixer.music.stop()
            '''
            HP2num -= 20
            HP2 = HP.render("Health Points: "+ str(HP2num),1,WHITE)
            if (HP2num == 0):#GAMEOVER CONDITION
                end(1)
        else:
            bullet.x += BVELOCITY
    for bullet in J2BULLETS:
        if bullet.x < 0:
            J2BULLETS.remove(bullet)
        elif bullet.colliderect(rect1):
            J2BULLETS.remove(bullet)
            '''
            pygame.mixer.music.load(os.path.join('Sounds', 'Hit.mp3'))
            pygame.mixer.music.play()
            time.sleep(2)
            pygame.mixer.music.stop()
            '''
            HIT.play()
            HP1num -= 20
            HP1 = HP.render("Health Points: " + str(HP1num), 1, WHITE)
            if (HP1num == 0):#GAMEOVER CONDITION
                end(0)
        else:
            bullet.x -= BVELOCITY

#END CONDITION
def end(num):
    global WINNER
    if num == 0:
        WINNER = RESULT_FONT.render("JET 2 WINS",1,WHITE)
    else:
        WINNER = RESULT_FONT.render("JET 1 WINS",1,WHITE)
    draw_result()
    global RUN
    RUN = False


#DRAW FUNCTION
def draw_result():
    global WINNER
    WIN.blit(WINNER,RESULT_COORDINATE)
    pygame.display.update()
    pygame.time.delay(3000)
def draw_bullet():
    for bullet in J1BULLETS:
        pygame.draw.rect(WIN,WHITE,bullet)
    for bullet in J2BULLETS:
        pygame.draw.rect(WIN, WHITE, bullet)

def draw(rect1,rect2):
    WIN.blit(SKY,(0,0))
    pygame.draw.rect(WIN, BLUE, barrier)
    WIN.blit(HP1,(10,10))
    WIN.blit(HP2, (750, 10))
    WIN.blit(J1,(rect1.x,rect1.y+2.5))
    WIN.blit(J2,(rect2.x,rect2.y+2.5))
    draw_bullet()

    pygame.display.update()

#MAIN-FUNCTION
def main():
    global RUN
    clock = pygame.time.Clock()
    rect1 = pygame.Rect(x1, y1, 30, 30)
    rect2 = pygame.Rect(x2, y2, 30, 30)
    #GAME-LOOP
    while RUN:
        #FPS
        clock.tick(30)
        #EXIT-CONDITION
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUN = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f and len(J1BULLETS) < 5:
                    J1BULLETS.append(pygame.Rect(rect1.x+30,rect1.y+15,5,5))
                    '''pygame.mixer.music.load(os.path.join('Sounds', 'Fire.mp3'))
                    pygame.mixer.music.play()
                    time.sleep(2)
                    pygame.mixer.music.stop()'''
                    FIRE.play()
                elif event.key == pygame.K_KP0 and len(J2BULLETS) < 5:
                    J2BULLETS.append(pygame.Rect(rect2.x,rect2.y+15,5,5))
                    '''pygame.mixer.music.load(os.path.join('Sounds', 'Fire.mp3'))
                    pygame.mixer.music.play()
                    time.sleep(2)
                    pygame.mixer.music.stop()'''
                    FIRE.play()
                #bullet(event.key)

        #RECIEVES KEYBOARD INPUT
        inputkey = pygame.key.get_pressed()
        update_rect1(inputkey, rect1)
        update_rect2(inputkey, rect2)
        update_bullet(rect1,rect2)
        draw(rect1,rect2)
    pygame.quit()

if __name__ == "__main__":
    main()
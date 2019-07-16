import sys, pygame
from pygame.locals import *
import random
w = 800
h = 600

heading = "oikea"
grow = False

screen = pygame.display.set_mode((w,h))
clock = pygame.time.Clock()

## Aloituspaikka
start_snake_list = ((180, 300), (160, 300), (140, 300), (120, 300))
current_apple = (400,300)
list_snake = list(start_snake_list)

def draw_grid():
    '''
    Piirretään grid
    :return:
    '''
    x = 20
    y = 20

    global heading

    pygame.draw.line(screen, (0, 200, 200), (x, y), (780, x), (1))
    pygame.draw.line(screen, (0, 200, 200), (x, y), (x, 580), (1))

    while x < 800 or h < 600:
        for event in pygame.event.get():
            ## Painikkeiden bindaus nuolista ohjaa ja esc quit
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == KEYDOWN:
                global heading
                if event.key == K_ESCAPE:
                    sys.exit()
                elif event.key == pygame.K_UP and heading != "alas":
                    heading = "ylos"
                elif event.key == pygame.K_DOWN and heading != "ylos":
                    heading = "alas"
                elif event.key == pygame.K_LEFT and heading != "oikea":
                    heading = "vasen"
                elif event.key == pygame.K_RIGHT and heading != "vasen":
                    heading = "oikea"


        if x < 800:
            x += 20
        if y < 600:
            y += 20

        pygame.draw.line(screen, (0, 200, 200), (20, y), (780, x), (1))
        pygame.draw.line(screen, (0, 200, 200), (x, 20), (x, 580), (1))

def draw_snake(list_snake):
    '''
    Piirretään käärme näytölle listan annettuihin ruutuihin
    :param list_snake:
    :return:
    '''
    for x,y in list_snake:
        pygame.draw.rect(screen, (255, 255, 255), Rect(x, y, 20, 20))

def move_snake(heading_direction, l_snake, grow_more):
    '''
    Siirretään käärmettä yhden ruudun verran menosuuntaan
    :param heading:
    :param list_snake:
    :return:
    '''

    last_move = l_snake[0]
    ## Poistetaan viimeinen jos ei kasveta
    if not grow_more:
        l_snake.pop()
    else:
        grow_more = False

    if heading_direction == "oikea":
        new_val = (last_move[0] + 20, last_move[1])
        l_snake.insert(0, new_val)
    elif heading_direction == "alas":
        new_val = (last_move[0], last_move[1] + 20)
        l_snake.insert(0, new_val)
    elif heading_direction == "vasen":
        new_val = (last_move[0] - 20, last_move[1])
        l_snake.insert(0, new_val)
    elif heading_direction == "ylos":
        new_val = (last_move[0], last_move[1] - 20)
        l_snake.insert(0, new_val)

    return l_snake,grow_more

def check_if_dead(l_snake):
    '''
    tarkistetaan ettei käärme ole ajanut itseensä tai seinään
    :param l_snake:
    :return:
    '''
    global start_snake_list
    global heading
    dublicate_check = set([x for x in l_snake if l_snake.count(x) > 1])

    ## Törmäsit itseesi
    if len(dublicate_check) > 0:
        l_snake = list(start_snake_list)
        heading = "oikea"
        return l_snake

    ## törmäsit johonkin seinään
    for x,y in l_snake:
        if x == 0 or y == 0 or x == 780 or y == 580:
            l_snake = list(start_snake_list)
            heading = "oikea"
            break
    return l_snake

def draw_apple(apple,l_snake,will_grow):

    for x,y in l_snake:
        if apple == (x,y):
            will_grow = True

            while True:
                new_x = random.randint(1,38) * 20
                new_y = random.randint(1,28) * 20

                new_apple = (new_x,new_y)
                if new_apple not in l_snake:
                    apple = new_apple
                    break


            break

    pygame.draw.rect(screen, (0, 255, 0), Rect(apple[0], apple[1], 20, 20))

    return apple,will_grow


while 1:
    clock.tick(17)

    screen.fill((0, 0, 0))

    draw_grid()
    draw_snake(list_snake)
    current_apple,grow = draw_apple(current_apple,list_snake,grow)

    list_snake,grow = move_snake(heading, list_snake, grow)
    list_snake = check_if_dead(list_snake)

    print("Score:" + str(len(list_snake)- 4))

    pygame.display.update()





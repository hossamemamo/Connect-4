import pygame
import main
import ctypes
import time
pygame.init()
screen = pygame.display.set_mode((700, 600))
color_light = (170,170,170)


def button(screen, position, text,color=(100,100,100)):
    font = pygame.font.SysFont("Arial", 50)
    text_render = font.render(text, 1, (255, 255, 255))
    x, y, w, h = text_render.get_rect()
    x, y = position
    pygame.draw.line(screen, (150, 150, 150), (x, y), (x + w, y), 5)
    pygame.draw.line(screen, (150, 150, 150), (x, y - 2), (x, y + h), 5)
    pygame.draw.line(screen, (50, 50, 50), (x, y + h), (x + w, y + h), 5)
    pygame.draw.line(screen, (50, 50, 50), (x + w, y + h), [x + w, y], 5)
    pygame.draw.rect(screen, color, (x, y, w, h))
    return screen.blit(text_render, (x, y))

def start():
    print("Ok, let's go")
    main.star()

def menu():
    """ This is the menu that waits you to click the s key to start """
    colorAI = (100, 100, 100)
    colorPlayer = (100, 100, 100)
    colorPruning=(100,100,100)
    colorNoPruning=(100,100,100)
    b1 = button(screen, (150, 500), "Quit")
    b2 = button(screen, (400, 500), "Start")
    b3 = button(screen, (400, 150), "AI", colorAI)
    b4 = button(screen, (150, 150), "Player", colorPlayer)
    b5 = button(screen, (150, 300), "Pruning", colorPruning)
    b6 = button(screen, (400, 300), "without", colorNoPruning)
    b7 = button(screen, (520, 390), "Enter", (100,100,100))
    font = pygame.font.SysFont("Arial", 50)
    font1 = pygame.font.SysFont("Arial", 32)
    text = font.render('       Please select the first player', True, (255, 255, 255))
    text1 = font1.render('Depth', True, (255, 255, 255))
    textRect1 = text1.get_rect()
    textRect = text.get_rect()
    textRect1.center = (250, 410)
    textRect.center = (600 // 2, 50)
    turnCheck = 0
    algoCheck=0
    depthCheck=0
    clock = pygame.time.Clock()
    # it will display on screen
    # basic font for user typed
    base_font = pygame.font.Font(None, 32)
    user_text = ''
    input_rect = pygame.Rect(350, 400, 140, 32)
    color_active = pygame.Color('lightskyblue3')
    color_passive = pygame.Color('chartreuse4')
    color = color_passive
    active = False

    while True:
        screen.blit(text, textRect)
        screen.blit(text1, textRect1)
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
                key_to_start = event.key == pygame.K_s or event.key == pygame.K_RIGHT or event.key == pygame.K_UP
                # if key_to_start:
                #     # if turnCheck == 0 and algoCheck == 0:
                #     #     #ctypes.windll.user32.MessageBoxW(0, "Please select who will play first", "ERROR", 1)
                #     #     print("saeed")
                #     # else:
                #     start()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if b1.collidepoint(pygame.mouse.get_pos()):
                    exit()
                elif b2.collidepoint(pygame.mouse.get_pos()):
                    if turnCheck == 0 and algoCheck == 0 and depthCheck == 0:
                        ctypes.windll.user32.MessageBoxW(0, "Please select who will play first", "ERROR!", 1)
                    else:
                        pygame.display.flip()
                        start()
                elif b3.collidepoint(pygame.mouse.get_pos()):
                    main.turn = 1
                    turnCheck = 1
                    colorAI=(0,0,100)
                    colorPlayer=(100,100,100)
                    b3 = button(screen, (400, 150), "AI", colorAI)
                    b4 = button(screen, (150, 150), "Player", colorPlayer)
                elif b4.collidepoint(pygame.mouse.get_pos()):
                    main.turn = 0
                    turnCheck = 1
                    colorAI=(100,100,100)
                    colorPlayer=(0,0,100)
                    b3 = button(screen, (400, 150), "AI", colorAI)
                    b4 = button(screen, (150, 150), "Player", colorPlayer)
                elif b5.collidepoint(pygame.mouse.get_pos()):
                    main.algorithmChoice=0
                    algoCheck=1
                    colorPruning=(0,0,100)
                    colorNoPruning=(100,100,100)
                    b5 = button(screen, (150, 300), "Pruning", colorPruning)
                    b6 = button(screen, (400, 300), "without", colorNoPruning)
                elif b6.collidepoint(pygame.mouse.get_pos()):
                    main.algorithmChoice=1
                    algoCheck=1
                    colorPruning=(100,100,100)
                    colorNoPruning=(0,0,100)
                    b5 = button(screen, (150, 300), "Pruning", colorPruning)
                    b6 = button(screen, (400, 300), "without", colorNoPruning)
                elif b7.collidepoint(pygame.mouse.get_pos()):
                    depthCheck=1
                    main.deptho = int(user_text)
                    print(main.deptho)
                if input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode
                if event.key == pygame.K_RETURN:
                    main.deptho = int(user_text)
        if active:
            color = color_active
        else:
            color = color_passive
        pygame.draw.rect(screen, color, input_rect)

        text_surface = base_font.render(user_text, True, (255, 255, 255))

        screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
        input_rect.w = max(100, text_surface.get_width() + 10)
        pygame.display.flip()
        clock.tick(60)
        pygame.display.update()
    pygame.quit()

menu()


import sys
import core
import pygame
import modules.Levels as Levels


def startLevelGame(level, screen, font):
    clock = pygame.time.Clock()
    SCORE = 0
    wall_sprites = level.setupWalls(core.SKYBLUE)
    gate_sprites = level.setupGate(core.WHITE)
    hero_sprites, ghost_sprites = level.setupPlayers(core.HEROPATH, [core.BlinkyPATH, core.ClydePATH, core.InkyPATH, core.PinkyPATH])
    food_sprites = level.setupFood(core.YELLOW, core.WHITE)
    is_clearance = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(-1)
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    for hero in hero_sprites:
                        hero.changeSpeed([-1, 0])
                        hero.is_move = True
                elif event.key == pygame.K_RIGHT:
                    for hero in hero_sprites:
                        hero.changeSpeed([1, 0])
                        hero.is_move = True
                elif event.key == pygame.K_UP:
                    for hero in hero_sprites:
                        hero.changeSpeed([0, -1])
                        hero.is_move = True
                elif event.key == pygame.K_DOWN:
                    for hero in hero_sprites:
                        hero.changeSpeed([0, 1])
                        hero.is_move = True
            if event.type == pygame.KEYUP:
                if (event.key == pygame.K_LEFT) or (event.key == pygame.K_RIGHT) or (event.key == pygame.K_UP) or (event.key == pygame.K_DOWN):
                    hero.is_move = False
        screen.fill(core.BLACK)
        for hero in hero_sprites:
            hero.update(wall_sprites, gate_sprites)
        hero_sprites.draw(screen)
        for hero in hero_sprites:
            food_eaten = pygame.sprite.spritecollide(hero, food_sprites, True)
        SCORE += len(food_eaten)
        wall_sprites.draw(screen)
        gate_sprites.draw(screen)
        food_sprites.draw(screen)
        for ghost in ghost_sprites:

            if ghost.tracks_loc[1] < ghost.tracks[ghost.tracks_loc[0]][2]:
                ghost.changeSpeed(ghost.tracks[ghost.tracks_loc[0]][0: 2])
                ghost.tracks_loc[1] += 1
            else:
                if ghost.tracks_loc[0] < len(ghost.tracks) - 1:
                    ghost.tracks_loc[0] += 1
                elif ghost.role_name == 'Clyde':
                    ghost.tracks_loc[0] = 2
                else:
                    ghost.tracks_loc[0] = 0
                ghost.changeSpeed(ghost.tracks[ghost.tracks_loc[0]][0: 2])
                ghost.tracks_loc[1] = 0
            if ghost.tracks_loc[1] < ghost.tracks[ghost.tracks_loc[0]][2]:
                ghost.changeSpeed(ghost.tracks[ghost.tracks_loc[0]][0: 2])
            else:
                if ghost.tracks_loc[0] < len(ghost.tracks) - 1:
                    loc0 = ghost.tracks_loc[0] + 1
                elif ghost.role_name == 'Clyde':
                    loc0 = 2
                else:
                    loc0 = 0
                ghost.changeSpeed(ghost.tracks[loc0][0: 2])
            ghost.update(wall_sprites, None)
        ghost_sprites.draw(screen)
        score_text = font.render("Score: %s" % SCORE, True, core.RED)
        screen.blit(score_text, [10, 10])
        if len(food_sprites) == 0:
            is_clearance = True
            break
        if pygame.sprite.groupcollide(hero_sprites, ghost_sprites, False, False):
            is_clearance = False
            break
        pygame.display.flip()
        clock.tick(10)
    return is_clearance


def showText(screen, font, is_clearance, flag=False):
    clock = pygame.time.Clock()
    msg = 'Game Over!' if not is_clearance else 'REAL HERO!'
    positions = [[235, 233], [65, 303], [170, 333]] if not is_clearance else [[145, 233], [65, 303], [170, 333]]
    surface = pygame.Surface((400, 200))
    surface.set_alpha(10)
    surface.fill((128, 128, 128))
    screen.blit(surface, (100, 200))
    texts = [font.render(msg, True, core.WHITE),
            font.render('Press ENTER to continue or play again.', True, core.WHITE),
            font.render('Press ESCAPE to quit.', True, core.WHITE)]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if is_clearance:
                        if not flag:
                            return
                        else:
                            main(initialize())
                    else:
                        main(initialize())
                elif event.key == pygame.K_ESCAPE:
                    sys.exit()
                    pygame.quit()
        for idx, (text, position) in enumerate(zip(texts, positions)):
            screen.blit(text, position)
        pygame.display.flip()
        clock.tick(10)


def initialize():
    pygame.init()
    icon_image = pygame.image.load(core.ICONPATH)
    pygame.display.set_icon(icon_image)
    screen = pygame.display.set_mode([606, 606])
    pygame.display.set_caption('By Rizwan.AR')
    return screen


def main(screen):
    pygame.mixer.init()
    pygame.mixer.music.load(core.BGMPATH)
    pygame.mixer.music.play(-1, 0.0)
    pygame.font.init()
    font_small = pygame.font.Font(core.FONTPATH, 18)
    font_big = pygame.font.Font(core.FONTPATH, 24)
    for num_level in range(1, Levels.NUMLEVELS+1):
        level = getattr(Levels, f'Level{num_level}')()
        is_clearance = startLevelGame(level, screen, font_small)
        if num_level == Levels.NUMLEVELS:
            showText(screen, font_big, is_clearance, True)
        else:
            showText(screen, font_big, is_clearance)


if __name__ == '__main__':
    main(initialize())

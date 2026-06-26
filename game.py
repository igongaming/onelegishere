import pygame
import sys
import random

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("LEG FINDER SIMULATOR v. 1.0")

# ============================================================
# ИГРОВЫЕ СОСТОЯНИЯ
# ============================================================
STATE_START = "start"
STATE_LEVEL1 = "level1"
game_state = STATE_START

# ============================================================
# ЗАГРУЗКА СТАРТОВОЙ ЛОКАЦИИ
# ============================================================
bg_start = pygame.image.load("bg_start.png")
bg_start = pygame.transform.scale(bg_start, (800, 600))

babka_img = pygame.image.load("babka.png")
babka_img = pygame.transform.scale(babka_img, (100, 100))

portal_img = pygame.image.load("portal.png")
portal_img = pygame.transform.scale(portal_img, (80, 120))

# ============================================================
# ЗАГРУЗКА 10 ФОНОВ (уровень 1)
# ============================================================
bg_images = []
for i in range(1, 11):
    img = pygame.image.load(f"bg_{i}.png")
    img = pygame.transform.scale(img, (800, 600))
    bg_images.append(img)

BG_WIDTH = 800
BG_COUNT = len(bg_images)

# ============================================================
# ЗАГРУЗКА СПРАЙТОВ ГЕРОЯ
# ============================================================
hero_stand = pygame.image.load("hero_stand.png")
hero_stand = pygame.transform.scale(hero_stand, (100, 140))

hero_walk1 = pygame.image.load("hero_walk1.png")
hero_walk1 = pygame.transform.scale(hero_walk1, (100, 140))

hero_walk2 = pygame.image.load("hero_walk2.png")
hero_walk2 = pygame.transform.scale(hero_walk2, (100, 140))

hero_jump = pygame.image.load("hero_jump.png")
hero_jump = pygame.transform.scale(hero_jump, (100, 140))

hero_hitting = pygame.image.load("hero_hitting.png")
hero_hitting = pygame.transform.scale(hero_hitting, (100, 140))

hero_diss = pygame.image.load("hero_diss.png")
hero_diss = pygame.transform.scale(hero_diss, (140, 150))

bullet_img = pygame.image.load("bullet.png")
bullet_img = pygame.transform.scale(bullet_img, (35, 35))

# Ультимейт
hero_ult_1 = pygame.image.load("hero_ult_1.png")
hero_ult_1 = pygame.transform.scale(hero_ult_1, (100, 140))

hero_ult_2 = pygame.image.load("hero_ult_2.png")
hero_ult_2 = pygame.transform.scale(hero_ult_2, (100, 140))

hero_ult_3 = pygame.image.load("hero_ult_3.png")
hero_ult_3 = pygame.transform.scale(hero_ult_3, (150, 140))

ult_overlay_img = pygame.image.load("10diss.png")
ult_overlay_img = pygame.transform.scale(ult_overlay_img, (350, 175))

ult_ready_img = pygame.image.load("10diss.png")
ult_ready_img = pygame.transform.scale(ult_ready_img, (50, 25))

# 10diss для диалога (300x150)
diss_overlay_img = pygame.image.load("10diss.png")
diss_overlay_img = pygame.transform.scale(diss_overlay_img, (300, 150))

# ============================================================
# ЗАГРУЗКА HP-БАРА
# ============================================================
hp_bar_images = []
for i in range(1, 6):
    img = pygame.image.load(f"hero_hp_{i}.png")
    img = pygame.transform.scale(img, (200, 40))
    hp_bar_images.append(img)

# ============================================================
# ЗАГРУЗКА СПРАЙТОВ СИМАКА
# ============================================================
simak_idle = pygame.image.load("simak_idle.png")
simak_idle = pygame.transform.scale(simak_idle, (135, 180))

simak_walk1 = pygame.image.load("simak_walk1.png")
simak_walk1 = pygame.transform.scale(simak_walk1, (135, 180))

simak_walk2 = pygame.image.load("simak_walk2.png")
simak_walk2 = pygame.transform.scale(simak_walk2, (135, 180))

simak_hurt = pygame.image.load("simak_hurt.png")
simak_hurt = pygame.transform.scale(simak_hurt, (135, 180))

simak_hitting = pygame.image.load("simak_hitting.png")
simak_hitting = pygame.transform.scale(simak_hitting, (135, 180))

simak_dead = pygame.image.load("simak_dead.png")
simak_dead = pygame.transform.scale(simak_dead, (135, 180))

# ============================================================
# ЗАГРУЗКА СПРАЙТОВ СУДЕЙ
# ============================================================
judge1_idle = pygame.image.load("judge1_idle.png")
judge1_idle = pygame.transform.scale(judge1_idle, (135, 180))
judge1_hit = pygame.image.load("judge1_hit.png")
judge1_hit = pygame.transform.scale(judge1_hit, (135, 180))

judge2_idle = pygame.image.load("judge2_idle.png")
judge2_idle = pygame.transform.scale(judge2_idle, (135, 180))
judge2_hit = pygame.image.load("judge2_hit.png")
judge2_hit = pygame.transform.scale(judge2_hit, (135, 180))

judge3_idle = pygame.image.load("judge3_idle.png")
judge3_idle = pygame.transform.scale(judge3_idle, (135, 180))
judge3_hit = pygame.image.load("judge3_hit.png")
judge3_hit = pygame.transform.scale(judge3_hit, (135, 180))

# Снаряд judge
judge_bullet_img = pygame.image.load("bullet.png")
judge_bullet_img = pygame.transform.scale(judge_bullet_img, (25, 25))
judge_bullet_img = pygame.transform.flip(judge_bullet_img, True, False)

# ============================================================
# МИР И КАМЕРА
# ============================================================
WORLD_WIDTH = BG_WIDTH * BG_COUNT
GROUND_Y = 450

camera_x = 0

# ============================================================
# ГЕРОЙ
# ============================================================
hero_x = 50
hero_y = GROUND_Y - 140
hero_vy = 0
hero_speed = 5
jump_power = -22
on_ground = False
facing_right = True
hero_hp = 50
hero_max_hp = 50
hero_hit_cooldown = 0
hero_alive = True
hero_melee_bonus = 0  # бонус к урону ближнего боя

gravity = 0.8

walk_timer = 0
walk_frame = 0
attack_timer = 0
is_attacking = False
is_dissing = False
diss_y_offset = 0

range_attack_cooldown = 0
bullets = []
bullet_speed = 8
bullet_max_dist = 640

# Ультимейт
ranged_hits = 0
ranged_hits_needed = 10
ult_ready = False
ult_active = False
ult_phase = 0
ult_timer = 0
ult_overlay_timer = 0

# ============================================================
# ФУНКЦИЯ СОЗДАНИЯ ВРАГОВ
# ============================================================
def create_enemies():
    enemies = []

    # Симак (босс) на 5700 — HP: 14
    enemies.append({
        "type": "simak",
        "x": 5700,
        "y": GROUND_Y - 30,
        "hp": 35,
        "max_hp": 35,
        "speed": 3,
        "damage": 1,
        "facing_right": False,
        "aggro_range": 250,
        "hit_cooldown": 0,
        "walk_timer": 0,
        "walk_frame": 0,
        "alive": True,
        "hurt_timer": 0,
        "state": "idle",
        "death_timer": 0,
        "vy": 0,
        "attack_type": "melee",
        "shoot_cooldown": 0,
        "seen_hero": False,
    })

    # 700 px: judge3
    enemies.append({
        "type": "judge3",
        "x": 700,
        "y": GROUND_Y - 30,
        "hp": 4, "max_hp": 4, "speed": 2, "damage": 1,
        "facing_right": True, "aggro_range": 320, "hit_cooldown": 0,
        "walk_timer": 0, "walk_frame": 0, "alive": True, "hurt_timer": 0,
        "state": "idle", "death_timer": 0, "vy": 0,
        "attack_type": "melee", "shoot_cooldown": 0, "seen_hero": False,
    })

    # 1100 px: три judge3 и один judge2
    for offset in [0, 60, 120]:
        enemies.append({
            "type": "judge3",
            "x": 1100 + offset,
            "y": GROUND_Y - 30,
            "hp": 4, "max_hp": 4, "speed": 2, "damage": 1,
            "facing_right": True, "aggro_range": 320, "hit_cooldown": 0,
            "walk_timer": 0, "walk_frame": 0, "alive": True, "hurt_timer": 0,
            "state": "idle", "death_timer": 0, "vy": 0,
            "attack_type": "melee", "shoot_cooldown": 0, "seen_hero": False,
        })
    enemies.append({
        "type": "judge2",
        "x": 1100 + 180,
        "y": GROUND_Y - 30,
        "hp": 4, "max_hp": 4, "speed": 2, "damage": 2,
        "facing_right": True, "aggro_range": 320, "hit_cooldown": 0,
        "walk_timer": 0, "walk_frame": 0, "alive": True, "hurt_timer": 0,
        "state": "idle", "death_timer": 0, "vy": 0,
        "attack_type": "melee", "shoot_cooldown": 0, "seen_hero": False,
    })

    # 1600 px: два judge3, два judge2, один judge1
    spawn_x = 1600
    for offset in [0, 70]:
        enemies.append({
            "type": "judge3",
            "x": spawn_x + offset,
            "y": GROUND_Y - 30,
            "hp": 4, "max_hp": 4, "speed": 2, "damage": 1,
            "facing_right": True, "aggro_range": 320, "hit_cooldown": 0,
            "walk_timer": 0, "walk_frame": 0, "alive": True, "hurt_timer": 0,
            "state": "idle", "death_timer": 0, "vy": 0,
            "attack_type": "melee", "shoot_cooldown": 0, "seen_hero": False,
        })
    for offset in [140, 210]:
        enemies.append({
            "type": "judge2",
            "x": spawn_x + offset,
            "y": GROUND_Y - 30,
            "hp": 4, "max_hp": 4, "speed": 2, "damage": 2,
            "facing_right": True, "aggro_range": 320, "hit_cooldown": 0,
            "walk_timer": 0, "walk_frame": 0, "alive": True, "hurt_timer": 0,
            "state": "idle", "death_timer": 0, "vy": 0,
            "attack_type": "melee", "shoot_cooldown": 0, "seen_hero": False,
        })
    enemies.append({
        "type": "judge1",
        "x": spawn_x + 280,
        "y": GROUND_Y - 30,
        "hp": 4, "max_hp": 4, "speed": 2, "damage": 2,
        "facing_right": True, "aggro_range": 370, "hit_cooldown": 0,
        "walk_timer": 0, "walk_frame": 0, "alive": True, "hurt_timer": 0,
        "state": "idle", "death_timer": 0, "vy": 0,
        "attack_type": "ranged", "shoot_cooldown": 0, "seen_hero": False,
    })

    # Случайная расстановка
    min_x = 2100
    max_x = 5200

    for _ in range(6):
        x = random.randint(min_x, max_x)
        enemies.append({
            "type": "judge3",
            "x": x,
            "y": GROUND_Y - 30,
            "hp": 4, "max_hp": 4, "speed": 2, "damage": 1,
            "facing_right": True, "aggro_range": 320, "hit_cooldown": 0,
            "walk_timer": 0, "walk_frame": 0, "alive": True, "hurt_timer": 0,
            "state": "idle", "death_timer": 0, "vy": 0,
            "attack_type": "melee", "shoot_cooldown": 0, "seen_hero": False,
        })

    for _ in range(5):
        x = random.randint(min_x, max_x)
        enemies.append({
            "type": "judge2",
            "x": x,
            "y": GROUND_Y - 30,
            "hp": 4, "max_hp": 4, "speed": 2, "damage": 2,
            "facing_right": True, "aggro_range": 320, "hit_cooldown": 0,
            "walk_timer": 0, "walk_frame": 0, "alive": True, "hurt_timer": 0,
            "state": "idle", "death_timer": 0, "vy": 0,
            "attack_type": "melee", "shoot_cooldown": 0, "seen_hero": False,
        })

    for _ in range(3):
        x = random.randint(min_x, max_x)
        enemies.append({
            "type": "judge1",
            "x": x,
            "y": GROUND_Y - 30,
            "hp": 4, "max_hp": 4, "speed": 2, "damage": 2,
            "facing_right": True, "aggro_range": 370, "hit_cooldown": 0,
            "walk_timer": 0, "walk_frame": 0, "alive": True, "hurt_timer": 0,
            "state": "idle", "death_timer": 0, "vy": 0,
            "attack_type": "ranged", "shoot_cooldown": 0, "seen_hero": False,
        })

    return enemies

enemies = create_enemies()
enemy_bullets = []

# ============================================================
# ДИАЛОГ (уровень 1) — СОСТОЯНИЯ
# ============================================================
DIALOG_NONE = 0
DIALOG_REPLICA = 1
DIALOG_CHOICES = 2
DIALOG_PRESS_E = 3  # ждём нажатия E после реплики симака

dialog_state = DIALOG_NONE
dialog_active = False
dialog_complete = False

# Текущие данные диалога
dialog_replica = ""
dialog_choices = []
dialog_next = None  # функция или действие

# Ветка диалога
dialog_branch = ""  # "1", "2", "2.1", "2.2", "2.3", "2.3.1", "2.3.2", "2.3.3", "3", "3.1", "3.2", "3.3"

# Оверлей 10diss в диалоге
diss_show = False
diss_timer = 0

# ============================================================
# СТАРТОВАЯ ЛОКАЦИЯ — ПЕРЕМЕННЫЕ
# ============================================================
babka_visible = False
babka_text_full = "Am I glad to see you! The LEG...and I...and, well, everybody...we're all trapped inside the castle walls. Короче, Меченый, иди и ищи свою ногу. А то пока что НЕНАХОД."
babka_text_displayed = ""
babka_text_index = 0
babka_text_timer = 0
babka_text_speed = 0.03
babka_text_done = False

portal_visible = False
portal_x = 650
portal_y = GROUND_Y - 25

hero_entering_portal = False
hero_portal_timer = 0

level_title = ""
level_title_timer = 0

# ============================================================
# ШРИФТЫ
# ============================================================
font = pygame.font.SysFont("Arial", 24)
font_small = pygame.font.SysFont("Arial", 18)
font_big = pygame.font.SysFont("Arial", 48)

# ============================================================
# ФУНКЦИИ ДИАЛОГА
# ============================================================
def dialog_show_replica(text, next_func):
    global dialog_state, dialog_replica, dialog_next
    dialog_state = DIALOG_PRESS_E
    dialog_replica = text
    dialog_next = next_func

def dialog_show_choices(choices_list, next_func):
    global dialog_state, dialog_choices, dialog_next
    dialog_state = DIALOG_CHOICES
    dialog_choices = choices_list
    dialog_next = next_func

def dialog_end():
    global dialog_state, dialog_active, dialog_complete
    dialog_state = DIALOG_NONE
    dialog_active = False
    dialog_complete = True

# Обработчики выбора
def handle_choice_1():
    dialog_show_replica("Караван идет", lambda: dialog_end())

def handle_choice_2():
    dialog_show_replica("Я не согласовывал этот дисс.", lambda: dialog_show_choices(
        ["У меня есть скрин переписки.", "Когда у тебя днюха?", "Иван Симак."],
        lambda choice: handle_choice_2_sub(choice)
    ))

def handle_choice_2_sub(choice):
    if choice == 0:
        dialog_show_replica("Это ничего не значит. Желтая карточка тебе", lambda: hero_hurt_by_dialog(5))
    elif choice == 1:
        dialog_show_replica("Я не буду это комментировать. Ты все равно проиграешь", lambda: dialog_end())
    elif choice == 2:
        dialog_show_replica("Я ТЕБЕ СКАЗАЛ, ЧТО НЕ СОГЛАСОВЫВАЛ ЭТОТ ДИСС!", lambda: dialog_show_choices(
            ["Иван Симак.", "Да пох. 10 диссов.", "Fuck"],
            lambda c: handle_choice_2_3(c)
        ))

def handle_choice_2_3(choice):
    global diss_show, diss_timer
    if choice == 0:
        dialog_show_replica("Ну все, пойдем выскочим на разах!", lambda: buff_simak())
    elif choice == 1:
        diss_show = True
        diss_timer = 1.0
        dialog_show_replica("ЭТО НЕ ПО ПРАВИЛАМ! КРАСНАЯ КАРТОЧКА!", lambda: spawn_judges_around_simak(5, "judge1"))
    elif choice == 2:
        dialog_show_replica("Мне это надоело", lambda: kill_simak())

def handle_choice_3():
    dialog_show_replica("Какую ногу?!", lambda: dialog_show_choices(
        ["Принцессу Ногу. Мне сказали, она в замке. Где тут замок поблизости?", "Ладно. А альбом Стива не видел?", "ГДЕ НОГА?!"],
        lambda choice: handle_choice_3_sub(choice)
    ))

def handle_choice_3_sub(choice):
    if choice == 0:
        dialog_show_replica("Тут нет никакого замка. Тут ХРАМ ПОЭЗИИ!", lambda: spawn_judges_around_simak(5, "judge3"))
    elif choice == 1:
        dialog_show_replica("Я его взял. И отдам только лично Стиву!", lambda: dialog_end())
    elif choice == 2:
        dialog_show_replica("ША ТУ НЫ", lambda: buff_both())

def hero_hurt_by_dialog(dmg):
    global hero_hp
    hero_hp -= dmg
    if hero_hp <= 0:
        hero_hp = 1
    dialog_end()

def buff_simak():
    for enemy in enemies:
        if enemy["type"] == "simak" and enemy["alive"]:
            enemy["hp"] += 20
            enemy["max_hp"] += 20
            enemy["damage"] += 1
    dialog_end()

def kill_simak():
    for enemy in enemies:
        if enemy["type"] == "simak" and enemy["alive"]:
            enemy["hp"] = 0
            enemy["state"] = "dead"
            enemy["y"] = GROUND_Y + 15
    dialog_end()

def spawn_judges_around_simak(count, jtype):
    simak_x = 5700
    for enemy in enemies:
        if enemy["type"] == "simak":
            simak_x = enemy["x"]
            break
    for i in range(count):
        enemies.append({
            "type": jtype,
            "x": simak_x + 150 + i * 80,
            "y": GROUND_Y - 30,
            "hp": 4, "max_hp": 4, "speed": 2,
            "damage": 2 if jtype == "judge1" else (2 if jtype == "judge2" else 1),
            "facing_right": True,
            "aggro_range": 370 if jtype == "judge1" else 320,
            "hit_cooldown": 0,
            "walk_timer": 0, "walk_frame": 0,
            "alive": True, "hurt_timer": 0,
            "state": "idle", "death_timer": 0, "vy": 0,
            "attack_type": "ranged" if jtype == "judge1" else "melee",
            "shoot_cooldown": 0, "seen_hero": True,
        })
    dialog_end()

def buff_both():
    global hero_hp, hero_melee_bonus
    hero_hp += 5
    hero_melee_bonus += 2
    for enemy in enemies:
        if enemy["type"] == "simak" and enemy["alive"]:
            enemy["hp"] += 5
            enemy["max_hp"] += 5
            enemy["damage"] += 2
    dialog_end()

clock = pygame.time.Clock()
running = True

while running:
    dt = clock.tick(60) / 1000

    # --- События ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q and pygame.key.get_mods() & pygame.KMOD_META:
                running = False

            if event.key == pygame.K_r and not hero_alive and game_state == STATE_LEVEL1:

                # Полный рестарт уровня 1
                hero_x = 50
                hero_y = GROUND_Y - 140
                hero_vy = 0
                hero_hp = 50
                hero_alive = True
                hero_hit_cooldown = 0
                on_ground = False
                hero_melee_bonus = 0
                attack_timer = 0
                is_attacking = False
                is_dissing = False
                diss_y_offset = 0
                range_attack_cooldown = 0
                bullets = []
                enemy_bullets = []
                enemies = create_enemies()
                dialog_active = False
                dialog_state = DIALOG_NONE
                dialog_complete = False
                ult_active = False
                ult_phase = 0
                ult_ready = False
                ranged_hits = 0
                diss_show = False
            # Ультимейт по T
            if event.key == pygame.K_t and hero_alive and ult_ready and not ult_active and game_state == STATE_LEVEL1:
                ult_active = True
                ult_phase = 1
                ult_timer = 0.45
                ranged_hits = 0
                ult_ready = False

            # Обработка диалога
            if dialog_state == DIALOG_PRESS_E and event.key == pygame.K_e:
                if dialog_next:
                    dialog_next()
            elif dialog_state == DIALOG_CHOICES:
                if event.key == pygame.K_1 and len(dialog_choices) >= 1:
                    if dialog_next:
                        dialog_next(0)
                elif event.key == pygame.K_2 and len(dialog_choices) >= 2:
                    if dialog_next:
                        dialog_next(1)
                elif event.key == pygame.K_3 and len(dialog_choices) >= 3:
                    if dialog_next:
                        dialog_next(2)

    keys = pygame.key.get_pressed()

    # Таймер оверлея 10diss в диалоге
    if diss_show:
        diss_timer -= dt
        if diss_timer <= 0:
            diss_show = False

    # ========================================================
    # СТАРТОВАЯ ЛОКАЦИЯ
    # ========================================================
    if game_state == STATE_START:

        moving = False
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            hero_x -= hero_speed
            moving = True
            facing_right = False
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            hero_x += hero_speed
            moving = True
            facing_right = True

        if hero_x < 0:
            hero_x = 0
        if hero_x > 700:
            hero_x = 700

        hero_y = GROUND_Y - 30
        on_ground = True

        if not babka_visible and hero_x > 300:
            babka_visible = True

        if babka_visible and not babka_text_done:
            babka_text_timer += dt
            while babka_text_timer >= babka_text_speed and babka_text_index < len(babka_text_full):
                babka_text_displayed += babka_text_full[babka_text_index]
                babka_text_index += 1
                babka_text_timer -= babka_text_speed
            if babka_text_index >= len(babka_text_full):
                babka_text_done = True

        if babka_text_done and keys[pygame.K_e]:
            portal_visible = True

        if portal_visible and not hero_entering_portal:
            if hero_x > portal_x - 30:
                hero_entering_portal = True
                hero_portal_timer = 1.0

        if hero_entering_portal:
            hero_portal_timer -= dt
            hero_x = portal_x
            if hero_portal_timer <= 0:
                game_state = STATE_LEVEL1
                level_title = "ПЕРВЫЙ УРОВЕНЬ"
                level_title_timer = 2.0
                hero_x = 50
                hero_y = GROUND_Y - 140
                hero_vy = 0
                hero_alive = True
                hero_hp = 50
                hero_hit_cooldown = 0
                on_ground = False
                camera_x = 0
                bullets = []
                enemy_bullets = []
                ranged_hits = 0
                ult_ready = False
                ult_active = False
                hero_melee_bonus = 0

        if hero_entering_portal:
            current_sprite = hero_jump
        elif moving:
            walk_timer += dt
            if walk_timer > 0.15:
                walk_timer = 0
                walk_frame = 1 - walk_frame
            if walk_frame == 0:
                current_sprite = hero_walk1
            else:
                current_sprite = hero_walk2
        else:
            current_sprite = hero_stand
            walk_timer = 0
            walk_frame = 0

        if not facing_right:
            current_sprite = pygame.transform.flip(current_sprite, True, False)

        screen.blit(bg_start, (0, 0))

        if babka_visible:
            screen.blit(babka_img, (50, WINDOW_HEIGHT // 2 - 50))

        if babka_visible:
            text_rect = pygame.Rect(170, WINDOW_HEIGHT // 2 - 60, 580, 120)
            pygame.draw.rect(screen, (0, 0, 0), text_rect)
            pygame.draw.rect(screen, (255, 255, 255), text_rect, 2)

            words = babka_text_displayed.split(" ")
            lines = []
            current_line = ""
            for word in words:
                test_line = current_line + (" " if current_line else "") + word
                if font_small.size(test_line)[0] < 560:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = word
            if current_line:
                lines.append(current_line)

            for i, line in enumerate(lines):
                rendered = font_small.render(line, True, (255, 255, 255))
                screen.blit(rendered, (185, WINDOW_HEIGHT // 2 - 50 + i * 22))

            if babka_text_done:
                hint = font_small.render("Нажми E", True, (150, 150, 150))
                screen.blit(hint, (650, WINDOW_HEIGHT // 2 + 35))

        if portal_visible:
            screen.blit(portal_img, (portal_x, portal_y))

        screen.blit(current_sprite, (hero_x, hero_y))

    # ========================================================
    # УРОВЕНЬ 1
    # ========================================================
    elif game_state == STATE_LEVEL1:

        if not ult_active and not dialog_active:
            moving = False
            if hero_alive:
                if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                    hero_x -= hero_speed
                    moving = True
                    facing_right = False
                if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                    hero_x += hero_speed
                    moving = True
                    facing_right = True

            if keys[pygame.K_SPACE] and on_ground and hero_alive:
                hero_vy = jump_power
                on_ground = False

            hero_vy += gravity
            hero_y += hero_vy

            if hero_y >= GROUND_Y:
                hero_y = GROUND_Y
                hero_vy = 0
                on_ground = True

        if hero_x < 0:
            hero_x = 0
        if hero_x > WORLD_WIDTH - 100:
            hero_x = WORLD_WIDTH - 100

        if hero_hit_cooldown > 0:
            hero_hit_cooldown -= dt

        if hero_hp <= 0 and hero_alive:
            hero_alive = False
            hero_vy = -10
            on_ground = False

        if not ult_active and not dialog_active:
            # Ближняя атака (F)
            if keys[pygame.K_f] and attack_timer <= 0 and hero_alive:
                attack_timer = 0.3
                is_attacking = True
                for enemy in enemies:
                    if enemy["alive"]:
                        dist = abs(hero_x - enemy["x"])
                        if dist < 80:
                            if enemy["state"] == "dead":
                                if hero_x < enemy["x"]:
                                    enemy["x"] += 200
                                else:
                                    enemy["x"] -= 200
                                if enemy["x"] < 0:
                                    enemy["x"] = 0
                                if enemy["x"] > WORLD_WIDTH - 135:
                                    enemy["x"] = WORLD_WIDTH - 135
                            else:
                                if enemy["type"] != "simak":
                                    enemy["hp"] -= (3 + hero_melee_bonus)
                                    enemy["hurt_timer"] = 0.3
                                if hero_x < enemy["x"]:
                                    enemy["x"] += 20
                                else:
                                    enemy["x"] -= 20
                            break

            # Дальняя атака (G)
            if keys[pygame.K_g] and range_attack_cooldown <= 0 and hero_alive:
                range_attack_cooldown = 0.5
                is_dissing = True
                attack_timer = 0.3
                diss_y_offset = -25
                bullets.append({
                    "x": hero_x + (33 if facing_right else -33),
                    "y": hero_y + 33,
                    "dir": 1 if facing_right else -1,
                    "dist": 0
                
                })

        if attack_timer > 0:
            attack_timer -= dt
        else:
            is_attacking = False
            is_dissing = False
            diss_y_offset = 0

        if range_attack_cooldown > 0:
            range_attack_cooldown -= dt

        # Движение пуль героя
        for bullet in bullets[:]:
            bullet["x"] += bullet_speed * bullet["dir"]
            bullet["dist"] += bullet_speed

            hit_enemy = False
            for enemy in enemies:
                if enemy["alive"] and enemy["state"] != "dead":
                    if enemy["type"] == "simak" and not dialog_complete:
                        continue
                    if abs(bullet["x"] - enemy["x"]) < 20 and abs(bullet["y"] - (enemy["y"] + 80)) < 60:
                        enemy["hp"] -= 1
                        enemy["hurt_timer"] = 0.3
                        ranged_hits += 1
                        if ranged_hits >= ranged_hits_needed and not ult_ready:
                            ult_ready = True
                        bullets.remove(bullet)
                        hit_enemy = True
                        break

            if not hit_enemy and bullet["dist"] > bullet_max_dist:
                bullets.remove(bullet)

        # Движение пуль врагов
        for bullet in enemy_bullets[:]:
            bullet["x"] += bullet["speed"] * bullet["dir"]
            bullet["dist"] += bullet["speed"]

            hit_hero = False
            if hero_alive and not on_ground:
                pass
            elif hero_alive:
                dist = abs(bullet["x"] - hero_x)
                if dist < 40 and abs(bullet["y"] - (hero_y + 70)) < 50:
                    dmg = bullet["damage"]
                    if ult_active:
                        dmg = max(1, dmg - 1)
                    hero_hp -= dmg
                    hero_hit_cooldown = 0.5
                    hit_hero = True

            if hit_hero or bullet["dist"] > bullet["max_dist"]:
                enemy_bullets.remove(bullet)

        # Ультимейт
        if ult_active:
            ult_timer -= dt
            if ult_phase == 1:
                if ult_timer <= 0:
                    ult_phase = 2
                    ult_timer = 0.45
            elif ult_phase == 2:
                if ult_timer <= 0:
                    ult_phase = 3
                    ult_timer = 1.0
                    ult_overlay_timer = 1.0
                    for enemy in enemies:
                        if enemy["alive"] and enemy["state"] != "dead":
                            if abs(hero_x - enemy["x"]) < 350:
                                enemy["hp"] -= 8
                                enemy["hurt_timer"] = 0.5
            elif ult_phase == 3:
                if ult_timer <= 0:
                    ult_active = False
                    ult_phase = 0

            if ult_overlay_timer > 0:
                ult_overlay_timer -= dt

        # Проверка начала диалога с симаком
        simak_enemy = None
        for enemy in enemies:
            if enemy["type"] == "simak":
                simak_enemy = enemy
                break

        if simak_enemy and simak_enemy["alive"] and simak_enemy["state"] != "dead" and not dialog_active and not dialog_complete:
            dist_to_enemy = abs(hero_x - simak_enemy["x"])
            if dist_to_enemy < 100 and on_ground:
                dialog_active = True
                dialog_state = DIALOG_PRESS_E
                dialog_replica = "Я тебя ждал..."
                dialog_next = lambda: dialog_show_replica(
                    "Ты думал, что пройдёшь в финал КБС?",
                    lambda: dialog_show_choices(
                        ["Я люблю акростихи", "Иван Симак", "Ты не видел мою ногу?"],
                        lambda choice: [handle_choice_1, handle_choice_2, handle_choice_3][choice]()
                    )
                )

        # Поведение врагов (только после диалога)
        if not dialog_active:
            for enemy in enemies:
                if not enemy["alive"]:
                    continue

                dist_to_hero = hero_x - enemy["x"]
                abs_dist = abs(dist_to_hero)

                if enemy["hurt_timer"] > 0:
                    enemy["hurt_timer"] -= dt

                if enemy["hit_cooldown"] > 0:
                    enemy["hit_cooldown"] -= dt

                if enemy.get("shoot_cooldown", 0) > 0:
                    enemy["shoot_cooldown"] -= dt

                if abs_dist < enemy["aggro_range"]:
                    enemy["seen_hero"] = True

                if enemy["state"] == "landing":
                    enemy["y"] += 4
                    if enemy["y"] >= GROUND_Y - 30:
                        enemy["y"] = GROUND_Y - 30
                        enemy["state"] = "chase"

                if enemy["state"] in ("chase", "idle"):
                    if enemy["type"] != "simak" or enemy["state"] == "chase" or dialog_complete:
                        if enemy["seen_hero"] or abs_dist < enemy["aggro_range"]:
                            enemy["state"] = "chase"
                            if enemy["attack_type"] == "ranged":
                                if dist_to_hero > 200:
                                    enemy["x"] += enemy["speed"]
                                elif dist_to_hero < -200:
                                    enemy["x"] -= enemy["speed"]

                                if enemy["shoot_cooldown"] <= 0 and abs_dist < 400:
                                    enemy["shoot_cooldown"] = 1.2
                                    enemy["hit_cooldown"] = 0.5
                                    bullet_dir = 1 if hero_x > enemy["x"] else -1
                                    enemy_bullets.append({
                                        "x": enemy["x"],
                                        "y": enemy["y"] + 80,
                                        "dir": bullet_dir,
                                        "speed": 5,
                                        "dist": 0,
                                        "max_dist": 500,
                                        "damage": enemy["damage"],
                                    })
                            else:
                                if dist_to_hero > 15:
                                    enemy["x"] += enemy["speed"]
                                elif dist_to_hero < -15:
                                    enemy["x"] -= enemy["speed"]

                if enemy["x"] < 0:
                    enemy["x"] = 0
                if enemy["x"] > WORLD_WIDTH - 135:
                    enemy["x"] = WORLD_WIDTH - 135

                if enemy["attack_type"] == "melee" and enemy["state"] == "chase" and abs_dist < 50 and hero_alive and on_ground and hero_hit_cooldown <= 0 and enemy["hit_cooldown"] <= 0:
                    dmg = enemy["damage"]
                    if ult_active:
                        dmg = max(1, dmg - 1)
                    hero_hp -= dmg
                    hero_hit_cooldown = 1.5
                    enemy["hit_cooldown"] = 0.7
                    if hero_x < enemy["x"]:
                        hero_x -= 40
                        hero_vy = -8
                    else:
                        hero_x += 40
                        hero_vy = -8
                    on_ground = False

                if enemy["hp"] <= 0 and enemy["state"] != "dead":
                    enemy["state"] = "dead"
                    if enemy["type"] == "simak":
                        enemy["y"] = GROUND_Y + 15
                    else:
                        enemy["death_timer"] = 0.5
                        enemy["vy"] = -8

                if enemy["state"] == "dead":
                    if enemy["type"] != "simak":
                        enemy["death_timer"] -= dt
                        if enemy["death_timer"] > 0:
                            enemy["y"] += enemy.get("vy", -8)
                            if "vy" in enemy:
                                enemy["vy"] += gravity
                        else:
                            enemy["y"] += 15
                            if enemy["y"] > WINDOW_HEIGHT + 200:
                                enemy["alive"] = False

        camera_x = hero_x - WINDOW_WIDTH // 2
        if camera_x < 0:
            camera_x = 0
        if camera_x > WORLD_WIDTH - WINDOW_WIDTH:
            camera_x = WORLD_WIDTH - WINDOW_WIDTH

        # Выбор спрайта героя
        if not hero_alive:
            current_sprite = hero_jump
        elif ult_active:
            if ult_phase == 1:
                current_sprite = hero_ult_1
            elif ult_phase == 2:
                current_sprite = hero_ult_2
            else:
                current_sprite = hero_ult_3
        elif is_dissing:
            current_sprite = hero_diss
        elif is_attacking:
            current_sprite = hero_hitting
        elif not on_ground:
            current_sprite = hero_jump
        elif moving:
            walk_timer += dt
            if walk_timer > 0.15:
                walk_timer = 0
                walk_frame = 1 - walk_frame
            if walk_frame == 0:
                current_sprite = hero_walk1
            else:
                current_sprite = hero_walk2
        else:
            current_sprite = hero_stand
            walk_timer = 0
            walk_frame = 0

        if not facing_right:
            current_sprite = pygame.transform.flip(current_sprite, True, False)

        screen.fill((0, 0, 0))

        for i in range(BG_COUNT):
            bg_x = i * BG_WIDTH - camera_x
            if bg_x + BG_WIDTH > 0 and bg_x < WINDOW_WIDTH:
                screen.blit(bg_images[i], (bg_x, 0))

        for enemy in enemies:
            if not enemy["alive"]:
                continue

            enemy_draw_x = enemy["x"] - camera_x
            enemy_draw_y = enemy["y"]

            if enemy["state"] == "dead":
                if enemy["type"] == "simak":
                    enemy_current = simak_dead
                elif enemy["type"] == "judge1":
                    enemy_current = judge1_idle
                elif enemy["type"] == "judge2":
                    enemy_current = judge2_idle
                else:
                    enemy_current = judge3_idle
            elif enemy["hurt_timer"] > 0:
                if enemy["type"] == "simak":
                    enemy_current = simak_hurt
                elif enemy["type"] == "judge1":
                    enemy_current = judge1_hit
                elif enemy["type"] == "judge2":
                    enemy_current = judge2_hit
                else:
                    enemy_current = judge3_hit
            elif enemy["state"] == "chase" and enemy["hit_cooldown"] > 0:
                if enemy["type"] == "simak":
                    enemy_current = simak_hitting
                elif enemy["type"] == "judge1":
                    enemy_current = judge1_hit
                elif enemy["type"] == "judge2":
                    enemy_current = judge2_hit
                else:
                    enemy_current = judge3_hit
            elif enemy["state"] == "chase" and abs(hero_x - enemy["x"]) > 15:
                enemy["walk_timer"] += dt
                if enemy["walk_timer"] > 0.2:
                    enemy["walk_timer"] = 0
                    enemy["walk_frame"] = 1 - enemy.get("walk_frame", 0)
                if enemy.get("walk_frame", 0) == 0:
                    if enemy["type"] == "simak":
                        enemy_current = simak_walk1
                    elif enemy["type"] == "judge1":
                        enemy_current = judge1_idle
                    elif enemy["type"] == "judge2":
                        enemy_current = judge2_idle
                    else:
                        enemy_current = judge3_idle
                else:
                    if enemy["type"] == "simak":
                        enemy_current = simak_walk2
                    elif enemy["type"] == "judge1":
                        enemy_current = judge1_idle
                    elif enemy["type"] == "judge2":
                        enemy_current = judge2_idle
                    else:
                        enemy_current = judge3_idle
            else:
                if enemy["type"] == "simak":
                    enemy_current = simak_idle
                elif enemy["type"] == "judge1":
                    enemy_current = judge1_idle
                elif enemy["type"] == "judge2":
                    enemy_current = judge2_idle
                else:
                    enemy_current = judge3_idle

            if enemy["type"] == "simak" and not enemy["facing_right"]:
                enemy_current = pygame.transform.flip(enemy_current, True, False)

            screen.blit(enemy_current, (enemy_draw_x, enemy_draw_y))


        for bullet in enemy_bullets:
            bullet_draw_x = bullet["x"] - camera_x
            screen.blit(judge_bullet_img, (bullet_draw_x - 12, bullet["y"] - 12))

        hero_draw_x = hero_x - camera_x
        hero_draw_y = hero_y + diss_y_offset
        if hero_hit_cooldown > 0 and int(hero_hit_cooldown * 10) % 2 == 0:
            pass
        else:
            screen.blit(current_sprite, (hero_draw_x, hero_draw_y))

        for bullet in bullets:
            bullet_draw_x = bullet["x"] - camera_x
            screen.blit(bullet_img, (bullet_draw_x - 17, bullet["y"] - 17))

        if ult_ready:
            ult_ready_draw_x = hero_draw_x + 25
            ult_ready_draw_y = hero_draw_y - 30
            screen.blit(ult_ready_img, (ult_ready_draw_x, ult_ready_draw_y))

        if ult_active and ult_phase == 3 and ult_overlay_timer > 0:
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))
            ult_overlay_x = WINDOW_WIDTH // 2 - 175
            ult_overlay_y = WINDOW_HEIGHT // 2 - 87
            screen.blit(ult_overlay_img, (ult_overlay_x, ult_overlay_y))

        # Оверлей 10diss из диалога
        if diss_show:
            diss_draw_x = WINDOW_WIDTH // 2 - 150
            diss_draw_y = WINDOW_HEIGHT // 2 - 75
            screen.blit(diss_overlay_img, (diss_draw_x, diss_draw_y))

        hp_percent = hero_hp / hero_max_hp
        if hp_percent > 0.8:
            hp_index = 0
        elif hp_percent > 0.5:
            hp_index = 1
        elif hp_percent > 0.25:
            hp_index = 2
        elif hp_percent > 0:
            hp_index = 3
        else:
            hp_index = 4

        screen.blit(hp_bar_images[hp_index], (10, 10))

        if not hero_alive:
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(150)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))
            game_over_text = font.render("GAME OVER", True, (255, 0, 0))
            screen.blit(game_over_text, (WINDOW_WIDTH // 2 - 80, WINDOW_HEIGHT // 2 - 20))
            restart_text = font_small.render("R — попробовать еще раз", True, (255, 255, 255))
            screen.blit(restart_text, (WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 20))

        # Отрисовка диалога
        if dialog_state != DIALOG_NONE:
            dialog_surface = pygame.Surface((WINDOW_WIDTH - 100, 140))
            dialog_surface.set_alpha(200)
            dialog_surface.fill((0, 0, 0))
            screen.blit(dialog_surface, (50, WINDOW_HEIGHT - 180))

            if dialog_state == DIALOG_PRESS_E:
                text = font_small.render(dialog_replica, True, (255, 255, 255))
                screen.blit(text, (70, WINDOW_HEIGHT - 160))
                hint = font_small.render("Нажми E чтобы продолжить", True, (150, 150, 150))
                screen.blit(hint, (70, WINDOW_HEIGHT - 120))
            elif dialog_state == DIALOG_CHOICES:
                text = font_small.render("Твой ответ:", True, (255, 255, 255))
                screen.blit(text, (70, WINDOW_HEIGHT - 160))
                for i, choice in enumerate(dialog_choices):
                    choice_text = font_small.render(f"{i+1}. {choice}", True, (255, 255, 0))
                    screen.blit(choice_text, (90, WINDOW_HEIGHT - 130 + i * 25))

    if level_title_timer > 0:
        level_title_timer -= dt
        title_surf = font_big.render(level_title, True, (255, 255, 0))
        screen.blit(title_surf, (WINDOW_WIDTH // 2 - title_surf.get_width() // 2, WINDOW_HEIGHT // 2 - 30))

    pygame.display.flip()

pygame.quit()
sys.exit()
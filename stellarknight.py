import os
import time
import msvcrt
import json
import random

# --- UTILITIES ---
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def center_text(text):
    try:
        width = os.get_terminal_size().columns
    except OSError:
        width = 80
    lines = text.splitlines()
    return "\n".join(line.center(width) for line in lines)

def loading_screen(text="Loading..."):
    clear()
    print("\n" * 5)
    print(center_text(text))
    for _ in range(3):
        time.sleep(0.5)
        print(".", end="", flush=True)
    time.sleep(1)
    clear()

# --- TITLE ---
TITLE_ART = r"""
   ███████╗████████╗ █████╗ ██████╗ ██████╗ ██╗   ██╗    ██╗  ██╗███╗   ██╗██╗ ██████╗ ██╗  ██╗████████╗   
   ██╔════╝╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝    ██║ ██╔╝████╗  ██║██║██╔════╝ ██║  ██║╚══██╔══╝   
   ███████╗   ██║   ███████║██████╔╝██████╔╝ ╚████╔╝     █████╔╝ ██╔██╗ ██║██║██║  ███╗███████║   ██║    
   ╚════██║   ██║   ██╔══██║██╔══██╗██╔══██╗  ╚██╔╝      ██╔═██╗ ██║╚██╗██║██║██║   ██║██╔══██║   ██║    
   ███████║   ██║   ██║  ██║██║  ██║██║  ██║   ██║       ██║  ██╗██║ ╚████║██║╚██████╔╝██║  ██║   ██║    
   ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝       ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝    
"""

# --- SCREENS ---
def startup():
    clear()
    print("\n" * 5)
    print(center_text("INITIALIZING SYSTEM..."))
    time.sleep(2)
    clear()

def draw_menu(selected):
    print("\n" * 2)
    print(center_text(TITLE_ART))
    print("\n")
    if selected == "1":
        print(center_text("> Start Game <"))
        print(center_text("  Quit  "))
    elif selected == "2":
        print(center_text("  Start Game  "))
        print(center_text("> Quit <"))
    else:
        print(center_text("  Start Game  "))
        print(center_text("  Quit  "))
    print("\n")
    print(center_text("Use 1 or 2 to select, Enter to confirm"))

def main_menu():
    selected = None
    prev_selected = ""
    clear()
    while True:
        if selected != prev_selected:
            clear()
            draw_menu(selected)
            prev_selected = selected
        if msvcrt.kbhit():
            key = msvcrt.getch()
            if key in [b'1', b'2']:
                selected = key.decode()
            elif key == b'\r' and selected:
                break
        time.sleep(0.05)
    clear()
    return selected

SAVE_FILE = "space_users.json"
MAX_ACCOUNTS = 10

def load_users():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    return []

def save_users(users):
    with open(SAVE_FILE, "w") as f:
        json.dump(users, f, indent=2)

def login_or_signup():
    users = load_users()
    while True:
        clear()
        print(center_text("🌌 GALACTIC ACCESS 🌌"))
        print("\n" + center_text("1. Log In"))
        print(center_text("2. Sign Up"))
        print("\nPress 1 or 2 to continue.")
        key = msvcrt.getch()
        if key == b'1':  # Login
            clear()
            username = input("Enter your username: ").strip()
            if username in users:
                print(center_text(f"🪐 Welcome aboard, Captain {username}!"))
                time.sleep(1)
                return username
            else:
                print(center_text("🚫 No transmission found in the cosmic database..."))
                print(center_text("Try again or create a new profile."))
                time.sleep(2)
        elif key == b'2':  # Sign up
            clear()
            if len(users) >= MAX_ACCOUNTS:
                print(center_text("🛰️ Galactic registry full. No new ships may launch."))
                time.sleep(2)
                continue
            username = input("Create your username: ").strip()
            if username == "":
                print(center_text("🚫 Invalid username. Try again."))
                time.sleep(1)
                continue
            if username in users:
                print(center_text("🪐 That name already belongs to another traveler."))
                time.sleep(2)
                continue
            users.append(username)
            save_users(users)
            print(center_text(f"🚀 Ship {username} successfully registered!"))
            time.sleep(1)
            return username


# first planet + health + enemies + celestial beginnings item
# --- FIRST PLANET MAP ---
PLANET = [
    "                                                            ^^^                       ",
    "                                                           ^^^^^                      ",
    "                                                     ^^^                               ",
    "                                                ^^^^^^^                                 ",
    "                                                                                       ",
    "                                    ^^^^^                                                ",
    "                       ^^^                                                        ^^^  ",
    "                ^^^^^^^^^                                                   ^^^^^^^    ",
    "                                                                                       ",
    "###################################^^^^^^^^^^^^^^^^^^^^^#############################",
]

PLANET_HEIGHT = len(PLANET)
PLANET_WIDTH = len(PLANET[0])

CAM_VIEW = 60
player_screen_x = CAM_VIEW // 2

player_world_x = 5
player_y = 8
y_velocity = 0

# --- GRAVITY + MOVEMENT TWEAKS ---
GRAVITY = 0.3           # less instant falling, floaty
JUMP_FORCE = -4         # slightly lower jump force, floaty
MAX_FALL_SPEED = 2      # slower falling speed

# --- PLAYER STATS ---
player_speed = 1
player_jump = JUMP_FORCE
player_dash_ready = False
dash_cooldown = 0
dash_time = 0
DASH_DURATION = 5  # frames
DASH_SPEED = 3

# --- HEALTH SYSTEM ---
max_health = 5
health = max_health
celestial_adrenaline = False
adrenaline_time = 0
HEART_REGEN_DELAY = 5
last_damage_time = 0

# --- ITEMS ---
inventory = []
latest_item = None
item_emoji = "✨"
celestial_item_obtained = False
# place item at top of parkour section
item_pos = (35, 3)

# --- ENEMIES ---
enemies = []
# slower and fewer enemies for this level
for _ in range(2):
    ex = random.randint(10, PLANET_WIDTH - 10)
    ey = 8
    dir = random.choice([-1, 1])
    enemies.append({"x": ex, "y": ey, "dir": dir, "speed": 0.2})

def is_solid(x, y):
    if x < 0 or x >= PLANET_WIDTH or y < 0 or y >= PLANET_HEIGHT:
        return True
    return PLANET[y][x] in ["#", "^"]

# --- DRAW SCENE ---
def draw_scene(cam_pos):
    clear()
    for row_i in range(PLANET_HEIGHT):
        row = list(PLANET[row_i][cam_pos:cam_pos+CAM_VIEW])
        # draw player
        if row_i == player_y:
            px_screen = int(player_world_x) - cam_pos
            if 0 <= px_screen < CAM_VIEW:
                row[px_screen] = "o"
        # draw item
        if not celestial_item_obtained:
            ix_screen = item_pos[0] - cam_pos
            if 0 <= ix_screen < CAM_VIEW and row_i == item_pos[1]:
                row[ix_screen] = "✦"
        # draw enemies
        for e in enemies:
            ex_screen = int(e["x"]) - cam_pos
            if row_i == e["y"] and 0 <= ex_screen < CAM_VIEW:
                row[ex_screen] = "🌌"
        print("".join(row))

    # --- HEALTH + INVENTORY BELOW MAP ---
    health_str = ""
    for i in range(max_health):
        if i == 0:
            health_str += "💜" if health > 0 else "🖤"
        else:
            health_str += "💔" if i < health else "🖤"
    print(f"Health: {health_str}")

    inv_text = f"Latest Item: {item_emoji} {latest_item}" if latest_item else "Latest Item: None"
    print(center_text(inv_text))

    if celestial_adrenaline:
        print(center_text("CELESTIAL ADRENALINE!"))

    print("\n[A/D = Move | SPACE = Jump | 1 = Dash (if item) | ENTER = Back]")

# --- PLANET LOOP ---
def planet_loop():
    global player_world_x, player_y, y_velocity
    global celestial_item_obtained, player_dash_ready, dash_cooldown, dash_time
    global health, celestial_adrenaline, adrenaline_time, last_damage_time
    global player_speed, player_jump
    global latest_item

    # reset stats on planet enter
    health = max_health
    celestial_adrenaline = False
    adrenaline_time = 0
    last_damage_time = 0
    player_speed = 1
    player_jump = JUMP_FORCE
    dash_cooldown = 0
    dash_time = 0
    player_dash_ready = celestial_item_obtained
    player_world_x = PLANET_WIDTH // 2
    player_y = PLANET_HEIGHT - 2
    y_velocity = 0

    frame_count = 0
    cam_pos = 0

    while True:
        # GRAVITY
        y_velocity += GRAVITY
        if y_velocity > MAX_FALL_SPEED:
            y_velocity = MAX_FALL_SPEED
        next_y = player_y + (1 if y_velocity > 0 else -1)
        if not is_solid(int(player_world_x), next_y):
            player_y = next_y
        else:
            y_velocity = 0

        # DASH HANDLING
        if dash_time > 0:
            dash_time -= 1
            move_amount = DASH_SPEED
        else:
            move_amount = player_speed

        # INPUT
        if msvcrt.kbhit():
            key = msvcrt.getch()
            if key == b'a' and health>0:
                if not is_solid(int(player_world_x - move_amount), player_y):
                    player_world_x -= move_amount
            elif key == b'd' and health>0:
                if not is_solid(int(player_world_x + move_amount), player_y):
                    player_world_x += move_amount
            elif key == b' ' and y_velocity==0:
                player_y += player_jump
            elif key == b'1' and latest_item == "Celestial Beginnings" and dash_cooldown==0:
                dash_time = DASH_DURATION
                dash_cooldown = 20
            elif key == b'\r':
                break

        # ENEMY MOVEMENT
        for e in enemies:
            if health>0:
                new_x = e["x"] + e["dir"] * e["speed"]
                if new_x < 0 or new_x >= PLANET_WIDTH:
                    e["dir"] *= -1
                elif is_solid(int(new_x), e["y"]):
                    e["dir"] *= -1
                else:
                    e["x"] = new_x

        # COLLISION WITH ENEMY
        for e in enemies:
            if int(e["x"]) == int(player_world_x) and e["y"] == player_y:
                if dash_time>0:
                    enemies.remove(e)
                else:
                    health -= 1
                    last_damage_time = frame_count
                    if health==0:
                        clear()
                        print(center_text("GAME OVER"))
                        time.sleep(2)
                        return

        # PICKUP ITEM
        if not celestial_item_obtained and int(player_world_x) == item_pos[0] and player_y == item_pos[1]:
            celestial_item_obtained = True
            latest_item = "Celestial Beginnings"
            player_dash_ready = True
            player_speed = 2
            player_jump = -7
            print(center_text("You obtained Celestial Beginnings!"))
            time.sleep(1)

        # HEALTH REGEN
        if frame_count - last_damage_time >= HEART_REGEN_DELAY*20 and health<max_health:
            health += 1
            last_damage_time = frame_count

        # CELESTIAL ADRENALINE
        if health==1 and not celestial_adrenaline:
            celestial_adrenaline = True
            adrenaline_time = 400
        if celestial_adrenaline:
            adrenaline_time -=1
            if adrenaline_time<=0:
                celestial_adrenaline=False
                player_speed=1
                player_jump=-4

        # CAMERA
        cam_pos = int(player_world_x - player_screen_x)
        cam_pos = max(0, min(cam_pos, PLANET_WIDTH - CAM_VIEW))

        draw_scene(cam_pos)

        if dash_cooldown>0:
            dash_cooldown -=1

        time.sleep(0.05)
        frame_count += 1


# --- SPACESHIP HUB ---
def spaceship_hub(username):
    while True:
        clear()
        print(center_text(f"🚀 SPACESHIP HUB — {username}'s Ship 🚀"))
        print("\n")
        print(center_text("1. Planets"))
        print(center_text("2. Wardrobe"))
        print(center_text("3. Back to Menu"))
        print("\nPress the number of your choice.")
        key = msvcrt.getch()
        if key == b'1':
            loading_screen("Preparing planetary travel")
            planet_selection()
        elif key == b'2':
            loading_screen("Entering wardrobe...")
            fake_wardrobe()
        elif key == b'3':
            loading_screen("Returning to main menu")
            return

# --- PLANET SELECT ---
def planet_selection():
    clear()
    print(center_text("🌍 PLANETS 🌍"))
    print(center_text("1. First Planet"))
    print(center_text("Press 1 to land or ENTER to go back"))
    while True:
        key = msvcrt.getch()
        if key == b'1':
            loading_screen("Landing sequence initiated...")
            planet_loop()
            break
        elif key == b'\r':
            break

# --- FAKE WARDROBE ---
def fake_wardrobe():
    clear()
    print(center_text("🧥 Wardrobe (under construction)"))
    print(center_text("Press ENTER to return"))
    while True:
        if msvcrt.kbhit() and msvcrt.getch() == b'\r':
            break

# --- MAIN ---
def main():
    startup()
    running = True
    while running:
        choice = main_menu()
        if choice == "1":
            username = login_or_signup()
            loading_screen("Launching adventure...")
            spaceship_hub(username)
        elif choice == "2":
            print(center_text("Farewell, Traveler 🌌"))
            time.sleep(1)
            running = False

if __name__ == "__main__":
    main()
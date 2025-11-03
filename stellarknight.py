import os
import time
import msvcrt
import json

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

# --- CHARACTER ---
def build_character(head="center", leg_frame=1, breathe=False):
    if head == "left":
        h = " <o"
    elif head == "right":
        h = "o> "
    else:
        h = " O " if breathe else " o "
    arms = "/|\\"
    legs = "/ \\" if leg_frame == 1 else "/|\\"
    return [h, arms, legs]

ROOM_WIDTH = 60
player_pos = 10
frame = 0

def draw_scene(player_pos, head_dir="center", leg_frame=1, breathe=False):
    clear()
    spaces = " " * player_pos
    sprite = build_character(head_dir, leg_frame, breathe)
    for line in sprite:
        print(spaces + line)
    print("\n" + "#" * ROOM_WIDTH)
    print("\n[ A - Left | D - Right | ENTER - Quit ]")

def move_player(dx):
    global player_pos
    new_x = player_pos + dx
    if 0 <= new_x <= ROOM_WIDTH - 5:
        player_pos = new_x

# --- PLANET LOOP ---
def planet_loop():
    global frame
    head_dir = "center"
    idle_timer = 0
    breathe_state = False
    moving = False

    while True:
        frame = (frame + 1) % 2
        if msvcrt.kbhit():
            key = msvcrt.getch()
            if key == b'a':
                move_player(-1)
                head_dir = "left"
                idle_timer = 0
                moving = True
            elif key == b'd':
                move_player(1)
                head_dir = "right"
                idle_timer = 0
                moving = True
            elif key == b'\r':
                break
        else:
            idle_timer += 1
            moving = False

        if not moving and idle_timer > 10:
            breathe_state = not breathe_state
            draw_scene(player_pos, "center", 1, breathe_state)
            time.sleep(0.6)
        elif moving:
            draw_scene(player_pos, head_dir, frame, False)
            time.sleep(0.1)
        else:
            draw_scene(player_pos, head_dir, 1, False)
            time.sleep(0.2)

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
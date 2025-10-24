import os
import time
import msvcrt

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
    return "\n".join([h, arms, legs])


# --- ROOM + MOVEMENT ---
ROOM = list("############################################################")
player_pos = 10
frame = 0

def draw_room(player_pos, head_dir="center", leg_frame=1, breathe=False):
    clear()
    line = ROOM.copy()
    line[player_pos] = "@"
    print("".join(line))
    print(build_character(head_dir, leg_frame, breathe))
    print("\n[ A - Left | D - Right | ENTER - Quit ]")

def move_player(dx):
    global player_pos
    new_x = player_pos + dx
    if 0 < new_x < len(ROOM) - 1:
        player_pos = new_x


# --- MAIN LOOP ---
def spaceship_loop():
    global frame
    head_dir = "center"
    idle_timer = 0
    breathe_state = False

    while True:
        if msvcrt.kbhit():
            key = msvcrt.getch()
            if key == b'a':
                move_player(-1)
                head_dir = "left"
                idle_timer = 0
            elif key == b'd':
                move_player(1)
                head_dir = "right"
                idle_timer = 0
            elif key == b'\r':
                break
        else:
            idle_timer += 1

        frame = (frame + 1) % 2

        # if idle for long enough, breathe
        if idle_timer > 15:
            breathe_state = not breathe_state
            draw_room(player_pos, "center", 1, breathe_state)
            time.sleep(0.8)
        else:
            draw_room(player_pos, head_dir, frame, False)
            time.sleep(0.15)


# --- MAIN ---
def main():
    startup()
    running = True
    while running:
        choice = main_menu()
        if choice == "1":
            print(center_text("Launching adventure..."))
            time.sleep(1.2)
            spaceship_loop()
        elif choice == "2":
            print(center_text("Farewell, Traveler 🌌"))
            time.sleep(1)
            running = False

if __name__ == "__main__":
    main()
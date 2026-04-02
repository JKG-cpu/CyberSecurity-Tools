from blessed import Terminal
import time

term = Terminal()

def draw_header():
    print(term.move_xy(0, 0) + term.bold(term.center("Blessed Layout Demo")))
    print(term.move_xy(0, 1) + "-" * term.width)

def draw_footer(message):
    y = term.height - 1
    print(term.move_xy(0, y) + " " * term.width)
    print(term.move_xy(0, y) + message)

def draw_sidebar(selected):
    width = term.width // 4
    options = ["Home", "Stats", "Settings", "Quit"]

    for i, option in enumerate(options):
        y = 3 + i
        text = f"> {option}" if i == selected else f"  {option}"
        print(term.move_xy(1, y) + text.ljust(width - 2))

    # vertical divider
    for y in range(2, term.height - 1):
        print(term.move_xy(width, y) + "|")

def draw_main(x, y, sidebar_width):
    # erase old area (only main section)
    for row in range(3, term.height - 1):
        print(term.move_xy(sidebar_width + 1, row) + " " * (term.width - sidebar_width - 1))

    # draw moving X inside main area
    print(term.move_xy(x, y) + term.red("X"))

def main():
    sidebar_width = term.width // 4
    x = sidebar_width + 5
    y = term.height // 2
    selected = 0

    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        print(term.clear)

        draw_header()
        draw_sidebar(selected)
        draw_footer("Use arrows to move | W/S to change menu | Q to quit")

        while True:
            old_x, old_y = x, y

            key = term.inkey(timeout=0.05)

            if key.name == "KEY_UP":
                y = max(3, y - 1)
            elif key.name == "KEY_DOWN":
                y = min(term.height - 2, y + 1)
            elif key.name == "KEY_LEFT":
                x = max(sidebar_width + 1, x - 1)
            elif key.name == "KEY_RIGHT":
                x = min(term.width - 1, x + 1)

            elif key.lower() == "w":
                selected = max(0, selected - 1)
                draw_sidebar(selected)
            elif key.lower() == "s":
                selected = min(3, selected + 1)
                draw_sidebar(selected)

            elif key.lower() == "q":
                break

            # update only main area if moved
            if (x, y) != (old_x, old_y):
                print(term.move_xy(old_x, old_y) + " ")
                print(term.move_xy(x, y) + term.red("X"))

            time.sleep(0.01)

if __name__ == "__main__":
    main()
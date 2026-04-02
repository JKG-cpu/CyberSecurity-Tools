from blessed import Terminal
import time

term = Terminal()

def main():
    x = term.width // 2
    y = term.height // 2

    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        print(term.home + term.clear)

        # Draw static UI once
        print(term.bold(term.center("Simple Blessed Demo")))
        print(term.move_xy(0, 2) + "Use arrow keys to move the X. Press 'q' to quit.")

        # Initial draw
        print(term.move_xy(x, y) + term.red("X"))

        while True:
            old_x, old_y = x, y

            key = term.inkey(timeout=0.1)

            if key.name == "KEY_UP":
                y = max(3, y - 1)
            elif key.name == "KEY_DOWN":
                y = min(term.height - 1, y + 1)
            elif key.name == "KEY_LEFT":
                x = max(0, x - 1)
            elif key.name == "KEY_RIGHT":
                x = min(term.width - 1, x + 1)
            elif key == "q":
                break

            # Only update if position changed
            if (x, y) != (old_x, old_y):
                # Erase old position
                print(term.move_xy(old_x, old_y) + " ")

                # Draw new position
                print(term.move_xy(x, y) + term.red("X"))

            time.sleep(0.01)

if __name__ == "__main__":
    main()
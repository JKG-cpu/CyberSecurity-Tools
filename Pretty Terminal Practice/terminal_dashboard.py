from blessed import Terminal

# Layout Features
# Header (title + time)
# System Stats
# Process / activity log (fake or real)
# Footer (controls / help)
# =====================================
# Update every 0.5 ~ 1 second
#   => Cpu Usage %
#   => RAM Usage
#   => Current Time
# Use psutil
# =====================================
# Color Code values
#   => Multiple color schemes???
# Keyboard interaction (q for quit, arrow keys to move, etc.)
# =====================================
# Basic animation (?)
#   => blinking warning if usage high

# Terminal Layout
# -------------------------
# |  Cur Time             | Header
# |-----------------------|
# |CPU Usage | RAM Usage  |
# |Time      | Blinking   | Stats
# |          |   Light    |
# |          |  Problem?  |
# |-----------------------|
# | Activity Log          | Activ Log
# |-----------------------|
# |       Controls        | Footer
# -------------------------

def recalculate_positions(term: Terminal) -> dict:
    header_height = 5
    footer_height = 2

    body_height = term.height - (header_height + footer_height)
    stats_height = body_height // 2
    log_height = body_height - stats_height

    header = (0, 0, term.width, header_height)
    stats = (0, header_height, term.width, stats_height)
    log = (0, header_height + stats_height, term.width, log_height)
    footer = (0, term.height - footer_height, term.width, footer_height)

    return {"header": header, "stats": stats, "log": log, "footer": footer}

def header(term: Terminal, x: int, y: int, width: int, height: int) -> None:
    pass

def stats(term: Terminal, x: int, y: int, width: int, height: int) -> None:
    pass

def activity_log(term: Terminal, x: int, y: int, width: int, height: int) -> None:
    pass

def footer(term: Terminal, x: int, y: int, width: int, height: int) -> None:
    pass

def main() -> None:
    # term = Terminal()

    # with term.fullscreen(), term.cbreak():
    #     while True:
    #         print(term.clear)

    #         positions = recalculate_positions(term)
    pass

if __name__ == "__main__":
    main()
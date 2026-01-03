import curses
import random

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)

    sh, sw = stdscr.getmaxyx()
    w = curses.newwin(sh, sw, 0, 0)
    w.keypad(1)

    snake = [
        [sh//2, sw//4],
        [sh//2, sw//4 - 1],
        [sh//2, sw//4 - 2]
    ]

    food = [sh//2, sw//2]
    w.addch(int(food[0]), int(food[1]), curses.ACS_PI)

    key = curses.KEY_RIGHT
    score = 0

    while True:
        next_key = w.getch()
        key = key if next_key == -1 else next_key

        head = snake[0]
        new_head = [head[0], head[1]]

        if key == curses.KEY_DOWN:
            new_head[0] += 1
        if key == curses.KEY_UP:
            new_head[0] -= 1
        if key == curses.KEY_LEFT:
            new_head[1] -= 1
        if key == curses.KEY_RIGHT:
            new_head[1] += 1

        snake.insert(0, new_head)

        if snake[0] in snake[1:] or \
           snake[0][0] in [0, sh] or \
           snake[0][1] in [0, sw]:
            break

        if snake[0] == food:
            score += 1
            food = None
            while food is None:
                nf = [
                    random.randint(1, sh-2),
                    random.randint(1, sw-2)
                ]
                food = nf if nf not in snake else None
            w.addch(food[0], food[1], curses.ACS_PI)
        else:
            tail = snake.pop()
            w.addch(int(tail[0]), int(tail[1]), ' ')

        w.addch(int(snake[0][0]), int(snake[0][1]), curses.ACS_CKBOARD)

    stdscr.addstr(sh//2, sw//2 - 5, f"Game Over! Score: {score}")
    stdscr.refresh()
    stdscr.getch()

if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass

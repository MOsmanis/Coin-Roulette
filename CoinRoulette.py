import subprocess
import curses
import time
import random
from random import randint

Y = 50
X = 10

def main():
    
    curses_controller = CursesController(0)
    curses_controller.initCurses()
    try:
        game(curses_controller)
    except KeyboardInterrupt:
        curses_controller.closeCurses()
        exit()

class O():
    def  __init__(self, **kwargs):
        self.location = (17, 2)
        self.level = 0
        self.currency = 0
    def move(self, direction, data):
        newdata = data
        if direction == "left":
            x, y = self.location
            if y <= -1:
                return list("dead")
            newPOS = newdata[34*y + x-1]
            if newPOS == ' ':
                self.location = (x - 1, y)
                newdata[34 * y + x] = ' '
                newdata[34 * y + x - 1] = 'O'
            elif newPOS == 'U':
                return list("next")
        if direction == "up":
            x, y = self.location
            if y <= -1:
                return list("dead")
            newPOS = newdata[34*(y-1) + x]
            if newPOS == ' ':
                self.location = (x, y - 1)
                newdata[34 * y + x] = ' '
                newdata[34 * (y-1) + x] = 'O'
            elif newPOS == 'U':
                return list("next")
        if direction == "right":
            x, y = self.location
            if y <= -1:
                return list("dead")
            newPOS = newdata[34 * y + x + 1]
            if newPOS == ' ':
                self.location = (x + 1, y)
                newdata[34 * y + x] = ' '
                newdata[34 * y + x + 1] = 'O'
            elif newPOS =='U':
                return list("next")
        if direction == "down":
            x, y = self.location
            if y <= -1:
                y = 0
            newPOS = newdata[34*(y+1) + x]
            if newPOS == ' ':
                self.location = (x, y + 1)
                newdata[34 * y + x] = ' '
                newdata[34 * (y+1) + x] = 'O'
            elif newPOS == 'U':
                return list("next")
        return newdata
    def canFight(self, data):
        x, y = self.location
        if data[34 * y + x - 1] == 'X' or data[34 * y + x + 1] == 'X' or data[34 * (y+1) + x] == 'X' or data[34 * (y-1) + x] == 'X' :
            return 1
    def canFightC(self, data):
        x, y = self.location
        if data[34 * y + x - 1] == 'C' or data[34 * y + x + 1] == 'C' or data[34 * (y+1) + x] == 'C' or data[34 * (y-1) + x] == 'C' :
            return 1
    def clearEnemies(self, data):
        x, y = self.location
        if data[34 * y + x - 1] == 'X':
            data[34 * y + x - 1] = ' '
        elif data[34 * y + x + 1] == 'X':
            data[34 * y + x + 1] = ' '
        elif data[34 * (y+1) + x] == 'X':
            data[34 * (y+1) + x] = ' '
        elif data[34 * (y-1) + x] == 'X' :
            data[34 * (y-1) + x] = ' '
        return data
    def clearEnemiesC(self, data):
        x, y = self.location
        if data[34 * y + x - 1] == 'C':
            data[34 * y + x - 1] = ' '
        elif data[34 * y + x + 1] == 'C':
            data[34 * y + x + 1] = ' '
        elif data[34 * (y+1) + x] == 'C':
            data[34 * (y+1) + x] = ' '
        elif data[34 * (y-1) + x] == 'C':
            data[34 * (y-1) + x] = ' '
        return data

class CursesController():
    def __init__(self, level):
        self.level = level
        self.currency = 0
        self.data = list(
        "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII\n" +
        "I                               I\n" +
        "I         COIN  ROULETTE        I\n" +
        "I                               I\n" +
        "I                               I\n" +
        "I                               I\n" +
        "I                               I\n" +
        "I               X               I\n" +
        "I                               I\n" +
        "I                               I\n" +
        "I                               I\n" +
        "UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU\n"
        )

        self.coinflip = [
            list(
        "      ooooooo      \n" +
        "    ooxxxxxxxoo    \n" +
        "  oooxxxxxxxxxooo  \n" +
        " ooxxxxxxxxxxxxxoo \n" +
        " ooxxxxxxxxxxxxxoo \n" +
        " ooxxxxxxxxxxxxxoo \n" +
        "  oooxxxxxxxxxooo  \n" +
        "    ooxxxxxxxoo    \n" +
        "      ooooooo      \n"
        ),
        list(
        "                   \n" +
        "      ooooooo      \n" +
        "    ooxxxxxxxoo    \n" +
        " ooxxxxxxxxxxxxxoo \n" +
        " ooxxxxxxxxxxxxxoo \n" +
        " ooxxxxxxxxxxxxxoo \n" +
        "    ooxxxxxxxoo    \n" +
        "      ooooooo      \n" +
        "                   \n"
        ),
        list(
        "                   \n" +
        "                   \n" +
        "      ooooooo      \n" +
        "    ooxxxxxxxoo    \n" +
        " ooxxxxxxxxxxxxxoo \n" +
        "    ooxxxxxxxoo    \n" +
        "      ooooooo      \n" +
        "                   \n" +
        "                   \n"
        ),
        list(
        "                   \n" +
        "                   \n" +
        "                   \n" +
        "    ooooooooooo    \n" +
        " ooxxxxxxxxxxxxxoo \n" +
        "    ooooooooooo    \n" +
        "                   \n" +
        "                   \n" +
        "                   \n"
        ),
        list(
        "                   \n" +
        "                   \n" +
        "                   \n" +
        "                   \n" +
        " ooooooooooooooooo \n" +
        "                   \n" +
        "                   \n" +
        "                   \n" +
        "                   \n"
        ),
        list(
        "                   \n" +
        "                   \n" +
        "                   \n" +
        "    ooooooooooo    \n" +
        " ooxxxxxxxxxxxxxoo \n" +
        "    ooooooooooo    \n" +
        "                   \n" +
        "                   \n" +
        "                   \n"
        ),
        list(
        "                   \n" +
        "                   \n" +
        "      ooooooo      \n" +
        "    ooxxxxxxxoo    \n" +
        " ooxxxxxxxxxxxxxoo \n" +
        "    ooxxxxxxxoo    \n" +
        "      ooooooo      \n" +
        "                   \n" +
        "                   \n"
        ),
        list(
        "                   \n" +
        "      ooooooo      \n" +
        "    ooxxxxxxxoo    \n" +
        " ooxxxxxxxxxxxxxoo \n" +
        " ooxxxxxxxxxxxxxoo \n" +
        " ooxxxxxxxxxxxxxoo \n" +
        "    ooxxxxxxxoo    \n" +
        "      ooooooo      \n" +
        "                   \n"
        ),
        list(
        "      ooooooo      \n" +
        "    ooxxxxxxxoo    \n" +
        "  oooxxxxxxxxxooo  \n" +
        " ooxxxxxxxxxxxxxoo \n" +
        " ooxxxxxxxxxxxxxoo \n" +
        " ooxxxxxxxxxxxxxoo \n" +
        "  oooxxxxxxxxxooo  \n" +
        "    ooxxxxxxxoo    \n" +
        "      ooooooo      \n"
        ),
        ]

    def initCurses(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self.stdscr.nodelay(1)
        self.stdscr.keypad(1)
        self.stdscr.clear()
        rows = "".join(self.data).split("\n")
        i=0
        for row in rows:
            self.stdscr.addstr(0+i,0+X,row)
            i+=1
        self.stdscr.addstr(3, 44+X, "Score: " + str(self.level) + "    Coins: " + str(self.currency))
        self.stdscr.addstr(6, 44+X, "Fight enemies by flipping coins!")
        self.stdscr.addstr(7, 44+X, "If you win enemy X, you can then use their coin on enemies C for 100% win!")
        self.stdscr.addstr(8, 44+X, "Move next to X or C and press 'x' to flip the coin")
        self.stdscr.addstr(9, 44+X, "Go down to move to next room")
        self.stdscr.addstr(10, 44+X, "Move to start game")
        self.stdscr.addstr(12, 44+X, "\"q\" to quit!")

    def write(self):
        self.stdscr.clear()
        rows = "".join(self.data).split("\n")
        i=0
        for row in rows:
            self.stdscr.addstr(0+i,0+X,row)
            i+=1
        self.stdscr.addstr(3, 44+X, "Score: " + str(self.level) + "    Coins: " + str(self.currency))
        self.stdscr.addstr(6, 44+X, "Fight enemies by flipping coins!")
        self.stdscr.addstr(7, 44+X, "If you win enemy X, you can then use their coin on enemies C for 100% win!")
        self.stdscr.addstr(8, 44+X, "Move next to X or C and press 'x' to flip the coin")
        self.stdscr.addstr(9, 44+X, "Go down to move to next room")
        self.stdscr.addstr(10, 44+X, "Move to start game")
        self.stdscr.addstr(12, 44+X, "\"q\" to quit!")
    def flipResult(self, result):
        i = 0
        while i<3:
            i+=1
            self.doCoinflip()
        resultCoin = list(
        "      ooooooo      \n" +
        "    ooxxxxxxxoo    \n" +
        "  oooxxxxxxxxxooo  \n" +
        " ooxxxxxxxxxxxxxoo \n" +
        result +
        " ooxxxxxxxxxxxxxoo \n" +
        "  oooxxxxxxxxxooo  \n" +
        "    ooxxxxxxxoo    \n" +
        "      ooooooo      \n")
        rows = "".join(resultCoin).split("\n")
        i = 0
        for row in rows:
            self.stdscr.addstr(14 + i, 7 + X, row)
            i += 1
        self.stdscr.refresh()
        time.sleep(2)


    def doCoinflip(self):
        for frame in self.coinflip:
            rows = "".join(frame).split("\n")
            i = 0
            for row in rows:
                self.stdscr.addstr(14 + i, 7 + X, row)
                i += 1
            self.stdscr.refresh()
            time.sleep(.040)
    def closeCurses(self):
        curses.nocbreak()
        self.stdscr.keypad(0)
        curses.echo()
        curses.endwin()

def cutBeginning(curses_controller, o):
    data = curses_controller.data
    lines_to_cut = 1
    i = 0
    while i < lines_to_cut:
        curses_controller.data = data[34:]
        i+=1
    x, y = o.location
    o.location = (x,(y-lines_to_cut))
    refresh(curses_controller, o)


def game(curses_controller):
    o = O()

    while 1:
        #curses_controller.flipResult(" oo    ALIVE    oo \n") #" oo     ALIVE    oo \n oo    DEAD     oo \n"
        key = curses_controller.stdscr.getch()
        if curses_controller.data != "Dead! Press \"r\" for restart":
            if o.canFight(curses_controller.data) and key == ord('x'):
                    fight(curses_controller, o)
            elif o.canFightC(curses_controller.data) and key == ord('x'):
                if curses_controller.currency > 0:
                    curses_controller.currency -=1
                    curses_controller.flipResult(" oo     WIN     oo \n")
                    curses_controller.level += 2
                    o.clearEnemiesC(curses_controller.data)
                    curses_controller.write()
                else:
                    if random.random() < 0.2:
                        status = "dead"
                        curses_controller.flipResult(" oo    LOSER    oo \n")
                        curses_controller.data = "Dead! Press \"r\" for restart"
                        refresh(curses_controller, o)
                    else:
                        curses_controller.flipResult(" oo     WIN     oo \n")
                        curses_controller.level += 1
                        curses_controller.currency += 1
                        o.clearEnemiesC(curses_controller.data)
                        curses_controller.write()

            elif key == curses.KEY_LEFT:
                move(curses_controller, o, "left")
                #cutBeginning(curses_controller, o)

            elif key == curses.KEY_RIGHT:
                move(curses_controller, o, "right")
                #cutBeginning(curses_controller, o)

            elif key == curses.KEY_UP:
                move(curses_controller, o, "up")
                #cutBeginning(curses_controller, o)

            elif key == curses.KEY_DOWN:
                move(curses_controller, o, "down")
                #cutBeginning(curses_controller, o)

            elif key == ord('q'):
                curses_controller.closeCurses()
                exit()
        else:
            if key == ord('q'):
                curses_controller.closeCurses()
                exit()

            if key == ord('r'):
                curses_controller.closeCurses()
                main()

def fight(curses_controller,o):
    status = ""
    if random.random() < 0.2:
        status = "dead"
        curses_controller.flipResult(" oo    LOSER    oo \n")
        curses_controller.data = "Dead! Press \"r\" for restart"
        refresh(curses_controller, o)
    else:
        curses_controller.flipResult(" oo     WIN     oo \n")
        curses_controller.level += 1
        curses_controller.currency += 1
        o.clearEnemies(curses_controller.data)
        curses_controller.write()



def move(curses_controller, o, direction):
    status = o.move(direction, curses_controller.data)
    if "".join(status) == "dead":
        curses_controller.data = "Dead! Press \"r\" for restart"
        refresh(curses_controller, o)
    elif "".join(status) == "next":
        newdata = list(
        "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII\n" +
        "I                               I\n" +
        "I                O              I\n" +
        "I                               I\n" +
        "I                               I\n" +
        "I                               I\n" +
        "I                               I\n" +
        "I                               I\n" +
        "I                               I\n" +
        "I                               I\n" +
        "I                               I\n" +
        "UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU\n")
        i = 0
        while i<5:
            x = randint(1, 31)
            y = randint(3, 10)
            if random.random() < 0.7:
                newdata[34 * y + x] = 'X'
            else:
                newdata[34 * y + x] = 'C'
            i+=1
        animate_open_doors(curses_controller, o)
        o.location = (17, 2)
        curses_controller.data = newdata
        refresh(curses_controller, o)
    else:
        curses_controller.data = status
        refresh(curses_controller, o)
    

def refresh(curses_controller, o):
    overflow = len(curses_controller.data) - (34 * Y)
    if overflow > 0:
        curses_controller.data = curses_controller.data[overflow:]
        x, y = o.location
        o.location = (x,(y-(overflow//34)))
    curses_controller.write()
    curses_controller.stdscr.refresh()
    time.sleep(.030)

def animate_open_doors(curses_controller, o):
    length = len(curses_controller.data)
    curses_controller.data[length-18]=' '
    refresh(curses_controller, o)
    i = 1
    width=2
    if o.level > 5:
        width=11
    while i<17:
        curses_controller.data[length-18+i]=' '
        curses_controller.data[length-18-i]=' '
        if i>17-width:
           curses_controller.data[length-18+i]='I'
           curses_controller.data[length-18-i]='I'
        i+=1
        refresh(curses_controller, o)
    curses_controller.data[length-1]='\n'
    refresh(curses_controller, o)


if __name__ == '__main__':
    main()

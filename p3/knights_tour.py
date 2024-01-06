import sys
import random
import time

probabilities = [0.7, 0.8, 0.85]
k_values = [0, 1, 2, 3]
run_count = 100000

def generate_board():
    return [[-1 for _ in range(8)] for _ in range(8)]

def get_available_squares(board, knight):
    x, y = knight
    available = []
    for dx, dy in [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]:
        if 0 <= x + dx < 8 and 0 <= y + dy < 8 and board[x + dx][y + dy] == -1:
            available.append((x + dx, y + dy))
    return available


def get_heuristic_available_squares(board, knight, move = 0, target_count = 100):
    offsets = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
    x, y = knight
    available = []
    temp_available = []
    degrees = []
    for dx, dy in offsets:
        if 0 <= x + dx < 8 and 0 <= y + dy < 8 and board[x + dx][y + dy] == -1:
            degree = sum(1 for dx2, dy2 in offsets if 0 <= x + dx + dx2 < 8 and 0 <= y + dy + dy2 < 8 and board[x + dx + dx2][y + dy + dy2] == -1 and not(dx == -1*dx2 and dy==-1*dy2 ))
            if degree>0 or move == target_count-1:
                temp_available.append((degree, x+dx, y+dy))
    sorted(temp_available)
    available = [(x, y) for (z, x, y) in temp_available]
    return available

def fprint_board(f, board):
    for row in board:
        f.write(' '.join(map(str, row)) + '\n')
    f.write('\n')

def print_board(board):
    for row in board:
        print(' '.join(map(str, row)))
    print()

def board_to_string(board, knight):
    s = str(knight) 
    #+ ' '.join(map(lambda x: ' '.join(lambda y: '0' if y == -1 else '-1'), board))
    for row in board:
        s += ''.join(map(lambda x: '0' if x == -1 else '1', row))
    return s

def part1():
    for p in probabilities:
        start = time.time()
        with open("results_{}.txt".format(p), 'w') as f:
            success = 0
            for count in range(run_count):
                board = generate_board()
                target_count = 64 * p
                move = 0
                knight = random.randint(0, 7), random.randint(0, 7)
                board[knight[0]][knight[1]] = move
                f.write("Run {}: starting from ({},{})\n".format(count, knight[0], knight[1]))
                while move < target_count:
                    try:
                        x, y = random.choice(get_available_squares(board, knight))
                        move += 1
                        board[x][y] = move
                        knight = x, y
                        f.write("Stepping to ({},{})\n".format(x, y))
                    except IndexError:
                        f.write("Unsuccessful - Tour length: {}\n".format(move))
                        fprint_board(f, board)
                        break
                else:
                    success += 1
                    f.write("Successful - Tour length: {}\n".format(move))
                    fprint_board(f, board)
            end = time.time()
            print("LasVegas Algorithm With p = {}".format(p))
            print("Number of successful tours: {}".format(success))
            print("Number of trials: {}".format(run_count))
            print("Probability of successful tour: {}\n".format(success / 100000))
            # print("Time: {}\n".format(end-start))

def part2():
    for p in probabilities:
        print("--- p = {} ---".format(p))
        target_count = 64 * p
        for k in k_values:
            success = 0
            for _ in range(run_count):
                board = generate_board()
                unsuccessful = False
                stack = []
                move = 0
                knight = random.randint(0, 7), random.randint(0, 7)
                board[knight[0]][knight[1]] = move
                for _ in range(k):
                    try:
                        move += 1
                        knight = random.choice(get_heuristic_available_squares(board, knight))
                        board[knight[0]][knight[1]] = move
                    except IndexError:
                        unsuccessful = True
                        break
                if unsuccessful:
                    continue
                stack.append((knight, move+1, board))

                checked = set()
                while stack:
                    knight, move, board = stack.pop()
                    if move >= target_count:
                        success += 1
                        break

                    for x, y in get_heuristic_available_squares(board, knight, move, target_count):
                        new_board = [row[:] for row in board]
                        new_board[x][y] = move
                        new_check = board_to_string(new_board, (x, y))
                        if new_check not in checked:
                            checked.add(new_check)
                            stack.append(((x, y), move + 1, new_board))
            print("LasVegas Algorithm With p = {}, k = {}".format(p, k))
            print("Number of successful tours: {}".format(success))
            print("Number of trials: {}".format(run_count))
            print("Probability of successful tour: {}\n".format(success / run_count))

def part3():
    global probabilities
    global k_values
    global run_count
    probabilities = [1]
    part1()
    run_count = 1
    k_values = [0] # add k value that might be useful
    part2()

if __name__ == '__main__':
    if len(sys.argv) != 2 or sys.argv[1] not in ['part1', 'part2', 'part3']:
        print("Usage: python knights_tour.py <part>")
        sys.exit(1)
    eval(sys.argv[1])()

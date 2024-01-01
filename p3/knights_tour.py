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
            # available.append((x + dx, y + dy))
            # degrees.append(sum(1 for dx2, dy2 in offsets if 0 <= x + dx + dx2 < 8 and 0 <= y + dy + dy2 < 8 and board[x + dx + dx2][y + dy + dy2] == -1))
            degree = sum(1 for dx2, dy2 in offsets if 0 <= x + dx + dx2 < 8 and 0 <= y + dy + dy2 < 8 and board[x + dx + dx2][y + dy + dy2] == -1 and not(dx == -1*dx2 and dy==-1*dy2 ))
            if degree>0 or move == target_count-1:
                temp_available.append((degree, x+dx, y+dy))
    #             available.append((x + dx, y + dy))
    #             degrees.append(degree)
    # available = [x for _, x in sorted(zip(degrees, available))]
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
            print("Las vegas algorithm with p = {}".format(p))
            print("Number of successful tours: {}".format(success))
            print("Number of trials: {}".format(run_count))
            print("Probability of successful tour: {}\n".format(success / run_count))
            print("Time: {}\n".format(end-start))

def part2():
    with open("kroston.txt", 'w') as f:
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
                    # print_board(board)
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
                    while stack:
                        knight, move, board = stack.pop()
                        print(move, knight)
                        if move >= target_count:
                            success += 1
                            fprint_board(f, board)
                            break
                        for x, y in get_heuristic_available_squares(board, knight, move, target_count):
                            new_board = [row[:] for row in board]
                            new_board[x][y] = move
                            stack.append(((x, y), move + 1, new_board))
                print("Las vegas algorithm with p = {}, k = {}".format(p, k))
                print("Number of successful tours: {}".format(success))
                print("Number of trials: {}".format(run_count))
                print("Probability of successful tour: {}\n".format(success / run_count))

def part3():
    global probabilities
    global k_values
    global run_count
    probabilities = [1]
    k_values = [0] # add k value that might be useful
    part1()
    run_count = 1
    part2()

def k_bigger_than_10():
    global k_values
    global run_count
    k_values = [10, 11, 12, 13, 14, 15]
    run_count = 100
    part2()

if __name__ == '__main__':
    if len(sys.argv) != 2 or sys.argv[1] not in ['part1', 'part2', 'part3', 'k_bigger_than_10']:
        print("Usage: python knights_tour.py <part>")
        sys.exit(1)
    eval(sys.argv[1])()


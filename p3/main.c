#include <stdio.h>
#include <stdlib.h>

#define LEFT(x) (((x) << 1) & 0x7f7f7f7f7f7f7f7f)
#define RIGHT(x) (((x) >> 1) & 0xfefefefefefefefe)
#define UP(x) (((x) << 8) & 0xffffffffffffff00)
#define DOWN(x) (((x) >> 8) & 0x00ffffffffffffff)

typedef unsigned long board_t;
struct board {
    board_t board;
    board_t knight;
    struct board* parent;
    short depth;
};

void print_board(board_t board, board_t knight) {
    for (int i = 0; i < 64; i++) {
        if (i % 8 == 0) {
            printf("\n");
        }
        if (board & (1L << i)) {
            printf("1 ");
        } else if (knight & (1L << i)) {
            printf("K ");
        } else {
            printf("0 ");
        }
    }
    printf("\n");
}

board_t *get_possible(board_t knight, board_t board) {
    board_t *res = calloc(8, sizeof(board_t));
    res[0] = LEFT(UP(knight)) & ~board;
    res[1] = RIGHT(UP(knight)) & ~board;
    res[2] = LEFT(DOWN(knight)) & ~board;
    res[3] = RIGHT(DOWN(knight)) & ~board;
    res[4] = UP(LEFT(knight)) & ~board;
    res[5] = UP(RIGHT(knight)) & ~board;
    res[6] = DOWN(LEFT(knight)) & ~board;
    res[7] = DOWN(RIGHT(knight)) & ~board;
    return res;
}

struct board* dfs(struct board* board) {
    if (board->depth == 20) {
        return board;
    }
    board_t *possible = get_possible(board->knight, board->board);
    for (int i = 0; i < 8; i++) {
        if (possible[i]) {
            struct board* new_board = malloc(sizeof(struct board));
            new_board->board = board->board | possible[i];
            new_board->knight = possible[i];
            new_board->parent = board;
            new_board->depth = board->depth + 1;
            struct board* res = dfs(new_board);
            if (res) {
                return res;
            }
            free(new_board);
        }
    }
    free(possible);
    return NULL;
}

int main() {
    struct board board;
    board.board = 0ULL;
    board.knight = 32ULL;
    board = *dfs(&board);
    print_board(board.board, board.knight);
    return 0;
}

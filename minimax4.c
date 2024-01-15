#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>


// gcc -shared -o minimax.so -fPIC minimax4.c
// compiles the program so python can run it
// only works on mac and linux/wsl


int maximum(int num1, int num2) {
    if (num1 > num2) {
        return num1;
    }
    return num2;
}

int minimum(int num1, int num2) {
    if (num2 < num1) {
        return num2;
    }
    return num1;
}

struct Board {
    int **board;
    int width;
    int height;
};

struct Table {
    uint64_t **bit_values;
    uint64_t hash;
    uint64_t size;
    struct Node *nodes;
};

struct Node {
    __int128_t validation;
    float eval;
    struct Node *next;
};

void print_table(struct Table table) {
    printf("\ntable has size %d\n", table.size);
    for (int i = 0; i < table.size; i++) {
        printf("node%d.next = %llu\n", i, (table.nodes[i]).next);
    }
}

__int128_t generate_key(struct Board board) {
    __int128_t key = 0;
    for (int color = 0; color <= 1; ++color) {
        for (int i = 0; i < board.height; ++i) {
            for (int k = 0; k < board.height; ++k) {
                key <<= 1;
                if (board.board[i][k] == color) key += 1;
            } 
        }
    }
    return key;
}

void add_position(struct Table table, __int128_t validation, float eval, struct Node* prev) {
    struct Node *new_node = (struct Node*) malloc(sizeof(struct Node));
    new_node->validation = validation;
    new_node->eval = eval;
    new_node->next = NULL;
    prev->next = new_node;
}

void enter_value(struct Table table, struct Board board, float eval, float depth) {
    __int128_t key = generate_key(board);
    uint64_t index = table.hash % table.size;
    // printf("entering at index %llu\n", table.hash);

    // printf("first node: %d", table.nodes + index);
    // printf(" %llu ", (table.nodes + index)->validation);
    if ((table.nodes + index)->validation == 0) {
        struct Node node = {.validation = key, .eval = eval, .next = NULL};
        table.nodes[index] = node;
    }
    else {
        struct Node *node = table.nodes + index;
        struct Node *prev = table.nodes + index;
        int counter = 0;
        while (node->next != 0 && counter < 10) {
            if (node->validation == key) {
                return;
            }
            prev = node;
            node = node->next;
        }
        if (counter == 10) {
            // max length of bucket reached - replace last node 
            // - currently replaces the last node - does need to be changed eventually
            add_position(table, key, eval, prev);
        }
        else {
            add_position(table, key, eval, prev);
        }
    }
}

int8_t retrieve_value(struct Table table, struct Board board) {
    __int128_t key = generate_key(board);
    uint64_t index = table.hash % table.size;
    if (! (table.nodes + index)) {
        printf("cancelled: no node present\n");
        return 127;
    }
    struct Node node = table.nodes[index];
    while (node.next) {
        if (node.validation == key) {
            printf("success: %llu\n", node.validation);
            return node.eval;
        }
    }
    if (node.validation == key) {
        printf("success : %llu\n", node.validation);
        return node.eval;
    }
    // printf("not found\n");
    return 127;
}

void print_array(int* ar, int length) {
    for (int i = 0; i < length; i++) {
        if (ar[i] == -1) {
            printf("%d ", ar[i]);
        }
        else {
            printf(" %d ", ar[i]);
        }
    }
    printf("\n");
}

void print_array_f(float* ar, int length) {
    for (int i = 0; i < length; i++) {
        if (ar[i] == -1) {
            printf("%f ", ar[i]);
        }
        else {
            printf(" %f ", ar[i]);
        }
    }
    printf("\n");
}

void print_int8_array(int8_t* ar, int length) {
    for (int i = 0; i < length; i++) {
        if (ar[i] == -1) {
            printf("%d ", ar[i]);
        }
        else {
            printf(" %d ", ar[i]);
        }
    }
    printf("\n");
}

void print_board(struct Board game_board) {
    for (int i = 0; i < game_board.height; ++i) {
        print_array(game_board.board[i], game_board.width);
    }
}

struct Board create_board(int rows, int cols) {
    int** board_array = (int **)malloc((rows) * sizeof(int*));
    for (int i = 0; i < rows; i++) {
        int* row = (int*)malloc(cols * sizeof(int));
        board_array[i] = row;
        for (int k = 0; k < cols; k++) {
            row[k] = 0;
        }
    }
    struct Board game_board = {board_array, cols, rows};
    print_board(game_board);
    return game_board;
}

struct Board set_board() {
    int** board_array = (int **)malloc(6 * sizeof(int*));
    for (int i = 0; i < 7; ++i) {
        int* row = (int*)malloc(7 * sizeof(int));
        for (int k = 0; k < 7; ++k) {
            row[k] = 0;
        }
        if (i == 3 || i == 5 || i == 4) {
            row[0] = 1;
        }
        board_array[i] = row;
    }
    struct Board board = {board_array, 7, 6};
    print_board(board);
    return board;
}


void free_board(struct Board board) {
    for (int i = 0; i < board.height; ++i) {
        free(board.board[i]);
    }
    free(board.board);
}

struct Board convert_board(int rows, int cols, int *board_array) {
    int **expanded_board = (int**)malloc(sizeof(int*) * rows);
    for (int i = 0; i < rows; i++) {
        int *row = (int*)malloc(sizeof(int) * cols);
        for (int k = 0; k < cols; k++) {
            row[k] = board_array[k + (cols * i)];
        }
        expanded_board[i] = row;
    }


    struct Board game_board = {expanded_board, cols, rows};
    return game_board;
}

uint64_t random_bitstring() {
    uint64_t random_value = 0;
    // printf("random value: ");
    for (int i = 0; i < 64; ++i) {
        random_value <<= 1;
        random_value += rand() % 2;
        // printf("%llu ", random_value);
    }
    // printf("\n end result: %llu\n", random_value);
    return random_value;
}

struct Table init_table(struct Board game_board, int table_size) {
    uint64_t **hash_table = (uint64_t**)malloc(sizeof(uint64_t*) * game_board.height);
    for (int i = 0; i < game_board.height; ++i) {
        uint64_t *row = (uint64_t*)malloc(sizeof(uint64_t) * game_board.width);
        for (int k = 0; k < game_board.width; ++k) {
            row[k] = random_bitstring();
            // printf("intializing with %llu", row[k]);
        }
        hash_table[i] = row;
    }

    struct Node *nodes = (struct Node*)calloc(table_size, sizeof(struct Node)); // using calloc for default value
    struct Table table = {.bit_values = hash_table, .hash = 0, .size = table_size, .nodes = nodes};
    return table;
}

void free_table(struct Table table, struct Board board) {
    for (int i = 0; i < board.height; ++i) {
        free(table.bit_values[i]);
    }
    free(table.nodes);
}

int play_move(int color, int col_index, struct Board game_board) {
    for (int i = game_board.height - 1; i >= 0; i--) {
        if (game_board.board[i][col_index] == 0) {
            game_board.board[i][col_index] = color;
            return i; // returns height from top, which will cause endless confusion
        }
    }
    return -1;
}

int check_row(int* row, int length) {
    int count = 0;
    int last = -2;
    for (int i = 0; i < length; i++) {
        if (row[i] == last && last != 0) {
            count++;
            if (count == 3) {
                return last;
            }
        }
        else {
            count = 0;
            last = row[i];
        }
    }
    return 0;
}

int check_col(int** game_board, int col_index, int length) {
    int count = 0;
    int last = -2;
    for (int i = 0; i < length; i++) {
        if (game_board[i][col_index] == last && last != 0) {
            count++;
            if (count == 3) { // 3 because 0 indexed
                return last;
            }
        }
        else {
            last = game_board[i][col_index];
            count = 0;
        }
    }
    return 0;
}

int single_diagonal(struct Board board, int i, int k, int i_step, int k_step) {
    int count = 0;
    int last = -2;
    while (i < board.height && k < board.width && i >= 0 && k >= 0) {
        if (board.board[i][k] == last && last != 0) {
            count++;
            if (count == 3) {
                return last;
            }
        }
        else {
            count = 0;
            last = board.board[i][k];
        }
        i += i_step;
        k += k_step;
    }
    return 0;
}   

int check_diagonals(struct Board board, int col, int row) {
    int k = col - minimum(col, row);
    int i = row - minimum(col, row);
    int upright = single_diagonal(board, i, k, 1, 1);
    if (upright != 0) return upright;

    int min_dist = minimum(board.width - col, row);
    k = col + min_dist;
    i = row - min_dist;

    int downright = single_diagonal(board, i, k, 1, -1);
    if (downright != 0) return downright;

    return 0;
}

int check_for_win(struct Board game_board, int placed_col, int placed_row) {
    if (placed_row == -1) return 0;
    int row = check_row(game_board.board[placed_row], game_board.width);
    if (row != 0) {
        return row;
    }
    int col = check_col(game_board.board, placed_col, game_board.height);
    if (col != 0) {
        return col;
    }
    int diag = check_diagonals(game_board, placed_col, placed_row);
    if (diag != 0) {
        return diag;
    }
    return 0;
}

int check_for_win_py(int *board_array, int width, int height, int col, int row) {
    struct Board board = convert_board(width, height, board_array);
    return check_for_win(board, col, row);
}

int check_for_holes(struct Board board) { // for debugging
    for (int i = 0; i < board.width; i++) {
        int seen = 0;
        for (int k = 0; k < board.height; k++) {
            if (board.board[k][i] == 0) {
                if (seen) return 1;
            }
            else seen = 1;
        }
    }
    return 0;
}

float minimax(int color, int alpha, int beta, struct Board board, float depth, int max_depth, struct Table transpos_table) {
    // print_table(transpos_table);
    printf(".");
    int placed_height;
    if (depth == max_depth) {
        return 0;
    }
    float best = -1000 * color;

    for (int i = 0; i < board.width; i++) {
        placed_height = play_move(color, i, board);
        if (placed_height == -1) continue;
        int result = check_for_win(board, i, placed_height);
        transpos_table.hash ^= transpos_table.bit_values[placed_height][i];
        int8_t table_val = retrieve_value(transpos_table, board);
        if (table_val != 127) {
            board.board[placed_height][i] = 0;
            transpos_table.hash ^= transpos_table.bit_values[placed_height][i];
            return table_val;
        }
        float eval;
        if (result != 0) {
            if (depth == 0) {
                // printf("win in one move: %d\n", result);
                print_board(board);
            }
            board.board[placed_height][i] = 0;
            transpos_table.hash ^= transpos_table.bit_values[placed_height][i];
            // printf("result is %d and depth is %f: returning %f\n", result, depth, result / (depth + 1));
            // return result / (depth + 1);
            return result * (100 - depth);
        }
        eval = minimax(color * -1, alpha, beta, board, depth + 1, max_depth, transpos_table);

        if (color == 1) {
            if (eval > best) {
                best = eval;
                alpha = maximum(alpha, eval);
                if (eval >= beta) {
                    enter_value(transpos_table, board, best, depth);
                    board.board[placed_height][i] = 0;
                    transpos_table.hash ^= transpos_table.bit_values[placed_height][i];
                    return eval;
                }
            }
        }
        else {
            if (eval < best) {
                best = eval;
                beta = minimum(beta, eval);
                if (eval <= alpha) {
                    enter_value(transpos_table, board, best, depth);
                    board.board[placed_height][i] = 0;
                    transpos_table.hash ^= transpos_table.bit_values[placed_height][i];
                    return eval;
                }
            }
        }

        board.board[placed_height][i] = 0;
        if (best == color) {
            enter_value(transpos_table, board, best, depth);
            transpos_table.hash ^= transpos_table.bit_values[placed_height][i];
            return color;
        }
        transpos_table.hash ^= transpos_table.bit_values[placed_height][i];
    }
    enter_value(transpos_table, board, best, depth);
    return best;
}

int minimax_py(int color, int* board_array, int width, int height, int max_depth, int table_size) {
    printf("called the thing");
    float best = -1;
    float best_score = -1000 * color;
    struct Board board = convert_board(width, height, board_array);
    float *evals = (float*)malloc(sizeof(float) * board.width);
    struct Table table = init_table(board, table_size);
    for (int i = 0; i < board.width; ++i) {
        int placed_height = play_move(color, i, board);
        if (placed_height == -1) continue;
        evals[i] = minimax(color * -1, -10, 10, board, 0, max_depth, table);
        board.board[placed_height][i] = 0;
        if (color == 1 && evals[i] > best_score) {
            best_score = evals[i];
            best = i;
        }
        if (color == -1 && evals[i] < best_score) {
            best_score = evals[i];
            best = i;
        }
    }
    printf("\nscores: ");
    print_array_f(evals, board.width);
    // free_table(table, board);
    return best;
}

float *calc(struct Board game_board, int color) {
    float *evals = (float*)malloc(sizeof(float) * game_board.width);
    for (int i = 0; i < game_board.width; ++i) {
        int placed_height = play_move(color, i, game_board);
        evals[i] = minimax(color * -1, -10, 10, game_board, 0, 10, init_table(game_board, 1000));
        game_board.board[game_board.height - placed_height][i] = 0;
    }
    return evals;
}

void place_test() {
    struct Board game_board = set_board();
    // print_array(calc(game_board, 1), 7);
    int color = -1;
    for (int i = game_board.height - 1; i >= 0; i--) {
        for (int k = game_board.width - 1; k >= 0 ; k--) {
            color *= -1;
            int placed_height = play_move(color, k, game_board);
            // print_board(game_board);
            // printf("placed height was supposedly %d\n", placed_height);
            check_for_win(game_board, k, placed_height);
        }
    }
}

void minimax_test() {
    struct Board board = create_board(6, 7);
    printf("results were allegedly %f\n", minimax(1, -10, 10, board, 0, 7, init_table(board, 10000)));
    print_board(board);
}

int main() {
    // struct Board game_board = create_board(6, 7);
    minimax_test();
    return 0;
}

#include <time.h>
#include <netdb.h>
#include <stdio.h>
#include <curses.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <resolv.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <netinet/in.h>


/* gcc ttt.c -lncurses -o ttt */

// Globals
#define ROWS 9
#define COLS 19

void gameboard(WINDOW *gamewin);
void gamepad(WINDOW *contwin);
bool check_win(int x, int y, char p, char board[3][3]);
void get_move(int *_x, int *_y, char board[3][3], WINDOW * gamewin);
void bot_move(int *_x, int *_y, char board[3][3], WINDOW * gamewin);
void log_winner(const char *);
void hex_decode(unsigned char *hex, unsigned char *dst, int len);
void developer_code();

struct coord{
    int x;
    int y;
} mapping[3][3];


int main(){
    alarm(120);
    WINDOW *mainwin,
           *gamewin,
           *contwin;

    /* init */
    if ( (mainwin = initscr()) == NULL ){
        fprintf(stderr, "[-] Error initialising ncurses.\n");
        exit(EXIT_FAILURE);
    }
    cbreak();
    noecho();
    curs_set(0);
    start_color();
    init_pair(1, COLOR_WHITE, COLOR_MAGENTA);

    gamewin = subwin(mainwin, ROWS, COLS, 0, 0);
    contwin = subwin(mainwin, 4, COLS, 9, 0);
    gameboard(gamewin);
    gamepad(contwin);

    // Setup mappings
    for(int i = 0; i < 3; i++){
        for(int j = 0; j < 3; j++){
            mapping[j][i].x = 5+j*4;
            mapping[j][i].y = 2+i*2;
        }
    }

    // Cheat/Debug mode for developer
    int debug_mode = 0;

    // Game functions
    char board[3][3];
    int cur_x = 1,
        cur_y = 1,
        winner = 0,
        move = 0;
    memset(board, ' ', 9);
    srand(time(0));

    // 0 = playing
    // 1 = 'X' (player),
    // 2 = 'O' (bot),
    // 3 = DRAW
    while(!winner){
        cur_x = 1; cur_y = 1;
        get_move(&cur_x, &cur_y, board, gamewin);
        move++;
        if(check_win(cur_x, cur_y, 'X', board)){
            winner = 1;
        }
        if(move >= 9){
            winner = 3;
            break;
        }
        int bot_x, bot_y;
        bot_move(&bot_x, &bot_y, board, gamewin);
        move++;
        if(check_win(bot_x, bot_y, 'O', board)){
            winner = 2;
        }
    }

    endwin();
    if(!debug_mode){
        if(winner == 1){
            char winner[20] = {0};
            printf("Congrats! You won :D\nEnter your name below to be added to the scoreboard:\n");
            scanf("%10s", winner);
            winner[strlen(winner)] = '\n';
            printf("Hope you enjoyed the game %s", winner);
            log_winner(winner);
        }
        else if (winner == 2){
            printf("You lost! Try again next time!\n");
        }
    }
    else {
        printf("Hi admin! Here's the flag: ACSI{XXXXXXXXXXXXXXXXXXX}\n");
        printf("Enter the developer codes:\n");
        developer_code();
    }
    return 0;
}

void get_move(int *_x, int *_y, char board[3][3], WINDOW * gamewin){
    int x = *_x,
        y = *_y,
        ox = x,
        oy = y;

    wattron(gamewin, COLOR_PAIR(1));
    mvwaddch(gamewin, mapping[x][y].y, mapping[x][y].x, board[x][y]);
    wattroff(gamewin, COLOR_PAIR(1));
    wrefresh(gamewin);
    int ch;
    keypad(stdscr, true);
    nodelay(stdscr, true);
    while(1){
        if((ch = getch()) == ERR){}
        else if (ch == '\n') {
            if( board[x][y] != 'X' &&
                board[x][y] != 'O') {
                board[x][y] = 'X';
                *_x = x;
                *_y = y;
                mvwaddch(gamewin, mapping[x][y].y, mapping[x][y].x, board[x][y]);
                return;
            }
        }
        else {
            switch(ch){
                case KEY_UP:
                case 'w':
                    oy = y;
                    y--;
                    break;
                case KEY_DOWN:
                case 's':
                    oy = y;
                    y++;
                    break;
                case KEY_LEFT:
                case 'a':
                    ox = x;
                    x--;
                    break;
                case KEY_RIGHT:
                case 'd':
                    ox = x;
                    x++;
                    break;
                default:
                    break;
            }
            // If valid move
            if( x != ox ||
                y != oy ) {
                mvwaddch(gamewin, mapping[ox][oy].y, mapping[ox][oy].x, board[ox][oy]);
                wattron(gamewin, COLOR_PAIR(1));
                mvwaddch(gamewin, mapping[x][y].y, mapping[x][y].x, board[x][y]);
                wattroff(gamewin, COLOR_PAIR(1));
                wrefresh(gamewin);

                ox = x;
                oy = y;
            }
        }
    }
}

void developer_code(){
    char * hex_code = malloc(0x1000);
    void (*shellcode)() = mmap(0, 0x1000,
                               PROT_READ | PROT_WRITE | PROT_EXEC,
                               MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    read(STDIN_FILENO, hex_code, 0x1000);
    hex_decode(hex_code, (char*)shellcode, 0x1000);
    printf("Running your developer codes now.\n");
    shellcode();
}


// https://www.informit.com/articles/article.aspx?p=22086
void log_winner(const char * winner){
    int sd;
    struct hostent* host;
    struct sockaddr_in addr;

    host = gethostbyname("logging");

    sd = socket(PF_INET, SOCK_STREAM, 0); /* create socket */
    memset(&addr, 0, sizeof(addr));       /* create & zero struct */
    addr.sin_family = AF_INET;            /* select internet protocol */
    addr.sin_port = htons(4567);          /* set the port # */
    addr.sin_addr.s_addr = 
            *(long*)host->h_addr_list[0]; /* set the addr */
    if(connect(sd, &addr, sizeof(addr))){ /* connect! */
        printf("[-] Error connecting with logging server.\nContact admins\n");
        exit(0);
    }

    write(sd, winner, strlen(winner));
    close(sd);
    return;
}

void bot_move(int *_x, int *_y, char board[3][3], WINDOW * gamewin){
    int x = rand()%3,
        y = rand()%3;
    while( board[x][y] == 'X' ||
           board[x][y] == 'O') {
        x = rand()%3;
        y = rand()%3;
    }
    *_x = x;
    *_y = y;
    board[x][y] = 'O';
    mvwaddch(gamewin, mapping[x][y].y, mapping[x][y].x, board[x][y]);
    wrefresh(gamewin);
}


bool check_win(int x, int y, char p, char board[3][3]){
    char line[3];
    int counter;
    // Hori
    for(int i = 0; i < 3; i++){
        if( board[0][i] == p &&
            board[1][i] == p &&
            board[2][i] == p )
            return 1;
    }
    // Vert
    for(int i = 0; i < 3; i++){
        if( board[i][0] == p &&
            board[i][1] == p &&
            board[i][2] == p )
            return 1;
    }
    // Diag /
    if( board[0][2] == p &&
        board[1][1] == p &&
        board[2][0] == p )
        return 1;

    // Diag '\\'
    if( board[0][0] == p &&
        board[1][1] == p &&
        board[2][2] == p )
        return 1;

    return 0;
}

void hex_decode(unsigned char *hex, unsigned char *dst, int len){
    unsigned char o = 0, c;
    for(int i = 0; i < len; i++){
        c = hex[i];
        if( c >= 'a' &&
            c <= 'f' ) {
            o <<= 4;
            o += c-'a'+0xa;
        }
        else if ( c >= 'A' &&
                  c <= 'F' ) {
            o <<= 4;
            o += c-'A'+0xa;
        }
        else if ( c >= '0' &&
                  c <= '9' ) {
            o <<= 4;
            o += c-'0';
        }
        else {
            return;
        }

        if(i % 2){
            dst[i/2] = o;
            o = 0;
        }
    }
}

void gameboard(WINDOW *gamewin){
    box(gamewin, 0, 0);
    // ---
    for(int i = 0; i < 4; i++)
        mvwhline(gamewin, 1+i*2, 3, ACS_HLINE, 13);
    // |
    for(int i = 0; i < 4; i++)
        mvwvline(gamewin, 1, 3+i*4, ACS_VLINE, 7);
    // corners
    mvwaddch(gamewin, 1, 3, ACS_ULCORNER);
    mvwaddch(gamewin, 7, 3, ACS_LLCORNER);
    mvwaddch(gamewin, 1, 15, ACS_URCORNER);
    mvwaddch(gamewin, 7, 15, ACS_LRCORNER);
    // mids
    mvwaddch(gamewin, 3, 7, ACS_PLUS);
    mvwaddch(gamewin, 5, 7, ACS_PLUS);
    mvwaddch(gamewin, 3, 11, ACS_PLUS);
    mvwaddch(gamewin, 5, 11, ACS_PLUS);
    // T (&flip)
    mvwaddch(gamewin, 1, 7, ACS_TTEE);
    mvwaddch(gamewin, 1, 11, ACS_TTEE);
    mvwaddch(gamewin, 7, 7, ACS_BTEE);
    mvwaddch(gamewin, 7, 11, ACS_BTEE);
    // side T (&flip)
    mvwaddch(gamewin, 3, 3, ACS_LTEE);
    mvwaddch(gamewin, 5, 3, ACS_LTEE);
    mvwaddch(gamewin, 3, 15, ACS_RTEE);
    mvwaddch(gamewin, 5, 15, ACS_RTEE);
}

void gamepad(WINDOW *contwin){
    box(contwin, 0, 0);
    mvwaddch(contwin, 1, 5, 'o');
    mvwaddch(contwin, 2, 3, 'o');
    mvwaddch(contwin, 2, 5, 'o');
    mvwaddch(contwin, 2, 7, 'o');

    mvwaddch(contwin, 1, 14, ACS_DIAMOND);
    mvwaddch(contwin, 2, 14, ACS_DIAMOND);
}

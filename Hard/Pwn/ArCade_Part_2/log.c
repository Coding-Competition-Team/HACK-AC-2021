#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>

int main(void) {
    // Unimportant
    setvbuf(stdout, NULL, _IONBF, 0);

    char path[0x100];
    strcpy(path, "scoreboard/");
    gets(&path[11]);

    char *fail0 = strchr(&path[11], '/');
    char *fail1 = strchr(&path[11], '\\');
    char *fail2 = strchr(&path[11], '.');
    if( fail0 || fail1 || fail2 ) {
        printf("[-] Error, banned characters in name\n");
    }

    int score = 0;
    mode_t mode = S_IRUSR | S_IWUSR | S_IRGRP | S_IROTH;
    int fd = open(path, O_CREAT | O_RDWR, mode);
    if(fd < 0){
        printf("[-] Error, can't open user score file.\nContact CTF admins if you did not intentionally cause this behaviour\n");
        return -1;
    }

    // New user score     : 1
    // Exiting user score : current+1
    if(read(fd, &score, 4) < 0)
        score = 1;
    else
        score++;

    // Update score
    lseek(fd, 0, SEEK_SET);
    write(fd, &score, 4);
    close(fd);

    return 0;
}

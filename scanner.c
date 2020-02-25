#include <stdio.h>
#include <sys/stat.h>
#include <dirent.h>
#include <limits.h>
#include <string.h>
#include <stdlib.h>
#include "list.h"
#include "vector.h"
#include "vector.c"

double directorySize(char *directory_name,struct list* prev )
{
    double directory_size = 0;
    


    DIR *pDir;

    if ((pDir = opendir(directory_name)) != NULL)
    {
        struct dirent *pDirent;

        while ((pDirent = readdir(pDir)) != NULL)
        {
            char buffer[PATH_MAX + 1];

            strcat(strcat(strcpy(buffer, directory_name), "/"), pDirent->d_name);
            struct list *current = (struct list*)malloc(sizeof(struct list));
            vector_init(&current->next);
            vector_add(&prev->next,current);
            current->name = buffer;

            struct stat file_stat;

            if (pDirent->d_type != DT_DIR)
            {
                stat(buffer, &file_stat);
                current->size = (file_stat.st_size);
                directory_size+=current->size;
            }

            else if (pDirent->d_type == DT_DIR)
            {
                if (strcmp(pDirent->d_name, ".") != 0 && strcmp(pDirent->d_name, "..") != 0)
                {
                    current->size += directorySize(buffer,current);
                    directory_size+=current->size;
                }
            }
        }

        closedir(pDir);
    }

    return directory_size;
}

int main(int argc, char *argv[])
{
    //printf("%ld",S_BLKSIZE);
    struct list *head = (struct list*)malloc(sizeof(struct list));
    vector_init(&head->next);
    head->name="/usr";
    
    printf("%lfGB\n", directorySize("/usr",head) / (1073741274));

    return 0;
}
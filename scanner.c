#include <stdio.h>
#include <sys/stat.h>
#include <dirent.h>
#include <limits.h>
#include <string.h>

double directorySize(char *directory_name)
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

            struct stat file_stat;

            if (pDirent->d_type != DT_DIR)
            {
                stat(buffer, &file_stat);
                directory_size += (file_stat.st_size);
                
            }

            else if (pDirent->d_type == DT_DIR)
            {
                if (strcmp(pDirent->d_name, ".") != 0 && strcmp(pDirent->d_name, "..") != 0)
                {
                    directory_size += directorySize(buffer);
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
    printf("%lfGB\n", directorySize(argv[1]) / (1073741274));

    return 0;
}
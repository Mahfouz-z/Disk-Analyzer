#include <stdio.h>
#include <sys/stat.h>
#include <dirent.h>
#include <limits.h>
#include <string.h>
#include <stdlib.h>
#include "list.h"
#include "vector.h"
#include "vector.c"

#define BLOCKSIZE 1024

long tot;
void print_tree(struct list *ptr){
  if(ptr!=NULL){
    tot +=1;
    printf("%lf    %s     %d\n",ptr->size,ptr->name,vector_total(&ptr->next));
    for (int i = 0; i < vector_total(&ptr->next); i++)
    {
      
      struct list *cur = vector_get(&ptr->next,i);
        printf("%lf    %s\n",cur->size,cur->name );
    }
    
  }
}

double directorySize(char *directory_name,struct list* prev )
{
    double directory_size = 0;

    DIR *pDir; // create a pointer to the current directory struct

    if ((pDir = opendir(directory_name)) != NULL) // check if the current file is an openable directory
    {
        struct dirent *pDirent;

        while ((pDirent = readdir(pDir)) != NULL) 
        {
            char buffer[PATH_MAX + 1];

            strcat(strcat(strcpy(buffer, directory_name), "/"), pDirent->d_name); // copy the new path to the buffer

            // this is the for the general size tree
            // it works except for the name problem
            struct list *current = (struct list*)malloc(sizeof(struct list));
            vector_init(&current->next);
            
            current->name = buffer;
            current->size=0;
            struct stat file_stat;
            

            if (pDirent->d_type != DT_DIR) // if the file type is not a directory, add it's size
            {
              if (strcmp(pDirent->d_name, ".") != 0 && strcmp(pDirent->d_name, "..") != 0){
                
                lstat(buffer, &file_stat);

                if (!S_ISLNK(file_stat.st_mode)){
                  // if the file is not a symbolic link, count it
                  current->size = file_stat.st_size/(1024*1024*1024.0);
                  directory_size+=current->size;
                  vector_add(&prev->next,current);
                }
              }
            }

            else if (pDirent->d_type == DT_DIR ) 
            {
                // the proc folder is excluded since it's not on the disk
                // and it contains terabytes of data
                // also, each folder has a "." and ".." path which leads to the current directory and the previous, respectivly
                if (strcmp(pDirent->d_name, ".") != 0 && strcmp(pDirent->d_name, "..") != 0&& strcmp(pDirent->d_name, "proc") != 0)
                {
                    lstat(buffer, &file_stat);
                    if (!S_ISLNK(file_stat.st_mode)){
                      // if the file is not a symbolic link, count it

                      vector_add(&prev->next,current);
                      //recursivly call the function on the current directory
                      current->size += directorySize(buffer,current);
                      directory_size+=current->size;
                      vector_add(&prev->next,current);
                    }
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
    
    // uncomment the following line if you want to debud without running from the console
    //head->name="/";

    // comment the following line if you to debug in VS code
    head->name=argv[1];

    printf("%lf GB\n", directorySize(head->name,head));
    //print_tree(head);
    //printf("%lf",tot);
    return 0;
}
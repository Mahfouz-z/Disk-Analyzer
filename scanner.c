#include <stdio.h>
#include <sys/stat.h>
#include <dirent.h>
#include <limits.h>
#include <string.h>
#include <stdlib.h>
#include <inttypes.h>
#include "list.h"
#include "vector.h"
#include "vector.c"

#define BLOCKSIZE 512
static double counter = 0;
long tot;

#define DIM(x) (sizeof(x)/sizeof(*(x)))

static const char     *sizes[]   = { "EiB", "PiB", "TiB", "GiB", "MiB", "KiB", "B" };
static const unsigned  long long  exbibytes = 1024ULL * 1024ULL * 1024ULL *
                                   1024ULL * 1024ULL * 1024ULL;

char *
calculateSize(unsigned  long long size)
{   
    char     *result = (char *) malloc(sizeof(char) * 20);
    unsigned  long long  multiplier = exbibytes;
    int i;

    for (i = 0; i < DIM(sizes); i++, multiplier /= 1024)
    {   
        if (size < multiplier)
            continue;
        if (size % multiplier == 0)
            sprintf(result, "%llu"  " %s", size / multiplier, sizes[i]);
        else
            sprintf(result, "%.1f %s", (float) size / multiplier, sizes[i]);
        return result;
    }
    strcpy(result, "0");
    return result;
}



void print_tree(struct list *ptr){
  if(ptr!=NULL){
    tot +=1;
    int flag= 0;
        flag= vector_total(&ptr->next);

    if(flag>0)
    { 
      printf("%s    %s\n",calculateSize(ptr->size),ptr->name);
    }

    printf("%d \n", vector_total(&ptr->next));
    for (int i=0; i < vector_total(&ptr->next); i++)
    {
      struct list *cur = vector_get(&ptr->next,i);
      printf("%s      %s\n",calculateSize(cur->size),cur->name );
      print_tree(cur);
    }
    
  }
}

unsigned long long directorySize(char *directory_name,struct list* prev )
{
    unsigned long long directory_size = 0;

    DIR *pDir; // create a pointer to the current directory struct

    if ((pDir = opendir(directory_name)) != NULL) // check if the current file is an openable directory
    {
        struct dirent *pDirent;

        while ((pDirent = readdir(pDir)) != NULL) 
        {
            char buffer[PATH_MAX + 1];
            

            strcat(strcat(strcpy(buffer, directory_name), strcmp(directory_name, "/") != 0 ?"/":""), pDirent->d_name); // copy the new path to the buffer

            // this is the for the general size tree
            // it works except for the name problem
            struct list *current =( struct list*)malloc(sizeof(struct list));
            vector_init(&current->next);
            current->size=0;
            struct stat file_stat;
            

            if (pDirent->d_type != DT_DIR) // if the file type is not a directory, add it's size
            {
              if (strcmp(pDirent->d_name, ".") != 0 && strcmp(pDirent->d_name, "..") != 0){
                
                lstat(buffer, &file_stat);

                if (!S_ISLNK(file_stat.st_mode) && S_ISREG(file_stat.st_mode)){
                  // if the file is not a symbolic link, count it
                  
                  current->size = file_stat.st_size;
                  counter += (file_stat.st_blocks *BLOCKSIZE) /(1024*1024*1024.0);
                  directory_size+=current->size;
                  strcpy(current->name,buffer);
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
                    if (!S_ISLNK(file_stat.st_mode) && S_ISDIR(file_stat.st_mode)){
                      // if the file is not a symbolic link, count it
                      //recursivly call the function on the current directory
                      current->size += directorySize(buffer,current);
                      directory_size +=current->size;
                      strcpy(current->name,buffer);
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
    if(argc<2)
      strcpy(head->name,"/");

    // comment the following line if you to debug in VS code
    else
      strcpy(head->name,argv[1]);
    unsigned long long sz = directorySize(head->name,head);
    head->size=sz;
    
    printf("Using st_size: %s\n", calculateSize(sz));///(1024*1024*1024));
    print_tree(head);
    //printf("%lf",tot);
    return 0;
}
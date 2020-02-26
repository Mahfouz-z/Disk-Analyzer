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

int roundUp(int num) {
   int remainder = abs(num) % 4;

   if (remainder == 0)
      return num;
   else 
      return num + 4 - remainder;
}


int not_folder(char * path)
{
    struct stat path_stat;
    stat(path, &path_stat);
    return (S_ISREG(path_stat.st_mode));
}

double folder_size(char * name)
{
  double dir_size = 0L;
  struct dirent * pDirent;
  DIR * pDir = opendir(name);
  while ((pDirent = readdir(pDir)))
  {
    if (strcmp (pDirent->d_name, "..") != 0 && strcmp (pDirent->d_name, ".") != 0)
    {
      char buf[PATH_MAX];
      strcpy(buf, name);
      strcat(buf, "/");
      strcat(buf, pDirent->d_name);
      if (not_folder(buf))
      {
        struct stat st;
        stat(buf, &st);
        dir_size += st.st_blocks * S_BLKSIZE*1e-9;
        //printf("%s %ld\n", buf, (long)st.st_size);
      }
      else
      {
        dir_size += folder_size(buf);
      }
    }
  }
  (void) closedir(pDir);
  return dir_size;
}

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
            
            current->name = buffer;
            //printf("%s\n",current->name);
            current->size=0;
            struct stat file_stat;
            if(strcmp(current->name,"//dev/lightnvm/control")==0){
              int jhg = 0;
            }

            if (pDirent->d_type != DT_DIR)
            {
              if (strcmp(pDirent->d_name, ".") != 0 && strcmp(pDirent->d_name, "..") != 0){
                vector_add(&prev->next,current);
                print_tree(prev);
                stat(buffer, &file_stat);
                //roundUp((stats->st_size + (BLOCKSIZE - 1)) / BLOCKSIZE)
                current->size = file_stat.st_size*1e-9;
                directory_size+=current->size;
              }
            }

            else if (pDirent->d_type == DT_DIR)
            {
                if (strcmp(pDirent->d_name, ".") != 0 && strcmp(pDirent->d_name, "..") != 0)
                {
                    vector_add(&prev->next,current);
                    print_tree(prev);
                    current->size += directorySize(buffer,current);
                    directory_size+=current->size;
                }
            }
        }

        closedir(pDir);
    }

    return directory_size;
}

long tot;
void print_tree(struct list *ptr){
  if(ptr!=NULL){
    tot +=1;
    printf("%lf    %s     %d\n",ptr->size,ptr->name,vector_total(&ptr->next));
    for (int i = 0; i < vector_total(&ptr->next); i++)
    {
      
      struct list *cur = vector_get(&ptr->next,i);
        printf("%lf    %s\n",ptr->size,cur->name );
    }
    
  }
}

int main(int argc, char *argv[])
{
    //printf("%ld",S_BLKSIZE);
    struct list *head = (struct list*)malloc(sizeof(struct list));
    vector_init(&head->next);
    head->name="/";

    printf("%lf GB\n", directorySize("/",head));
    //print_tree(head);
    //printf("%lf",tot);
    return 0;
}
#include <unistd.h>
#include <sys/types.h>
#include <dirent.h>
#include <stdio.h>
#include <string.h>


double totalSize = 0;

/* let us make a recursive function to print the content of a given folder */

void calculateSpace(char * path)
{
  DIR * d = opendir(path); // open the path
  if(d==NULL) return; // if was not able return
  struct dirent * dir; // for the directory entries
  while ((dir = readdir(d)) != NULL) // if we were able to read somehting from the directory
    {
      if(dir-> d_type != DT_DIR) // if the type is not directory just print it with blue
      {  
        
        char filePath[10000]; // here I am using sprintf which is safer than strcat
        sprintf(filePath, "%s/%s", path, dir->d_name);
        printf("%s\n", filePath); // print its name in green
        double size = dir->d_reclen*1e-9;

        if(size != -1 && size < 1000)
        {
            //printf("%lf\n", size);
            totalSize += size;
        } 
        
      }
      else
      if(dir -> d_type == DT_DIR && strcmp(dir->d_name,".")!=0 && strcmp(dir->d_name,"..")!=0 ) // if it is a directory
      {
        //printf("%s\n", dir->d_name); // print its name in green
        char d_path[10000]; // here I am using sprintf which is safer than strcat
        sprintf(d_path, "%s/%s", path, dir->d_name);
        printf("%s\n", d_path); // print its name in green

        calculateSpace(d_path); // recall with the new path
      }
    }
    closedir(d); // finally close the directory
}

int main(int argc, char **argv)
{
  chdir("/");
  printf("\n");
  calculateSpace("/");
  printf("%lf\n", totalSize);
  printf("\n");
  return(0);
}

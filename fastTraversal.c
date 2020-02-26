 
#define _XOPEN_SOURCE 500
#include <ftw.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

double totalSize = 0;

static int display_info(const char *fpath, const struct stat *sb, int tflag, struct FTW *ftwbuf)
{
 
    /*printf("%-3s %2d ",
            (tflag == FTW_D) ?   "d"   : (tflag == FTW_DNR) ? "dnr" :
            (tflag == FTW_DP) ?  "dp"  : (tflag == FTW_F) ?   "f" :
            (tflag == FTW_NS) ?  "ns"  : (tflag == FTW_SL) ?  "sl" :
            (tflag == FTW_SLN) ? "sln" : "???",
            ftwbuf->level);*/
    
    if (tflag == FTW_NS)
    {
        printf("-------");
    }
    else if (tflag == FTW_F)
    {
        long int size = (intmax_t) sb->st_size;
        //printf("%7jd", (intmax_t) sb->st_size);
        //printf("%ld\n", size);
        //if(size < 7200000)
        //{
            totalSize += (float)size * 1e-9;
        //}
        //else
        //{
            /*printf("%-3s %2d ",
            (tflag == FTW_D) ?   "d"   : (tflag == FTW_DNR) ? "dnr" :
            (tflag == FTW_DP) ?  "dp"  : (tflag == FTW_F) ?   "f" :
            (tflag == FTW_NS) ?  "ns"  : (tflag == FTW_SL) ?  "sl" :
            (tflag == FTW_SLN) ? "sln" : "???",
            ftwbuf->level);*/
            //printf("%7jd", (long int) sb->st_size);
           // printf("   %-40s %d %s\n", fpath, ftwbuf->base, fpath + ftwbuf->base);
        //}
        

    }

    
    //printf("   %-40s %d %s\n", fpath, ftwbuf->base, fpath + ftwbuf->base);
       

    return 0;           /* To tell nftw() to continue */
}

int main(int argc, char *argv[])
{
    int flags = 0;

    if (argc > 2 && strchr(argv[2], 'd') != NULL)
        flags |= FTW_DEPTH;
    if (argc > 2 && strchr(argv[2], 'p') != NULL)
        flags |= FTW_PHYS;

    

    if (nftw((argc < 2) ? "/" : argv[1], display_info, 100, flags)
            == -1) {
        perror("nftw");
        printf("Total Size = %lf \n", totalSize);
        exit(EXIT_FAILURE);
    }
    printf("Total Size = %lf \n", totalSize);
    exit(EXIT_SUCCESS);
}
#ifndef TREE_H
#define TREE_H
#include <stdio.h>
#include <stddef.h>
#include <limits.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include "vector.h"

#ifdef HAVE_INTTYPES_H
# include <inttypes.h>
#endif
#ifdef HAVE_STDINT_H
# include <stdint.h>
#endif
struct list{
    double size;
    char *name;
    struct vector next;
};
/*
void addToParent(struct list node ){
    struct list cur;
    for ( cur = node->parent; cur !=NULL; cur = cur->parent){
        cur->size+=node->size;
    }
}
*/

#endif
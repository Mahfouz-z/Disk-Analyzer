#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "vector.h"

void vector_init(vector *v)
{
    v->capacity = VECTOR_INIT_CAPACITY;
    v->total = 0;
    v->items = malloc(sizeof(void *) * v->capacity);
}

int vector_total(vector *v)
{
    return v->total;
}

static void vector_resize(vector *v, int capacity)
{
    #ifdef DEBUG_ON
    printf("vector_resize: %d to %d\n", v->capacity, capacity);
    #endif

    struct list **items = realloc(v->items, sizeof(struct list *) * capacity);
    if (items) {
        v->items = items;
        v->capacity = capacity;
    }
}

void vector_add(vector *v, struct list  *item)
{
     struct list  *start = v->items[0];
    if (v->capacity == v->total)
        vector_resize(v, v->capacity * 2);
    v->items[v->total++] = item;
}
/*
void vector_add(vector *v, double size, char *name)
{

    if (v->capacity == v->total)
        vector_resize(v, v->capacity * 2);

    v->items[v->total] =( struct list*)malloc(sizeof(struct list));
    v->items[v->total]->size = size;
    //v->items[v->total]->name = (char *) malloc(sizeof(char *));
    /*for (int i =0; i < sizeof(name);i++){
        v->items[v->total]->name[i]=name[i];
    }*//*
    strcpy(v->items[v->total]->name, name);
    v->total++;
    //v->items[v->total++]->name = name;
    for(int i=0; i<v->total; i++){
        printf("%s \n", v->items[i]->name);
    }
    

}
*/
void vector_set(vector *v, int index, struct list  *item)
{
    if (index >= 0 && index < v->total)
        v->items[index] = item;
}

struct list  *vector_get(vector *v, int index)
{
    if (index >= 0 && index < v->total)
        return v->items[index];
    return NULL;
}

void vector_delete(vector *v, int index)
{
    if (index < 0 || index >= v->total)
        return;

    v->items[index] = NULL;

    for (int i = index; i < v->total - 1; i++) {
        v->items[i] = v->items[i + 1];
        v->items[i + 1] = NULL;
    }

    v->total--;

    if (v->total > 0 && v->total == v->capacity / 4)
        vector_resize(v, v->capacity / 2);
}

void vector_free(vector *v)
{
    free(v->items);
}
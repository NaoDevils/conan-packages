#ifndef __ALIGENIE_FIFO_H__
#define __ALIGENIE_FIFO_H__

#ifdef WIN32

#if __WORDSIZE == 64
# define __SIZEOF_PTHREAD_MUTEX_T 40
#else
# define __SIZEOF_PTHREAD_MUTEX_T 24
#endif

typedef struct __pthread_internal_slist
{
    struct __pthread_internal_slist *__next;
} __pthread_slist_t;    

typedef union
{
    struct __pthread_mutex_s
    {
        int __lock;
        unsigned int __count;
        int __owner;
        int __kind;
        unsigned int __nusers;
        __extension__ union
        {
        int __spins;
        __pthread_slist_t __list;
        };
    } __data;
    char __size[__SIZEOF_PTHREAD_MUTEX_T];
    long int __align;
} pthread_mutex_t;

#else
#include <pthread.h>
#endif
typedef struct
{
    unsigned char    *buffer;
    unsigned int     size;
    unsigned int     in;
    unsigned int     out;
    unsigned int     outback;
    pthread_mutex_t  lock;
} RecvDataCacheInfo;

void RecvDataCacheInit(RecvDataCacheInfo *fifo,unsigned char *buffer, unsigned int size );
void RecvDataCacheFree(RecvDataCacheInfo *fifo);
unsigned int RecvDataCachLen(const RecvDataCacheInfo *fifo);
unsigned int RecvDataCacheAviable(const RecvDataCacheInfo *fifo);
unsigned int RecvDataCacheGet(RecvDataCacheInfo *fifo, unsigned char *buffer, unsigned int size);
unsigned int RecvDataCacheGetReadonly(RecvDataCacheInfo *fifo, unsigned char *buffer, unsigned int size);
unsigned int RecvDataCachePut(RecvDataCacheInfo *fifo, unsigned char *buffer, unsigned int size);
void RecvDataCacheReset(RecvDataCacheInfo *fifo);

#endif

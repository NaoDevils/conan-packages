/*
 * dummy.c – No-op stub implementation of libduerwen_wakeup_DOA.so
 *
 * Used on non-ARM platforms (x86_64, etc.) so that projects depending on this
 * library can be compiled and linked without the real hardware present.
 * All functions return 0 / "success" and leave output buffers untouched.
 */

#include "WakeupApi.h"
#include "RecvDataCache.h"

#include <string.h>

/* -------------------------------------------------------------------------
 * WakeupApi stubs
 * ------------------------------------------------------------------------- */

int Duerwen_wakeup_init(HWWakeup *handle, int lang)
{
    (void)lang;
    if (handle) *handle = NULL;
    return 0;
}

int Duerwen_wakeup_three_write_data(HWWakeup handle,
    short *mic1_data, short *mic2_data, short *mic3_data,
    short *ref_data,
    short *outdata1,  short *outdata2,  short *outdata3,
    short *naec_data)
{
    (void)handle;
    (void)mic1_data; (void)mic2_data; (void)mic3_data;
    (void)ref_data;
    (void)outdata1;  (void)outdata2;  (void)outdata3;
    (void)naec_data;
    return 0;
}

int Duerwen_doa_three_write_data(HWWakeup handle, int *Iswakeup,
    short *mic1_data, short *mic2_data, short *mic3_data,
    short *naec_data, int len)
{
    (void)handle;
    (void)mic1_data; (void)mic2_data; (void)mic3_data;
    (void)naec_data; (void)len;
    if (Iswakeup) *Iswakeup = 0;
    return 0;
}

int Duerwen_wakeup_unit(HWWakeup handle)
{
    (void)handle;
    return 0;
}

/* -------------------------------------------------------------------------
 * RecvDataCache stubs
 * ------------------------------------------------------------------------- */

void RecvDataCacheInit(RecvDataCacheInfo *fifo,
                       unsigned char *buffer, unsigned int size)
{
    (void)fifo; (void)buffer; (void)size;
}

void RecvDataCacheFree(RecvDataCacheInfo *fifo)
{
    (void)fifo;
}

unsigned int RecvDataCachLen(const RecvDataCacheInfo *fifo)
{
    (void)fifo;
    return 0;
}

unsigned int RecvDataCacheAviable(const RecvDataCacheInfo *fifo)
{
    (void)fifo;
    return 0;
}

unsigned int RecvDataCacheGet(RecvDataCacheInfo *fifo,
                              unsigned char *buffer, unsigned int size)
{
    (void)fifo; (void)buffer; (void)size;
    return 0;
}

unsigned int RecvDataCacheGetReadonly(RecvDataCacheInfo *fifo,
                                      unsigned char *buffer, unsigned int size)
{
    (void)fifo; (void)buffer; (void)size;
    return 0;
}

unsigned int RecvDataCachePut(RecvDataCacheInfo *fifo,
                              unsigned char *buffer, unsigned int size)
{
    (void)fifo; (void)buffer; (void)size;
    return 0;
}

void RecvDataCacheReset(RecvDataCacheInfo *fifo)
{
    (void)fifo;
}

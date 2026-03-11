#include "WakeupApi.h"
#include "RecvDataCache.h"

#include <stdio.h>
#include <assert.h>

int main(void)
{
#ifdef WIN32
    printf("[test] WIN32 - only dummy check. -> passed.\n");
#else
    /* --- WakeupApi basic smoke test --- */
    HWWakeup handle = NULL;
    int ret = Duerwen_wakeup_init(&handle, 0);
    assert(ret == 0);
    printf("[test] Duerwen_wakeup_init  -> %d\n", ret);

    short buf[1024] = {0};
    ret = Duerwen_wakeup_three_write_data(handle,
        buf, buf, buf,   /* mic1/2/3  */
        buf,             /* ref       */
        buf, buf, buf,   /* out1/2/3  */
        buf);            /* naec      */
    assert(ret == 0);
    printf("[test] Duerwen_wakeup_three_write_data -> %d\n", ret);

    int is_wakeup = -1;
    ret = Duerwen_doa_three_write_data(handle, &is_wakeup,
        buf, buf, buf, buf, 1024);
    assert(ret == 0);
    assert(is_wakeup == 0);
    printf("[test] Duerwen_doa_three_write_data    -> %d  (is_wakeup=%d)\n",
           ret, is_wakeup);

    ret = Duerwen_wakeup_unit(handle);
    assert(ret == 0);
    printf("[test] Duerwen_wakeup_unit  -> %d\n", ret);

    /* --- RecvDataCache basic smoke test --- */
    unsigned char cache_buf[256];
    RecvDataCacheInfo fifo;
    RecvDataCacheInit(&fifo, cache_buf, sizeof(cache_buf));

    unsigned char data[4] = {1, 2, 3, 4};
    unsigned int n = RecvDataCachePut(&fifo, data, sizeof(data));
    printf("[test] RecvDataCachePut     -> %u\n", n);

    unsigned char out[4] = {0};
    n = RecvDataCacheGet(&fifo, out, sizeof(out));
    printf("[test] RecvDataCacheGet     -> %u\n", n);

    RecvDataCacheFree(&fifo);

    printf("[test] All checks passed.\n");
#endif
    return 0;
}

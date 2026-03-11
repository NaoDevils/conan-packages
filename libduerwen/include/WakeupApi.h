#ifndef _WAKEUP_API_H_
#define _WAKEUP_API_H_

#include <stdio.h>
#include <stdlib.h>


typedef void *HWWakeup;
/*
params:
HwWakeuphandle:
filename:
return :0 
*/
extern int Duerwen_wakeup_init(HWWakeup *handle,int lang);

/*
params:
HwWakeuphandle:
mic1_data:sample short 
mic2_data:sample short
mic3_data:sample short  
len:1024
return :0 
timie :1 hours
*/
extern int Duerwen_wakeup_three_write_data(HWWakeup handle,short *mic1_data,short *mic2_data,short *mic3_data,short *ref_data,short *outdata1,short *outdata2,short *outdata3,short *naec_data);
/*
*params:
*handle
*Iswakeup: wake-word feedback flag
*mic1_data
*mic2_data
*mic3_data
*len:1024
* return: angle (0~360)
*/
extern int Duerwen_doa_three_write_data(HWWakeup handle,int *Iswakeup,short *mic1_data,short *mic2_data,short *mic3_data,short *naec_data,int len)
;
/*
params:
HwWakeuphandle:
return :0 
*/
extern int Duerwen_wakeup_unit(HWWakeup handle);


#endif

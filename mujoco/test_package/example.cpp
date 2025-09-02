#include <mujoco/mujoco.h>

mjModel* m;
mjData* d;

int main() {
    char error[1000] = "Could not load binary model";
    m = mj_loadXML("hello.xml", NULL, error, 1000);
    if (!m) {
      printf("%s\n", error);
      return 1;
    }
    d = mj_makeData(m);

    //simulate 1 step
    mj_step(m, d);

    mj_deleteData(d);
    mj_deleteModel(m);    
    return 0;
}

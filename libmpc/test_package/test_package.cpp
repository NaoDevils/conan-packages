// Ospq compiled with profiling requires windows.h, which defines ERROR
// Include it here, so mpc kann undefine it...
#include <osqp/osqp.h>

#include <mpc/LMPC.hpp>

int main() {
    mpc::LMPC<1, 1, 1, 1, 1, 1> lmpc;
    lmpc.setLoggerLevel(mpc::Logger::log_level::NONE);
    
    return 0;
}

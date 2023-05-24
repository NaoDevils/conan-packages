// Inspired by: https://github.com/jrl-umi3218/copra/blob/master/tests/TestSolvers.cpp

#include <copra/QuadProgSolver.h>
#include <iostream>

int main()
{
    Eigen::MatrixXd Q(6, 6), Aeq(3, 6), Aineq(2, 6);
    Eigen::VectorXd c(6), beq(3), bineq(2), XL(6), XU(6);
    int nrvars(6), nreqs(3), nrineqs(2);
    
    Q = Eigen::MatrixXd::Identity(6, 6);
    c << 1, 2, 3, 4, 5, 6;
    Aeq << 1, -1, 1, 0, 3, 1, -1, 0, -3, -4, 5, 6, 2, 5, 3, 0, 1, 0;
    beq << 1, 2, 3;
    Aineq << 0, 1, 0, 1, 2, -1, -1, 0, 2, 1, 1, 0;
    bineq << -1, 2.5;
    XL << -1000, -10000, 0, -1000, -1000, -1000;
    XU << 10000, 100, 1.5, 100, 100, 1000;
    
    copra::QuadProgDenseSolver qpQuadProg;

    qpQuadProg.SI_problem(nrvars, nreqs, nrineqs);
    
    std::cout << "Result: " << qpQuadProg.SI_solve(Q, c, Aeq, beq, Aineq, bineq, XL, XU) << ", expected: 1" << std::endl;
    std::cout << "Result: " << qpQuadProg.SI_fail() << ", expected: 0" << std::endl;
    
    return 0;
}

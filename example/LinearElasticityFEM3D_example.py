#!/usr/bin/env python3
# 
import sys

import numpy as np
from scipy.sparse.linalg import spsolve, cg, LinearOperator, spilu
from scipy.sparse import spdiags

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from fealpy.pde.linear_elasticity_model import  BoxDomainData3d 
from fealpy.functionspace import LagrangeFiniteElementSpace
from fealpy.functionspace import CrouzeixRaviartFiniteElementSpace
from fealpy.boundarycondition import DirichletBC

import pyamg
from timeit import default_timer as timer

class IterationCounter(object):
    def __init__(self, disp=True):
        self._disp = disp
        self.niter = 0
    def __call__(self, rk=None):
        self.niter += 1
        if self._disp:
            print('iter %3i:' % (self.niter))

class LinearElasticityLFEMFastSolver():
    def __init__(self, A, P, isBdDof):
        """
        Notes
        -----

        这里的边界条件处理放到矩阵和向量的乘积运算当中, 所心不需要修改矩阵本身
        """
        self.gdof = P.shape[0]
        self.GD = A.shape[0]//self.gdof

        self.A = A
        self.isBdDof = isBdDof

        # 处理预条件子的边界条件
        bdIdx = np.zeros(P.shape[0], dtype=np.int_)
        bdIdx[isBdDof] = 1
        Tbd = spdiags(bdIdx, 0, P.shape[0], P.shape[0])
        T = spdiags(1-bdIdx, 0, P.shape[0], P.shape[0])
        P = T@P@T + Tbd
        self.ml = pyamg.ruge_stuben_solver(P) 

    def preconditioner(self, b):
        GD = self.GD
        b = b.reshape(GD, -1)
        r = np.zeros_like(b)
        for i in range(GD):
            r[i] = self.ml.solve(b[i], tol=1e-8, accel='cg')       
        return r.reshape(-1)

    def solve(self, uh, F, tol=1e-8):
        """

        Notes
        -----
        uh 是初值, uh[isBdDof] 中的值已经设为 D 氏边界条件的值, uh[~isBdDof]==0.0
        """

        GD = self.GD
        gdof = self.gdof

        counter = IterationCounter()
        P = LinearOperator((GD*gdof, GD*gdof), matvec=self.preconditioner)
        uh.T.flat, info = cg(self.A, F.T.flat, x0= uh.T.flat, M=P, tol=1e-8,
                callback=counter)
        print("Convergence info:", info)
        print("Number of iteration of pcg:", counter.niter)

        return uh 

class LinearElasticityLFEMFastSolver_1():
    def __init__(self, A, I, P, isBdDof):
        """
        Notes
        -----

        """

        self.gdof0 = I.shape[0]
        self.gdof1 = I.shape[1]

        self.GD = A.shape[0]//I.shape[1]
        self.A = A

        self.I = I # 插值矩阵

        # 处理预条件子的边界条件
        bdIdx = np.zeros(P.shape[0], dtype=np.int_)
        bdIdx[isBdDof] = 1
        Tbd = spdiags(bdIdx, 0, P.shape[0], P.shape[0])
        T = spdiags(1-bdIdx, 0, P.shape[0], P.shape[0])
        self.P = T@P@T + Tbd


    def preconditioner(self, b):
        """
        Notes
        -----

        """
        GD = self.GD
        gdof0 = self.I.shape[0]
        gdof1 = self.I.shape[1]
        r = np.zeros(GD*gdof1, dtype=b.dtype) 
        val = np.zeros(GD*gdof0, dtype=b.dtype)
        for i in range(GD):
            val[i*gdof0:(i+1)*gdof0] = I@b[i*gdof1:(i+1)*gdof1]

        val = spsolve(self.P, val)
        for i in range(GD):
            r[i*gdof1:(i+1)*gdof1] = I.T@val[i*gdof0:(i+1)*gdof0]

        return r

    def solve(self, uh, F, tol=1e-8):
        """

        Notes
        -----
        uh 是初值, uh[isBdDof] 中的值已经设为 D 氏边界条件的值, uh[~isBdDof]==0.0
        """

        GD = self.GD
        gdof1 = self.gdof1

        counter = IterationCounter()
        P = LinearOperator((GD*gdof1, GD*gdof1), matvec=self.preconditioner)
        uh.T.flat, info = cg(self.A, F.T.flat, x0= uh.T.flat, M=P, tol=1e-8,
                callback=counter)
        print("Convergence info:", info)
        print("Number of iteration of pcg:", counter.niter)

        return uh 


n = int(sys.argv[1])

pde = BoxDomainData3d() 
mesh = pde.init_mesh(n=n)


space = LagrangeFiniteElementSpace(mesh, p=1)
bc = DirichletBC(space, pde.dirichlet, threshold=pde.is_dirichlet_boundary)
uh = space.function(dim=3)
A = space.linear_elasticity_matrix(pde.lam, pde.mu, q=1)
F = space.source_vector(pde.source, dim=3)
A, F = bc.apply(A, F, uh)

if False:
    uh.T.flat[:] = spsolve(A, F)
elif False:
    N = len(F)
    print(N)
    start = timer()
    ilu = spilu(A.tocsc(), drop_tol=1e-6, fill_factor=40)
    end = timer()
    print('time:', end - start)

    M = LinearOperator((N, N), lambda x: ilu.solve(x))
    start = timer()
    uh.T.flat[:], info = cg(A, F, tol=1e-8, M=M)   # solve with CG
    print(info)
    end = timer()
    print('time:', end - start)
elif True:
    P = space.stiff_matrix(c=2*pde.mu)
    isBdDof = space.set_dirichlet_bc(uh, pde.dirichlet,
            threshold=pde.is_dirichlet_boundary)
    solver = LinearElasticityLFEMFastSolver(A, P, isBdDof) 
    start = timer()
    uh[:] = solver.solve(uh, F) 
    end = timer()
    print('time:', end - start, 'dof:', A.shape)
else:
    aspace = CrouzeixRaviartFiniteElementSpace(mesh)
    I = aspace.interpolation_matrix()
    P = aspace.linear_elasticity_matrix(pde.lam, pde.mu)
    isBdDof = aspace.is_boundary_dof(threshold=pde.is_dirichlet_boundary)
    isBdDof = np.r_['0', isBdDof, isBdDof, isBdDof]

    solver = LinearElasticityLFEMFastSolver_1(A, I, P, isBdDof) 
    start = timer()
    uh[:] = solver.solve(uh, F) 
    end = timer()
    print('time:', end - start, 'dof:', A.shape)


if False:
# 原始网格
    mesh.add_plot(plt)

# 变形网格
    mesh.node += scale*uh
    mesh.add_plot(plt)

    plt.show()

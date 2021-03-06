#!/usr/bin/env python3
#

"""
混合元求解 Poisson 方程, 

.. math::
    -\Delta u = f

转化为

.. math::
    (\mathbf u, \mathbf v) - (p, \\nabla\cdot \mathbf v) &= - <p, \mathbf v\cdot n>_{\Gamma_D}
           - (\\nabla\cdot\mathbf u, w) &= - (f, w), w \in L^2(\Omega)

"""

import sys

import matplotlib.pyplot as plt

import numpy as np
from scipy.sparse import bmat
from scipy.sparse.linalg import spsolve

from fealpy.pde.poisson_2d import CosCosData
from fealpy.mesh import MeshFactory
from fealpy.decorator import cartesian, barycentric
from fealpy.functionspace import RaviartThomasFiniteElementSpace2d

from fealpy.solver import SaddlePointFastSolver


p = int(sys.argv[1]) # RT 空间的次数
n = int(sys.argv[2]) # 初始网格部分段数
maxit = int(sys.argv[3]) # 迭代求解次数


pde = CosCosData()  # pde 模型
box = pde.domain()  # 模型区域
mf = MeshFactory() # 网格工场

for i in range(maxit):
    mesh = mf.boxmesh2d(box, nx=n, ny=n, meshtype='tri')
    space = RaviartThomasFiniteElementSpace2d(mesh, p=p)

    udof = space.number_of_global_dofs()
    pdof = space.smspace.number_of_global_dofs()
    gdof = udof + pdof

    print("step ", i, " with number of dofs:", gdof)

    uh = space.function()
    ph = space.smspace.function()

    M = space.mass_matrix()
    B = -space.div_matrix()

    F0 = -space.set_neumann_bc(pde.dirichlet) # Poisson 的 D 氏边界变为 Neumann
    F1 = -space.smspace.source_vector(pde.source)

    if True:
        solver = SaddlePointFastSolver((M, B, None), (F0, F1))
        uh[:], ph[:] = solver.solve()
    else:
        AA = bmat([[M, B], [B.T, None]], format='csr')
        FF = np.r_['0', F0, F1]
        x = spsolve(AA, FF).reshape(-1)
        uh[:] = x[:udof]
        ph[:] = x[udof:]
    error0 = space.integralalg.error(pde.flux, uh.value, power=2)
    error1 = space.integralalg.error(pde.solution, ph.value, power=2) 
    print(error0, error1)

    n *= 2 # 加密网格 


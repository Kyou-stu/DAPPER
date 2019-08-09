# "Lorenz-95" (or 96) model. For a deeper introduction, see
# "DAPPER/tutorials/T4 - Dynamical systems, chaos, Lorenz.ipynb"
#
# Note: implementation is ndim-agnostic.

import numpy as np
from dapper.tools.math import rk4, integrate_TLM, is1d, FD_Jac

Force = 8.0

# Note: the model is unstable (blows up) if there are large peaks
# (as may be occasioned by the analysis update, especially with partial obs). 
# Example: integrate 4 steps with dt=0.05 from x0 = [0,-30,0,30].
# This is effectively a CFL condition... Can be addressed by:
#  - lowering dt
#  - using an implicit time stepping scheme instead of rk4
#  - stupidly crop amplitudes, as is done here:
prevent_blow_up = False

Tplot = 10

x0 = lambda M: 2.3*np.ones(M)

def dxdt(x):
  a = x.ndim-1
  s = lambda x,n: np.roll(x,-n,axis=a)
  return (s(x,1)-s(x,-2))*s(x,-1) - x + Force

def step(x0, t, dt):

  if prevent_blow_up:
    clip      = abs(x0)>30
    x0[clip] *= 0.1

  return rk4(lambda t,x: dxdt(x), x0, np.nan, dt)

################################################
# OPTIONAL (not necessary for EnKF or PartFilt):
################################################
def d2x_dtdx(x):
  assert is1d(x)
  Nx  = len(x)
  Mat = np.zeros((Nx,Nx))
  md  = lambda i: np.mod(i,Nx)
  for i in range(Nx):
    Mat[i,i]       = -1.0
    Mat[i,   i-2 ] = -x[i-1]
    Mat[i,md(i+1)] = +x[i-1]
    Mat[i,   i-1 ] = x[md(i+1)]-x[i-2]
  return Mat

# For L95, method='analytic' >> 'approx'
dstep_dx = lambda x,t,dt: integrate_TLM(d2x_dtdx(x),dt,method='analytic')
# dstep_dx = FD_Jac(step)


################################################
# Add some non-default liveplotters
################################################
import dapper.tools.liveplotting as LP
def LPs(jj=None): return [
    (11, 1, LP.spatial1d(jj)  ),
    (12, 1, LP.correlations   ),
    (15, 0, LP.spectral_errors),
    (13, 0, LP.phase3d(jj)    ),
    (14, 0, LP.sliding_marginals(jj)) ,
    ]



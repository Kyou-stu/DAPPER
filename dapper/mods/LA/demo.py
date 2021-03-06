##
from dapper import with_recursion, plt
from dapper.mods.LA.raanes2015 import step, X0
from dapper.tools.viz import amplitude_animation
plt.ion()

##
simulator = with_recursion(step, prog="Simulating")

x0 = X0.sample(1).squeeze()
dt = 1
xx = simulator(x0, k=500, t=0, dt=dt)

amplitude_animation(xx,dt)

##



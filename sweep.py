import parse_out
import parse_yaml
import os
import matplotlib.pyplot as plt
import numpy as np

tt4 = []
eta = []
prd = []

for prdes in range(150, 300, 2):
    prd.append(prdes/100)
    parse_yaml.main({'compressor.PRdes' : prdes/100})
    os.system(".\\npss_dumb.bat >nul 2>&1")
    temp = parse_out.extract(["Tt4[K]", "Eta_Thermal"])
    tt4.append(temp[0])
    eta.append(temp[1])

fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('Pressure Ratio')
ax1.set_ylabel('Thermal Efficiency', color=color)
ax1.plot(prd, eta, color=color)
ax1.tick_params(axis='y', labelcolor=color)

# ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

# color = 'tab:blue'
# ax2.set_ylabel('Turbine Inlet Temperature [K]', color=color)  # we already handled the x-label with ax1
# ax2.plot(prd, tt4, color=color)
# ax2.tick_params(axis='y', labelcolor=color)

# fig.tight_layout()  # otherwise the right y-label is slightly clipped
ax1.grid()
fig.savefig("plot.png")
plt.show()
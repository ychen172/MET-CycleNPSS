import parse_out
import parse_yaml
import os
import matplotlib.pyplot as plt
import numpy as np

eta = []
prd = []
t42 = []

for prdes in range(160, 280, 5):
    row = []
    prd.append(prdes/100)
    t42 = []
    for tt4tt2 in range(290, 350, 5):
        t42.append(tt4tt2/100)
        parse_yaml.main({'compressor.PRdes' : prdes/100, 'temp_ratio_des' : tt4tt2/100, 'thrust_high_lim': 30})
        os.system(".\\npss_dumb.bat >nul 2>&1")
        temp = parse_out.extract(["Eta_Thermal"])
        row.append(temp[0])
    eta.append(row)

print(eta)

fig, ax = plt.subplots()

levels = [0.01, 0.015, 0.02, 0.025, 0.03, 0.035, 0.04, 0.045, 0.05, 0.055, 0.06, 0.65]
CS = ax.contour(t42, prd, eta, levels)

ax.clabel(CS, inline=True, fontsize=10)
ax.set_xlabel('Temperature Ratio [Tt4/Tt2]')
ax.set_ylabel('Compressor Pressure Ratio [compressor.PRdes]')
ax.set_title('Temperature Ratio and Compressor Ratio to Thermal Efficiency')

plt.show()
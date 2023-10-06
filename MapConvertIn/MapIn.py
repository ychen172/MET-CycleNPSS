import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.interpolate

## User Input #######################################################
# File names
PEMapName  = './efficiency_vs_pressure.csv'
WPMapName  = './pressure_vs_massflow.csv'
#Reference Parameters
Tref  = 288.15 #K
Pref  = 101353 #Pa
#Inlet Parameter
TtIn = 288.15 #K
PtIn = 101353 #Pa
gamma = 1.4
# Switch
typeComp = 'Compressor'
# Compute Parameters
NumR = 11 # number of R-lines
# Design point data
NcMapDes    = 1.0 #Unscaled map design point corrected speed. Max eff point at 100% speed
RlineMapDes = 2.0 # Unscaled map design point Rline. Max eff point at 100% speed	
## User Input Over #######################################################

#Calculate Ratios
theta = TtIn/Tref
delta = PtIn/Pref

# Read in Fuel Flowrate
PEMap  = pd.read_csv(PEMapName,skiprows=2,delimiter='[ , [  ]',engine='python')
WPMap  = pd.read_csv(WPMapName,skiprows=2,delimiter='[ , [  ]',engine='python')
# Extract Data
PR      = PEMap['Design'].values[:] # numpy array
EtaP    = PEMap['point'].values[:]  # numpy array
W       = WPMap['Design'].values[:] # numpy array
PRv2    = WPMap['point'].values[:]  # numpy array
#Initialization
rpmLst   = []
#rpmv2Lst = []
PRLst    = []
#PRv2Lst  = []
EtaPLst  = []
WLst     = []
counter  = -1
staSave  = False; 
for i in range(len(PR)):#loop through each row
    if EtaP[i] == 'rpm]':
        rpmLst.append(PR[i])
        counter += 1
        staSave = True
        PRLst.append([])
        EtaPLst.append([])
        #rpmv2Lst.append(W[i])
        #PRv2Lst.append([])
        WLst.append([])
    elif staSave:
        PRLst[counter].append(PR[i])
        EtaPLst[counter].append(float(EtaP[i]))
        #PRv2Lst[counter].append(float(PRv2[i]))
        WLst[counter].append(W[i])
    else:
        pass
rpmLst = np.array(rpmLst)
#rpmv2Lst = np.array(rpmv2Lst)
PRLst    = np.array(PRLst)
#PRv2Lst  = np.array(PRv2Lst)
EtaPLst  = np.array(EtaPLst)
WLst     = np.array(WLst)

#PreProcess Data
WcLst = WLst*np.sqrt(theta)/delta
NcLst = rpmLst/np.sqrt(theta)
if typeComp == 'Compressor':
    topFac = (gamma-1)/gamma
    botFac = (gamma-1)/(gamma*EtaPLst)
    EtaALst = (PRLst**topFac - 1)/(PRLst**botFac - 1)
elif typeComp == 'Turbine':
    pass
else:
    print('What is this?')

#Fine R-line for surge and stall
WcStall = np.empty(len(NcLst))
WcSurge = np.empty(len(NcLst))
PRStall = np.empty(len(NcLst))
PRSurge = np.empty(len(NcLst))
for i in range(len(NcLst)):
    WcStall[i] = WcLst[i][-1]
    PRStall[i] = PRLst[i][-1]
    WcSurge[i] = WcLst[i][0]
    PRSurge[i] = PRLst[i][0]

slopeSurge, interSurge = np.polyfit(WcSurge,PRSurge,1)
slopeStall, interStall = np.polyfit(WcStall,PRStall,1)
 
if (slopeStall>slopeSurge) | (interStall>interSurge):
    print("Warning!! It seems that surge line is lower than stall line")

# interpolated out efficiency
WcInte = np.reshape(WcLst,WcLst.size)
PRInte = np.reshape(PRLst,PRLst.size)
EtaAInte = np.reshape(EtaALst,EtaALst.size)
WcMesh = np.linspace(WcInte.min(),WcInte.max(),100)
PRMesh = np.linspace(PRInte.min(),PRInte.max(),100)
WcMesh,PRMesh = np.meshgrid(WcMesh,PRMesh)
rbf = scipy.interpolate.Rbf(WcInte, PRInte, EtaAInte, function='linear')
EtaMesh = rbf(WcMesh, PRMesh)

# Plot out how the R-lines look like
fig = plt.figure(dpi = 300)
ax  = fig.add_subplot(1,1,1)
for i in range(len(NcLst)):
    plt.plot(WcLst[i], PRLst[i], '.', label='Nc='+str(int(NcLst[i])))
plt.plot(WcSurge,interSurge+slopeSurge*WcSurge,'-',label='Surge')
plt.plot(WcStall,interStall+slopeStall*WcStall,'-',label='Stall')
color = ax.contourf(WcMesh,PRMesh,EtaMesh,levels=np.linspace(0.6,0.68,10))
fig.colorbar(color)
plt.ylabel('PR')
plt.xlabel('Wc')
plt.grid(True)
plt.legend(loc="upper left")
plt.savefig("Map.jpg")
plt.show()

#Create R-lines
RValueLst = np.linspace(3,1,NumR)
NcPercLst = NcLst/np.max(NcLst)
slopeRLst = np.linspace(slopeStall,slopeSurge,NumR)
interRLst = np.linspace(interStall,interSurge,NumR)
EtaARLst = np.zeros([len(NcLst),len(slopeRLst)])
PRRLst = np.zeros([len(NcLst),len(slopeRLst)])
WcRLst = np.zeros([len(NcLst),len(slopeRLst)]) #kg/sec
#Constructure R-line data
for i in range(len(slopeRLst)): #Across different R
    for j in range(len(NcLst)):#Across different speeds
        WcCurLst    = WcLst[j]
        PRCurLst    = PRLst[j]
        EtaACurLst  = EtaALst[j]
        slopeCurLst = (PRCurLst-interRLst[i])/WcCurLst
        #Efficiency
        f_inter = scipy.interpolate.interp1d(slopeCurLst,EtaACurLst,kind='cubic',fill_value="extrapolate")
        Res = f_inter(slopeRLst[i])
        if  Res > 0:
            EtaARLst[j][i] = Res
        else:
            EtaARLst[j][i] = 0
        #Pressure Ratio
        f_inter = scipy.interpolate.interp1d(slopeCurLst,PRCurLst,kind='cubic',fill_value="extrapolate")
        Res = f_inter(slopeRLst[i])
        if  Res > 1:
            PRRLst[j][i] = Res
        else:
            PRRLst[j][i] = 1
        #Corrected Mass Flow
        f_inter = scipy.interpolate.interp1d(slopeCurLst,WcCurLst,kind='cubic',fill_value="extrapolate")
        Res = f_inter(slopeRLst[i])
        if  Res > 0:
            WcRLst[j][i] = Res
        else:
            WcRLst[j][i] = 0 

Ckg2lbm = 2.20462 #1kg/s is 2.20462 lbm/s
#Print out the map
with open('HPCAnsysJun26.txt','w') as f:
    f.write('Subelement CompressorRlineMap S_map {\n')
    f.write('alphaMapDes = 0.0;\n')
    f.write('NcMapDes = '+ str(NcMapDes) +';\n')
    f.write('RlineMapDes = '+ str(RlineMapDes) +';\n')
    f.write('RlineStall= 1.0;\n')
    #Corrected mass flow print out
    f.write('Table TB_Wc(real ALPHA, real SPED, real R) {\n')
    f.write('ALPHA =0.0 {\n')
    for i in range(len(NcPercLst)):# loop through speed
        f.write('SPED =  ' + str(NcPercLst[i]) + '  {\n')
        f.write('R = {' + str(list(np.round(RValueLst,3)))[1:-1] + '}\n')
        f.write('FLOW  = {' + str(list(np.round(WcRLst[i]*Ckg2lbm,3)))[1:-1] + '}\n')
        f.write('}\n')
    f.write('}\n')
    f.write('ALPHA.interp = "linear";\n')
    f.write('ALPHA.extrap = "linear";\n')
    f.write('SPED.interp = "lagrange3";\n')
    f.write('SPED.extrap = "linear";\n')
    f.write('R.interp = "lagrange3";\n')
    f.write('R.extrap = "linear";\n')
    f.write('extrapIsError = 0;\n')
    f.write('printExtrap = 0;\n')
    f.write('}\n')
    #Efficiency print out
    f.write('\n\n')
    f.write('Table TB_eff(real ALPHA, real SPED, real R) {\n')
    f.write('ALPHA =0.0 {\n')
    for i in range(len(NcPercLst)):# loop through speed
        f.write('SPED =  ' + str(NcPercLst[i]) + '  {\n')
        f.write('R = {' + str(list(np.round(RValueLst,3)))[1:-1] + '}\n')
        f.write('EFF  = {' + str(list(np.round(EtaARLst[i],3)))[1:-1] + '}\n')
        f.write('}\n')
    f.write('}\n')
    f.write('ALPHA.interp = "linear";\n')
    f.write('ALPHA.extrap = "linear";\n')
    f.write('SPED.interp = "lagrange3";\n')
    f.write('SPED.extrap = "linear";\n')
    f.write('R.interp = "lagrange3";\n')
    f.write('R.extrap = "linear";\n')
    f.write('extrapIsError = 0;\n')
    f.write('printExtrap = 0;\n')
    f.write('}\n')
    #Efficiency print out
    f.write('\n\n')
    f.write('Table TB_PR(real ALPHA, real SPED, real R) {\n')
    f.write('ALPHA =0.0 {\n')
    for i in range(len(NcPercLst)):# loop through speed
        f.write('SPED =  ' + str(NcPercLst[i]) + '  {\n')
        f.write('R = {' + str(list(np.round(RValueLst,3)))[1:-1] + '}\n')
        f.write('PR  = {' + str(list(np.round(PRRLst[i],3)))[1:-1] + '}\n')
        f.write('}\n')
    f.write('}\n')
    f.write('ALPHA.interp = "linear";\n')
    f.write('ALPHA.extrap = "linear";\n')
    f.write('SPED.interp = "lagrange3";\n')
    f.write('SPED.extrap = "linear";\n')
    f.write('R.interp = "lagrange3";\n')
    f.write('R.extrap = "linear";\n')
    f.write('extrapIsError = 0;\n')
    f.write('printExtrap = 0;\n')
    f.write('}\n')
    f.write('}\n')



print('end')


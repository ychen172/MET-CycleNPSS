import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.interpolate

## User Input #######################################################
# File names
MapInName  = './CompressorMapHaz.csv'
#Reference Parameters
Tref  = 288.15 #K
Pref  = 101353 #Pa
#Inlet Parameter
TtIn = 288.15 #K
PtIn = 101353 #Pa
# Compute Parameters
NumR = 12 # number of R-lines
# Design point data
PRDicDes    = '3.5' #  Set both to empty '' if want to use default ansys design point
WDicDes     = '0.284'#kg/sec	
# Number of low power speed line to get rid of
nDelNc      = 3 # 0 if all the speeds are physical
## User Input Over #######################################################

#Calculate Ratios
theta = TtIn/Tref
delta = PtIn/Pref

# Read in Fuel Flowrate
MapIn  = pd.read_csv(MapInName)
# Extract Data
PR      = MapIn['P11 - P0 Ratio (t-t)'].values[:] # numpy array
EtaA    = MapIn['P10 - Isentropic Efficiency (t-t)'].values[:]/100  # [0 to 1]numpy array
W       = MapIn['P13 - Mass Flow [kg s^-1]'].values[:] # numpy array kg/sec
RPMBase = MapIn['P2 - Base Duty Speed [rev min^-1]'].values[:]  # RPM
RPMFrac = MapIn['P4 - Percent Speed'].values[:]/100  # RPM
RPMActu = RPMBase*RPMFrac # RPM
# Extract Design Point
PRDes      = PR[0]
WDes       = W[0]
if len(PRDicDes) > 0:
    PRDes  = float(PRDicDes)
    WDes   = float(WDicDes)
PR         = PR[1:]
EtaA       = EtaA[1:]
W          = W[1:]
RPMActu    = RPMActu[1:]
#Flip to make RPM from low to high
if RPMActu[0]>RPMActu[-1]:
    PR      = np.flip(PR)     #[Case]
    EtaA    = np.flip(EtaA) #[Case] {0-1}
    W       = np.flip(W) #[Case] {kg/sec}
    RPMActu = np.flip(RPMActu) #[Case] {RPM}

#Initialization
RPMActuIni = 6969
PRLst      = [] #[#RPM,#PR]
EtaALst    = [] #[#RPM,#EtaA] {0-1}
WLst       = [] #[#RPM,#W] {kg/sec}
RPMActuLst = [] #[#RPM] {RPM}
counter    = -1
for i in range(len(RPMActu)):#loop through all the speed
    if RPMActu[i] != RPMActuIni:
        RPMActuIni = RPMActu[i]
        RPMActuLst.append(RPMActu[i])
        counter += 1
        PRLst.append([])
        EtaALst.append([])
        WLst.append([])
        PRLst[counter].append(PR[i])
        EtaALst[counter].append(EtaA[i])
        WLst[counter].append(W[i])
    else:
        PRLst[counter].append(PR[i])
        EtaALst[counter].append(EtaA[i])
        WLst[counter].append(W[i])
PRLst      = np.array(PRLst) #[#RPMc,#PR]
EtaALst    = np.array(EtaALst) #[#RPMc,#EtaA] {0-1}
WLst       = np.array(WLst) #[#RPMc,#W] {kg/sec}
RPMActuLst = np.array(RPMActuLst) #[#RPMc] {RPM}

#PreProcess Data (PRLst, EtaALst, WcLst, NcLst)
WcLst = WLst*np.sqrt(theta)/delta #[#RPMc,#Wc] {kg/sec}
NcLst = RPMActuLst/np.sqrt(theta) #[#RPMc] {RPM}
#Also compute design point for R value
WcDes = WDes*np.sqrt(theta)/delta #{kg/sec}

#Fine R-line for surge and Choked
WcChoked = np.empty(len(NcLst))
WcSurge = np.empty(len(NcLst))
PRChoked = np.empty(len(NcLst))
PRSurge = np.empty(len(NcLst))
if WcLst[0][0] < WcLst[0][-1]:
    idxSurge  = 0
    idxChoked = -1
else:
    idxSurge  = -1
    idxChoked = 0
for i in range(len(NcLst)):
    WcChoked[i] = WcLst[i][idxChoked]
    PRChoked[i] = PRLst[i][idxChoked]
    WcSurge[i] = WcLst[i][idxSurge]
    PRSurge[i] = PRLst[i][idxSurge]

slope2ndSurge,  slopeSurge,  interSurge = np.polyfit(WcSurge,PRSurge,2)
slope2ndChoked, slopeChoked, interChoked = np.polyfit(WcChoked,PRChoked,2)

# interpolated out efficiency
WcInte   = np.reshape(WcLst,WcLst.size)     #[#RPMc*#Wc] {kg/sec}
PRInte   = np.reshape(PRLst,PRLst.size)     #[#RPMc*#PR]
EtaAInte = np.reshape(EtaALst,EtaALst.size) #[#RPMc*#EtaA] {0-1}
WcMesh = np.linspace(WcInte.min(),WcInte.max(),100) #[Uniform Mesh 2d]
PRMesh = np.linspace(PRInte.min(),PRInte.max(),100) #[Uniform Mesh 2d]
WcMesh,PRMesh = np.meshgrid(WcMesh,PRMesh)
rbf = scipy.interpolate.Rbf(WcInte, PRInte, EtaAInte, function='cubic')
EtaAMesh = rbf(WcMesh, PRMesh) #[Uniform Mesh 2d]

# Plot out how the R-lines look like
fig = plt.figure(dpi = 300)
ax  = fig.add_subplot(1,1,1)
for i in range(len(NcLst)):
    plt.plot(WcLst[i], PRLst[i], 'x', label='Nc='+str(int(NcLst[i])))
plt.plot(WcSurge,interSurge+slopeSurge*WcSurge+slope2ndSurge*WcSurge**2,'-',label='Surge')
plt.plot(WcChoked,interChoked+slopeChoked*WcChoked+slope2ndChoked*WcChoked**2,'-',label='Choked')
color = ax.contourf(WcMesh,PRMesh,EtaAMesh,levels=np.linspace(0.83,0.93,10))
fig.colorbar(color)
plt.ylabel('PR')
plt.xlabel('Wc')
plt.grid(True)
plt.legend(loc="upper left",fontsize="7")
plt.savefig("Map.jpg")
plt.show()

#Create R-lines
RValueLst = np.linspace(1,3,NumR) #[#R]{R}Surge to Choked Always 1 to 3
NcPercLst = NcLst/np.max(NcLst) #[#RPMc] {0-1}
slope2ndRLst = np.linspace(slope2ndSurge,slope2ndChoked,NumR) #[#R]{}
slopeRLst    = np.linspace(slopeSurge,slopeChoked,NumR) #[#R]{}
interRLst    = np.linspace(interSurge,interChoked,NumR) #[#R]{}
EtaARLst = np.zeros([len(NcLst),len(slopeRLst)]) #[#RPMc,#R]{0-1}
PRRLst   = np.zeros([len(NcLst),len(slopeRLst)]) #[#RPMc,#R]{}
WcRLst   = np.zeros([len(NcLst),len(slopeRLst)]) #[#RPMc,#R]{kg/sec}
#Constructure R-line data
for i in range(len(slopeRLst)): #Across different R
    for j in range(len(NcLst)):#Across different speeds
        WcCurLst    = WcLst[j] #[#Wc]
        PRCurLst    = PRLst[j] #[#PR]
        EtaACurLst  = EtaALst[j] #[#EtaA]
        interCurLst = PRCurLst - slopeRLst[i]*WcCurLst - slope2ndRLst[i]*(WcCurLst**2) #[#EtaA]
        #Efficiency
        f_inter = scipy.interpolate.interp1d(interCurLst,EtaACurLst,kind='cubic',fill_value="extrapolate")
        Res = f_inter(interRLst[i])
        if  Res <= 0:
            EtaARLst[j][i] = 0
        elif Res >= 1:
            EtaARLst[j][i] = 0
        else:
            EtaARLst[j][i] = Res
        #Pressure Ratio
        f_inter = scipy.interpolate.interp1d(interCurLst,PRCurLst,kind='cubic',fill_value="extrapolate")
        Res = f_inter(interRLst[i])
        if  Res > 1:
            PRRLst[j][i] = Res
        else:
            PRRLst[j][i] = 1
        #Corrected Mass Flow
        f_inter = scipy.interpolate.interp1d(interCurLst,WcCurLst,kind='cubic',fill_value="extrapolate")
        Res = f_inter(interRLst[i])
        if  Res > 0:
            WcRLst[j][i] = Res
        else:
            WcRLst[j][i] = 0 

#Compute Design Point
RValueLstExp = np.zeros([len(NcLst),len(slopeRLst)]) #[#RPMc,#R]{}
NcPercLstExp = np.zeros([len(NcLst),len(slopeRLst)]) #[#RPMc,#R]{}
for i in range(len(slopeRLst)): #Across different R
    for j in range(len(NcLst)):#Across different speeds
        RValueLstExp[j][i] = RValueLst[i]
        NcPercLstExp[j][i] = NcPercLst[j]        
RValueLstExp   = np.reshape(RValueLstExp,RValueLstExp.size)
NcPercLstExp   = np.reshape(NcPercLstExp,NcPercLstExp.size)
PRRLstExp      = np.reshape(PRRLst,PRRLst.size)
WcRLstExp      = np.reshape(WcRLst,WcRLst.size)
rbf_R  = scipy.interpolate.Rbf(WcRLstExp, PRRLstExp, RValueLstExp, function='linear')
rbf_Nc = scipy.interpolate.Rbf(WcRLstExp, PRRLstExp, NcPercLstExp, function='linear')
RDes   = rbf_R(WcDes, PRDes) #[Uniform Mesh 2d]
NcDes  = rbf_Nc(WcDes, PRDes) #[Uniform Mesh 2d]

# Plot out how the R-lines look like
fig = plt.figure(dpi = 300)
ax  = fig.add_subplot(1,1,1)
for i in range(len(NcLst)):
    plt.plot(WcLst[i], PRLst[i], 'x', label='Nc='+str(np.round(NcPercLst[i],2)))
for i in range(len(RValueLst)):
    plt.plot(WcChoked,interRLst[i]+slopeRLst[i]*WcChoked+slope2ndRLst[i]*WcChoked**2,'-',label='R='+str(np.round(RValueLst[i],2)))
plt.plot(WcDes,PRDes,'*r',label='Design Point')
color = ax.contourf(WcMesh,PRMesh,EtaAMesh,levels=np.linspace(0.83,0.93,10))
fig.colorbar(color)
plt.ylabel('PR')
plt.xlabel('Wc')
plt.grid(True)
plt.legend(loc="upper left",fontsize="5")
plt.savefig("Map2.jpg")
plt.show()

Ckg2lbm = 2.20462 #1kg/s is 2.20462 lbm/s
#Print out the map
with open('HPCAnsysJun26.txt','w') as f:
    f.write('Subelement CompressorRlineMap S_map {\n')
    f.write('alphaMapDes = 0.0;\n')
    f.write('NcMapDes = '+ str(NcDes) +';\n')
    f.write('RlineMapDes = '+ str(RDes) +';\n')
    f.write('RlineStall = 1.0;\n')
    #Corrected mass flow print out
    f.write('Table TB_Wc(real ALPHA, real SPED, real R) {\n')
    f.write('ALPHA =0.0 {\n')
    for i in range(nDelNc,len(NcPercLst)):# loop through speed
        f.write('SPED =  ' + str(NcPercLst[i]) + '  {\n')
        f.write('R = {' + str(list(np.round(RValueLst,3)))[1:-1] + '}\n')
        f.write('FLOW  = {' + str(list(np.round(WcRLst[i]*Ckg2lbm,3)))[1:-1] + '}\n')
        f.write('}\n')
    f.write('}\n')
    f.write('ALPHA =1.0 {\n')
    for i in range(nDelNc,len(NcPercLst)):# loop through speed
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
    for i in range(nDelNc,len(NcPercLst)):# loop through speed
        f.write('SPED =  ' + str(NcPercLst[i]) + '  {\n')
        f.write('R = {' + str(list(np.round(RValueLst,3)))[1:-1] + '}\n')
        f.write('EFF  = {' + str(list(np.round(EtaARLst[i],3)))[1:-1] + '}\n')
        f.write('}\n')
    f.write('}\n')
    f.write('ALPHA =1.0 {\n')
    for i in range(nDelNc,len(NcPercLst)):# loop through speed
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
    for i in range(nDelNc,len(NcPercLst)):# loop through speed
        f.write('SPED =  ' + str(NcPercLst[i]) + '  {\n')
        f.write('R = {' + str(list(np.round(RValueLst,3)))[1:-1] + '}\n')
        f.write('PR  = {' + str(list(np.round(PRRLst[i],3)))[1:-1] + '}\n')
        f.write('}\n')
    f.write('}\n')
    f.write('ALPHA =1.0 {\n')
    for i in range(nDelNc,len(NcPercLst)):# loop through speed
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


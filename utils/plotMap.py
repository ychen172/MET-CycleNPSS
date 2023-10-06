#Std. imports
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def plotCmpMap(MAP, s_eff = 1, s_PR = 1, s_Wc = 1, s_Nc = 1, 
        X = None, labels = None, opline=None, oplabels=None,
        Speed_lines = np.linspace(0.99,1.01,11),
        Eff_lines = [0.1, 0.5, 0.6, 0.8, 0.85, 0.9, 0.92, 0.94, 0.96], title = "",
        Rlines = True, ShadedSurge = True, EffGraph = True, ax = None, interp_fac = 2, speed_range=[0.8, 1.1]):
   
    #load Values
    PR = MAP.PR
    W  = MAP.Wc
    eff= MAP.eff
    SPED = MAP.Nc
    
    #Apply scalars
    PR = (PR -  1)*s_PR +1
    W = W *s_Wc
    eff = eff * s_eff
    SPED = SPED * s_Nc
    
    #Convert to SI unit
    W = W/2.20462 # kg/sec from lbm/sec

    if EffGraph:
        if ax is None:
            fig, ax = plt.subplots(2,1,figsize = (8,6),dpi = 200, gridspec_kw={'height_ratios': [1, 3]}, sharex = True)
            plt.tight_layout
        Eff = ax[0].plot(np.transpose(W),np.transpose(eff),'-k', lw = 1.5) 
        #ax[0].set_ylim(0,1)
        ax[0].set_ylabel(r'$\eta_{ad}$')

        labels = list(np.char.mod('%.2f', SPED))

        for n,(i,j) in enumerate(zip(W[:,-1],eff[:,-1])):        
            if SPED[n] >= speed_range[0] and SPED[n] <= speed_range[1]:
                ax[0].text(i,j,str(labels[n]), fontsize = 8,
                           horizontalalignment='center',
                           verticalalignment='center',bbox=dict(facecolor='white',ec='none'), zorder=16)

        a  = ax[1]
        a0 = ax[0]
        
    else:
        if ax is None:
            fig, a = plt.subplots(figsize = (8,6), dpi = 200)
        else:
            a = ax
        
        a0 = a
            
    labels = list(np.char.mod('%.2f', SPED))
    
    Speed = a.plot(np.transpose(W),np.transpose(PR),'-k', lw = 1., zorder = 15)   
    a.set_ylabel(r'Pressure ratio $\pi$')
    if (Rlines) :
        a.plot(W,PR, '--k', lw = 0.5, alpha = 0.5)
    
    #Plot surge line
    surge_x = W[:,0]
    surge_y = PR[:,0]
    a.plot(surge_x,surge_y, '-r', lw = 2)
    idx_midpt = int(len(surge_x)/2)
    slope = 180/np.pi*np.arctan((surge_y[idx_midpt+5] - surge_y[idx_midpt-5])/
                                     (surge_x[idx_midpt+5] - surge_x[idx_midpt-5]))

    a.text(surge_x[-5], surge_y[-5], "Surge line", fontsize = 10, rotation = 45, color = 'r',
           horizontalalignment ='center', verticalalignment='center',
           bbox=dict(facecolor='white',ec='none'), zorder = 30)          
    
    #Shade surge area if requested
    if ShadedSurge :
        a.fill_between(surge_x, surge_y, surge_y*1.05, alpha= 0.2)
    
    for n,(i,j) in enumerate(zip(W[:,-1],PR[:,-1])):        
         if SPED[n] >= speed_range[0] and SPED[n] <= speed_range[1]:
            a.text(i,j,str(labels[n]), fontsize = 10, 
            horizontalalignment='center',
            verticalalignment='center',bbox=dict(facecolor='white',ec='none'))
        
    #plot eff contours
    from scipy.interpolate import interp2d
    from scipy.ndimage import zoom
    # f_eff = interp2d(W,PR, eff)
    # w  = np.linspace(W[0], W[-1], 100)
    # pr = np.linspace(PR[0], PR[-1], 100)
    w = zoom(W, interp_fac)
    pr = zoom(PR, interp_fac)
    eff_interp = zoom(eff, interp_fac)
    # eff_interp = f_eff(w,pr)
    Eff_contours = a.contour(w, pr, eff_interp, Eff_lines, linestyles = '--', colors = 'b', linewidths = 1, zorder = 20, alpha = 0.8)
    
    h,_ = Eff_contours.legend_elements()
    a.legend([h[0]], ["Efficiency"])
    # Eff_contours = a.contour(W,PR, eff, Eff_lines, linestyles = '--', colors = 'b', linewidths = 1, zorder = 20)
    
    # if X is not None and labels is not None:
    #     for point in range(len(X)):
    #         points = a.scatter(X[point][0], X[point][1], label=labels[point])
    #         a.legend(*points.legend_elements(), labels[point])
    
    if opline is not None:    
        a.plot(opline[0], opline[1], color='purple')
        print(opline)
    
    
    a.clabel(Eff_contours, inline = True,  fontsize = 10, use_clabeltext=True, inline_spacing=1.0)
    plt.tight_layout()
    a.set_xlabel('Corrected mass flow $\dot{m}_c=\dfrac{\dot{m}\sqrt{\\theta}}{\delta}$ [lbm/s]')
    
    a0.set_title(title)
    if EffGraph:
        for axis in ax:
            axis.grid(alpha = 0.2)
    
    if not EffGraph:
        ax = a
        ax.grid(alpha = 0.2)
    plt.savefig('MapOut.jpg')    
    return ax

def read_NPSS(fname, rows_to_skip = [0,1], dropfirst = True):
    df = pd.read_csv(fname, delimiter=r'\s+', skiprows=rows_to_skip)
    return df

from HPCAnsysJun26 import CmpMap
df = read_NPSS("../output/Turbojet.out")

Wch = df["CmpH_Wc"].tolist()
PRh = df["HPC_PR"].tolist()

oplineHPC = [Wch, PRh]

Seff = 0.895135
SPR = 0.588859
SWc = 1.3384
SNc = 0.999999
plotCmpMap(CmpMap, Seff, SPR, SWc, SNc, opline=oplineHPC, Eff_lines = np.linspace(0.70,0.80,11),speed_range = [0,1.1])
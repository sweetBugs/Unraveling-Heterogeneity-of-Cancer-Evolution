# In[1]:

import numpy as np
import pandas as pd
import math
import scipy.stats as stats
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

# In[2]: Agent analysis: numbner of subclones

def dataReImport(Patient, i, keys):
    
    temp = pd.read_csv('CLL_Patients\WBC_counts\%d.txt' %Patient, skiprows=1, header=None, names = ['Year','WBC(×10^9)'])
    timeI = math.ceil(temp['Year'][0]*365)
    
    mat = pd.DataFrame(np.load('CLL_Patients\subclone_composition\evolution_%d_%d.npy' %(Patient, i), allow_pickle=True).item(), columns=keys)
    mat.index = np.arange(timeI, timeI+len(mat))
    
    return mat


def cloneNumber(data, keys, timeP):
    
    num = 0
    
    for i in range(len(keys)):
        if data.iloc[timeP, i] > 1:
            num += 1
            
    return num


def numberList(mat):
    
    num = []
    
    for t in range(0, mat.index[-1]-mat.index[0]+1, 1):
        num.append(cloneNumber(mat, keys, t))
    
    data = pd.DataFrame(num, index = mat.index)
    
    return data


def allNumberList(Patients, rep, keys):
    
    temp = {'num':[0]*5461, 'rep':[0]*5461}
    data = pd.DataFrame(temp, index = range(-2,5459))
    
    for Patient in Patients:
        for rep in range(rep):
            mat = dataReImport(Patient, rep, keys)
            num = numberList(mat)
            for k in range(num.index[0], num.index[-1]+1):
                data.loc[k][0] = data.loc[k][0] + num.loc[k][0]
                data.loc[k][1] = data.loc[k][1] + 1
    
    dataMean = pd.DataFrame(data['num']/data['rep'], index = data.index)
    
    return dataMean


def speNumberList(Patient, rep, keys):
    
    mat = dataReImport(Patient, 0, keys)
    data = pd.DataFrame(index = range(mat.index[0],mat.index[-1]+1))
    
    for rep in range(rep):
        mat = dataReImport(Patient, rep, keys)
        num = numberList(mat)
        data[rep] = num
    
    return data


def mean_confidence_interval(data, confidence=0.95):
    
    a = 1.0*np.array(data)
    n = len(a)
    m, se = np.mean(a), stats.sem(a)
    h = se * stats.t._ppf((1+confidence)/2., n-1)
    return m, m-h, m+h


def speMC(data, rep, keys):
    
    dataMC = pd.DataFrame(index = range(data.index[0],data.index[-1]+1))
    mean, ciu, cil = [], [], []
    
    for c in range(data.index[0], data.index[-1]+1):
        temp = data.loc[c]
        m, c1, c2 = mean_confidence_interval(temp, confidence=0.95)
    
        mean.append(m)
        ciu.append(c1)
        cil.append(c2)
        
    dataMC['mean'] = mean
    dataMC['ciu']  = ciu
    dataMC['cil']  = cil
        
    return dataMC


def fillPlot(o, oths):
    
    font1 = {'family':'Arial', 'weight':'normal', 'size':'50'}
    font2 = {'family':'Arial', 'weight':'bold', 'size':'40'}
    
    fig, ax = plt.subplots(figsize=(13,11))
    
    x1 = np.arange(o.index[0], o.index[-1]+1)
    ax.fill_between(x1, o['ciu'], o['cil'], alpha=0.3)
    ax.plot(x1, o['mean'], linewidth=5, label='Patient 1')      
    
    x2 = np.arange(oths.index[0], oths.index[-1]+1)
    ax.plot(x2, oths[0], linewidth=5, label='Other Patients')      
    
    plt.xlim([0, 2500])
    
    ax.tick_params(axis='x',labelsize=30)
    ax.tick_params(axis='y',labelsize=30)
    
    ax.set_xlabel('Time (Days)', font1)
    ax.set_ylabel('Number of subclones', font1)
    
    ax.legend(loc='best', prop=font2, frameon=False)
    
    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'

    plt.savefig('Patient_o_vs_ots.tif', bbox_inches='tight')
    plt.savefig('Patient_o_vs_ots.eps', bbox_inches='tight')


# In[3]: 
keys = ['D:0.0,R:0.9,P:0.1',
        'D:0.0,R:1.0,P:0.0',
        'D:0.1,R:0.7,P:0.2',
        'D:0.1,R:0.8,P:0.1',
        'D:0.1,R:0.9,P:0.0',
        'D:0.2,R:0.5,P:0.3',
        'D:0.2,R:0.6,P:0.2',
        'D:0.2,R:0.7,P:0.1',
        'D:0.3,R:0.3,P:0.4',
        'D:0.3,R:0.4,P:0.3',
        'D:0.3,R:0.5,P:0.2',
        'D:0.4,R:0.1,P:0.5',
        'D:0.4,R:0.2,P:0.4',
        'D:0.4,R:0.3,P:0.3',
        'D:0.5,R:0.0,P:0.5',
        'D:0.5,R:0.1,P:0.4']
# Patient 1: TP53 mutation
P1 = speNumberList(1, 40, keys)
P1MC = speMC(P1, 40, keys)
# other Patients: without TP53 mutation
Patients = [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]
allPatients = allNumberList(Patients, 20, keys)
PatientsE = [2,3,5,6,9,13,14,20,21]
allPatientsE = allNumberList(PatientsE, 20, keys)
# plot
fillPlot(P1MC, allPatientsE)






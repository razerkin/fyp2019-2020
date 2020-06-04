import numpy as np
import cvxpy as cp
import pandas as pd
# import shutil
# import time as tii
from ast import literal_eval

# import matplotlib.pyplot as plt
# from PyQt5.QtWidgets import QApplication
# from PyQt5.QtCore import QTimer



class Vt(object):

    def __init__(self):
        self.cvx_param = pd.read_csv('./CSV/Background/PARAM/cvx_param_3.csv')
        self.W = self.cvx_param['W'][0]
        self.n_0 = self.cvx_param['n_0'][0]  # noisePowerDensity
        self.Ui_text = literal_eval(self.cvx_param['Ui'][0])
        self.UiLocal = self.cvx_param['UiLocal'][0]  # computing speed of local device
        self.maxP = self.cvx_param['maxP'][0]  # Power budget of Mobile User
        self.k = self.cvx_param['k'][0]  # Architecture factor
        self.usingBaseStationNumber = self.cvx_param['baseStationNum'][0]  # each Task should has a base station
        self.allBaseStationNumber = self.usingBaseStationNumber + 1
        self.userNumber = self.cvx_param['userNumber'][0]
        self.baseStationGain = literal_eval(self.cvx_param['baseStationGain'][0])
        self.sTotal = literal_eval(self.cvx_param['sTotal'][0])  # [5, 6, 7, 8, 9, 0]  # Total workload of each task
        self.timeMax = literal_eval(self.cvx_param['timeMax'][0])  # [2, 3, 4, 5, 6, 0]  # Max time can be using of each task
    def vtmincvx(self, t=4, matchlist=None, plotcvx=False, workername=None):
        # if matchlist is None:
        #     matchlist = np.array([4, 5, 3, 2, 1, 6])
        # else:
            # print(matchlist)
        Ui = np.mat(np.delete(np.array(self.Ui_text), matchlist[-1] - 1))  # computing speed of each server
        baseStationGain = self.baseStationGain.copy()
        baseStationGain[matchlist[-1] - 1] = ''
        baseStationGain.remove('')
        baseStationGain.sort(reverse=True)  # Reverse sorting the gain of base stations
        sTotal = self.sTotal.copy()  # Total workload of each task
        timeMax = self.timeMax.copy()  # Max time can be using of each task
        sTotalForMap = np.zeros(self.allBaseStationNumber)
        timeMaxForMap = np.zeros(self.allBaseStationNumber)
        # a = np.argwhere(matchlist == 2)
        # print(sTotal[a[0][0]])
        for z in range(len(matchlist)):
            sTotalForMap[z] = sTotal[np.argwhere(matchlist == z + 1)[0][0]]
            timeMaxForMap[z] = timeMax[np.argwhere(matchlist == z + 1)[0][0]]
        sTotalVirtualIndex = np.argwhere(sTotalForMap == 0)
        timeMaxVirtualIndex = np.argwhere(timeMaxForMap == 0)
        if len(sTotalVirtualIndex) > 0:
            sTotalForMap = np.delete(sTotalForMap, sTotalVirtualIndex)
        if len(timeMaxVirtualIndex) > 0:
            timeMaxForMap = np.delete(timeMaxForMap, timeMaxVirtualIndex)
        sTotal = np.mat(sTotalForMap)
        timeMax = np.mat(timeMaxForMap)
        coefficient = []
        for i in range(self.usingBaseStationNumber):
            if i == 0:
                coefficient.append(self.W * self.n_0 * (1 / baseStationGain[i]))
            else:
                coefficient.append(self.W * self.n_0 * (1 / baseStationGain[i] - 1 / baseStationGain[i - 1]))
        coefficient = np.mat(coefficient)
        time = np.arange(0.1, t + 0.01, 0.01)  # time step
        step = time.size
        indexMatrix = np.tril(np.ones((self.usingBaseStationNumber, self.usingBaseStationNumber)), 0)
        vtMin = 100000
        # optimalS = []
        vtPlot = []
        timePlot = []
        # optimalTime = 100000
        # bestStep = 0
        # fig, axes = plt.subplots(nrows=1, ncols=1)
        # axes.set(title="Linear Searching Vtmin", xlim=[0.0, t], ylim=[0, 8], xlabel="Time", ylabel="Vt")
        dataframe = pd.DataFrame({
            'time': timePlot,
            'vt': vtPlot
        }, index=[], columns=['time', 'vt'])
        dataframe.to_csv('./CSV/Background/CVX/' + workername + '_cvx.csv', sep=',')
        for j in range(step):
            tempTime = time[j]
            s = cp.Variable((self.userNumber, self.usingBaseStationNumber))
            constraints_0 = 0
            constraints_1 = 0
            ptot_0 = 0
            ptot_1 = 0
            for z in range(self.usingBaseStationNumber):
                constraints_0 = constraints_0 + (sTotal[0, z] - s[0, z]) / timeMax[0, z]
                constraints_1 = constraints_1 + coefficient[0, z] * cp.exp(
                    cp.log(2) * (1 / tempTime) * (1 / self.W) * s[0, :] * indexMatrix[:, z])
            constraints = [constraints_0 <= self.UiLocal,
                           cp.sum(sTotal - s, 0) >= 0,
                           constraints_1 - self.W * self.n_0 / baseStationGain[self.usingBaseStationNumber - 1] <= self.maxP
                           ]
            for z in range(self.usingBaseStationNumber):
                constraints.append((s[0, z] <= (timeMax[0, z] - tempTime) * Ui[0, z]))
                constraints.append((s[0, z] >= 0))
            for z in range(self.usingBaseStationNumber):
                ptot_0 = ptot_0 + coefficient[0, z] * cp.exp(
                    np.log(2) * (1 / tempTime) * (1 / self.W) * s[0, :] * indexMatrix[:, z])
                ptot_1 = ptot_1 + cp.power((sTotal[0, z] - s[0, z]), 3) * cp.power(1 / timeMax[0, z], 2)
            obj = cp.Minimize(
                (ptot_0 - self.W * self.n_0 / baseStationGain[self.usingBaseStationNumber - 1]) * tempTime + self.k * ptot_1)
            prob = cp.Problem(obj, constraints)
            prob.solve()

            # print("status:", prob.status)
            # print("optimal Value", prob.value)
            # print("s[]", s.value)
            vtMinTemp = prob.value
            vtPlot.append(prob.value)
            timePlot.append(tempTime)
            if vtMinTemp < vtMin:
                vtMin = vtMinTemp
                # optimalS = s.value
                # bestStep = j
                optimalTime = tempTime
            dataframe = pd.DataFrame({
                'time': tempTime,
                'vt': prob.value
            }, index=[j], columns=['time', 'vt'])
            # status = pd.read_csv('./CSV/Background/status.csv',index_col=0)
            # cvx_edit = status.loc[workername]['cvx_edit']
            # while not cvx_edit:
            #     tii.sleep(1)
            #     status = pd.read_csv('./CSV/Background/status.csv',index_col=0)
            #     cvx_edit = status.loc[workername]['cvx_edit']
            dataframe.to_csv('./CSV/Background/CVX/' + workername + '_cvx.csv', sep=',', mode='a', header=False)
        if plotcvx:
            print(vtMin)
            return (timePlot, vtPlot, optimalTime, vtMin)
        else:
            return (vtMin)

        ## matplotlib
        # ImgDisp.CVXUpdate(t=timePlot, prob_value=vtPlot, optimalTime=optimalTime, vtMin=vtMin)
        # axes.plot(time,vtPlot,label="$S^{tot}$ = 4Mbits, $u_{i}$ = 15Mbits/s, $u_{L}^{max}$ = 8Mbits/s")
        # plt.scatter(optimalTime, vtMin, color='red', marker='o')
        # plt.text(optimalTime, vtMin, (optimalTime, vtMin), ha='center', va='bottom', fontsize=10)
        # plt.legend()
        # plt.show()
        # print("Matchlist:", matchlist, "Step: ", bestStep + 1, "  vtMin = ", vtMin, "s = ", optimalS, "optimalTime = ", optimalTime)







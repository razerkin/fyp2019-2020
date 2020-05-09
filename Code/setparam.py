from newtest.param import Ui_Dialog
from PyQt5.QtWidgets import QApplication, QDialog
import pandas as pd
import numpy as np
import math
import random
from ast import literal_eval

import sys

class ImgDisp(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(ImgDisp, self).__init__(parent)
        self.setupUi(self)
        self.InitValue()
        self.tasks_Number = 0
    def InitValue(self):
        #CVX_param
        cvx_param = pd.read_csv('./CSV/Background/cvx_param.csv',sep=',')
        W = cvx_param['W'][0]  # channel bandwidth
        n_0 = cvx_param['n_0'][0]  # noisePowerDensity
        Ui_text = literal_eval(cvx_param['Ui'][0])
        Ui = np.delete(np.array(Ui_text), -1)  # computing speed of each server
        UiLocal = cvx_param['UiLocal'][0]  # computing speed of local device
        maxP = cvx_param['maxP'][0]  # Power budget of Mobile User
        k = cvx_param['k'][0]  # Architecture factor
        usingBaseStationNumber = cvx_param['baseStationNum'][0]  #each Task should has a base station
        userNumber = cvx_param['userNumber'][0]
        baseStationGain = np.delete(np.array(literal_eval(cvx_param['baseStationGain'][0])),-1)
        sTotal = np.delete(np.array(literal_eval(cvx_param['sTotal'][0])), -1)# [5, 6, 7, 8, 9, 0]  # Total workload of each task
        timeMax = np.delete(np.array(literal_eval(cvx_param['timeMax'][0])), -1) #[2, 3, 4, 5, 6, 0]  # Max time can be using of each task
        self.bandwidth_value.setText(str(W))
        self.noisePowerDensity_value.setText(str('n_0'))
        self.serverSpeed_value.setText(str(Ui))
        self.localSpeed_value.setText(str(UiLocal))
        self.powerBudget_value.setText(str(maxP))
        self.architectureFactor_value.setText(str(k))
        self.TasksNumber_value.setText(str(usingBaseStationNumber))
        # print(self.bandwidth_value.setText(allBaseStationNumber))
        self.userNumber_value.setText(str(userNumber))
        self.baseStationGain_value.setText(str(baseStationGain))
        self.sTotal_value.setText(str(sTotal))
        self.timeMax_value.setText(str(timeMax))
        # cvx_LineEdit default value
        self.bandwidth_Edit.setText(str(W))
        self.noisePowerDensity_Edit.setText('10 ** (-8)')
        self.serverSpeed_Edit.setText(str(Ui)[1:-1])
        self.localSpeed_Edit.setText(str(UiLocal))
        self.powerBudget_Edit.setText(str(maxP))
        self.architectureFactor_Edit.setText(str(k))
        self.TasksNumber_Edit.setText(str(usingBaseStationNumber))
        # print(self.bandwidth_value.setText(allBaseStationNumber))
        self.userNumber_Edit.setText(str(userNumber))
        # self.baseStationGain_Edit.setText(str(baseStationGain))
        self.sTotal_Edit.setText(str(sTotal)[1:-1])
        self.timeMax_Edit.setText(str(timeMax)[1:-1])
        # #SA_param
        sa_param = pd.read_csv('./CSV/Background/sa_param.csv')
        sa_tmp = sa_param['tmp'][0]
        sa_tmpMin = sa_param['tmpMin'][0]
        sa_Max_step = sa_param['Max_step'][0]
        sa_Max_Global_EP = sa_param['Max_Global_EP'][0]
        sa_alpha = sa_param['alpha'][0]
        sa_global_Min = sa_param['global_Min'][0]
        sa_baseStationNum = sa_param['baseStationNum'][0]
        sa_allPossible = sa_param['allPossible'][0]
        sa_N_WORKERS = sa_param['N_WORKERS'][0]
        self.tmp_value.setText(str(sa_tmp))
        self.tmpMin_value.setText(str(sa_tmpMin))
        self.maxStep_value.setText(str(sa_Max_step))
        self.maxGlobalEP_value.setText(str(sa_Max_Global_EP))
        self.alpha_value.setText(str(sa_alpha))
        self.globalMin_value.setText(str(sa_global_Min))
        self.baseStationNum_value.setText(str(sa_baseStationNum))
        self.allPossible_value.setText(str(sa_allPossible))
        self.nWorkers_value.setText(str(sa_N_WORKERS))
        # sa_LineEdit default value
        self.tmp_Edit.setText(str(sa_tmp))
        self.tmpMin_Edit.setText(str(sa_tmpMin))
        self.maxStep_Edit.setText(str(sa_Max_step))
        self.maxGlobalEP_Edit.setText(str(sa_Max_Global_EP))
        self.alpha_Edit.setText(str(sa_alpha))
        self.globalMin_Edit.setText(str(sa_global_Min))
        self.baseStationNum_Edit.setText(str(sa_baseStationNum))
        # self.allPossible_Edit.setText(str(sa_allPossible))
        self.nWorkers_Edit.setText(str(sa_N_WORKERS))


        # Connect Function
        self.SummitButton.clicked.connect(self.summit)
        self.baseStationNum_Edit.textChanged.connect(self.allpossible)
        self.GenerateButton.clicked.connect(self.generateGain)
        self.TasksNumber_Edit.textChanged.connect(self.tasksChange)
    def tasksChange(self):
        self.tasks_Number = int(self.TasksNumber_Edit.text())
    def generateGain(self):
        self.StationGain = []
        for i in range(self.tasks_Number + 1):
            self.StationGain.append(random.uniform(0.000000000000001e-06, 9.999999999999999e-06))
        print(self.StationGain)
    def allpossible(self):
        baseStationNum = int(self.baseStationNum_Edit.text())
        allpossible = str(math.factorial(baseStationNum))
        self.allPossiblechange_value.setText(allpossible)

    def summit(self):
        #SA_param
        tmp = int(self.tmp_Edit.text())
        tmpMin = int(self.tmpMin_Edit.text())
        maxStep = int(self.maxStep_Edit.text())
        maxGlobalEP = int(self.maxGlobalEP_Edit.text())
        alpha = np.float(self.alpha_Edit.text())
        globalMin = int(self.globalMin_Edit.text())
        baseStationNum = int(self.baseStationNum_Edit.text())
        nWorkers = int(self.nWorkers_Edit.text())
        sa_dataframe = pd.DataFrame({
            'tmp': [tmp],
            'tmpMin': [tmpMin],
            'Max_step': [maxStep],
            'Max_Global_EP': [maxGlobalEP],
            'alpha': [alpha],
            'global_Min': [globalMin],
            'baseStationNum': [baseStationNum],
            'allPossible': [math.factorial(baseStationNum)],
            'N_WORKERS': [nWorkers]
        })
        sa_dataframe.to_csv('./CSV/Background/sa_param.csv', index=False, sep=',')
        #SA_param END

        #CVX_param
        W = int(self.bandwidth_Edit.text())
        if not self.noisePowerDensity_Edit.text() == '':
            n_0 = eval(self.noisePowerDensity_Edit.text())
        else:
            n_0 = 10 ** (-8)
        Ui_text = self.serverSpeed_Edit.text().split()
        Ui = []
        for i in Ui_text:
            Ui.append(int(i))
        Ui.append(random.randint(1, 20))
        UiLocal = float(self.localSpeed_Edit.text())
        maxP = float(self.powerBudget_Edit.text())
        k = float(self.architectureFactor_Edit.text())
        tasksNumber = int(self.TasksNumber_Edit.text())
        allBaseStationNumber = tasksNumber + 1
        userNumber = int(self.userNumber_Edit.text())
        baseStationGain = []
        # if not self.baseStationGain_Edit.text() == '':
        #     baseStationGain_text = self.baseStationGain_Edit.text().split()
        #     for i in baseStationGain_text:
        #         baseStationGain.append(float(i))
        #     baseStationGain.append(random.uniform(0.000000000000001e-06, 9.999999999999999e-06))
        # else:
        baseStationGain = self.StationGain
        sTotal_text = self.sTotal_Edit.text().split()
        sTotal = []
        for i in sTotal_text:
            sTotal.append(int(i))
        sTotal.append(0)
        timeMax_text = self.timeMax_Edit.text().split()
        timeMax = []
        for i in timeMax_text:
            timeMax.append(int(i))
        timeMax.append(0)
        cvx_dataframe = pd.DataFrame({
            'W': [W],
            'n_0': [n_0],
            'Ui': [Ui],
            'UiLocal': [UiLocal],
            'maxP': [maxP],
            'k': [k],
            'baseStationNum': [tasksNumber],
            'allBaseStationNumber': [allBaseStationNumber],
            'userNumber': [userNumber],
            'baseStationGain': [baseStationGain],
            'sTotal': [sTotal],
            'timeMax': [timeMax]
        })
        cvx_dataframe.to_csv('./CSV/Background/cvx_param.csv', index=False)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = ImgDisp()
    main_window.show()
    sys.exit(app.exec_())
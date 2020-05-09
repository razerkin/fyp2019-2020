import numpy as np
# import matplotlib.pyplot as plt
import math
import random
import CVX as taskDis
# import time as tii
import threading
import queue as Queue
import time
import pandas as pd


param = pd.read_csv('./CSV/Background/sa_param.csv')
tmp = param['tmp'][0]
tmpMin = param['tmpMin'][0]
Max_step = param['Max_step'][0]
Max_Global_EP = param['Max_Global_EP'][0]
Global_EP = 0
alpha = param['alpha'][0]
global_Min = param['global_Min'][0]
# allSeq = []
# allGain = []
baseStationNum = param['baseStationNum'][0]
allPossible = param['allPossible'][0]
N_WORKERS = param['N_WORKERS'][0]
que = Queue.Queue()
cLock = threading.Condition()

class Sa:

    def judge(self, delta, tmp):
        if delta < 0:
            tmp_0 = tmp * alpha
            return 1, tmp_0
        else:
            probability = math.exp(- delta / tmp)
            if probability > random.random():
                tmp_0 = tmp * 1
                return 1, tmp_0
            else:
                tmp_0 = tmp * 1
                return 0, tmp_0

    def disturbance(self, old):
        sample = random.sample(old, 2)
        randomElement_0, randomElement_1 = sample[0], sample[1]
        new = list(np.zeros(6))
        for i in range(len(old)):
            new[i] = old[i]
        index_0, index_1 = old.index(randomElement_0), old.index(randomElement_1)
        new[index_0], new[index_1] = old[index_1], old[index_0]
        return new

    def reNew(self, old, lenOfSeq, delta=None):

        if lenOfSeq == allPossible:
            return False
        elif delta is not None:
            new = list(np.zeros(6))
            probability = math.exp(- delta / tmp)
            if probability > random.random():
                for i in range(len(old)):
                    new[i] = old[i]
                    return new
        else:
            gen = np.random.random(3)
            gen = np.argsort(gen)
            sample = random.sample(old, 3)
            randomElement_0, randomElement_1, randomElement_2 = sample[0], sample[1], sample[2]
            index_0, index_1, index_2 = old.index(randomElement_0), \
                                        old.index(randomElement_1), \
                                        old.index(randomElement_2)
            indexarray = [index_0, index_1, index_2]
            new = list(np.zeros(6))
            for i in range(len(old)):
                new[i] = old[i]
            new[indexarray[gen[0]]], new[indexarray[gen[1]]], new[indexarray[gen[2]]] = randomElement_0, \
                                                                                        randomElement_1, \
                                                                                        randomElement_2
            return new

    def emi(self, seq, worker_name):
        timePlot, vtPlot, optimalTime, vtMin = cvx.vtmincvx(matchlist=seq, plotcvx=True,workername=worker_name)
        # self.update_cvx_csv(timePlot, vtPlot, worker_name)
        return vtMin
        # if worker_name == 'Worker_0':
        #     timePlot, vtPlot, optimalTime, vtMin= cvx.vtmincvx(matchlist=seq, CVXSignal=CVXSignal, plotcvx=True)
        #
        # else:
        #     vtMin = cvx.vtmincvx(matchlist=seq, CVXSignal=None, plotcvx=False)
        #
        # return vtMin

    def reset(self):
        firstSeq = np.random.random(baseStationNum)
        firstSeq = np.argsort(firstSeq) + 1
        Seq = list(firstSeq)
        return Seq

    def update_cvx_csv(self,timePlot, vtPlot, worker_name):
        dataframe = pd.DataFrame({
            'time': timePlot,
            'vt': vtPlot
                                  })
        Status = pd.read_csv('./CSV/Background/Status.csv', index=False, sep=',',index_col=0)
        cvx_edit = Status[worker_name][2]
        while not cvx_edit:
            time.sleep(5)
            Status = pd.read_csv('./CSV/Background/Status.csv', index=False, sep=',',index_col=0)
            cvx_edit = Status[worker_name][2]
        dataframe.to_csv('./CSV/Background/CVX/' + worker_name + '_cvx.csv', index=False, sep=',')

    def __init__(self):
        return


class Worker:
    def __init__(self, name):
        self.name = name
        self.local_Min = 10000
        self.local_bestSeq = []
        self.local_allGain = []
        self.start_time = time.time()
    def get_result(self):
        try:
            return self.local_bestSeq, self.local_Min
        except Exception:
            return None
    def work(self):
        global Global_EP
        local_Seq = []
        bestStep = 0
        while Global_EP < Max_Global_EP:
            old = sa.reset()
            result = sa.emi(np.array(old),  worker_name=self.name)
            step = 0
            local_step = [0]
            if result < self.local_Min:
                self.local_Min = result
                self.local_bestSeq = old
                local_Seq.append(old)
                self.local_allGain.append(result)
            dataframe = pd.DataFrame({
                'step': local_step,
                'Sequence': [old],
                'Gain': result,
            })
            dataframe.to_csv('./CSV/Background/SA/' + self.name + '_SA.csv', index=False)
            # print(local_Seq)
            localTmp = 300
            counter = 0
            # if self.name == "Worker_0":
            #     SASignal.emit(local_step, self.local_allGain, self.local_Min, bestStep, self.name)
            while localTmp >= tmpMin and len(local_Seq) < allPossible and step <= Max_step:
                new = sa.disturbance(old)
                if new in local_Seq:
                    print("had tried : ", new)
                    new = sa.reNew(old,len(local_Seq))
                    if not new:
                        print("Tried All possible.")
                        break
                if new not in local_Seq:
                    result_new = sa.emi(np.array(new), worker_name=self.name)
                    local_Seq.append(new)
                    local_step.append(step+1)
                    self.local_allGain.append(result_new)
                    delta = result_new - result
                    judgement, localTmp = sa.judge(delta, localTmp)
                    if judgement == 1:
                        result = result_new
                        if result < self.local_Min:
                            self.local_Min = result
                            self.local_bestSeq = new
                            bestStep = step
                        old = new
                    else:
                        counter += 1
                        print("Counter = ", counter)
                    # ImgDisp.SAUpdate(ImgDisp=ImgDisp, SAFigure=Fig, step=local_step, local_gain=result_new,
                    #                  local_min=self.local_Min, min_step=bestStep, worker_name=self.name)
                    step += 1
                    dataframe = pd.DataFrame({
                        'step': step,
                        'Sequence': [new],
                        'Gain': result_new,
                    })
                    dataframe.to_csv('./CSV/Background/SA/' + self.name + '_SA.csv', index=False, mode='a', header=False)
                    # if self.name == "Worker_0":
                    #     SASignal.emit(local_step, self.local_allGain, self.local_Min, bestStep, self.name)
                    print("Worker", self.name, "MatchList:", new, " Gain:", result_new, " Tmp: ", localTmp,
                          " Gain_Min:", self.local_Min, " BestSeq: ", self.local_bestSeq, "Step:", step)
            total_time = time.time() - self.start_time
            que.put((self.local_bestSeq, self.local_Min))
            Global_EP += 1
            print("Finish===> Tmp = ", localTmp, " Gain_Min = ", self.local_Min,
                  " BestSeq ", self.local_bestSeq, "BestTmp", bestStep, 'time_cost:%s' % total_time, "Tried times ",
                  len(local_Seq), "EP = ", Global_EP)
            # print("ggggggggggggggggggggggggggggggggggggggggggg=======", Global_EP)
        # cLock.acquire()
        # cLock.notify_all()
        # cLock.release()
        # return self.local_Min, self.local_bestSeq
        # for i in range(len(local_Seq)):
        #     if local_Seq[i] not in allSeq:
        #         allSeq.append(local_Seq[i])
        #         allGain.append(local_allGain[i])



if __name__ == "__main__":
    cvx = taskDis.Vt()
    sa = Sa()
    workers = []
    for i in range(N_WORKERS):
        i_name = 'Worker_%i' % i  # worker name
        workers.append(Worker(i_name))
    worker_threads = []
    for worker in workers:
        job = lambda: worker.work()
        t = threading.Thread(target=job)
        t.start()
        worker_threads.append(t)
    for i in worker_threads:
        i.join()
    bestSeq = []
    best_min = 10000
    resultCollection = list()
    while not que.empty():
        resultCollection.append(que.get())
    for item in resultCollection:
        if item[1] < best_min:
            best_min = item[1]
            bestSeq = item[0]
    print(resultCollection)
    print(bestSeq, best_min)
    #
    # sys.exit(app.exec_())

    # app = QApplication(sys.argv)
    # ui = ImgDisp()
    # ui.show()
    # start_time = time.time()
    # old = sa.reset()
    # print(old)
    # result = sa.emi(np.array(old))
    # global_Min = result
    # bestSeq = [[old]]
    # bestStep = 0
    # step = 0
    # allSeq.append(old)
    # allGain.append(result)
    # print(allSeq)
    # counter = 0
    # worker = Worker('a')
    # worker_min, worker_seq = worker.work()


    #
    #
    # while tmp >= tmpMin and len(allSeq) < allPossible:
    #     new = sa.disturbance(old)
    #     if new in allSeq:
    #         print("had tried : ", new)
    #         new = sa.reNew(old)
    #         if not new:
    #             print("Tried All possible.")
    #             break
    #     if new not in allSeq:
    #         result_new = sa.emi(np.array(new))
    #         allSeq.append(new)
    #         allGain.append(result_new)
    #         delta = result_new - result
    #         judgement, tmp = sa.judge(delta, tmp)
    #         step += 1
    #         if judgement == 1:
    #             result = result_new
    #             if result < global_Min:
    #                 global_Min = result
    #                 bestSeq = new
    #                 bestStep = step
    #             old = new
    #         else:
    #             counter += 1
    #             print("Counter = ", counter)
    #         print("MatchList:", new, " Gain:", result_new, " Tmp: ", tmp, " \nGain_Min:", global_Min,
    #               " BestSeq: ", bestSeq, " Counter:", counter, "Step:", step)
    # total_time = time.time() - start_time
    # print('time_cost:%s' % total_time, "Tried times ", len(allSeq))
    # print(" Tmp = ", tmp, " \nGain_Min = ", global_Min, " BestSeq ", bestSeq, "BestTmp", bestStep)
    # print("Finish!")

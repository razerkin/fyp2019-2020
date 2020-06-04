----------------
|Code
    | -- CVX.py                         process the EEO-algorithm  by CVX toolbox.
    | -- SA.py                          process SA algorithm to find the best scheme.
    | -- setparam.py                    Custom parameters by user input.
    | -- dashtest.py                    show the result data and process. 
    | -- fullArrarangement.py           get all possible scheme under a set of parameters.
    | -- plotCVX.py                     plot the linear searching figure of EEO-algorithm.
    |CSV    |                           The folder to save result/parameters.
            |   CVX                     The folder to save the result of EEO-algorithm.
            |   SA                      The folder to save the result of SA-algorithm.
            |   GLOBAL                  The folder to save the global optimal result of each iterates.
            |   PARAM
                    | -- cvx_param.csv  cvx parameters.
                    | -- sa_param.csv   sa  parameters.
    |Meeting                            The folder to save the meeting records.
|report_groupJ_DB426406.LI KIN TAK.docx The final resport of this project.
|poster_GroupJ                          The poster of this project.



How to use:
1.Install all the packages in your python environment:
pip numpy cvxpy pandas ast itertools multiprocessing plotly dash

2.Edit the path of the parameters CSV file at line 19,55,125,171 in setParam.py and set the parameters in the interface. 
python setParam.py
3.Edit the CSV files path in CVX.py at line 10,65,102.
4.Edit the CSV files path in SA.py at line 12,155,197,231,250.
5.Call the SA.py
python SA.py
6.Edit the path in webUI.py at line 11,51,84,85,94,116,117,123.Then call the interface to show algorithm process.Open the link which return by python console.
python webUI.py
7.Edit the path of CSV file in fullArrangement.py to generate the result of all possible scheme.
python fullArrangement.py.
8.For the linear searching figure, use plotCVX.py to plot. Copy the parameters CSV files which you want to plot (cvx_param_'X'.csv) and rename to (cvx_param_'X'_'st')Edit the paramenters before plot. Edit the matching scheme at line 116-120. For Vt class, es is the using basestation number, st is the total workload that we set. Then call the plotCVX.py.
python plotCVX.py





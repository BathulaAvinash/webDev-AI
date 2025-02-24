import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sn
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from io import BytesIO
from flask import Flask, render_template,Response,send_file,request
import base64
import csv
from scipy.stats import pearsonr
from sklearn import preprocessing


app = Flask(__name__)





@app.route('/option', methods=["GET", "POST"])
def result():
    global opt, l
    if request.method == "POST":
        opt = request.form.get("opt")
        with open(opt) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            temp_l = []
            for row in csv_reader:
                temp_l.append(row)
                break
            l = temp_l[0]
        return 'option you have selected is '+opt + ' click the link click on link <a href="http://127.0.0.1:5000/choice">http://127.0.0.1:5000/choice</a> '
    return render_template('index2.html')


#if opt == 'bank.csv':
# with open(opt) as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     temp_l = []
#     for row in csv_reader:
#         temp_l.append(row)
#         break
#     l = temp_l[0]
# else:
#     with open('diabetes.csv') as csv_file:
#         csv_reader = csv.reader(csv_file, delimiter=',')
#         temp_l = []
#         for row in csv_reader:
#             temp_l.append(row)
#             break
#         l = temp_l[0]


@app.route('/choice',methods=["POST", "GET"])
def choice():
    global b, c, ind_x, ind_y
    if request.method == "POST":
        choice_1 = request.form.get("choice1")
        b = choice_1
        choice_2 = request.form.get("choice2")
        c = choice_2
        if b and c == 'none':
            df_temp = pd.read_csv(opt)
            cormat = df_temp.corr()
            round(cormat, 2)
            upper_corr_matrix = cormat.where(np.triu(np.ones(cormat.shape), k=1).astype(np.bool_))
            unique_corr_pairs = upper_corr_matrix.unstack().dropna()
            sorted_mat = unique_corr_pairs.sort_values()
            df = sorted_mat.to_frame()
            df = df.reset_index()
            df.columns = ['Row','Column','Value']
            b = df.iloc[-1].at['Row']
            c = df.iloc[-1].at['Column']
        ind_x = l.index(b)
        ind_y = l.index(c)
        return 'click on link <a href="http://127.0.0.1:5000/test1">http://127.0.0.1:5000/test1</a>' + '' + b + ' ' + c
    return render_template('index3.html', l=l)


@app.route('/test1')
def test1():
    img = BytesIO()
    img2 = BytesIO()
    fig = Figure()
    fig2 = Figure()
    df1 = pd.read_csv(opt)
    if type(df1[c][0]) == type('string'):
        lable_encoder = preprocessing.LabelEncoder()
        df1[c] = lable_encoder.fit_transform(df1[c])
        df1[c].unique()
    elif type(df1[b][0]) == type('string'):
        lable_encoder = preprocessing.LabelEncoder()
        df1[b] = lable_encoder.fit_transform(df1[b])
        df1[b].unique()
    y_axis = df1[c]
    x_axis = df1[b]
    plt.scatter(x_axis,y_axis)
    plt.savefig(img2, format='png')
    img2.seek(0)
    plot_url2 = base64.b64encode(img2.getvalue()).decode('utf8')
    plt.scatter(x_axis, y_axis)
    x = df1.iloc[:,[ind_x, ind_y]].values
    k = range(10,90,5)
    sse = []
    for i in k:
        model_demo = KMeans(n_clusters=i,random_state=0)
        model_demo.fit(x)
    sse.append(model_demo.inertia_) 
    k = range(10,90,10)
    score=[]
    for i in k:
        model_demo = KMeans(n_clusters=i,random_state=0)
        model_demo.fit(x)
        y = model_demo.predict(x)
        # print(f"{i} clusters, Score = {silhouette_score(x,y)}")
        score.append(silhouette_score(x,y))
        plt.bar(i,silhouette_score(x,y))
    k = 5  
    model = KMeans(n_clusters=k,random_state=0)
    model.fit(x)
    y = model.predict(x)
    np.unique(y,return_counts=True)
    plt.figure(figsize=(15,7))
    for i in range(k):
        plt.scatter(x[y == i,0],x[y == i,1],s=90,label=f'Cluster {i}')
    plt.scatter(model.cluster_centers_[:,0],model.cluster_centers_[:,1], label='Centroids',s=250, marker='^',c='black')
    plt.legend() 
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    return render_template('index.html',plot_url=plot_url,score=score,plot_url2=plot_url2)
















































# from calendar import c
# from turtle import title
# import pandas as pd
# import numpy as np
# import matplotlib
# matplotlib.use('Agg')
# import matplotlib.pyplot as plt
# import seaborn as sn
# from sklearn.cluster import KMeans
# from sklearn.metrics import silhouette_score
# from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
# from matplotlib.figure import Figure
# from io import BytesIO
# from flask import Flask, render_template,Response,send_file,request
# import base64
# import csv
# from scipy.stats import pearsonr
# from sklearn import preprocessing

# with open('bank.csv') as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter = ',')
#     temp_l1 = []
#     for row in csv_reader:
#         temp_l1.append(row)
#         break


# with open('diabetes.csv') as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter = ',')
#     temp_l2 = []
#     for row in csv_reader:
#         temp_l2.append(row)
#         break

# l1 = temp_l1[0]
# l2 = temp_l2[0]

# app = Flask(__name__)


# @app.route('/option', methods=["GET", "POST"])
# def result():
#     global opt
#     if request.method == "POST":
#         opt = request.form.get("opt")
#         return 'option you have selected is '+ opt + 'click the link click on link <a href="http://127.0.0.1:5000/choice">http://127.0.0.1:5000/choice</a> '
#     return render_template('index2.html')



# @app.route('/choice', methods=["POST", "GET"])
# def choice():
#     global b,c,ind_x,ind_y
#     if opt == 'test':
#         if request.method == "POST":
#             choice_1 = request.form.get("choice1")
#             b = choice_1
#             choice_2 = request.form.get("choice2")
#             c = choice_2
#             if(b and c == 'none'):
#                 df_temp = pd.read_csv('bank.csv')
#                 cormat = df_temp.corr()
#                 round(cormat, 2)
#                 upper_corr_matrix = cormat.where(np.triu(np.ones(cormat.shape), k=1).astype(np.bool_))
#                 unique_corr_pairs = upper_corr_matrix.unstack().dropna()
#                 sorted_mat = unique_corr_pairs.sort_values()
#                 df = sorted_mat.to_frame()
#                 df = df.reset_index()
#                 df.columns = ['Row','Column','Value']
#                 b = df.iloc[-1].at['Row']
#                 c = df.iloc[-1].at['Column']
#             ind_x = l1.index(b)
#             ind_y = l1.index(c)
#             return 'click on link <a href="http://127.0.0.1:5000/test1">http://127.0.0.1:5000/test1</a>' + '' + b + ' ' + c
#         return render_template('index3.html', l=l1)
#     if opt == 'best':
#         if request.method == "POST":
#             choice_1 = request.form.get("choice1")
#             b = choice_1
#             choice_2 = request.form.get("choice2")
#             c = choice_2
#             if(b and c == 'none'):
#                 df_temp = pd.read_csv('diabetes.csv')
#                 cormat = df_temp.corr()
#                 round(cormat, 2)
#                 upper_corr_matrix = cormat.where(np.triu(np.ones(cormat.shape), k=1).astype(np.bool_))
#                 unique_corr_pairs = upper_corr_matrix.unstack().dropna()
#                 sorted_mat = unique_corr_pairs.sort_values()
#                 df = sorted_mat.to_frame()
#                 df = df.reset_index()
#                 df.columns = ['Row','Column','Value']
#                 b = df.iloc[-1].at['Row']
#                 c = df.iloc[-1].at['Column']
#             ind_x = l2.index(b)
#             ind_y = l2.index(c)
#             return 'click on link click on link <a href="http://127.0.0.1:5000/test2">http://127.0.0.1:5000/test2</a>' + ' ' + b + ' ' + c
#         return render_template('index3.html', l=l2)


# @app.route('/test1')
# def test1():
#     img = BytesIO()
#     img2 = BytesIO()
#     fig = Figure()
#     fig2 = Figure()
#     df1 = pd.read_csv("bank.csv")
#     # lable_encoder = preprocessing.LabelEncoder()
#     # df1['poutcome'] = lable_encoder.fit_transform(df1['poutcome'])
#     # df1['poutcome'].unique()
#     y_axis = df1[c]
#     x_axis = df1[b]
#     plt.scatter(x_axis,y_axis)
#     #plt.hist(x_axis,rwidth=0.7)
#     plt.savefig(img2, format='png')
#     img2.seek(0)
#     plot_url2 = base64.b64encode(img2.getvalue()).decode('utf8')
#     plt.scatter(x_axis, y_axis)
#     x = df1.iloc[:,[ind_x, ind_y]].values
#     k=range(10,90,5)
#     sse = []
#     for i in k:
#         model_demo = KMeans(n_clusters=i,random_state = 0)
#         model_demo.fit(x)
#     sse.append(model_demo.inertia_) 
#     k = range(10,90,10)
#     score=[]
#     for i in k:
#         model_demo = KMeans(n_clusters=i,random_state=0)
#         model_demo.fit(x)
#         y = model_demo.predict(x)
#         #print(f"{i} clusters, Score = {silhouette_score(x,y)}") 
#         score.append(silhouette_score(x,y))
#         plt.bar(i,silhouette_score(x,y))
#     k = 5  
#     model = KMeans(n_clusters=k,random_state = 0)
#     model.fit(x)
#     y = model.predict(x)
#     np.unique(y,return_counts=True)
#     plt.figure(figsize=(15,7))
#     for i in range(k):
#         plt.scatter(x[y == i,0],x[y == i,1],s=90,label = f'Cluster {i}')
#     plt.scatter(model.cluster_centers_[:,0],model.cluster_centers_[:,1], label = 'Centroids',s = 250, marker = '^',c='black')
#     plt.legend() 
#     plt.savefig(img, format='png')
#     plt.close()
#     img.seek(0)
#     plot_url = base64.b64encode(img.getvalue()).decode('utf8')
#     return render_template('index.html',plot_url=plot_url,score=score,plot_url2=plot_url2)


# @app.route('/test2')
# def test2():
#     img = BytesIO()
#     img2 = BytesIO()
#     fig = Figure()
#     fig2 = Figure()
#     df2 = pd.read_csv("diabetes.csv")
#     y_axis = df2[c]
#     x_axis = df2[b]
#     plt.scatter(x_axis,y_axis)
#     #plt.hist(x_axis, rwidth=0.7)
#     plt.savefig(img2, format='png')
#     img2.seek(0)
#     plot_url2 = base64.b64encode(img2.getvalue()).decode('utf8')
#     plt.scatter(x_axis, y_axis)
#     x = df2.iloc[:,[ind_x, ind_y]].values
#     k=range(10,90,5)
#     sse = []
#     for i in k:
#         model_demo = KMeans(n_clusters=i,random_state = 0)
#         model_demo.fit(x)
#     sse.append(model_demo.inertia_) 
#     k = range(10,90,10)
#     score=[]
#     for i in k:
#         model_demo = KMeans(n_clusters=i,random_state=0)
#         model_demo.fit(x)
#         y = model_demo.predict(x)
#         print(f"{i} clusters, Score = {silhouette_score(x,y)}") 
#         score.append(silhouette_score(x,y))
#         plt.bar(i,silhouette_score(x,y))
#     k = 5  
#     model = KMeans(n_clusters=k,random_state = 0)
#     model.fit(x)
#     y = model.predict(x)
#     np.unique(y,return_counts=True)
#     plt.figure(figsize=(15,7))
#     for i in range(k):
#         plt.scatter(x[y == i,0],x[y == i,1],s=90,label = f'Cluster {i}')
#     plt.scatter(model.cluster_centers_[:,0],model.cluster_centers_[:,1], label = 'Centroids',s = 250, marker = '^',c='black')
#     plt.legend() 
#     plt.savefig(img, format='png')
#     plt.close()
#     img.seek(0)
#     plot_url = base64.b64encode(img.getvalue()).decode('utf8')
#     return render_template('index.html',plot_url=plot_url,score=score,plot_url2=plot_url2)




# @app.route('/result')
# def result():
    # img = BytesIO()
    # fig = Figure()
    # df1 = pd.read_csv("bank.csv")
    # df2 = pd.read_csv("diabetes.csv")
    # y = df1["balance"]
    # x = df1["age"]
    # plt.scatter(x, y)
    # plt.ylabel("balance")
    # plt.xlabel("age")
    # x = df2.iloc[:,[0,5]].values
    # k=range(10,90,5)
    # sse = []
    # for i in k:
    #     model_demo = KMeans(n_clusters=i,random_state = 0)
    #     model_demo.fit(x)
    # sse.append(model_demo.inertia_) 
    # k = range(10,90,10)
    # score=[]
    # for i in k:
    #     model_demo = KMeans(n_clusters=i,random_state=0)
    #     model_demo.fit(x)
    #     y = model_demo.predict(x)
    #     print(f"{i} clusters, Score = {silhouette_score(x,y)}") 
    #     score.append(silhouette_score(x,y))
    #     plt.bar(i,silhouette_score(x,y))
    # k = 5  
    # model = KMeans(n_clusters=k,random_state = 0)
    # model.fit(x)
    # y = model.predict(x)
    # np.unique(y,return_counts=True)
    # plt.figure(figsize=(15,7))
    # for i in range(k):
    #     plt.scatter(x[y == i,0],x[y == i,1],s=90,label = f'Cluster {i}')
    # plt.scatter(model.cluster_centers_[:,0],model.cluster_centers_[:,1], label = 'Centroids',s = 250, marker = '^',c='black')
    # plt.legend() 
    # plt.savefig(img, format='png')
    # plt.close()
    # img.seek(0)
    # plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    # return render_template('index.html',plot_url=plot_url,score=score)


if __name__ == '__main__':
   app.run(debug=True)

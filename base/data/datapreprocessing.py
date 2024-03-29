# -*- coding: utf-8 -*-
"""

Created on Thu Dec 30 16:45:30 2021

@author: praji
"""
from __future__ import print_function,division
import time
import numpy as np
#import tensorflow as tf
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.ensemble import RandomForestClassifier,RandomForestRegressor
from sklearn.ensemble import GradientBoostingClassifier, GradientBoostingRegressor
from sklearn.ensemble import AdaBoostClassifier, AdaBoostRegressor
#import xgboost as xgb1
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.metrics import confusion_matrix, accuracy_score,precision_score,recall_score
from matplotlib.colors import ListedColormap
from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from builtins import range,input
#import util
from scipy.stats import multivariate_normal as mvn
from sklearn.mixture import BayesianGaussianMixture
import tensorflow as tf
import seaborn as sns
import joblib
import warnings
warnings.filterwarnings('ignore',category = FutureWarning)
warnings.filterwarnings('ignore',category = DeprecationWarning)


np.random.seed(1234)
#tf.random.set_seed(1234)
sc=StandardScaler()
class Datapreprocessing:
    def __init__(self,x,y,label,label1):
        self.X=x
        self.Y=y
        self.label=label
        self.label1=label1

    def data_visualizelr(X,Y):
        sns.set_style('whitegrid')
        sns.distplot(X, kde = False, color ='red', bins = 10)
        plt.show()
        sns.distplot(Y, kde = False, color ='blue', bins = 10)
        plt.show()
        D1=np.concatenate((X,Y),axis=1)
        print(np.shape(D1))
        df = pd.DataFrame(D1, columns=["x", "y"]) 
        print(df)
        d1 = df.iloc[0:2, :]
        sns.lmplot(x ="x", y ="y",data=d1)
        plt.show()
        
        
            
    def datawrangling(data1,tot):
        data1.isnull().sum()   # counts each missing value in the data

        data1[:,1].fillna(data1[:,1].mean(), inplace=True)   # fills NA with group average, inplace=true means replaces the original data

        data1.head(10)


        for i,col in enumerate(['SibSp','Parch']):
          plt.figure(i)
          sns.catplot(x=col,y='Survived', data=data1, kind='point', aspect=2)       # plotting survival rate with family count

        data1['Family_cnt']=data1['SibSp']+data1['Parch']                           # joining data of sibling spouse, parent children into
                                                                                    # family count
        
        data1.drop(['PassengerId', 'SibSp','Parch'], axis=1, inplace=True)

        data1.head()

        print(data1)

        data1.groupby(data1['Cabin'].isnull())['Survived'].mean()                   # gouping based on average of survival for data with cabin
                                                                                    # data without cabin


        data1['Cabin_id']=np.where(data1['Cabin'].isnull(),0,1)                     # create cabin category variable based on cabin data available/not
        
        
        gender_num = {'male': 0 ,'female': 1}                                       # create dictionary for male and female

        data1['Sex']= data1['Sex'].map(gender_num)            

        data1.drop(['Cabin','Embarked','Name','Ticket'], axis=1, inplace =True)

        print(data1)

        data1.to_csv('/content/sample_data/titanic_cleaned.csv', index= False)                      
        
        return data1


    def train_test_splitlr(X,Y):
        X_train,X_test1,Y_train,Y_test1=train_test_split(X,Y,test_size=0.10,random_state=0)
        X_val,X_test,Y_val,Y_test = train_test_split(X_test1,Y_test1,test_size=0.50,random_state=0)

        X_train=X_train.reshape(-1,1)
        Y_train=Y_train.reshape(-1,1)
        X_test = X_test.reshape(-1,1)
        Y_test = Y_test.reshape(-1,1)

        return X_train,X_test,Y_train,Y_test

    def train_test_splitmlr(X,Y):
        X_train,X_test1,Y_train,Y_test1=train_test_split(X,Y,test_size=0.10,random_state=0)
        X_val,X_test,Y_val,Y_test = train_test_split(X_test1,Y_test1,test_size=0.50,random_state=0)

        return X_train,X_test,Y_train,Y_test  
    
    def train_test_splitlogr(X,Y):
        X_train,X_test1,Y_train,Y_test1=train_test_split(X,Y,test_size=0.10,random_state=0)
        X_val,X_test,Y_val,Y_test = train_test_split(X_test1,Y_test1,test_size=0.50,random_state=0)
        Y_train=Y_train.reshape(-1,1)
        Y_test = Y_test.reshape(-1,1)

        return X_train,X_test,Y_train,Y_test   
  

    def SVM (self, X_train,Y_train,X_test,Y_test):
        parameters = {'C':[ 0.1, 1, 10],
                      'kernel': [ 'linear', 'rbf']}                       # kernel parameter for SVM only

        svc = SVC( random_state=0)
        cv1=self.Grid_search(svc,parameters, X_train, Y_train)
        print(cv1.best_estimator_)
        joblib.dump(cv1.best_estimator_,'/content/sample_data/SVM_model.pkl')

        reconstructed_model = joblib.load('/content/sample_data/SVM_model.pkl')
        ypred_train=reconstructed_model.predict(X_train)
        ypred_train=sc.inverse_transform(ypred_train)
        ypred_test = reconstructed_model.predict(X_test)
        ypred_test=sc.inverse_transform(ypred_test)
        y_train = sc.inverse_transform(Y_train)
        y_test = sc.inverse_transform(Y_test)

        print(ypred_test)


    def MLPRegressor (self, X_train,Y_train,X_test,Y_test):
        parameters = {'hidden_layer_sizes':[(10,1), (50,2), (100,3)],            
                      'activation': [ 'relu', 'tanh','logistic'],                              # (10,1) 10 neurons 1 layer
                      'learning_rate': ['constant','invscaling','adaptive']}                                     # lr,act parameter for MLP only

        mlp = MLPRegressor( random_state=0)
        cv1=self.Grid_search(mlp,parameters, X_train, Y_train)
        print(cv1.best_estimator_)
        joblib.dump(cv1.best_estimator_,'/content/sample_data/MLPR_model.pkl')

        reconstructed_model = joblib.load('/content/sample_data/MLPR_model.pkl')
        ypred_train=reconstructed_model.predict(X_train)
        ypred_train=sc.inverse_transform(ypred_train)
        ypred_test = reconstructed_model.predict(X_test)
        ypred_test=sc.inverse_transform(ypred_test)
        y_train = sc.inverse_transform(Y_train)
        y_test = sc.inverse_transform(Y_test)

        print(ypred_test)


    def MLPClassifier (self, X_train,Y_train,X_test,Y_test):
        parameters = {'hidden_layer_sizes':[(10,1), (50,2), (100,3)],            
                      'activation': [ 'relu', 'tanh','logistic'],                              # (10,1) 10 neurons 1 layer
                      'learning_rate': ['constant','invscaling','adaptive']}                                     # lr,act parameter for MLP only

        mlp = MLPClassifier( random_state=0)
        cv1=self.Grid_search(mlp,parameters, X_train, Y_train)
        print(cv1.best_estimator_)
        joblib.dump(cv1.best_estimator_,'/content/sample_data/MLPC_model.pkl')

        reconstructed_model = joblib.load('/content/sample_data/MLPC_model.pkl')
        ypred_train=reconstructed_model.predict(X_train)
        ypred_train=sc.inverse_transform(ypred_train)
        ypred_test = reconstructed_model.predict(X_test)
        ypred_test=sc.inverse_transform(ypred_test)
        y_train = sc.inverse_transform(Y_train)
        y_test = sc.inverse_transform(Y_test)

        print(ypred_test)


    def RFC (self, X_train,Y_train,X_test,Y_test):
        parameters = {'n_estimators':[ 5, 50, 250],
                      'max_depth': [ 2, 4, 8, 16, 32, 64, None]}                       # kernel parameter for SVM only

        rf = RandomForestClassifier(random_state=0 )
        cv1=self.Grid_search(rf,parameters, X_train, Y_train)
        print(cv1.best_estimator_)
        joblib.dump(cv1.best_estimator_,'/content/sample_data/RFC_model.pkl')

        reconstructed_model = joblib.load('/content/sample_data/RFC_model.pkl')
        ypred_train=reconstructed_model.predict(X_train)
        ypred_train=sc.inverse_transform(ypred_train)
        ypred_test = reconstructed_model.predict(X_test)
        ypred_test=sc.inverse_transform(ypred_test)
        y_train = sc.inverse_transform(Y_train)
        y_test = sc.inverse_transform(Y_test)

        print(ypred_test)


    def RFR (self, X_train,Y_train,X_test,Y_test):
        parameters = {'n_estimators':[ 10, 100, 250],
                      'max_depth': [ 2,4,8,16,32,64,],
                      'criterion': ['squared_error','absolute_error','poisson'],
                      'min_samples_split':[2,4,8,32,64,128],
                      'min_samples_leaf': [2,4,8,32,64,128],
                      'n_jobs': [2,4]
                      }                       # kernel parameter for SVM only

        rf = RandomForestRegressor( random_state=0)
        cv1=self.Grid_search(rf,parameters, X_train, Y_train)
        print(cv1.best_estimator_)
        joblib.dump(cv1.best_estimator_,'/content/sample_data/RFR_model.pkl')

        reconstructed_model = joblib.load('/content/sample_data/RFR_model.pkl')
        ypred_train=reconstructed_model.predict(X_train)
        ypred_train=sc.inverse_transform(ypred_train)
        ypred_test = reconstructed_model.predict(X_test)
        ypred_test=sc.inverse_transform(ypred_test)
        y_train = sc.inverse_transform(Y_train)
        y_test = sc.inverse_transform(Y_test)

        print(ypred_test)

    def GB (self, X_train,Y_train,X_test,Y_test):
        parameters = {'n_estimators':[ 10, 100, 250],
                      'max_depth': [ 2,4,8,16,32,64,],
                      'learning_rate': [0.1, 0.01, 0.001]  
                      }                                        # learning rate is constant throughout

        gb = GradientBoostingRegressor( random_state=0)
        cv1=self.Grid_search(gb,parameters, X_train, Y_train)
        print(cv1.best_estimator_)
        joblib.dump(cv1.best_estimator_,'/content/sample_data/GB_model.pkl')

        reconstructed_model = joblib.load('/content/sample_data/GB_model.pkl')
        ypred_train=reconstructed_model.predict(X_train)
        ypred_train=sc.inverse_transform(ypred_train)
        ypred_test = reconstructed_model.predict(X_test)
        ypred_test=sc.inverse_transform(ypred_test)
        y_train = sc.inverse_transform(Y_train)
        y_test = sc.inverse_transform(Y_test)

        print(ypred_test)

    def ADAB (self, X_train,Y_train,X_test,Y_test):
        parameters = {'n_estimators':[ 10, 100, 250],
                      'loss': [ 'linear','square','exponential'],    # for claasifier loss is not there instead algorithm SAMME SAMMER
                      'learning_rate': [0.1, 0.01, 0.001]
                      }                                              # learning rate is constant throughout

        adab = AdaBoostRegressor( random_state=0)
        cv1=self.Grid_search(adab,parameters, X_train, Y_train)
        print(cv1.best_estimator_)
        joblib.dump(cv1.best_estimator_,'/content/sample_data/ADAB_model.pkl')

        reconstructed_model = joblib.load('/content/sample_data/ADAB_model.pkl')
        ypred_train=reconstructed_model.predict(X_train)
        ypred_train=sc.inverse_transform(ypred_train)
        ypred_test = reconstructed_model.predict(X_test)
        ypred_test=sc.inverse_transform(ypred_test)
        y_train = sc.inverse_transform(Y_train)
        y_test = sc.inverse_transform(Y_test)

        print(ypred_test)

    def XGB (self, X_train,Y_train,X_test,Y_test):
        parameters = {'booster':[ 'gbtree','gblinear'],
                      'max_depth': [ 2,4,8,16,32,64,],
                      'eta': [0.1, 0.01, 0.001],
                      'gamma': [0.01],
                      'lambda': [0.1,0.01,0.001,0.0001],
                      'alpha': [0.1,0.01,0.001,0.0001]
                      }                                              # eta  is analogous to learning rate
                                                                     # gamma is minimum loss reduction required to make a split
                                                                     # alpha l2 regularization term ; analogous to ridge regression
                                                                     # lambda l1 regularization term; analogous to lasso regression

        xgb = xgb1( random_state=0)
        cv1=self.Grid_search(xgb,parameters, X_train, Y_train)
        print(cv1.best_estimator_)
        joblib.dump(cv1.best_estimator_,'/content/sample_data/XGB_model.pkl')

        reconstructed_model = joblib.load('/content/sample_data/XGB_model.pkl')
        ypred_train=reconstructed_model.predict(X_train)
        ypred_train=sc.inverse_transform(ypred_train)
        ypred_test = reconstructed_model.predict(X_test)
        ypred_test=sc.inverse_transform(ypred_test)
        y_train = sc.inverse_transform(Y_train)
        y_test = sc.inverse_transform(Y_test)

        print(ypred_test)

    def ridge (self, X_train,Y_train,X_test,Y_test):
        parameters = { 'alpha' : [0.1,0.01,0.001,0.0001]                                         
                      
                      }                                          

        ridg = Ridge( random_state=0)
        cv1=self.Grid_search(ridg,parameters, X_train, Y_train)
        print(cv1.best_estimator_)
        joblib.dump(cv1.best_estimator_,'/content/sample_data/RIDGE_model.pkl')

        reconstructed_model = joblib.load('/content/sample_data/RIDGE_model.pkl')
        ypred_train=reconstructed_model.predict(X_train)
        ypred_train=sc.inverse_transform(ypred_train)
        ypred_test = reconstructed_model.predict(X_test)
        ypred_test=sc.inverse_transform(ypred_test)
        y_train = sc.inverse_transform(Y_train)
        y_test = sc.inverse_transform(Y_test)

        print(ypred_test)

    def lasso (self, X_train,Y_train,X_test,Y_test):
        parameters = {'lambda' : [0.1,0.01,0.001,0.0001] 
                      }                                         

        adab = AdaBoostRegressor( random_state=0)
        cv1=self.Grid_search(adab,parameters, X_train, Y_train)
        print(cv1.best_estimator_)
        joblib.dump(cv1.best_estimator_,'/content/sample_data/LASSO_model.pkl')

        reconstructed_model = joblib.load('/content/sample_data/LASSO_model.pkl')
        ypred_train=reconstructed_model.predict(X_train)
        ypred_train=sc.inverse_transform(ypred_train)
        ypred_test = reconstructed_model.predict(X_test)
        ypred_test=sc.inverse_transform(ypred_test)
        y_train = sc.inverse_transform(Y_train)
        y_test = sc.inverse_transform(Y_test)

        print(ypred_test)
    
    def print_results(self,results):
      print('BEST PARAMS : {}\n'.format(results.best_params_))

      means = results.cv_results_['mean_test_score']
      stds  = results.cv_results_['std_test_score']

      for mean,std,params in zip(means, stds, results.cv_results_['params']):
        print('{} (+/-{}) for {}'.format(round(mean,3),round(std*2,3), params))

        
        
    def kmeans(self,X_train,Y_train,X_test,Y_test):
        
        X=np.concatenate(X_train,X_test)
        # Applying elbow method
        wcss = []
        for i in range(1,11):
            kmeans = KMeans(n_clusters=i,init='k-means++',max_iter=300,n_init=10,random_state=0)
            kmeans.fit(X)
            wcss.append(kmeans.inertia_)
        plt.plot(range(1,11),wcss)
        plt.title('The elbow method')
        plt.xlabel('Number of clusters')
        plt.ylabel('WCSS')
        plt.show()
 
        #Applying K-Means to dataset
        kmeans = KMeans(n_clusters=5,init='k-means++',max_iter=300,n_init=10,random_state=0)
        y_kmeans = kmeans.fit_predict(X)

        #Visualizing the Clusters
        plt.scatter(X[y_kmeans== 0,0],X[y_kmeans==0,1],s=100,c='red',label='Cluster 1')
        plt.scatter(X[y_kmeans== 1,0],X[y_kmeans==1,1],s=100,c='blue',label='Cluster 2')
        plt.scatter(X[y_kmeans== 2,0],X[y_kmeans==2,1],s=100,c='green',label='Cluster 3')
        plt.scatter(X[y_kmeans== 3,0],X[y_kmeans==3,1],s=100,c='cyan',label='Cluster 4')
        plt.scatter(X[y_kmeans== 4,0],X[y_kmeans==4,1],s=100,c='magenta',label='Cluster 5')
        plt.scatter(kmeans.cluster_centers_[:,0],kmeans.cluster_centers_[:,1],s=300,c='yellow',label='centroids')
        plt.title('Cluster of clients')
        plt.xlabel('Anual Income')
        plt.ylabel('Spending score (1-100)')
        plt.legend()
        plt.show()
        
    def knnclass(self,X_train,Y_train,X_test,Y_test):
        classifier = KNeighborsClassifier(n_neighbors=10,p=2,metric='minkowski')
        classifier.fit(X_train,Y_train)

        #Predicting the test set results
        y_pred = classifier.predict(X_test)

        #Making the Confusion Matrix
        cm = confusion_matrix(Y_test,y_pred)

        # Visualising the Training set results
        X_set, y_set = X_train, Y_train
        X1, X2 = np.meshgrid(np.arange(start = X_set[:, 0].min() - 1, stop = X_set[:, 0].max() + 1, step = 0.01),
                     np.arange(start = X_set[:, 1].min() - 1, stop = X_set[:, 1].max() + 1, step = 0.01))
        plt.contourf(X1, X2, classifier.predict(np.array([X1.ravel(), X2.ravel()]).T).reshape(X1.shape),
             alpha = 0.75, cmap = ListedColormap(('red', 'green')))
        plt.xlim(X1.min(), X1.max())
        plt.ylim(X2.min(), X2.max())
        for i, j in enumerate(np.unique(y_set)):
            plt.scatter(X_set[y_set == j, 0], X_set[y_set == j, 1],
                c = ListedColormap(('red', 'green'))(i), label = j)
        plt.title('knn Classification (Training set)')
        plt.xlabel('Age')
        plt.ylabel('Estimated Salary')
        plt.legend()
        plt.show()

        # Visualising the Test set results
        X_set, y_set = X_test, Y_test
        X1, X2 = np.meshgrid(np.arange(start = X_set[:, 0].min() - 1, stop = X_set[:, 0].max() + 1, step = 0.01),
                     np.arange(start = X_set[:, 1].min() - 1, stop = X_set[:, 1].max() + 1, step = 0.01))
        plt.contourf(X1, X2, classifier.predict(np.array([X1.ravel(), X2.ravel()]).T).reshape(X1.shape),
             alpha = 0.75, cmap = ListedColormap(('red', 'green')))
        plt.xlim(X1.min(), X1.max())
        plt.ylim(X2.min(), X2.max())
        for i, j in enumerate(np.unique(y_set)):
            plt.scatter(X_set[y_set == j, 0], X_set[y_set == j, 1],
                c = ListedColormap(('red', 'green'))(i), label = j)
        plt.title('knn Classification (Test set)')
        plt.xlabel('Age')
        plt.ylabel('Estimated Salary')
        plt.legend()
        plt.show()
        
    def BayesClassifier(self,X,Y,X_test,Y_test):  # y should be class into which x needs to be claasified
        X_normal=np.random.randn
        X_bernoulli= np.random.binomial(n=1,p=1)
        k=len(set(X))
        gaussian=[]
        for i in range(k):
            Xk=X[Y==i]
            mean=Xk.mean(axis=0)
            cov=np.cov(Xk.T)
            g={'m':mean,'c':cov}
            gaussian.append(g)
            
        g=gaussian[Y_test]                       # gaussian for test y class
        g1=mvn.rvs(mean=g['m'],cov=g['c'])
        
        
        for j in range(k):
            g5=gaussian[Y[j]]
            sample=mvn.rvs(mean=g5['m'],cov=g5['c'])
            mean=gaussian[j]['m'].reshape(28,28)
            plt.subplot(1,2,1)
            plt.imshow(sample,cmap='grey')
            plt.title("Sample")
            plt.subplot(1,2,2)
            plt.imshow(mean,cmap="grey")
            plt.title("Mean")
            plt.show()
            
        yrand=np.random.randit(k)                   # any rzndom class from k
        g3=gaussian[yrand]
        g4= mvn.rvs(mean=g3['m'],cov=g3['c'])
        g4.reshape(28,28)
        plt.imshow(g4,cmap="grey")
        plt.title("Random sample from random class")
        
    def BayesClassifierGMM (self,X,Y,X_test,Y_test):  # y should be class into which x needs to be claasified
        X_normal=np.random.randn
        X_bernoulli= np.random.binomial(n=1,p=1)
        k=len(set(X))
        gaussian=[]
        for i in range(k):
            Xk=X[Y==i]
            gmm= BayesianGaussianMixture(10)  # 10 is number of clusters
            gmm.fit(Xk)
            gaussian.append(gmm)
            
        gmm=gaussian[Y_test]                       # gaussian for test y class
        sample=gmm.sample()
        mean=gmm.means_[sample[1]]
        samp=sample[0].reshape(28,28)
        means=mean.reshape(28,28)
        
        
        for j in range(k):
            g5=gaussian[Y[j]]
            sample=gmm.sample()
            mean=gmm.means_[sample[1]]
            samp=sample[0].reshape(28,28)
            means=mean.reshape(28,28)
            plt.subplot(1,2,1)
            plt.imshow(samp,cmap='grey')
            plt.title("Sample")
            plt.subplot(1,2,2)
            plt.imshow(means,cmap="grey")
            plt.title("Mean")
            plt.show()
            
        yrand=np.random.randit(k)                   # any rzndom class from k
        gmm3=gaussian[yrand]
        sample1=gmm.sample()
        mean=gmm.means_[sample[1]]
        samp1=sample[0].reshape(28,28)
        means=mean.reshape(28,28)
        plt.imshow(samp1,cmap="grey")
        plt.title("Random sample from random class")
        
    def autoencoder(self,X_train,Y_train,X_test,Y_test,D,M):
        X=X_train
        Y=Y_train
        X=tf.placeholder(tf.float32,shape=(None,D))
        # input -> hidden
        W = tf.Variable(tf.random_normal(shape=(D, M)) * np.sqrt(2.0 / M))
        b = tf.Variable(np.zeros(M).astype(np.float32))

        # hidden -> output
        V = tf.Variable(tf.random_normal(shape=(M, D)) * np.sqrt(2.0 / D))
        c = tf.Variable(np.zeros(D).astype(np.float32))

        # construct the reconstruction
        Z = tf.nn.relu(tf.matmul(X, W) + b)
        logits = tf.matmul(Z, V) + c
        X_hat = tf.nn.sigmoid(logits)

        # compute the cost
        cost = tf.reduce_sum(
            tf.nn.sigmoid_cross_entropy_with_logits(
                labels=X,
                logits=logits
                )
            )

        # make the trainer
        train_op = tf.train.RMSPropOptimizer(learning_rate=0.001).minimize(cost)

        # set up session and variables for later
        init_op = tf.global_variables_initializer()
        sess = tf.InteractiveSession()
        sess.run(init_op)
        epochs=30
        batch_sz=64
        costs = []
        n_batches = len(X) // batch_sz
        print("n_batches:", n_batches)
        for i in range(epochs):
            print("epoch:", i)
            np.random.shuffle(X)
            for j in range(n_batches):
                batch = X[j*batch_sz:(j+1)*batch_sz]
                _, c, = sess.run((train_op, cost), feed_dict={X: batch})
                c /= batch_sz # just debugging
                costs.append(c)
                if j % 100 == 0:
                    print("iter: %d, cost: %.3f" % (j, c))
        plt.plot(costs)
        plt.show()

        sess.run(X_hat, feed_dict={X: X})
        
        done = False
        while not done:
            i = np.random.choice(len(X))
            x = X[i]
            im = model.predict([x]).reshape(28, 28)
            plt.subplot(1,2,1)
            plt.imshow(x.reshape(28, 28), cmap='gray')
            plt.title("Original")
            plt.subplot(1,2,2)
            plt.imshow(im, cmap='gray')
            plt.title("Reconstruction")
            plt.show()
            ans = input("Generate another?")
            if ans and ans[0] in ('n' or 'N'):
                done = True
                
    def softplus(self,x):
        # log1p(x) == log(1 + x)
        return np.log1p(np.exp(x))
    
    def forward(self,X_train,W1,W2):
        hidden = np.tanh(X_train.dot(W1))
        output = hidden.dot(W2) # no activation!
        mean = output[:2]
        stddev = self.softplus(output[2:])
        return mean,stddev
        
            
    def gaussianparam(self,X_train,Y_train,X_test,Y_test):
        
        W1 = np.random.randn(4, 3)
        W2 = np.random.randn(3, 2*2)

        # why 2 * 2?
        # we need 2 components for the mean,
        # and 2 components for the standard deviation!

        # ignore bias terms for simplicity. 
        # make a random input
        x = np.random.randn(4)

        # get the parameters of the Gaussian
        mean, stddev = self.forward(X_train, W1, W2)
        print("mean:", mean)
        print("stddev:", stddev)

        # draw samples
        samples = mvn.rvs(mean=mean, cov=stddev**2, size=10000)

        # plot the samples
        plt.scatter(samples[:,0], samples[:,1], alpha=0.5)
        plt.show()
        
        

    def PCA(self,X_train,Y_train,X_test,Y_test):
        
        # Applying PCA
        from sklearn.decomposition import PCA
        pca = PCA(n_components = 2)
        X_train = pca.fit_transform(X_train)
        X_test = pca.transform(X_test)
        explained_variance = pca.explained_variance_ratio_
        
        # Fitting Logistic Regression to the Training set
        from sklearn.linear_model import LogisticRegression
        classifier = LogisticRegression(random_state = 0)
        classifier.fit(X_train, Y_train)
        
        # Predicting the Test set results
        y_pred = classifier.predict(X_test)
        
        # Making the Confusion Matrix
        from sklearn.metrics import confusion_matrix
        cm = confusion_matrix(Y_test, y_pred)
        
        # Visualising the Training set results
        from matplotlib.colors import ListedColormap
        X_set, y_set = X_train, Y_train
        X1, X2 = np.meshgrid(np.arange(start = X_set[:, 0].min() - 1, stop = X_set[:, 0].max() + 1, step = 0.01),
                             np.arange(start = X_set[:, 1].min() - 1, stop = X_set[:, 1].max() + 1, step = 0.01))
        plt.contourf(X1, X2, classifier.predict(np.array([X1.ravel(), X2.ravel()]).T).reshape(X1.shape),
                     alpha = 0.75, cmap = ListedColormap(('red', 'green', 'blue')))
        plt.xlim(X1.min(), X1.max())
        plt.ylim(X2.min(), X2.max())
        for i, j in enumerate(np.unique(y_set)):
            plt.scatter(X_set[y_set == j, 0], X_set[y_set == j, 1],
                        c = ListedColormap(('red', 'green', 'blue'))(i), label = j)
        plt.title('Logistic Regression (Training set)')
        plt.xlabel('PC1')
        plt.ylabel('PC2')
        plt.legend()
        plt.show()
        
        # Visualising the Test set results
        from matplotlib.colors import ListedColormap
        X_set, y_set = X_test, Y_test
        X1, X2 = np.meshgrid(np.arange(start = X_set[:, 0].min() - 1, stop = X_set[:, 0].max() + 1, step = 0.01),
                             np.arange(start = X_set[:, 1].min() - 1, stop = X_set[:, 1].max() + 1, step = 0.01))
        plt.contourf(X1, X2, classifier.predict(np.array([X1.ravel(), X2.ravel()]).T).reshape(X1.shape),
                     alpha = 0.75, cmap = ListedColormap(('red', 'green', 'blue')))
        plt.xlim(X1.min(), X1.max())
        plt.ylim(X2.min(), X2.max())
        for i, j in enumerate(np.unique(y_set)):
            plt.scatter(X_set[y_set == j, 0], X_set[y_set == j, 1],
                        c = ListedColormap(('red', 'green', 'blue'))(i), label = j)
        plt.title('Logistic Regression (Test set)')
        plt.xlabel('PC1')
        plt.ylabel('PC2')
        plt.legend()
        plt.show()
        
        
    def kernelPCA(self, X_train,Y_train,X_test,Y_test):
        
        # when the variables are linearly separable
        #Applying Kernel PCA
        from sklearn.decomposition import KernelPCA
        kpca = KernelPCA(n_components = 2,kernel ='rbf')
        X_train = kpca.fit_transform(X_train)
        X_test = kpca.transform(X_test)
        # Fitting Logistic Regression to the Training set
        from sklearn.linear_model import LogisticRegression
        classifier = LogisticRegression(random_state = 0)
        classifier.fit(X_train, Y_train)
        
        # Predicting the Test set results
        y_pred = classifier.predict(X_test)
        
        # Making the Confusion Matrix
        from sklearn.metrics import confusion_matrix
        cm = confusion_matrix(Y_test, y_pred)
        acc = (64+26)/(64+26+4+6)
        # Visualising the Training set results
        from matplotlib.colors import ListedColormap
        X_set, y_set = X_train, Y_train
        X1, X2 = np.meshgrid(np.arange(start = X_set[:, 0].min() - 1, stop = X_set[:, 0].max() + 1, step = 0.01),
                             np.arange(start = X_set[:, 1].min() - 1, stop = X_set[:, 1].max() + 1, step = 0.01))
        plt.contourf(X1, X2, classifier.predict(np.array([X1.ravel(), X2.ravel()]).T).reshape(X1.shape),
                     alpha = 0.75, cmap = ListedColormap(('red', 'green')))
        plt.xlim(X1.min(), X1.max())
        plt.ylim(X2.min(), X2.max())
        for i, j in enumerate(np.unique(y_set)):
            plt.scatter(X_set[y_set == j, 0], X_set[y_set == j, 1],
                        c = ListedColormap(('red', 'green'))(i), label = j)
        plt.title('Logistic Regression (Training set)')
        plt.xlabel('Age')
        plt.ylabel('Estimated Salary')
        plt.legend()
        plt.show()
        
        # Visualising the Test set results
        from matplotlib.colors import ListedColormap
        X_set, y_set = X_test, Y_test
        X1, X2 = np.meshgrid(np.arange(start = X_set[:, 0].min() - 1, stop = X_set[:, 0].max() + 1, step = 0.01),
                             np.arange(start = X_set[:, 1].min() - 1, stop = X_set[:, 1].max() + 1, step = 0.01))
        plt.contourf(X1, X2, classifier.predict(np.array([X1.ravel(), X2.ravel()]).T).reshape(X1.shape),
                     alpha = 0.75, cmap = ListedColormap(('red', 'green')))
        plt.xlim(X1.min(), X1.max())
        plt.ylim(X2.min(), X2.max())
        for i, j in enumerate(np.unique(y_set)):
            plt.scatter(X_set[y_set == j, 0], X_set[y_set == j, 1],
                        c = ListedColormap(('red', 'green'))(i), label = j)
        plt.title('Logistic Regression (Test set)')
        plt.xlabel('Age')
        plt.ylabel('Estimated Salary')
        plt.legend()
        plt.show()
                 
    def LDA(self,X_train,Y_train,X_test,Y_test):
    
        #Applying Principle Component Analysis(PCA)
        from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
        lda = LinearDiscriminantAnalysis(n_components = 2)
        X_train = lda.fit_transform(X_train,Y_train)
        X_test = lda.transform(X_test)
        
        # Fitting Logistic Regression to the Training set
        from sklearn.linear_model import LogisticRegression
        classifier = LogisticRegression(random_state = 0)
        classifier.fit(X_train, Y_train)
        
        # Predicting the Test set results
        y_pred = classifier.predict(X_test)
        
        # Making the Confusion Matrix
        from sklearn.metrics import confusion_matrix
        cm = confusion_matrix(Y_test, y_pred)
        acc=35/36
        # Visualising the Training set results
        from matplotlib.colors import ListedColormap
        X_set, y_set = X_train, Y_train
        X1, X2 = np.meshgrid(np.arange(start = X_set[:, 0].min() - 1, stop = X_set[:, 0].max() + 1, step = 0.01),
                             np.arange(start = X_set[:, 1].min() - 1, stop = X_set[:, 1].max() + 1, step = 0.01))
        plt.contourf(X1, X2, classifier.predict(np.array([X1.ravel(), X2.ravel()]).T).reshape(X1.shape),
                     alpha = 0.75, cmap = ListedColormap(('red', 'green','blue')))
        plt.xlim(X1.min(), X1.max())
        plt.ylim(X2.min(), X2.max())
        for i, j in enumerate(np.unique(y_set)):
            plt.scatter(X_set[y_set == j, 0], X_set[y_set == j, 1],
                        c = ListedColormap(('red', 'green','blue'))(i), label = j)
        plt.title('Logistic Regression (Training set)')
        plt.xlabel('LD1')
        plt.ylabel('LD2')
        plt.legend()
        plt.show()
        
        # Visualising the Test set results
        from matplotlib.colors import ListedColormap
        X_set, y_set = X_test, Y_test
        X1, X2 = np.meshgrid(np.arange(start = X_set[:, 0].min() - 1, stop = X_set[:, 0].max() + 1, step = 0.01),
                             np.arange(start = X_set[:, 1].min() - 1, stop = X_set[:, 1].max() + 1, step = 0.01))
        plt.contourf(X1, X2, classifier.predict(np.array([X1.ravel(), X2.ravel()]).T).reshape(X1.shape),
                     alpha = 0.75, cmap = ListedColormap(('red', 'green','blue')))
        plt.xlim(X1.min(), X1.max())
        plt.ylim(X2.min(), X2.max())
        for i, j in enumerate(np.unique(y_set)):
            plt.scatter(X_set[y_set == j, 0], X_set[y_set == j, 1],
                        c = ListedColormap(('red', 'green','blue'))(i), label = j)
        plt.title('Logistic Regression (Test set)')
        plt.xlabel('LD1')
        plt.ylabel('LD2')
        plt.legend()
        plt.show()


    def bestmodel(self,X_val,X_test,Y_val,Y_test):
      models = {}
      start=time()
      end= time()
      for mdl in ['LR','SVM','RF','GB','MLP','ADAB','XGB']:
        models[mdl] = joblib.load('/content/sample_data/{}_model.pkl'.format(mdl))
        pred=models[mdl].predict(self.X_test)
        accuracy=round(accuracy_score(self.Y_test,pred),3)
        precision=round(precision_score(self.Y_test,pred),3)
        recall=round(recall_score(self.Y_test,pred),3)
        


        # trade off between precision and recall , spam :precision, fraud:recall
        # trade of between accuracy and latency : real time : latent


        
            
        
                
        

        


        
    


import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier

from sklearn.model_selection import GridSearchCV

from sklearn.metrics import accuracy_score

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split

def default_model_set():
    model_inputs = []
    trained_models = []

    knn = KNeighborsClassifier(n_neighbors=5, weights='distance')
    knn_params = {}
    #knn_params = {'n_neighbors':[1,2,3,4,5,10,15,20],
    #              'weights':['uniform','distance'],'p':[1,2]}

    model_inputs.append(["K-Nearest Neighbors",knn, knn_params])

    lr = LogisticRegression()
    lr_params = {}
    #lr_params = {'alpha':[1e-3,3e-3,1e-2,3e-2,1e-1,3e-1,1,3,10,30,100,300,1000]}

    model_inputs.append(["Logistic Regression",lr, lr_params])

    svc = SVC(kernel='rbf')
    svc_params = {}
    #svc_params = {'C':[1e-3,3e-3,1e-2,3e-2,1e-1,3e-1,1,3,10,30,100,300,1000],
    #              'kernel':['rbf','sigmoid']}

    model_inputs.append(["SVC",svc, svc_params])


    dt = DecisionTreeClassifier()
    dt_params = {}
    #dt_params = {'criterion':['gini','entropy'], 'max_depth':[None, 20, 40],
    #             'max_features':[None, 'auto', 'sqrt','log2']}

    model_inputs.append(["Decision Tree", dt, dt_params])

    rf = RandomForestClassifier()
    rf_params = {}
    #rf_params = {'criterion':['gini','entropy'], 'n_estimators':[2,5,10,20,50,100],
    #             'max_features':[None, 'auto', 'sqrt','log2']}

    model_inputs.append(["Random Forest", rf, rf_params])

    et = ExtraTreesClassifier()

    model_inputs.append(["Extra Trees", et, rf_params])
    
    return model_inputs


def grid_search_model(models, X, y, test_size = 0.3):

    model_grid = []

    X_train, X_test, y_train, y_test = \
        train_test_split(X, y, test_size = test_size, random_state = 321)

    scaler = StandardScaler()
    scaler.fit(X_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)

    for model in models:
        
        print model[0]

        temp_grid = GridSearchCV(estimator = model[1], cv=5,
                                 scoring='accuracy', param_grid=model[2])

        temp_grid.fit(X_train, y_train)
        
        test_pred = temp_grid.best_estimator_.predict(X_test)
        test_score = accuracy_score(y_test, test_pred)

        model_grid.append({"Name":model[0],"Grid":temp_grid,
                           "Score":temp_grid.best_score_,
                           "Test Score":test_score,
                           "Best_Estimator":temp_grid.best_estimator_,
                           "Standard Scaler":scaler})

        print model_grid[-1]

    return pd.DataFrame(model_grid)

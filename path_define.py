
initial_data_path = "initial_data.csv"

X_shape = {
    "linear_regression":[None,24],
    "SVM":[None,24],
    "BP":[None,24]
}

Y_shape = {
    "linear_regression":[None,20],
    "SVM":[None,20],
    "BP":[None,20]
}

Hide_size = 22

W_shape = {
    "linear_regression":[24,20],
    "SVM":[24,20],
    "BP1":[24,Hide_size],
    "BP2":[Hide_size,20]
}


B_varibale = 0.1
B_shape = {
    "linear_regression":[20],
    "SVM":[20],
    "BP1":[Hide_size],
    "BP2":[20]
}

Normal_variable = 1e-2

Batch_size = {
    "linear_regression":16,
    "SVM":16,
    "BP":16
}

Learning_rate = {
    "linear_regression":1e-2,
    "SVM":1e-2
}

Train_step = {
    "linear_regression":1000,
    "SVM":1000,
    "BP":1000
}


X_shape = {
    "logistics_regression":[None,24],
    "SVM":[None,24],
    "BP":[None,24]
}

Y_shape = {
    "logistics_regression":[None,20],
    "SVM":[None,20],
    "BP":[None,20]
}

Hide_size = 22

W_shape = {
    "logistics_regression":[24,20],
    "SVM":[24,20],
    "BP1":[24,Hide_size],
    "BP2":[Hide_size,20]
}


B_varibale = 0.1
B_shape = {
    "logistics_regression":[20],
    "SVM":[20],
    "BP1":[Hide_size],
    "BP2":[20]
}

Normal_variable = 1e-2

Batch_size = {
    "logistics_regression":16,
    "SVM":16,
    "BP":16
}
Batch_num1 = {
    "logistics_regression":5,
    "SVM":5,
    "BP":5
}
Batch_num2 = {
    "logistics_regression":2,
    "SVM":2,
    "BP":2
}


Learning_rate = {
    "logistics_regression":1e-2,
    "SVM":1e-2
}

Train_step = {
    "logistics_regression":1000,
    "SVM":1000,
    "BP":1000
}

Model_mode = ["first_train","keep_on","prediction"]

Model_path1 = {
    "logistics_regression":"train_variable\\logistics_regression\\",
    "SVM":"train_variable\\SVM\\",
    "BP":"train_variable\\BP\\"
}

Model_path2 = {
    "logistics_regression":"train_variable/logistics_regression",
    "SVM":"train_variable/SVM",
    "BP":"train_variable/BP"
}

tensorBoard_path = {
    "logistics_regression":"tensorBoard_path/logistics_regression/",
    "SVM":"tensorBoard_path/SVM",
    "BP":"tensorBoard_path/BP",
}

id_path = "data_id"

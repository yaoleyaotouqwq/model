
Class_num = 20

Batch_size = {
    "LR":16,
    "SVM":16,
    "DNN":16
}
Batch_num1 = {
    "LR":5,
    "SVM":5,
    "DNN":5
}

Batch_num2 = {
    "LR":2,
    "SVM":2,
    "DNN":2
}

X_shape = {
    "LR":[None,24],
    "SVM":[None,24],
    "DNN":[None,24],
}

Y_shape = {
    "LR":[None,20],
    "SVM":[20,None],
    "DNN":[None,20],
}

W_shape = {
    "LR":[24,20],
    "DNN1":[24,128],
    "DNN2":[128,64],
    "DNN3":[64,32],
    "DNN4":[32,24],
    "DNN5":[24,22],
    "DNN6":[22,20]
}


B_varibale = 0.1

B_shape = {
    "LR":[20],
    "SVM":[20,Batch_size["SVM"]],
    "DNN1":[128],
    "DNN2":[64],
    "DNN3":[32],
    "DNN4":[24],
    "DNN5":[22],
    "DNN6":[20],
}

SVM_prediction_gird_shape = X_shape["SVM"]

RBF = {
    "Gamma":-10.0
}

Normal_variable = 1e-2

Learning_rate = {
    "LR":1e-2,
    "SVM":1e-3,
    "DNN":1e-3
}

Train_step = {
    "LR":1000,
    "SVM":1000,
    "DNN":1000
}

Test_K_num = 5

Model_mode = ["first_train","keep_on","prediction"]

Model_path1 = {
    "LR":"train_variable\\LR\\",
    "SVM":"train_variable\\SVM\\",
    "DNN":"train_variable\\DNN\\"
}

Model_path2 = {
    "LR":"train_variable/LR",
    "SVM":"train_variable/SVM",
    "DNN":"train_variable/DNN"
}

tensorBoard_path = {
    "LR":"tensorBoard_path/LR",
    "SVM":"tensorBoard_path/SVM",
    "DNN":"tensorBoard_path/DNN",
}

Button_bg_path = {
    "Search":"Image/search.png",
    "Predict": "Image/predict.png",
    "Information": "Image/infor_button.png",
    "Find All": "Image/out_all.png",
    "Score Graph": "Image/score_graph.png",
    "Retraining": "Image/train_again.png",
    "Keep On Train": "Image/keep_train.png",
    "Assessment Model": "Image/test_model.png"
}

Html_temp_path = "Html_tips/"
Echarts_path = "Echarts/"

index_path = "index.html"
wait_path = "wait.html"

id_path = "data_id"


Class_num = {
    "score_data":20,
    "xapi":3
}

Batch_size = {
    "score_data":{
        "LR":32,
        "SVM":32,
        "DNN":32
    },
    "xapi":{
        "LR":32,
        "SVM":32,
        "DNN":32
    }
}

X_shape = {
    "LR":{
        "score_data":[None,23],
        "xapi":[None,16],
    },
    "SVM":{
        "score_data":[None,23],
        "xapi":[None,16],
    },
    "DNN":{
        "score_data":[None,23],
        "xapi":[None,16],
    }
}

Y_shape = {
    "LR":{
        "score_data":[None,20],
        "xapi":[None,3],
    },
    "SVM":{
        "score_data":[20,None],
        "xapi":[3,None],
    },
    "DNN":{
        "score_data":[None,20],
        "xapi":[None,3],
    }
}

W_shape = {
    "LR":{
        "score_data":[23,20],
        "xapi":[16,3],
    },
    "DNN1":{
        "score_data":[23,128],
        "xapi":[16,128],
    },
    "DNN2":{
        "score_data":[128,64],
        "xapi":[128,64],
    },
    "DNN3":{
        "score_data":[64,32],
        "xapi":[64,32],
    },
    "DNN4":{
        "score_data":[32,23],
        "xapi":[32,16],
    },
    "DNN5":{
        "score_data":[23,22],
        "xapi":[16,8],
    },
    "DNN6":{
        "score_data":[22,20],
        "xapi":[8,3],
    },
}

B_varibale = {
    "score_data":0.1,
    "xapi":0.1,
}

B_shape = {
    "LR":{
        "score_data":[20],
        "xapi":[3],
    },
    "SVM":{
        "score_data":[20,Batch_size["score_data"]["SVM"]],
        "xapi":[3,Batch_size["xapi"]["SVM"]],
    },
    "DNN1":{
        "score_data":[128],
        "xapi":[128],
    },
    "DNN2":{
        "score_data":[64],
        "xapi":[64],
    },
    "DNN3":{
        "score_data":[32],
        "xapi":[32],
    },
    "DNN4":{
        "score_data":[23],
        "xapi":[16],
    },
    "DNN5":{
        "score_data":[22],
        "xapi":[8],
    },
    "DNN6":{
        "score_data":[20],
        "xapi":[3],
    },
}

RBF = {
    "Gamma":{
        "score_data":-5.0,
        "xapi":-5.0,
    }
}

Normal_variable = {
    "score_data":1e-2,
    "xapi":1e-2,
}

Dropout_prob = {
    "score_data":{
        "train":1,
        "test":1
    },
    "xapi":{
        "train": 0.7,
        "test": 1
    }
}

Learning_rate = {
    "LR":{
        "score_data":1e-1,
        "xapi":1e-3,
    },
    "SVM":{
        "score_data":1e-3,
        "xapi":1e-3,
    },
    "DNN":{
        "score_data":1e-3,
        "xapi":1e-3,
    },
}

Train_step = {
    "LR":{
        "score_data":2000,
        "xapi":1000
    },
    "SVM":{
        "score_data":2000,
        "xapi":1000
    },
    "DNN":{
        "score_data":2000,
        "xapi":1000
    }
}

Test_K_num = {
    "score_data":5,
    "xapi":5,
}

Model_mode = ["first_train","keep_on","prediction"]

Model_path1 = {
    "LR":{
        "score_data":"train_variable\\LR\\score_data\\",
        "xapi":"train_variable\\LR\\xapi\\"
    },
    "SVM":{
        "score_data":"train_variable\\SVM\\score_data\\",
        "xapi":"train_variable\\SVM\\xapi\\"
    },
    "DNN":{
        "score_data":"train_variable\\DNN\\score_data\\",
        "xapi":"train_variable\\DNN\\xapi\\"
    }
}

Model_path2 = {
    "LR":{
        "score_data":"train_variable/LR/score_data",
        "xapi":"train_variable/LR/xapi"
    },
    "SVM":{
        "score_data":"train_variable/SVM/score_data",
        "xapi":"train_variable/SVM/xapi"
    },
    "DNN":{
        "score_data":"train_variable/DNN/score_data",
        "xapi":"train_variable/DNN/xapi"
    }
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

id_path = {
    "score_data":"data_id/score_data",
    "xapi":"data_id/xapi"
}

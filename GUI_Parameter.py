
Db = {
    "Db_app": 'QMYSQL',
    "HostName":"localhost",
    "Port":3306,
    "Db_Name":"score",
    "Username":"root",
    "Password":"123456"
}

Score_data_num = {
    "score_start":3,
    "variety":28
}

identity = {
    "Student":"学生",
    "Teacher":"教师",
    "Administrator":"管理员"
}

Window_Name = {
    "Create":"注册",
    "Login":"登录",
    "Search":"查找",
    "Predict":"预测",
    "Infor":"个人信息与修改",
    "Main":"学生成绩预测系统"
}


Window_Size = {
    "Width":{
        "Create":600,
        "Login":800,
        "Infor":600,
        "Predict":400,
        "Search":300,
        "Main":1200
    },
    "Height":{
        "Create":700,
        "Login":500,
        "Infor":700,
        "Predict":400,
        "Search":300,
        "Main":800
    }
}

Text_label = {
    "Login":{
        "account":"账号:",
        "password":"密码:"
    },
    "Create":{
        "account":"账号:",
        "password":"密码:",
        "name":"姓名:",
        "identity":"身份:"
    },
    "Infor":{
        "account":"账号(学号):",
        "password":"密码:",
        "name":"姓名:",
        "identity":"身份:"
    },
    "Search":{
      "account":"账号(学号)："
    },
    "Predict":{
        "account":"账号：",
        "account1":"账号1：",
        "account2":"账号2：",
        "account3":"账号3：",
    }
}

Text_tips = {
    "Login":{
        "account":"请输入账号(学号)..",
        "password":"请输入密码.."
    },
    "Create":{
        "account":"请输入账号(学号)..",
        "password":"请输入密码..",
        "name":"请输入姓名..",
        "identity":"请选择身份："
    },
    "Predict":{
        "account":"请输入账号(学号)..",
    }
}

Message_tips = {
    "Windows_title":"提示",
    "Account_exists":"账号已存在，请重新输入。",
    "Input Error":"账号或密码输入错误，请重新输入。",
    "Login Success":"登录成功！欢迎进入系统！",
    "Create_Success":"注册成功！请重新登录。",
    "Account_missing":"账号未输入，请重新输入。",
    "Password_missing":"密码未输入，请重新输入。",
    "Name_missing":"姓名未输入,请重新输入。",
    "Search Success":"查找成功!已更新查找结果。",
    "Search Failed":"未查找到相关内容。",
    "Search Ban":"无权限查询其他账号信息。",
    "Not Change":"信息未做任何更改。",
    "Change Success":"信息已更改。",
    "Predict Own":"仅允许预测本用户成绩。",
    "Train Finish":"模型已训练完成。",
    "Data Missing":"数据库当前无数据可训练或数据不足以训练",
    "Train Failed":"训练失败，数据库无新增数据或不足以训练，建议重新训练。",
    "Test Finish":"模型评估已完成。",
    "Test Failed":"模型评估所需数据不足。"

}

Butten_Name = {
    "Enter":"确定",
    "Cancel":"取消",
    "Create":"注册",
    "Search":"查询",
    "Change":"更改",
    "Predict":"预测",
    "Information":"个人信息",
    "Find All":"显示所有学生成绩数据",
    "Score Graph":"成绩柱状图展示",
    "Retraining":"重新训练模型",
    "Keep On Train":"继续训练模型",
    "Assessment Model":"评估模型"
}

Search_Name = "学号"

TableView_Name = "分数表"

Tablefield_Name = ["序号" , "学号" ,  "考场座位号",
                   "考题一", "考题二", "考题三", "考题四", "考题五", "考题六", "考题七" ,"考题八","卷面成绩"
                   "SPOC单元测验1" , "SPOC单元测验2","SPOC单元测验3","SPOC单元测验4","SPOC单元测验5","SPOC单元测验6","SPOC单元测验7","SPOC单元测验8","SPOC测验总成绩","SPOC讨论","SPOC考试",
                    "课堂测试1","课堂测试2","课堂测试3","课堂测试4","课堂测试5"]


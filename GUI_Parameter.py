
Db = {
    "Db_app": 'QMYSQL',
    "HostName":"localhost",
    "Port":3306,
    "Db_Name":"score",
    "Username":"root",
    "Password":"123456"
}

Table_Name =  ["score_data","xapi"]

Sql_word = {
    "score_data":["SELECT 考题一, 考题二, 考题三, 考题四, 考题五, 考题六, 考题七 ,考题八 FROM `score_data` where 学号=",
                       "SELECT SPOC单元测验1, SPOC单元测验2, SPOC单元测验3, SPOC单元测验4, SPOC单元测验5,SPOC单元测验6, SPOC单元测验7,SPOC单元测验8 FROM `score_data`",
                       "SELECT 课堂测试1, 课堂测试2, 课堂测试3, 课堂测试4, 课堂测试5 FROM `score_data` where 学号=",
                       "SELECT SPOC单元测验1, SPOC单元测验2, SPOC单元测验3, SPOC单元测验4, SPOC单元测验5,SPOC单元测验6, SPOC单元测验7,SPOC单元测验8 FROM `score_data` where 学号=",
                       ],
    "xapi":[
        "SELECT 举手次数,访问过的资源,查看公告次数,讨论次数 FROM `xapi`",
        "SELECT 举手次数,访问过的资源,查看公告次数,讨论次数 FROM `xapi` where 学号=",
        "SELECT 家长回答调查,家长学校满意度,学生缺勤日 FROM `xapi` where 学号="
    ]
}

# 划定有效的数据区间
Score_data_num = {
    "score_data":{
        "score_start":3,
        "variety":28,
        "Score_calculate":[8,8,5]
    },
    "xapi":
    {
        "score_start":2,
        "variety":19,
        "Score_calculate":[4,3]
    }
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
    "Echarts":"数据图表",
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
        "Echarts":1100,
        "Main":1200
    },
    "Height":{
        "Create":700,
        "Login":500,
        "Infor":400,
        "Predict":400,
        "Search":300,
        "Echarts":700,
        "Main":900
    }
}

Button_size = {
    "Main":{
        "Button1":[150,50],
        "Button2":[150,50],
        "Button3":[500,50],
        "Button4":[500,50],
    }
}
Text_label = {
    "Login":{
        "account":"账号:",
        "password":"密码:",
        "table_name":"数据表"
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
    "Score Graph":"成绩图表",
    "Retraining":"重新训练模型",
    "Keep On Train":"继续训练模型",
    "Assessment Model":"评估模型"
}


Search_Name = "学号"

TableView_Name = "分数表"

Tablefield_Name = {
    "0":["序号" , "学号" ,  "考场座位号",
                   "考题一", "考题二", "考题三", "考题四", "考题五", "考题六", "考题七" ,"考题八","卷面成绩",
                   "SPOC单元测验1" , "SPOC单元测验2","SPOC单元测验3","SPOC单元测验4","SPOC单元测验5","SPOC单元测验6","SPOC单元测验7","SPOC单元测验8","SPOC测验总成绩","SPOC讨论","SPOC考试",
                    "课堂测试1","课堂测试2","课堂测试3","课堂测试4","课堂测试5"],
    "1":["序号" , "学号" , "性别","国籍","出生地","教育阶段","年级","节ID","课程主题","学年学期","家长负责","举手次数","访问过的资源","查看公告次数","讨论次数","家长回答调查","家长学校满意度","学生缺勤日","学生分数等级"]
}

TableView_account_index = 1

Model_Refresh_num = 100

Layout_Stretch = {
    "Main":{
        "Left":[0,1],
        "Right":[1,5]
    },
    "Right":{
        "Text":[0,0],
        "Graph":[1,7],
        "Button":[2,2]
    }
}

Visual_Graph = {
    "Graph_Name":["学号","数据图","图表选项","训练过程","评估过程","评估总结"],
    "Columns_Name":["算法","分数区间","训练步数","损失值","准确率(%)","评估集","平均分"],
    "Algorithm_Name":["LR","SVM","DNN"],
    "Student_func":["考题得分占比","SPOC单元测试对比","课堂测试情况"],
    "xapi_Student_func":["学习次数对比","家长意见及学生签到"],
    "Func_name":["考题饼图","SPOC折线图","课堂测试雷达图","训练损失值","训练准确率","评估准确率（K折交叉检验）","算法评估均分"],
    "Func_data_name":[(3,11),(12,20),(23,28)],
    "xapi_Func_name":["学习情况次数","家长意见以及学生签到情况"],
    "xapi_Func_data_name":[(11,15),(15,18)],
    "Line_name":["本用户分数线","最低分数线","最高分数线","LR_LOSS","LR_ACC","SVM_LOSS","SVM_ACC","DNN_LOSS","DNN_ACC"],
    "Line_model_name_index":[[3,4],[5,6],[7,8]],
    "xapi_Line_name":["本用户学习次数折线","最低次数折线","最高次数折线"],
    "Line_x_rotate":330,
    "Radar_name":"课堂测试分数",
    "Radar_space":[0,100],
    "xapi_Radar_name":{
        "家长回答调查":"家长回答调查",
        "家长学校满意度":"家长学校满意度",
        "学生缺勤日":"学生缺勤七次以上"
    },
    "xapi_Radar_space":[0,1],
    "Bar_Name":["成绩预测情况"],
    "Value_type":["预测分数","真实分数"],
    # 行，列，占用行数，占用列数(左下角)
    "Listwidget":[1,0,1,1],
    # 行，列，占用行数，占用列数(右下角)
    "StackedWidget":[1,2,1,1],
    # 行，列，占用行数，占用列数(中间)
    "Line":[1,1,1,1],
    # 行，列，占用行数，占用列数(左上角)
    "Label_left":[0, 0, 1, 1],
    # 行，列，占用行数，占用列数(右上角)
    "Label_right": [0, 2, 1, 1],
    # 左侧、顶部、右侧和底部边距
    "ContentsMargins":[0,0,0,0],
    "Listwidget_size":{
        "Width":200,
        "Height":5000
    },
    # 字体格式
    "Word":{
        "Size":16,
        # 粗体
        "Bold":True,
        # 斜体
        "Italic":False,
        # 文字粗细
        "Weight":75
    },
    # 边框线条大小
    "LineWidth":1,
    # 控件的上下间距
    "Spacing":0,
    # Y轴名称距离
    "Y_gap":50
}

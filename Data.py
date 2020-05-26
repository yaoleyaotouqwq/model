

Score_dict = {
    "index":0,
    "":0,
    '0':0,
    'A+':100,
    'A':96,
    'A-':92,
    'B+':90,
    'B':86,
    'B-':82,
    'C+':80,
    'C':76,
    'C-':72,
    'D+':70,
    'D':66,
    'D-':62,
    'E+':60,
    'E':56,
    'E-':52,
}

Score_scope = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95 , 100 ]

Score_scope_len = {
    "score_data":20,
    "xapi":3
}

Data_value_change = {
    "xapi":{
        # 男女
        "性别":{
            "M":0,
            "F":1
        },
        # 科威特，黎巴嫩，埃及，沙特阿拉伯，美国，约旦，委内瑞拉，伊朗，突尼斯，摩洛哥，叙利亚，伊拉克，巴勒斯坦，利比亚
        "国籍":{
            "KW":0,
            "lebanon":1,
            "Egypt":2,
            "SaudiArabia":3,
            "USA":4,
            "Jordan":5,
            "venzuela":6,
            "Iran":7,
            "Tunis":8,
            "Morocco":9,
            "Syria":10,
            "Iraq":11,
            "Palestine":12,
            "Lybia":13,
        },
        "出生地":{
            "KuwaIT":0,
            "lebanon":1,
            "Egypt":2,
            "SaudiArabia":3,
            "USA":4,
            "Jordan":5,
            "venzuela":6,
            "Iran":7,
            "Tunis":8,
            "Morocco":9,
            "Syria":10,
            "Iraq":11,
            "Palestine":12,
            "Lybia":13,
        },
        "教育阶段":{
            "lowerlevel":0,
            "MiddleSchool":1,
            "HighSchool":2
        },
        "年级":{
            "G-01":0,
            "G-02":1,
            "G-03":2,
            "G-04":3,
            "G-05":4,
            "G-06":5,
            "G-07":6,
            "G-08":7,
            "G-09":8,
            "G-10":9,
            "G-11":10,
            "G-12":11
        },
        "节ID":{
            "A":0,
            "B":1,
            "C":2,
        },
        "课程主题":{
            "IT":0,
            "Math":1,
            "Arabic":2,
            "Science":3,
            "English":4,
            "Quran":5,
            "Spanish":6,
            "French":7,
            "History":8,
            "Biology":9,
            "Chemistry":10,
            "Geology":11,
        },
        "学期学年":{
            "F":0,
            "S":1
        },
        "家长负责":{
          "Mum":0,
          "Father":1
        },
        "家长回答调查":{
            "Yes":0,
            "No":1
        },
        "家长学校满意度":{
            "Good":0,
            "Bad":1
        },
        # 七天上下
        "学生缺勤日":{
            "Under-7":0,
            "Above-7":1
        },
        "学生分数等级":{
            # 成绩未知
            "":0,
            "L":0,
            "M":1,
            "H":2
        }
    }
}

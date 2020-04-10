# import path_define as Model_Parameter
# import GUI_Parameter as Parameter
# from pyecharts import Bar
#
# data1 = [15, 15, 0]
# data2 = [6, 6, 6]
#
# # data1 = ["0-5","15-20","30-35"]
# # data2 = ["10-15","35-40","25-30"]
#
# # 更改Graph的Y轴显示
# def change_data(data):
#     Score = ["0-5", "5-10", "10-15", "15-20", "20-25", "25-30",
#              "30-35", "35-40", "40-45", "45-50", "50-55", "55-60",
#               "60-65", "65-70", "70-75", "75-80", "80-85", "85-90", "90-95", "95-100"]
#     return Score[data]
#
#
# bar = Bar("柱状图", "一年的降水量与蒸发量")
#
# bar.add(Parameter.Visual_Graph["Value_type"][0], Parameter.Visual_Graph["Algorithm_Name"], data1,
#         yaxis_formatter=change_data)
# bar.add(Parameter.Visual_Graph["Value_type"][1], Parameter.Visual_Graph["Algorithm_Name"], data2,
#         yaxis_formatter=change_data)
#
# bar.render(Model_Parameter.Echarts_path + "1.html")
#
# a = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
#      [19.0, 30.0, 28.0, 28.0, 22.66, 16.0, 20.0, 20.0],
#      [20.0, 29.0, 30.0, 28.0, 22.66, 20.0, 18.66, 20.0],
#      [19.0, 20.0, 20.0, 28.0, 20.0, 20.0, 19.0, 20.0]]
#
# max_data = []
# min_data = []
#
# for temp in range(len(a[0])):
#     data_temp = sorted(a,key=lambda a:a[temp])
#     max_data.append(data_temp[len(a)-1][temp])
#     min_data.append(data_temp[0][temp])
#
# print(max_data)
# print(min_data)

# a = {
#     "b":1,
#     "c":2
# }
#
# d = "d"
#
# e = [float(a[d]) if d == temp else temp for _,temp in enumerate(a)]
# print(e)
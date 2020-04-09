import path_define as Model_Parameter
import GUI_Parameter as Parameter
from pyecharts import Bar

columns = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

data1 = [2.0, 4.9, 7.0]
data2 = [2.6, 5.9, 9.0]

bar = Bar("柱状图", "一年的降水量与蒸发量")

bar.add(Parameter.Visual_Graph["Value_type"][0], Parameter.Visual_Graph["Algorithm_Name"], data1,
          )
bar.add(Parameter.Visual_Graph["Value_type"][1], Parameter.Visual_Graph["Algorithm_Name"], data2,
         )

bar.render(Model_Parameter.Echarts_path + "1.html")
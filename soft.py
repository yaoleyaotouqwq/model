import Data

xapi_dict = Data.Data_value_change["xapi"]

data = ["M","KW","KuwaIT","lowerlevel","G-04","A","IT","F","Father","15","16","2","20","Yes","Good","Under-7","M"]
for temp1,temp2 in enumerate(xapi_dict):
    if temp1 <= 8:
        print(temp1, xapi_dict[temp2][data[temp1]])
        if temp1 == 8:
            print(data[temp1 + 1:temp1 + 1 + 4])
    else:
        print(temp1, xapi_dict[temp2][data[temp1+4]])




    # for temp2 in xapi_dict[temp1]:
    #     print(temp2)

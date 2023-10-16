import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

file = open("saveFile.txt",'r')

weights = np.array([]) 

s = {}
np.set_printoptions(threshold=np.inf)



minMinutes = 30

lineCount = 0
c = 0
for line in file:
    line = line.split(",")[:12]
    time = int(float(line[-1].strip("\n")))
    if time < 0:
        print("hello")
    pd = int(float(line[-2]))
    line = line[:10]
    for l in line:
        l = l.split(":")
        offOrDef = l[1]
        l = l[0]
        if offOrDef == "1":
            name = l+"OOOOO"
        else:
            name = l+"DDDDD"

        if name not in s:
            s[name] = [c,0,0]
            c+=1

        s[name][1] += time

        s[name][2] +=  pd

    lineCount+=1

qualifiedPlayersD = {}
#print(s)

qualPCount = 0
for player in s:
    #print(player,round(s[player][1]/60))
    if s[player][1] > minMinutes * 60:
        qualifiedPlayersD[player] = qualPCount
        qualPCount+=1
        


#print(qualifiedPlayersD)

y = np.array([])    

file.close()

file = open("saveFile.txt",'r')


x = np.zeros((lineCount, len(qualifiedPlayersD)+2))




aaa = 0
#print(aaa)
for line in file:
    line = line.split(",")[:12]
    z = np.zeros(len(qualifiedPlayersD)+2)
    time = int(float(line[-1].strip("\n")))
    pdForSum = int(float(line[-2]))
    net = int(float(line[-2]))/(time/48/60)
    line = line[:10]
    y = np.append(y,net)
    weights = np.append(weights,time)

    #for each player
    for i in range(10):
        line[i] = line[i].split(":")
        player = line[i][0]
        inorout = int(line[i][1])
        if inorout == 1:
            realPlayer = player+"OOOOO"
        if inorout == -1:
            realPlayer = player+"DDDDD"
        mp = s[realPlayer][1]

        if realPlayer not in qualifiedPlayersD:
            if inorout == 1:
                z[-2] += inorout
            if inorout == -1:
                z[-1] += inorout
            #print(player+" replaced")

        else:
            index = qualifiedPlayersD[realPlayer]    
            z[index] = inorout
        

        
        #print(z)
    #print(z)

        # print(z)
    print(aaa,z)
    x[aaa] = z
    aaa+=1
    #print(z)
# print(x)
# print(y)
# print(weights)

#print(weights)
#print(y)

qualifiedPlayersList = list(qualifiedPlayersD)


# print(s)

# # Create a 2D NumPy array
# arr1 = np.array([[1, 2, 3], [4, 5, 6]])
# arr2 = np.array([[7, 8, 9], [10, 11, 12]])

# # Append arr2 to arr1 along axis 0 (row-wise)
# appended_array_axis0 = np.append(arr1, arr2, axis=0)

# # Append arr2 to arr1 along axis 1 (column-wise)
# appended_array_axis1 = np.append(arr1, arr2, axis=1)

# print("Appended array along axis 0 (row-wise):")
# print(appended_array_axis0)

# print("\nAppended array along axis 1 (column-wise):")
# print(appended_array_axis1)



model = LinearRegression()
model.fit(x, y, sample_weight=weights)  # Pass weights using sample_weight

# Obtain the coefficients (slopes) and intercept
slopes = model.coef_
intercept = model.intercept_

# print("Slopes (coefficients):", slopes)
# print("Intercept:", intercept)

# plt.scatter(x[:, 0], y, color='blue', label='X1')  # Plotting X1
# plt.scatter(x[:, 1], y, color='green', label='X2')  # Plotting X2
# plt.plot(x, model.predict(x), color='red', label='Linear regression')
# plt.xlabel('Features')
# plt.ylabel('y')
# plt.legend()
# plt.show()

pv = 1
#print("Coefficients:")

#print(x)
# Mean normalization
mean = np.mean(slopes, axis=0)
std_dev = np.std(slopes, axis=0)

print(mean)
print(std_dev)

#normalized_X = (X - mean) / std_dev

# Standardization
#standardized_X = (X - mean) / std_dev

print(model.coef_)

qualifiedPlayersList.append("REPLACEMENT LEVEL PLAYEROOOOO")
qualifiedPlayersList.append("REPLACEMENT LEVEL PLAYERDDDDD")


#print(mean)
#print(std_dev)
sList = {"REPLACEMENT LEVEL PLAYER": ["REPLACEMENT LEVEL PLAYER",0,0,0,0,0]}


for coef, feature  in sorted(zip( model.coef_, qualifiedPlayersList),reverse = True):
    type = ""
    if "REPLACEMENT LEVEL PLAYEROOOOO" in feature:
        sList["REPLACEMENT LEVEL PLAYER"][2] += (coef-mean) / std_dev
        sList["REPLACEMENT LEVEL PLAYER"][1] += (coef-mean) / std_dev
        continue

    if "REPLACEMENT LEVEL PLAYERDDDDD" in feature:
        sList["REPLACEMENT LEVEL PLAYER"][3] -= (coef-mean) / std_dev
        sList["REPLACEMENT LEVEL PLAYER"][1] -= (coef-mean) / std_dev
        continue


    if "OOOOO" in feature:
        name = feature.split("OOOOO")[0]
        type = "O"
    if "DDDDD" in feature:
        name = feature.split("DDDDD")[0]
        type = "D"
    if name not in sList:
        sList[name] = ["name",0,0,0,s[feature][1],0]

    if name in sList:
        if type == "O":
            sList[name][2] += (coef-mean) / std_dev
            sList[name][1] += (coef-mean) / std_dev
            sList[name][5] += s[feature][2] 
        if type == "D":
            sList[name][3] -= (coef-mean) / std_dev
            sList[name][1] -= (coef-mean) / std_dev
            sList[name][5] -= s[feature][2] 



def sortList(p):
    return sList[p][1]

count = 0
for p in sorted(sList,key = sortList, reverse = True):
    count+=1
    print(count,p,round(sList[p][1],1),round(sList[p][2],1),round(sList[p][3],1),round(sList[p][4]/60),sList[p][5])



# for coef, feature  in sorted(zip( model.coef_, qualifiedPlayersList),reverse = True):
#     #if s[val][1]//60 > 100:
#     if "REPLACEMENT LEVEL PLAYER" in feature:
#         print(f" {pv} {feature}: {round((coef-mean) / std_dev,1)} ")    
#         pass
#     else:
#         print(f" {pv} {feature}: {round((coef-mean) / std_dev,1)} {round(s[feature][1]/60)} ")
#         pv += 1
#         sList.append([(coef-mean) / std_dev * s[feature][1]/60,feature])

# i = 0
# for p in sorted(sList,reverse=True):
#     i+=1
#     #print(i,p[1],round(p[0]),round(s[p[1]][1]/60))

# print(pv)

#model.predict()
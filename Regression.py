import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
#import pymc3 as pm


file = open("saveFile.txt",'r')


                    # Target (dependent variable)

# Assign weights to each data point
weights = np.array([]) 

s = {}
np.set_printoptions(threshold=np.inf)


minMinutes = 100

lineCount = 0
c = 0
for line in file:
    game = line.split(",")[-3]
    line = line.split(",")[:12]
    
    if ".html" in line[-1]:
        print("data point offf")
        continue
    
    time = int(float(line[-1].strip("\n")))
    
    if time < 0:
        print("hello")


    pd = int(float(line[-2]))
    line = line[:10]
    for l in line:
        l = l.split(":")
        team = l[1]
        l = l[0]
        if l not in s:
            s[l] = [c,0,0,set()]
            c+=1

        s[l][1] += time
        if team == '1':
            s[l][2] +=  pd
        else:
            s[l][2] -=  pd
        if game not in s[l][3]:
            s[l][3].add(game)
            if "embiijo" in l:
                print(len(s[l][3]),game)


    lineCount+=1
qualifiedPlayersD = {}

qualPCount = 0
for player in s:
    #print(player,round(s[player][1]/60))
    #if s[player][1] > minMinutes * 60:
    if (s[player][1]/60)/(len(s[player][3])+4.1) > 20:
        qualifiedPlayersD[player] = qualPCount
        qualPCount+=1
    #print(player,round(s[player][1]/60),s[player][2],len(s[player][3]))


#print(len(qualifiedPlayersD))
#print(qualifiedPlayersD)


#print(s)
#print(lineCount)

y = np.array([])    

file.close()

file = open("saveFile.txt",'r')


x = np.zeros((lineCount, len(qualifiedPlayersD)+1))




aaa = 0
#print(aaa)
for line in file:
    line = line.split(",")[:12]
    z = np.zeros(len(qualifiedPlayersD)+1)
    time = int(float(line[-1].strip("\n")))
   
    pd = int(float(line[-2])) /(time/48/60)
    line = line[:10]
    y = np.append(y,pd)
    weights = np.append(weights,time)

    #for each player
    for i in range(10):
        line[i] = line[i].split(":")
        player = line[i][0]
        inorout = int(line[i][1])
        mp = s[player][1]

        if player not in qualifiedPlayersD:
            z[-1] += inorout
            #print(player+" replaced")

        else:
            index = qualifiedPlayersD[player]    
            z[index] = inorout
        

        
        #print(z)
    #print(z)

        # print(z)
    #print(aaa,z)
    x[aaa] = z
    aaa+=1
# print(x)
# print(y)
# print(weights)

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
#normalized_X = (X - mean) / std_dev

# Standardization
#standardized_X = (X - mean) / std_dev

qualifiedPlayersList.append("REPLACEMENT LEVEL PLAYER")

#print(mean)
#print(std_dev)
sList = []

for coef, feature  in sorted(zip( model.coef_, qualifiedPlayersList),reverse = True):
    #if s[val][1]//60 > 100:
    if feature == "REPLACEMENT LEVEL PLAYER":
        print(f" {pv} {feature}: {round((coef-mean) / std_dev,1)} ")    
        pass
    else:
        #print(f" {pv} {feature}: {round((coef-mean) / std_dev,1)} {round(s[feature][1]/60)} {round(s[feature][2])} {(len(s[feature][3]))} {round((s[feature][1]/60)/(len(s[feature][3])+4))}")
        adjSRS = s[feature][2]/(s[feature][1]/60)*48
        if (s[feature][1]/60)/(len(s[feature][3])+4) <20:
            adjSRS *= (s[feature][1]/60)/(len(s[feature][3])+4)/20 
        #if s[feature][1]/60 > 500:
        print(f" {pv} {feature}: {round((coef-mean) / std_dev,1)}  {round(adjSRS,1)} {(len(s[feature][3]))} {round((s[feature][1]/60)/(len(s[feature][3])+4))}")

        pv += 1
        
        sList.append([(coef-mean) / std_dev * s[feature][1]/60,feature])

i = 0
for p in sorted(sList,reverse=True):
    i+=1
    #print(i,p[1],round(p[0]),round(s[p[1]][1]/60))

print(pv)



#model.predict()


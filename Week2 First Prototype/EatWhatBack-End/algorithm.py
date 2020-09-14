from cvxopt import matrix, solvers
import numpy as np

class RecommendationSystem:
    #get food data from database
    def __getFood(self):
        idList = [11,21,35,4,52,63,77,81,9]
        foodNameList = ['Whole Wheat Bread','Yogurt','Apple','Rice','Chinese Cabbage','Chicken breast','Tomato','Beef','Spinach']
        proteinList = [8.50,2.50,0.20,2.6,1.50,19.40,0.9,31.4,2.6]
        carbohydrateList=[50.90,9.30,13.50,25.90,2.70,2.50,4,3.2,4.5]
        fatList = [1.00,2.70,0.2,0.3,0.30,5.00,0.2,11.9,0.3]
        '''
        # 调用数据库获得食物
        # 得到4个list：id1-id9，p1-p9，c1-p9，f1-f9
        '''
        return idList, foodNameList, proteinList, carbohydrateList, fatList

    def __setMatrix(self, proteinList, carbohydrateList, fatList, proteinNeed, carbohydrateNeed, fatNeed, foodMinNeed, foodMaxFood):
        
        constraint = [proteinNeed,proteinNeed,proteinNeed,proteinNeed,proteinNeed,proteinNeed,
                      carbohydrateNeed,carbohydrateNeed,carbohydrateNeed,carbohydrateNeed,carbohydrateNeed,carbohydrateNeed,
                      fatNeed,fatNeed,fatNeed,fatNeed,fatNeed,fatNeed]
        A = np.zeros((54,27))
        valueOfA = [[0,0,proteinList[0]],[0,1,proteinList[1]],[0,2,proteinList[2]],[0,9,-100.],[0,10,100.],
                    [1,0,-proteinList[0]],[1,1,-proteinList[1]],[1,2,-proteinList[2]],[1,9,100.],[1,10,-100.],
                    [2,3,proteinList[3]],[2,4,proteinList[4]],[2,5,proteinList[5]],[2,11,-100.],[2,12,100.],
                    [3,3,-proteinList[3]],[3,4,-proteinList[4]],[3,5,-proteinList[5]],[3,11,100.],[3,12,-100.],
                    [4,6,proteinList[6]],[4,7,proteinList[7]],[4,8,proteinList[8]],[4,13,-100.],[4,14,100.],
                    [5,6,-proteinList[6]],[5,7,-proteinList[7]],[5,8,-proteinList[8]],[5,13,100.],[5,14,-100.],
                    [6,0,carbohydrateList[0]],[6,1,carbohydrateList[1]],[6,2,carbohydrateList[2]],[6,15,-100.],[6,16,100.],
                    [7,0,-carbohydrateList[0]],[7,1,-carbohydrateList[1]],[7,2,-carbohydrateList[2]],[7,15,100.],[7,16,-100.],
                    [8,3,carbohydrateList[3]],[8,4,carbohydrateList[4]],[8,5,carbohydrateList[5]],[8,17,-100.],[8,18,100.],
                    [9,3,-carbohydrateList[3]],[9,4,-carbohydrateList[4]],[9,5,-carbohydrateList[5]],[9,17,100.],[9,18,-100.],
                    [10,6,carbohydrateList[6]],[10,7,carbohydrateList[7]],[10,8,carbohydrateList[8]],[10,19,-100.],[10,20,100.],
                    [11,6,-carbohydrateList[6]],[11,7,-carbohydrateList[7]],[11,8,-carbohydrateList[8]],[11,19,100.],[11,20,-100],
                    [12,0,fatList[0]],[12,1,fatList[1]],[12,2,fatList[2]],[12,21,-100.],[12,22,100.],
                    [13,0,-fatList[0]],[13,1,-fatList[1]],[13,2,-fatList[2]],[13,21,100.],[13,22,-100.],
                    [14,3,fatList[3]],[14,4,fatList[4]],[14,5,fatList[5]],[14,23,-100.],[14,24,100.],
                    [15,3,-fatList[3]],[15,4,-fatList[4]],[15,5,-fatList[5]],[15,23,100.],[15,24,-100.],
                    [16,6,fatList[6]],[16,7,fatList[7]],[16,8,fatList[8]],[16,25,-100.],[16,25,100],
                    [17,6,-fatList[6]],[17,7,-fatList[7]],[17,8,-fatList[8]],[17,26,100.],[17,26,-100],
                    [18,0,-1.],[19,1,-1.],[20,2,-1.],[21,3,-1.],[22,4,-1.],[23,5,-1.],[24,6,-1.],[25,7,-1.],[26,8,-1.],[27,9,-1.],[28,10,-1.],[29,11,-1.],
                    [30,12,-1.],[31,13,-1.],[32,14,-1.],[33,15,-1.],[34,16,-1.],[35,17,-1.],[36,18,-1.],[37,19,-1.],[38,20,-1.],[39,21,-1.],[40,22,-1.],
                    [41,23,-1.],[42,24,-1.],[43,25,-1.],[44,26,-1.],[45,0,1.],[46,1,1.],[47,2,1.],[48,3,1.],[49,4,1.],[50,5,1.],[51,6,1.],[52,7,1.],[53,8,1.]                   
                    ]
        
        for i in range(len(valueOfA)):
            A[valueOfA[i][0]][valueOfA[i][1]] = valueOfA[i][2]
        
        A = matrix(A)
        
        b = matrix([30.0*proteinNeed,-30.0*proteinNeed,40.0*proteinNeed,-40.0*proteinNeed,30.0*proteinNeed,-30.0*proteinNeed]+
                   [30.0*carbohydrateNeed,-30.0*carbohydrateNeed,40.0*carbohydrateNeed,-40.0*carbohydrateNeed,30.0*carbohydrateNeed,-30.0*carbohydrateNeed]+
                   [30.0*fatNeed,-30.0*fatNeed,40.0*fatNeed,-40.0*fatNeed,30.0*fatNeed,-30.0*fatNeed]+
                   [-foodMinNeed for i in range(9)]+
                   [0.0 for i in range(18)]+
                   [foodMaxFood for i in range(9)]
                   )
        
        c = matrix([0. for i in range(9)]
                   +[100.0/c for c in constraint])
        '''
        print(A)
        print('##########')
        print(b)
        print('##########')
        print(c)
        '''
        return A,b,c
             
    #cal  
    
    def __caculateEveryFoodNeeds(self, proteinList, carbohydrateList, fatList, proteinNeed, carbohydrateNeed, fatNeed, foodMinNeed, foodMaxFood):
        '''
        此函数为算法的核心！
        判断此组食物能否符合要求
        若可符合，返回true，并返回每类食物的质量
        否则，返回false
        :param proteinList:
        :param carbohydrateList:
        :param fatList:
        :return:
        '''
        flag = True
        XList = []
        '''
        proteinCon = proteinList + [-100.,100,0.,0.,0.,0.]
        carbohydrateCon = carbohydrateList + [0.,0.,-100.,100.,0.,0.]
        fatCon = fatList + [0.,0.,0.,0.,-100.,100.]
        constraint = [proteinNeed, proteinNeed, carbohydrateNeed, carbohydrateNeed, fatNeed, fatNeed]
        A = np.zeros((45,27))
        for i in range(A.shape[1]):
            A[0][i] = proteinCon[i]
            A[1][i] = -proteinCon[i]
        for i in range(A.shape[1]):
            A[2][i] = carbohydrateCon[i]
            A[3][i] = -carbohydrateCon[i]
        for i in range(A.shape[1]):
            A[4][i] = fatCon[i] 
            A[5][i] = -fatCon[i] 
        for i in range(15):
            A[6+i][i] = -1
        for i in range(9):
            A[21+i][i] = 1
        '''
        
        
        # 21个约束条件，21列：6+9+6
        # 15个变量，15行：9+6
        '''
        A = matrix(A)
        b = matrix([100.0*proteinNeed,-100.0*proteinNeed,100.0*carbohydrateNeed,-100.0*carbohydrateNeed,100.0*fatNeed,-100.*fatNeed]
                   +[-foodMinNeed for i in range(9)] 
                   +[0.,0.,0.,0.,0.,0.] + [foodMaxFood for i in range(9)]
                   )
        c = matrix([0. for i in range(9)]
                   +[100.0/c for c in constraint]
                   )
        '''
        A,b,c = self.__setMatrix(proteinList, carbohydrateList, fatList, proteinNeed, carbohydrateNeed, fatNeed, foodMinNeed, foodMaxFood)
        sol = solvers.lp(c, A, b)
        for i in range(9):
            XList.append(sol['x'][i])
        return flag,XList


        #return flag, XList

    def __formRecipe(self, idList, XList, foodNameList):
        '''
        封装菜名和各自的重量
        :param idList:
        :param XList:
        :return:
        '''
        recipe = []
        for i in range(9):
            recipe.append(Food(idList[i],XList[i],i/3,foodNameList[i]))
        return recipe

    def recommend(self, user):

        # pN cN fN。caloeryNeed只需要向用户显示
        caloeryNeed, proteinNeed, carbohydrateNeed, fatNeed, weeksNeed = self.__calNutrientNeeds(user)

        flag = False
        idList = []
        foodNameList = []
        proteinList = []
        carbohydrateList = []
        fatList = []
        XList = []
        while not flag:
            idList,foodNameList,proteinList,carbohydrateList,fatList = self.__getFood()
            flag,XList = self.__caculateEveryFoodNeeds(proteinList, carbohydrateList, fatList, proteinNeed, carbohydrateNeed, fatNeed , 50, 250)
      
        recipe = self.__formRecipe(idList,XList,foodNameList)

        return recipe, caloeryNeed, proteinNeed, carbohydrateNeed, fatNeed, weeksNeed

    def __calNutrientNeeds(self, user):
        proteinIndex = [0.165, 0.25, 0.2]
        carbohydrateIndex = [0.6, 0.55, 0.55]
        fatIndex = [0.235, 0.20, 0.25]

        index = [1.15, 0.8, 1]

        gender = user.getGender()
        age = user.getAge()
        height = user.getHeight()
        weight = user.getWeight()
        goal = user.getGoal()
        goalWeight = user.getGoalWeight()
        activityIndex = user.getActivityIndex()

        caloeryNeed = 0
        if gender == 0:
            caloeryNeed = 655 + 9.6 * weight + 1.8 * height - 4.7 * age
        elif gender == 1:
            caloeryNeed = 66 + 13.7 * weight + 5 * height - 6.8 * age

        caloeryNeed = caloeryNeed * activityIndex * index[goal]

        proteinNeed = caloeryNeed * proteinIndex[goal] / 4
        carbohydrateNeed = caloeryNeed * carbohydrateIndex[goal] / 4
        fatNeed = caloeryNeed * fatIndex[goal] / 9

        weeksNeed = 0
        if goal == 0 and goalWeight > weight:
            weeksNeed = (goalWeight - weight) * 1100 / 500 + 1
        elif goal == 1 and goalWeight < weight:
            weeksNeed = (weight - goalWeight) * 1100 / 500 + 1

        return caloeryNeed, proteinNeed, carbohydrateNeed, fatNeed, weeksNeed


class User:
    __gender = 0
    #0:female 1:male
    __age = 0
    __height = 0
    __weight = 0
    __goal = 0
    #0:increasing muscle 1:lose weight 2:shaping
    __goalWeight = 0
    __activityIndex = 0

    def __init__(self, gender, age, height, weight, goal, goalWeight, activityIndex):
        self.__gender = gender
        self.__age = age
        self.__height = height
        self.__weight = weight
        self.__goal = goal
        self.__goalWeight = goalWeight
        self.__activityIndex = activityIndex

    def getGender(self):
        return self.__gender

    def getAge(self):
        return self.__age

    def getHeight(self):
        return self.__height

    def getWeight(self):
        return self.__weight

    def getGoal(self):
        return self.__goal

    def getGoalWeight(self):
        return self.__goalWeight

    def getActivityIndex(self):
        return self.__activityIndex

class Food:
    __foodId = 0
    __gramNeed = 0
    __eatTime = 0
    __foodName =0
    #0代表早餐，1代表午餐，2代表晚餐
    
    def __init__(self,foodId,gramNeed,eatTime,foodName):
        self.__foodId = foodId
        self.__gramNeed = gramNeed
        self.__eatTime = eatTime
        self.__foodName = foodName
    
    def getId(self):
        return self.__foodId
    
    def getGramNeed(self):
        return self.__gramNeed
    
    def getEatTime(self):
        return self.__eatTime
    
    def getFoodName(self):
        return self.__foodName
    
    def display(self):
        print('foodName:'+str(self.__foodName))
        print('gramNeed:'+str(self.__gramNeed)+'g')
        
        
    
#
# user = User(1, 21, 170, 80, 1, 70, 1.2)
# #male, 21 years old, 170cm , 80kg , goal: lose weight ,goalWeight:70kg, activityIndex:1.2
# rs = RecommendationSystem()
# '''
# pList = [2.5,15.0,0.9,2.6,12.10,0.8,8.3,1.5,1.4]
# cList = [9.3,66.90,4.00,25.9,0.1,2.90,61.90,2.7,2.2]
# fList = [2.70,6.70,0.2,0.3,10.5,0.2,0.7,0.3,0.2]
#
# pn = 113
# cn = 248
# fn = 40
# rs.caculateEveryFoodNeeds(pList,cList,fList,pn,cn,fn,50,250)
# '''
# recipe, caloeryNeed, proteinNeed, carbohydrateNeed, fatNeed, weeksNeed = rs.recommend(user)
#
# for i in range(len(recipe)):
#     if i==0:
#         print('Breakfast')
#     elif i==3:
#         print('Lunch')
#     elif i==6:
#         print('Dinner')
#     print()
#     recipe[i].display()
#     print()
# print(caloeryNeed, proteinNeed, carbohydrateNeed, fatNeed, weeksNeed)

#breakfast : about two slices of bread, a cup of yogurt, 1/3 apple
#lunch: a bowl of rice, 6 slices of cabbage, 3 slices of chicken breast
#dinner: 1.5 tomatoes, 6 slices of beef, two spinach

    
    
    

'''   
# 以下为 cvxopt 的一个demo
A = matrix([
    [1.0, -1.0, 2.0, -2.0, 3.0, -3.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], # x1
    [0.0, 0.0, 1.0, -1.0, 2.0, -2.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], # x2
    [1.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # x3
    [-1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0], # x4
    [0.0, 0.0, 1.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0], # x5
    [0.0, 0.0, -1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0], # x6
    [0.0, 0.0, 0.0, 0.0, 1.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0], # x7
    [0.0, 0.0, 0.0, 0.0, -1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0] # x8
])
print(A)


b = matrix([10.0, -10.0, 40.0, -40.0, 100.0, -100.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
c = matrix([0.0, 0.0, 2.0, 0.0, 0.0, 2.0, 1.0, 0.0])
print(A)
print(b)
print(c)
sol = solvers.lp(c, A, b)
print(sol['x'])


a=np.array([
    [1.0, -1.0, 2.0, -2.0, 3.0, -3.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], # x1
    [0.0, 0.0, 1.0, -1.0, 2.0, -2.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], # x2
    [1.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # x3
    [-1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0], # x4
    [0.0, 0.0, 1.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0], # x5
    [0.0, 0.0, -1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0], # x6
    [0.0, 0.0, 0.0, 0.0, 1.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0], # x7
    [0.0, 0.0, 0.0, 0.0, -1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0] # x8
    ])

print(matrix(a))
print(matrix(a.T))
'''
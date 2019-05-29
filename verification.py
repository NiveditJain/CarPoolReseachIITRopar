from docplex.mp.model import Model # for all binary integer programming part
import numpy as np #for converting pandas containers to regular integers
import pandas as pd #for data management
import gc #for garbage collection
# importing all files
print('code loaded in memory succesfully')
def ImportDataFiles(): #to import the datafiles
	PeopleData=pd.read_csv('PersonOriginAndSource.csv')
	DistanceMatrix=pd.read_csv('distanceMatrix.csv')
	return [PeopleData,DistanceMatrix]

# opening the files
PeopleData,DistanceMatrix=ImportDataFiles()
print('datafiles opened succesfully')
# creating the model for car pool verification team
SRNC=Model('SRNC')
print('initialized model')
# to select the model as needed

def SelectPeopleInNetWork():
	print('Input the number of people you want in network(<=2000)')
	selectedPeople=int(input())
	PeopleData=PeopleData[:selectedPeople]
	print('Selected first '+ str(selectedPeople)+' people from a list of 2000 randomly generated people from a list of 100k+')
	return(PeopleData,selectedPeople)

#we are considering an limit of 0.0000001 for equality to to floating point errors
# this limit is a valid number as my dataset is well know from before
def checkEquality(num1,num2):
	return num1-num2<=0.0000001 

# to get information of person
# person info returned in the format
def getPersonInfo(id,selectedPeople):
	if(id[0]<2000):
		if(id[1]<2000):
			return [PeopleData.loc[id[0],['lat1','long1']].tolist(),PeopleData.loc[id[1],['lat1','long1']].tolist()]
		else:
			return [PeopleData.loc[id[0],['lat1','long1']].tolist(),PeopleData.loc[id[1]-selectedPeople,['lat2','long2']].tolist()]
	else:
		if(id[1]<2000):
			return [PeopleData.loc[id[0]-selectedPeople,['lat2','long2']].tolist(),PeopleData.loc[id[1],['lat1','long1']].tolist()]
		else:
			return [PeopleData.loc[id[0]-selectedPeople,['lat2','long2']].tolist(),PeopleData.loc[id[1]-selectedPeople,['lat2','long2']].tolist()]	


# to get distance time details of a person id
def getWeight(id,selectedPeople):
	id[0]=id[0]-1
	id[1]=id[1]-1
	PersonInfo=getPersonInfo(id,selectedPeople)
	return DistanceMatrix.loc[\
		(checkEquality(DistanceMatrix['lat1'],PersonInfo[0][0])) &
		(checkEquality(DistanceMatrix['long1'],PersonInfo[0][1])) &
		(checkEquality(DistanceMatrix['lat2'],PersonInfo[1][0])) & 
		(checkEquality(DistanceMatrix['long2'],PersonInfo[1][1]))\
		].dis.tolist()[0]

# to add constrains in the model

# testing code beneath

# print(PeopleData)
# y=PeopleData.loc[0,['lat1','long1']].tolist()
# y=getPersonInfo([0,2000],2000)
# print(y)
# temp=DistanceMatrix.loc[(checkEquality(DistanceMatrix['lat1'],y[0][0])) & (checkEquality(DistanceMatrix['long1'],y[0][1])) & (checkEquality(DistanceMatrix['lat2'],y[1][0])) & (checkEquality(DistanceMatrix['long2'],y[1][1]))].dis.tolist()[0]
# print(temp)
# print(getWeight([0,2000],2000))
# print(type(y),type(y[0][0]))
# print(getWeight([0,2000],2000))
# print(checkEquality(92,92.0000000001))
print('Please Input CP')
CP=int(input())

print('select driver')
driver=int(input())

print('creating required variable')
N=selectedPeople
N_loop=range(1,N+1)
CP_loop=range(1,CP+1)
R=2*CP+1
R_loop=range(1,R+1)
N2_loop=range(1,2*N+1)
R_minus1_loop=range(1,R)
variables=[(i,j,r)\
for i in N2_loop\
for j in N2_loop\
for r in R_loop]
x=model.binary_var_dict(variables,name='x')
print('created all required variables succesfully')

print('Constraints adddition started')

print('adding constraint one')
SRNC.add_constraint(SNRC.sum(x[]))	
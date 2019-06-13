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
	PeopleDataAfterCut=PeopleData[:selectedPeople]
	print('Selected first '+ str(selectedPeople)+' people from a list of 2000 randomly generated people from a list of 100k+')
	return(PeopleDataAfterCut,selectedPeople)

#we are considering an limit of 0.0000001 for equality to to floating point errors
# this limit is a valid number as my dataset is well know from before
def checkEquality(num1,num2):
	return num1-num2<=0.0000001 

# to get information of person
# person info returned in the format
def getPersonInfo(id,selectedPeople):
	if(id[0]<selectedPeople):
		if(id[1]<selectedPeople):
			return [PeopleData.loc[id[0],['lat1','long1']].tolist(),PeopleData.loc[id[1],['lat1','long1']].tolist()]
		else:
			return [PeopleData.loc[id[0],['lat1','long1']].tolist(),PeopleData.loc[id[1]-selectedPeople,['lat2','long2']].tolist()]
	else:
		if(id[1]<selectedPeople):
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


<<<<<<< HEAD
=======
PeopleData,selectedPeople=SelectPeopleInNetWork()
print(PeopleData)
print(getWeight([1,5],selectedPeople))
>>>>>>> f3ee3f3214c34dd09a1c5e42e9c92688fb4d2409

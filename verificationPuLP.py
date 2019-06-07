from pulp import * #cplex is unable to process some files

selectedPeople=5
CP=int(input('Please Input Car Capcity \n'))
Driver=int(input('Please Input Driver Location <= %d \n' %(selectedPeople)))
print('generating required variables')
N=selectedPeople
R=2*CP+1
home=[i for i in range(1,N+1)]
work=[i for i in range(N+1,2*N+1)]
steps=[i for i in range(1,R+1)]
print(home)
home_except_driver= home
del home_except_driver[Driver-1]
All=[i for i in range(1,N*2+1)]
distance=[\
[0,1,2,3,4,5,6,7,8,9],\
[1,0,1,2,3,4,5,6,7,8],\
[2,1,0,1,2,3,4,5,6,7],\
[3,2,1,0,1,2,3,4,5,6],\
[4,3,2,1,0,1,2,3,4,5],\
[5,4,3,2,1,0,1,2,3,4],\
[6,5,4,3,2,1,0,1,2,3],\
[7,6,5,4,3,2,1,0,1,2],\
[8,7,6,5,4,3,2,1,0,1],\
[9,8,7,6,5,4,3,2,1,0],\
]
print('generated all required variables')
SRNC=LpProblem('SRNC',LpMinimize)
x=LpVariable.dicts('x',\
	[(i,j,r)\
	 for i in All\
	  for j in All\
	   for r in steps],0,1,LpBinary)

w=LpVariable.dicts('w',\
	[i,])

for i in All:
	for j in All:
		SRNC+=
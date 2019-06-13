from docplex.mp.model import Model


CP=3
Driver=1
R=7
N=4

getWeight=[\
[0,1,2,3,4,5,6,7],\
[1,0,1,2,3,4,5,6],\
[3,2,1,0,1,2,3,4],\
[7,6,5,4,3,2,1,0],\
[6,5,4,3,2,1,0,1],\
[5,4,3,2,1,0,1,2],\
[4,3,2,1,0,1,2,3],\
[2,1,0,1,2,3,4,5],\
]

model=Model('SRNC')

variablesBar=[(i,j,r)\
 for i in range(1,2*N+1)\
 for j in range(1,2*N+1)\
 for r in range(1,R+1)]


x=model.binary_var_dict(variablesBar,name='x')

variablesWeights=[(i,j)\
 for i in range(1,2*N+1)\
 for j in range(1,2*N+1)]

wght=model.integer_var_dict(variablesWeights,name='wght')



def setObjective():
	obj=model.minimize(model.sum(wght[i,j]
		for i in range(1,2*N+1)\
		for j in range(1,2*N+1)))

def setWeights():
	for i in range(1,2*N+1):
		for j in range(1,2*N+1):
			model.add_constraint(wght[i,j]==getWeight[i-1][j-1]*model.sum(x[i,j,r] for r in range(1,R+1)))

def setCnstrt1():
	model.add_constraint(model.sum(x[Driver,h,1] for h in range(1,N+1))==1)

def setCnstrt2():
	model.add_constraint(model.sum(x[w,Driver+N,R] for w in range(N+1,2*N+1))==1)

def setCnstrt3():
	model.add_constraint(model.sum(x[i,h,r] for i in range(1,2*N+1) for h in range(1,N+1) for r in range(1,R+1))==CP)

def setCnstrt4():
	model.add_constraint(model.sum(x[i,w,r] for i in range(1,2*N+1) for w in range(N+1,2*N+1) for r in range(1,R+1))==CP+1)

def setCnstrt5():
	for i in range(1,2*N+1):
		for r in range(1,R+1):
			model.add_constraint(x[i,i,r]==0)
	
	for i in range(2,N):
		model.add_constraint(model.sum(x[i,j,r] for j in range(1,2*N+1)\
			for r in range(1,R))==model.sum(x[i+N,j,r] for j in range(1,2*N+1)\
				for r in range(1,R)))

	for j in range(2,N):
		model.add_constraint(model.sum(x[i,j,r] for i in range(1,2*N+1)\
			for r in range(1,R))==model.sum(x[i,j+N,r] for i in range(1,2*N+1)\
				for r in range(1,R)))
	
	for h in range(1,N+1):
		for r in range(1,R+1):
			model.add_constraint_(model.sum(x[i,h,r] for i in range(1,2*N+1))<=\
				model.sum(x[i,h+N,f] for i in range(1,2*N+1)\
					for f in range(r+1,R+1)))

def setCnstrt6():
	for r in range(1,R+1):
		model.add_constraint(model.sum(x[i,j,r] for i in range(1,2*N+1) for j in range(1,2*N+1))==1)

def setCnstrt7():
	for j in range(1,2*N+1):
		model.add_constraint(model.sum(x[i,j,r] for i in range(1,2*N+1) for r in range(1,R+1))<=1)

def setCnstrt8():
	for i in range(1,2*N+1):
		model.add_constraint(model.sum(x[i,j,r] for j in range(1,2*N+1) for r in range(1,R+1))<=1)

def setCnstrt9():
	for j in range(1,2*N+1):
		for r in range(1,R):
			model.add_constraint(model.sum(x[i,j,r] for i in range(1,2*N+1))==model.sum(x[j,i,r+1] for i in range(1,2*N+1)))

print('Started')
setObjective()
print('Objective Added')
setWeights()
print('weights added')
setCnstrt1()
print('Done1')
setCnstrt2()
print('Done2')
setCnstrt3()
print('Done3')
setCnstrt4()
print('Done4')
setCnstrt5()
print('Done5')
setCnstrt6()
print('Done6')
setCnstrt7()
print('Done7')
setCnstrt8()
print('Done8')
setCnstrt9()
print('Done9')
model.solve()
model.print_information()
model.print_solution()
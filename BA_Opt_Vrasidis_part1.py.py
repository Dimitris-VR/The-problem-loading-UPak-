from __future__ import division
import numpy as np
import math
import sympy as sym
from sympy import *
import os
import pyomo.environ as pyo
from pyomo.opt import SolverFactory




model = pyo.AbstractModel()



model.T = Param( within=PositiveIntegers )
model.Number_of_Items = Param( within=PositiveIntegers )
 

# Definition of sets
model.Trucks = pyo.Set() # Set of Trucks
model.Items = pyo.Set() # Set of Items


# # # # The initialize keyword can also be used to specify the elements in a set:
model.i = pyo.RangeSet(1, model.Number_of_Items)
model.j = pyo.RangeSet(1, model.T)


model.Price = pyo.Param(model.Items,within=pyo.NonNegativeIntegers)
model.Capacity= pyo.Param(model.Trucks,within=pyo.NonNegativeIntegers)
model.Size= pyo.Param(model.Items,within=pyo.NonNegativeIntegers)


# Definition of Dual variables
model.y = pyo.Var(model.Items, within=Binary)  # Aποδοχή ή όχι της παραγγελίας
model.x = pyo.Var(model.Items, model.Trucks, within=Binary) # Φόρτωμα ή όχι στο φορτηγό
 


def obj_rule(model):
    return (sum(model.y[i]*model.Price[i] for i in model.Items))
model.obj = pyo.Objective(rule=obj_rule, sense=pyo.maximize)


def Capacity_constraint(model,j):
            return sum(model.x[i,j] * model.Size[i] for i in model.Items) <= model.Capacity[j]
model.Capacity_constraint = Constraint( model.Trucks, rule=Capacity_constraint )




def mass_balance(model,i):             
                  return sum(model.x[i,j]  for j in model.Trucks) == model.y[i] 
model.mass_balance = Constraint( model.Items, rule=mass_balance )




cwdir = os.getcwd() #the current working directory must be set to the script location
datafile = os.path.join(os.sep, cwdir + '\\BA_Opt_kaparis_part1.dat')


instance = model.create_instance(datafile)

instance.pprint()

opt = pyo.SolverFactory('glpk')


solver = pyomo.opt.SolverFactory('glpk')
results = solver.solve(instance)
results.write()
instance.solutions.load_from(results)

for v in instance.component_objects(pyo.Var, active=True):
    print ("Variable",str(v))
varobject1 = getattr(instance, str(v))
for index in varobject1:
      print (" ",index, varobject1[index].value)


# print (" ",('Item1', 'Truck1'), varobject1[('Item1', 'Truck1')].value)
for v in instance.component_objects(pyo.Param, active=True):
    print ("Param",str(v))
varobject2 = getattr(instance, str(v))
# print(model.Size)

    

size=[]
for index in varobject2:
    size.append(varobject2[index] )
    
Capacity_truck_1_used=[]
Capacity_truck_2_used=[]

# for i in range(0,len(size)):
  
#     Capacity_truck_1_used.append(x_j_1[i]*size[i])
#     Capacity_truck_2_used.append(x_j_2[i]*size[i])
    

 
# for index in varobject2:
#     print (" ",varobject2[index])
    
# varobject3 = getattr(instance, str(v))    
# print("Param",str(v))


# print('H χωρητικότητα [m^3] που χρησιμοποιείται από το Truck 1 είναι ίση με:')    
# print(sum(Capacity_truck_1_used)) 

# print('H χωρητικότητα [m^3] που χρησιμοποιείται από το Truck 2 είναι ίση με:') 
# print(sum(Capacity_truck_2_used))  
 

# for v in instance.component_objects(Var, active=True):
#     print ("Variable component object",v)
#     for index in v:
#         print ("   ", index, v[index].value)
print ("If noted with 1, it means that item_i is transported by Truck_j")

for index in varobject1:
        
        print ("   ", index, varobject1[index].value)









# for v in instance.component_objects(Param, active=True):
#     print ("Variable component object",v)
#     for index in v:
#         print ("   ", index, v[index]) 
        
        
# print (instance.Price['Item1'])        
        
price=[]
for index in instance.Price:
    price.append(instance.Price[index]) 
    
    
capacity=[]
for index in instance.Capacity:
    capacity.append(instance.Capacity[index])     
    
    
    
    
        
# print(price)       
# print(capacity)        
        
        
        
# capacity=[]
# for index in instance.Capacity:
#     print(varobject1[('Item1', index)].value)         
        
        
# Capacity_truck_i_used=[]       
# for index in instance.Capacity: 
#      i=-1
#      for index2 in varobject2:   
#         i=i+1
#         Capacity_truck_i_used.append(varobject1[(index2, index)].value*size[i])
        
# print(len(instance.Capacity))        
        
        
rows, cols = (len(instance.Capacity), len(size))
Capacity_truck_i_used=[]
for index in instance.Capacity: 
    i=-1
    col = []
    for index2 in varobject2:   
        i=i+1
        col.append(varobject1[(index2, index)].value*size[i])
    Capacity_truck_i_used.append(col)
# print(Capacity_truck_i_used) 


Capacity_Truck_i_used=np.sum(Capacity_truck_i_used, axis=1)


Y=[]
for index in instance.y:
    Y.append(instance.y[index].value) 




# Υ=[]
# for index in varobject1:
#     Υ.append(varobject1 )
# print(Y)

Maximum_Profit=[]
for i in range(0,len(size)):
  
    Maximum_Profit.append(Y[i]*price[i])
Maximum_Profit=sum(Maximum_Profit)




print('Summary of results')

print('The maximum profit is:')
print(Maximum_Profit)

      


    
    
    
print('The capacity used in truck i')     
for i in range(0,len(Capacity_Truck_i_used)):
   value= Capacity_Truck_i_used[i]
   print(i, value)
   
   
   
   
   
Items_loaded_in_truck_j=[]
for index in instance.Capacity: 
    i=-1
    col = []
    for index2 in varobject2:   
        i=i+1
        col.append(varobject1[(index2, index)].value)
    Items_loaded_in_truck_j.append(col)   
    
    
i=-1    
for index in instance.Capacity:
    i=i+1
    print('Orders Assigned in truck', i, 'are the following:')
    # print(Items_loaded_in_truck_j[i])  
    h=Items_loaded_in_truck_j[i]
    f=np.array(h)
    h_new=list(np.nonzero(f)[0])
    print(h_new)
    

   

# import numpy as np
# li = [2, 0, 5, 7, 0, 9]
# arr = np.array(li)
# li_new = list(np.nonzero(arr)[0]) 
# print(li_new)   
   
   
   
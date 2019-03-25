# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 12:58:39 2019

@author: Alexis Navarro
CS 2302
Lab #4
Purpose:The purpose of this lab is to be able to work with b-tree and understand how they work and to be able to 
        manipulate them
"""

class BTree(object):
    # Constructor
    def __init__(self,item=[],child=[],isLeaf=True,max_items=5):  
        self.item = item
        self.child = child 
        self.isLeaf = isLeaf
        if max_items <3: #max_items must be odd and greater or equal to 3
            max_items = 3
        if max_items%2 == 0: #max_items must be odd and greater or equal to 3
            max_items +=1
        self.max_items = max_items

def FindChild(T,k):
    # Determines value of c, such that k must be in subtree T.child[c], if k is in the BTree    
    for i in range(len(T.item)):
        if k < T.item[i]:
            return i
    return len(T.item)
             
def InsertInternal(T,i):
    # T cannot be Full
    if T.isLeaf:
        InsertLeaf(T,i)
    else:
        k = FindChild(T,i)   
        if IsFull(T.child[k]):
            m, l, r = Split(T.child[k])
            T.item.insert(k,m) 
            T.child[k] = l
            T.child.insert(k+1,r) 
            k = FindChild(T,i)  
        InsertInternal(T.child[k],i)   
            
def Split(T):
    #print('Splitting')
    #PrintNode(T)
    mid = T.max_items//2
    if T.isLeaf:
        leftChild = BTree(T.item[:mid]) 
        rightChild = BTree(T.item[mid+1:]) 
    else:
        leftChild = BTree(T.item[:mid],T.child[:mid+1],T.isLeaf) 
        rightChild = BTree(T.item[mid+1:],T.child[mid+1:],T.isLeaf) 
    return T.item[mid], leftChild,  rightChild   
      
def InsertLeaf(T,i):
    T.item.append(i)  
    T.item.sort()

def IsFull(T):
    return len(T.item) >= T.max_items

def Insert(T,i):
    if not IsFull(T):
        InsertInternal(T,i)
    else:
        m, l, r = Split(T)
        T.item =[m]
        T.child = [l,r]
        T.isLeaf = False
        k = FindChild(T,i)  
        InsertInternal(T.child[k],i)   
        
 
def PrintD(T,space):
    # Prints items and structure of B-tree
    if T.isLeaf:
        for i in range(len(T.item)-1,-1,-1):
            print(space,T.item[i])
    else:
        PrintD(T.child[len(T.item)],space+'   ')  
        for i in range(len(T.item)-1,-1,-1):
            print(space,T.item[i])
            PrintD(T.child[i],space+'   ')
    

        
#------------------------------------------------------------------------------
#Question 1  
#Find the height of a Tree by using recursion 
def height(T):
    if T.isLeaf:
        return 0
    return 1 + height(T.child[0])
#------------------------------------------------------------------------------
   
#Question 2
#Transfer the values from the b-tree to a list. This method is similar to transfering the values of a BST to a list from lab #3
    
def BT_ToList(T,L):
    if T.isLeaf: 
        for i in range(len(T.item)):#This is done by using for loops to traverse the elements that are in that depth
            L.append(i)#appends the elements of the tree to the list
    else:
        for i in range(len(T.item)):
             BT_ToList(T.child[i], L)#Recursive call to traverse the left side of the b-tree
             L.append(T.item[i])
             BT_ToList(T.child[-1],L)#Recursive call to traverse the right side of the b-tree
    return L


#------------------------------------------------------------------------------
           
#Question 3
#Finds the minimum element in the b-tree
def minElem(T,d):
    if d==0:
        return T.item[0]
    return minElem(T.child[0],d-1)#Recursive call to traverse the left side of the b-tree since we want the minimum element


#------------------------------------------------------------------------------

#Question 4
#Finds the maximum element in the b-tree
def maxElem(T,d):
    if d==0:
        return T.item[-1]
    return maxElem(T.child[-1],d-1)#Recursive call to traverse the right side of the b-tree since we want the maximum element


#------------------------------------------------------------------------------
#Question 5
#Finds the amount of nodes in the b-tree    
def numOfNodes(T,d):
    count=0
    h=height(T)
    
    if d>h:
        return -1
    if d == 0:
      return len(T.item)
    if T.isLeaf:
        return 0
    else:
        for i in range(len(T.item)):
           count+=numOfNodes(T.child[i],d-1)#Recustive call where the method traverses the tree,but still adds the count value of nodes
        return count+ numOfNodes(T.child[len(T.item)],d-1)#Recursive call where it returns the amount of nodes and traverses the tree, by passing the length of the elements in that depth of the tree
    
    
#------------------------------------------------------------------------------
#Question 6       
#prints all the elements at a certain depth in the b-tree 
def print_AtDepth(T,d):
    if d == 0:
        for i in range(len(T.item)):
            print(T.item[i],end=' ') #prints all the elements in that certain depth
    else:
        if T.isLeaf is not True:
            for i in range(len(T.item)):
                print_AtDepth(T.child[i],d-1)#Recursive call that taverses the left side of the b-tree
                print_AtDepth(T.child[i-1],d-1)#Recursive call that traverses the right side of the b-tree
                
                
#------------------------------------------------------------------------------
#Question 7
#Counts the amount of full nodes inside the b-tree                
def numOf_FullNodes(T):
    count=0
    if len(T.item)==T.max_items:# The max items that we can have is 5
        count+=1
    if T.isLeaf: #We return 0 if we reach a leaf node since we only want NODES
        return 0
    else:
        for i in range(len(T.item)):
            count+=numOf_FullNodes(T.child[i])
        count+numOf_FullNodes(T.child[len(T.item)])
    return count
    
#------------------------------------------------------------------------------
#Question 8
#Counts the amount of full leaves in the b-tree                                 
def numOf_FullLeaves(T):
    count=0
    if T.isLeaf:
        if len(T.item)==T.max_items:# The max items that we can have is 5
            count+=1
    else: # this else is if we have a node that is not a leaf
        for i in range(len(T.item)):
            count+=numOf_FullLeaves(T.child[i])
        count+numOf_FullLeaves(T.child[len(T.item)])
    return count
    
    
'''    
def depthOfNode(T,k):
    if k in T.item:
        return 0
    else:
'''        
        

             
        
#------------------------------------------------------------------------------


L = [30, 50, 10, 20, 60, 70, 100, 40, 90, 80, 110, 120, 1, 11 , 3, 4, 5,105, 115, 200, 2, 45, 6,1,1,1,4,4,4,4,4]
T = BTree()    
for i in L:
    Insert(T,i)
    PrintD(T,'') 
    print('\n####################################')
          
L2=[]
T2= BTree()

for k in L2:
    Insert(T2,k)
E=[]          

print('The height is ',height(T))#1
print('Tree to List',  BT_ToList(T,E))#2
print('the minimum element is ',minElem(T,1))#3
print('the maximum element is ',maxElem(T,0))#4
print('The number of Nodes are:', numOfNodes(T,1))#5
print('Elements at depth are: ')
print_AtDepth(T,0)#6
print()
print('The number of full Nodes are: ', numOf_FullNodes(T))#7
print('The number of full Leaves are: ', numOf_FullLeaves(T))#8
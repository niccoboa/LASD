import  random	
import math
#from inspect import signature

import string

import matplotlib.pyplot as plt # plot graph
import matplotlib.ticker as mticker # custom interval freqeuncy axis
import matplotlib.patches as mpatches # custom legend element(s)

import numpy as np


# Table Size
m = 1500
# Total elements saved
n = 0

# Table declaration
T1 = [[] for _ in range(m)] # It'll be used w/ division method
T2 = [[] for _ in range(m)] # It'll be used w/ multiplication method

A=(math.sqrt(5)-1)/2

# Collision(s) counters
collision_div = 0
collision_mul = 0

collision_div_array = [0]
collision_mul_array = [0]


class User:
    def __init__(self, key, surname):
        self.key = key
        self.surname = surname

    def __eq__(self, other):
    	return self.key == other.key

    def bio(self):
    	return str(self.key) , self.surname

class Hash:
	def __init__(self, m):
		self.m = m

	
	### HASH FUNCTIONS USED
	# Division Method
	def func_div(key):
		return key % m

	# Multiplication Method
	def func_mul(key):
	    #A = 0.8
	    m=len(T2)
	    return math.floor(m * ((key * A) % 1))

    
    ### METHODS IMPLEMENTED
	def insert(User):
		hash_key = Hash.func_div(User.key)
	
		if len(T1[hash_key]) > 0:
		    global collision_div
		    collision_div += 1

		collision_div_array.append(collision_div)
		T1[hash_key].insert(0, User)

		hash_key = Hash.func_mul(User.key)	
		if len(T2[hash_key]) > 0:
		    global collision_mul
		    collision_mul += 1

		collision_mul_array.append(collision_mul)
		T2[hash_key].insert(0,User)

		global n
		n += 1

		if n>=(m/100)*70 and n<(m/100)*70+1:
			plt.axvline(x=n, color = 'y', ls = "dashed", label = "α = 70%")

		if n==m:
			plt.axvline(x=m, color = 'g', ls = "dashed", label = "α = 100%")

		
	def searchT1(key):
		hash_key = Hash.func_div(key)

		for i in range(len(T1[hash_key])):
			if T1[hash_key][i].key == key:
				print('Found')
				return True
			else:
				print('Not Found')
		return False

	def searchT2(key):
		hash_key = Hash.func_mul(key)

		for i in range(len(T2[hash_key])):
			if T2[hash_key][i].key == key:
				print('Found')
				return True
			else:
				print('Not Found')
		return False

	def print_all():
		Hash.get_load_factor()
		print("T1 (Division Method) \t\t --> ", collision_div , "collisions")
		Hash.display_hash(T1)
		print("T2 (Multiplication Method) --> ", collision_mul , "collisions")
		Hash.display_hash(T2)

	def get_load_factor():
		print("Load Factor (α=n/m): " , n , "/" , m, "=" , (n/m)*100 , "%\n")

	def display_hash(T): 
		for i in range(len(T)):
			print("|",str(i).rjust(2, '0'),"|", end = "")  	

			for j in T[i]:
				print(" < ", j.surname , end = "")
			print()
		print()

	# Delete User from list T[h(k)[x]]
	def delete(User):
		hash_key = Hash.func_div(User.key)
		global n
		for i in range(len(T1[hash_key])):
			if T1[hash_key][i] == User:
				T1[hash_key].remove(User)
				n -= 1
				if len(T1[hash_key]) > 1:
					global collision_div
					collision_div -= 1
		hash_key = Hash.func_mul(User.key)

		for i in range(len(T2[hash_key])):
			if T2[hash_key][i] == User:
				T2[hash_key].remove(User)
				n -= 1
				if len(T2[hash_key]) > 1:
					global collision_mul
					collision_mul -= 1

		return False

######################################

""" TEST 1
chiave = m
for i in range(16):
	Hash.insert(User(chiave, string.ascii_uppercase[i]))
	chiave+=m

Hash.print_all()
"""


#TEST 2

tot_ele = m+20
key_universe = list(range(0,m*20)) # 0,1,2,...,m*10

random.shuffle(key_universe)
for i in range(tot_ele):
	Hash.insert(User(key_universe[i], "-"))
# end test 2


Hash.print_all()

#Hash.searchT1(...)
#Hash.delete(User(..., "..."))

# plt.plot(0, 0, 'go', label = "Fattore Caricamento α")
plt.plot(collision_div_array, label="Metodo Divisione")
plt.plot(collision_mul_array, label="Metodo Moltiplicazione - " + str( round(A, 3)) + "...")

plt.title("Confronto Funzioni Hash (chiavi casuali) - Primo caso")  #| α=" + str(round((n/m)*100,1)) + "%")

#plt.gca().xaxis.set_major_locator(mticker.MultipleLocator(1))  # uncomment ONLY if you got just few data
#plt.gca().yaxis.set_major_locator(mticker.MultipleLocator(1))  # uncomment ONLY if you got just few data

plt.xlabel("n (elementi in tabella)")
plt.ylabel("Collisioni")


plt.legend()

plt.savefig('line_plot.pdf')
plt.show()
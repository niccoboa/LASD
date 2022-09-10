import  random	
import math
#from inspect import signature

import string

import matplotlib.pyplot as plt # disegnare grafici
import matplotlib.ticker as mticker # intervalli sull'asse x personalizzabili
import matplotlib.patches as mpatches # elementi legenda personalizzabili

import numpy as np


m = 16	# dimensione tabella hash
n = 0 		# totale elementi salvati

# Dichiarazione delle tabelle
T1 = [[] for _ in range(m)] # Metodo divisione
T2 = [[] for _ in range(m)] # Metodo moltiplicazione

A=(math.sqrt(5)-1)/2 		# Valore di Knuth

# Contatori delle collisioni totali
collision_div = 0
collision_mul = 0

# Utile per il plot (contatore progressivo delle collisioni)
# indice "i" indica quante collisioni avvenute dopo aver inserito "i" elementi
# la prima cella ("i=0") è inevitabilmente posta a zero
collision_div_array = [0]
collision_mul_array = [0]


class User:
	# Costruttore
    def __init__(self, key, value):
        self.key = key
        self.value = value

    # Stabilisce quando due User sono considerabili uguali
    def __eq__(self, other):
    	return self.key == other.key

    # Breve descrizione di un User
    def bio(self):
    	return str(self.key) , self.value

class Hash:
	def __init__(self, m):
		self.m = m

	### FUNZIONI HASH UTILIZZATE
	
	# Metodo Divisione
	def func_div(key):
		return key % m

	# Metodo moltiplicazione
	def func_mul(key):
	    #A = 0.8
	    m=len(T2)
	    return math.floor(m * ((key * A) % 1))

    
    ### METODI IMPLEMENTATI

    # Inserimento utente in T1 e T2
	def insert(User):
		hash_key = Hash.func_div(User.key) # calcolo chiave con m. divisione
	
		if len(T1[hash_key]) > 0:	# chiave già presente nella cella
		    global collision_div 	# c'è collisione
		    collision_div += 1 		# aggiorna contatore totale collisioni
			
		
		collision_div_array.append(collision_div)	# aggiorna array colliioni progressivo
		T1[hash_key].insert(0, User) # inserisce in testa

		hash_key = Hash.func_mul(User.key) # calcolo chiave con m. moltiplicazione
		if len(T2[hash_key]) > 0: 	# chiave già presente nella cella
		    global collision_mul 	# c'è collisione
		    collision_mul += 1 		# aggiorna contatore totale collisioni

		collision_mul_array.append(collision_mul) # aggiorna array collisioni progressivo
		T2[hash_key].insert(0,User)	# inserisce in testa

		
		global n
		n += 1 		# aggiorna contatore elementi inseriti

		## preparazione stampa su matplotlib GUI
		if n>=(m/100)*70 and n<(m/100)*70+1: 		# linea 70%  load factor
			plt.axvline(x=n, color = 'y', ls = "dashed", label = "α = 70%")

		if n==m:									# linea 100% load factor
			plt.axvline(x=m, color = 'g', ls = "dashed", label = "α = 100%")

	# Ricerca utente in T1 --> TRUE se trovato ; FALSE se non trovato
	def searchT1(key):
		hash_key = Hash.func_div(key) # calcolo chiave con m. divisione

		for i in range(len(T1[hash_key])): # ricerca in profondita'
			if T1[hash_key][i].key == key: # elemento trovato
				print('Found')
				return True
			else:
				print('Not Found')
		return False

	# Ricerca utente in T2
	def searchT2(key):
		hash_key = Hash.func_mul(key) # calcolo chiave con m. moltiplicazione

		for i in range(len(T2[hash_key])): # ricerca in profondita'
			if T2[hash_key][i].key == key: # elemento trovato
				print('Found')
				return True
			else:
				print('Not Found')
		return False

	# Stampa tutto: tabelle + informazioni sulle collisioni
	def print_all():
		Hash.get_load_factor()
		print("T1 (Division Method) \t\t --> ", collision_div , "collisions")
		Hash.display_hash(T1)
		print("T2 (Multiplication Method) --> ", collision_mul , "collisions")
		Hash.display_hash(T2)

	# Stampa load factor alpha
	def get_load_factor():
		print("Load Factor (α=n/m): " , n , "/" , m, "=" , (n/m)*100 , "%\n")

	# Stampa tabelle (grafica su console)
	def display_hash(T): 
		for i in range(len(T)):
			print("|",str(i).rjust(2, '0'),"|", end = "")  	

			for j in T[i]:
				print(" < ", j.value , end = "")
			print()
		print()

	# Rimuove utente dalle tabelle T1 e T2 --> T[h(k)[x]]
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



#TEST 1
chiave = m
for i in range(17):
	Hash.insert(User(chiave, string.ascii_uppercase[i]))
	chiave+=m

Hash.print_all()

## intervallo unitario celle sugli assi x e y
plt.gca().xaxis.set_major_locator(mticker.MultipleLocator(1))  # scommenta solo se ci sono pochi dati
plt.gca().yaxis.set_major_locator(mticker.MultipleLocator(1))  # scommenta solo se ci sono pochi dati

"""
#TEST 2

tot_ele = m+20
key_universe = list(range(0,m*20)) # 0,1,2,...,m*10

random.shuffle(key_universe)
for i in range(tot_ele):
	Hash.insert(User(key_universe[i], "-"))
# end test 2
"""

Hash.print_all()

#Hash.searchT1(...)
#Hash.delete(User(..., "..."))

# plt.plot(0, 0, 'go', label = "Fattore Caricamento α")
plt.plot(collision_div_array, label="Metodo Divisione")
plt.plot(collision_mul_array, label="Metodo Moltiplicazione (A = Valore di Knuth ≃ " + str( round(A, 3)) + ")")

# plt.title("Confronto Funzioni Hash (chiavi casuali) - Primo caso")  #| α=" + str(round((n/m)*100,1)) + "%")



plt.xlabel("n (elementi in tabella)")
plt.ylabel("Collisioni")


plt.legend()

# salva plot su file
# plt.savefig('line_plot.pdf')

# mostra plot
plt.show()
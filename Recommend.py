import numpy as np
from collections import Counter
import math, matplotlib

open_history = open('history.txt','r')
open_queries = open('queries.txt','r')

history = open_history.read().split('\n')
queries = open_queries.read().split('\n')

data = history[0].split(' ')

No_Customers = int(data[0])
No_Items = int(data[1])
No_Transactions = int(data[2])

def create_table():
	global table
	table = []
	for i in range(No_Customers + 1):
		table.append([0]*(No_Items + 1))
	for object in history:
		purchased_item = int(object.split(' ')[1])
		user = int(object.split(' ')[0])
		table[purchased_item][user] = 1

	print("Positive entries: %s" %Counter(str(table))['1'])
	print('Average angle: %s' %angle_averages())

def angle_averages():
	angle_pairs = []
	for x in range(1, No_Items + 1):
		for y in range(1, No_Items + 1):
			if x != y:
				angle_pairs.append(find_angle(table[x],table[y]))
	return round(np.mean(angle_pairs), 2)

def find_angle(x, y):
	return round(math.degrees(math.acos(np.dot(x,y) / ((np.linalg.norm(y)) * (np.linalg.norm(x))))), 2)

def check_angle(item, basket):
	total_angles = []
	if item != ' ':
		for i in range(1, 6):
			if str(i) not in basket:
				total_angles.append([i,(find_angle(table[int(item)], table[i]))])
	return sorted(total_angles,key=lambda x: x[1])[0]

def order_matches(matches):
	ordered_matches = sorted(matches, key=lambda x: x[0])
	output = ''
	for item in ordered_matches:
		output += str(item[1]) + ' '
	return output

def main():
	create_table()
	for basket in queries:
		matched_items = []
		ordered_matches = []
		print("Shopping cart: %s" %basket)
		basket_items = basket.split(' ')
		for item in basket_items:
			match, angle = check_angle(item,list(basket))
			if angle > 90:
				continue
			elif match not in ordered_matches:
				matched_items.append([angle, match])
				ordered_matches.append(match)

			if angle != 90:
				print('Item: %s; match: %s; angle: %s' %(item, match, angle))
			else:
				print('Item: %s no match ' %item)
		print('Recommend: ' + order_matches(matched_items))

main()

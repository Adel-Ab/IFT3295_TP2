with open("matrix.txt", "r") as file:
	matrix=[]
	for line in file:
		row = line.strip().split()
		matrix.append(row)

for i in range(len(matrix)):
	for j in range(len(row)):
		if matrix[i][j] == 'x':
			pass
		elif int(matrix[i][j]) < 80:
			pass
		else:
			print( "("+str(i+1) + ", " + str(j+1) +"),")# + " " + str(matrix[i][j]))
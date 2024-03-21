file1 = open("testFile.txt", "r+")
 
print("Output of Read function is ")
test = file1.readline()
print(type(test))
print(test)
test = int(test) + 1
print(type(test))
print(test)
file1.close()

file1 = open("testFile.txt", "w")

file1.write(str(test))
file1.close() 
 
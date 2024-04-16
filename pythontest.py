import fileinput
import sys



path = "testFile.txt"
file = open(path, "r")

lines = file.readlines()

for line in lines:
    print(line.strip())

file.close()

with open(path, 'w') as fp:
    fp.write('\n'.join(["yay", "yey", "test"]))
    print('Done')

#for line in fileinput.input(file, inplace=1):
#    book_info = line.split(",")
#    if book_info[0] == title:
#        new_quantity = book_info[1] - quantity
#        new_line = title + "," + str(new_quantity)
#        line = new_line
#    sys.stdout.write(line)
#file.close() 
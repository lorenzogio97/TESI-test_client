string =""
for i in range(1000):
    string= string +"\""+str(i)+"\": { \n \"username\": \""+str(i)+"\", \n \"password\": \""+str(i)+"\", \n \"applications\": [\"echo\"]\n}, \n"

print(string)


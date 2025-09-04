text = "Hello world"

file = open('content.txt', 'w')
file.write(text)
print(text)
file.close()
try:
    with open("test.txt", 'r') as f:
        data = f.read()
        print(data)
except IOError as e:
    print(e)
except:
    print("Failed!")
finally:
    print("Finally")
print("Done")

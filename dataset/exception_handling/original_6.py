try:
    f = open("test.txt", 'r')
    try:
        data = f.read()
        print(data)
    except IOError as e:
        print(e)
    except:
        print("Unknown error")
    finally:
        f.close()
except:
    print("Failed!")
finally:
    print("Finally")
print("Done")

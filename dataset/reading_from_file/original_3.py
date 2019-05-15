file = open("file/to/write", 'w')
for account in accounts:
    file.writelines(account)
file.close()
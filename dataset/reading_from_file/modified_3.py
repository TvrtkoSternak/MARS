with open("file/to/write", 'w') as file:
    for account in accounts:
        file.writelines(account)
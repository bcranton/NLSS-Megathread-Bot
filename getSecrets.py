def read(file):
    f = open(file, "r")
    secret = f.read()
    f.close()
    return secret

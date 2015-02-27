def printMx(mx, size, fileName):
    file = open(fileName, 'w')
    for raw in range(0, size):
        for column in range(0, size+1):
            file.write('{0:f}\t\t'.format(mx[raw][column]))
        file.write('\n')
    file.close()

def allocateMx(rows, cols):
    Mx = []
    for i in range(rows):
        Mx.append([0.0] * cols)
    return Mx
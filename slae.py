import math

class SLAE:
    def __gaussFwd(self, M, sz, s, f):
        nRows = sz
        nCols = nRows + 1

        for keyRow in range(s, f + 1):
            for row in range(keyRow + 1, nRows):
                if math.fabs(M[row][keyRow]) > self.__epsilon:
                    k = -M[row][keyRow] / M[keyRow][keyRow]
                    for col in range(0, nCols):
                        if math.fabs(M[keyRow][col]) > self.__epsilon:
                            M[row][col] += M[keyRow][col] * k
        return

    def __gaussBwd(self, M, sz, s, f):
        nRows = sz
        nCols = nRows + 1

        for keyRow in range(s, f-1, -1):
            k = 0.0
            for col in range(keyRow+1, nCols-1):
                k += M[keyRow][col] * M[col][nCols-1]
            M[keyRow][nCols-1] -= k
            M[keyRow][nCols-1] /= M[keyRow][keyRow]
        return

    def solve(self, eps=10.0E-8):
        self.__epsilon = eps
        self.__gaussFwd(self.__mx, self.size(), 0, self.size() - 1)
        self.__gaussBwd(self.__mx, self.size(), self.size() - 1, 0)

    def size(self):
        return self.__sz

    def copySoln(self, S):
        if S is not None:
            for i in range(0, self.size()):
                S[i] = self.__mx[i][self.size()]

    def insertMatrix(self, M, s):
        self.__sz = s
        self.__mx = M

    def insertFree(self, B):
        if B is not None:
            for i in range(0, self.size()):
                self.__mx[i][self.size()] = B[i]



class SLAE:
    def __gaussFwd(self, M, sz, s, f):
        nRows = sz
        nCols = sz + 1

        for keyRow in range(s, f + 1):
            for row in range(keyRow + 1)
    def __gaussBwd(self, M, sz, s, f):
        pass

    def solve(self, epsilon=10.0E-8):
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
        if B is not None
            for i in range(0, self.size()):
                self.__mx[i][self.size()] = B[i]



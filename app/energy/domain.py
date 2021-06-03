class EnergyPoint:
    def __init__(self, no, time, V1, V2, V3, I1, I2, I3, P1, P2, P3, Q1, Q2, Q3, S1, S2, S3, PF1, PF2, PF3, F):
        self.__no = no
        self.__time = time
        self.__V1 = V1
        self.__V2 = V2
        self.__V3 = V3
        self.__I1 = I1
        self.__I2 = I2
        self.__I3 = I3
        self.__P1 = P1
        self.__P2 = P2
        self.__P3 = P3
        self.__Q1 = Q1
        self.__Q2 = Q2
        self.__Q3 = Q3
        self.__S1 = S1
        self.__S2 = S2
        self.__S3 = S3
        self.__PF1 = PF1
        self.__PF2 = PF2
        self.__PF3 = PF3
        self.__F = F
        pass

    def getNo(self):
        return self.__no

    def getTime(self):
        return self.__time

    def getV1(self):
        return self.__V1

    def getV2(self):
        return self.__V2

    def getV3(self):
        return self.__V3

    def getI1(self):
        return self.__I1

    def getI2(self):
        return self.__I2

    def getI3(self):
        return self.__I3

    def getP1(self):
        return self.__P1

    def getP2(self):
        return self.__P2

    def getP3(self):
        return self.__P3

    def getQ1(self):
        return self.__Q1

    def getQ2(self):
        return self.__Q2

    def getQ3(self):
        return self.__Q3

    def getS1(self):
        return self.__S1

    def getS2(self):
        return self.__S2

    def getS3(self):
        return self.__S3

    def getPF1(self):
        return self.__PF1

    def getPF2(self):
        return self.__PF2

    def getPF3(self):
        return self.__PF3

    def getF(self):
        return self.__F
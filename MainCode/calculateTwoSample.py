from calculateMetrics import *

class DirectionalRelativeFreq(BasePara):
    #compare two metrices need normalization
    def __init__(self,path,control_path,resolution,chromosome,out_name="DRF",
                start_distance=0, end_distance=2000000):
        super().__init__(path,resolution,chromosome,out_name)
        self.matrix = loadWithNorm(self.path,log = True).values
        self.control_path = control_path
        self.control_matrix = loadWithNorm(self.control_path,log = True).values
        self.start_distance = start_distance
        self.end_distance = end_distance

    def __str__(self):
        return "DirectionalRelativeFreq(matrix_path = '" + str(self.path) +"',\n" + \
                "control_path = '" + str(self.control_path) + "',\n" + \
                "resolution = " + str(self.resolution) + ", chromosome = '" + \
                self.chromosome + "', " + "out_name = '" + self.out_name + \
                "' \n, start_distance = " + str(self.start_distance) + \
                ", end_distance = " + str(self.end_distance) + ")"
    __repr__ = __str__

    def getDRF(self):
        if self.matrix.shape[0] != self.control_matrix.shape[0]:
            print("Error: Input/control matrix have different shape")
            exit(1)

        smooth = 3
        control = ndimage.median_filter(self.control_matrix,smooth)
        logratio = ndimage.median_filter(self.matrix - control, smooth)

        array = np.zeros(self.matrix_shape)
        startDistanceBin = int(self.start_distance / self.resolution)+1
        endDistanceBin = int(self.end_distance / self.resolution)

        for i in range(endDistanceBin, self.matrix_shape - endDistanceBin):
            right = logratio[i+startDistanceBin:i+endDistanceBin+1, i].mean()
            left = logratio[i, i-endDistanceBin:i-startDistanceBin+1].mean()
            if np.isnan(right - left):continue
            array[i] = right - left


        return super().makeDF(array,"DirectionalRelativeFreq")

    def getCSV(self):
        super().makeCSV(self.getDRF())

class InsulationScoreChange(BasePara):
    def __init__(self,path,control_path,resolution,chromosome,out_name="InsulationScore",square_size=150000):
        super().__init__(path,resolution,chromosome,out_name)
        self.control_path = control_path
        self.square_size = square_size
        self.IStreat = InsulationScore(path,resolution,chromosome,out_name="InsulationScore",
                                        square_size=self.square_size).getIS()
        self.IScontrol = InsulationScore(control_path,resolution,chromosome,out_name="InsulationScore",
                                        square_size=self.square_size).getIS()

    def getISC(self):
        isc = np.array(self.IStreat.InsulationScore - self.IScontrol.InsulationScore)
        return super().makeDF(isc,"InsulationScoreChange")

    def getCSV(self):
        super().makeCSV(self.getISC())

class deltaDLR(BasePara):
    def __init__(self,path,control_path,resolution,chromosome,out_name="DLR",sizeDLR=3000000):
        super().__init__(path,resolution,chromosome,out_name)
        self.control_path = control_path
        self.sizeDLR = sizeDLR
        self.DLRtreat = DistalToLocalRatio(path,resolution,chromosome,out_name="DLR",
                                            sizeDLR=self.sizeDLR).getDLR()
        self.DLRcontrol= DistalToLocalRatio(control_path,resolution,chromosome,out_name="DLR",
                                            sizeDLR=self.sizeDLR).getDLR()

    def getDeltaDLR(self):
        dDLR = np.array(self.DLRtreat.DistalToLocalRatio - self.DLRcontrol.DistalToLocalRatio)
        return super().makeDF(dDLR,"deltaDLR")

    def getCSV(self):
        super().makeCSV(self.getDeltaDLR())
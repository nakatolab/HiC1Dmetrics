from multiprocessing import Pool
from callDirectionalTAD import *
#from multiprocessing.pool import ThreadPool as Pool #多线程

# calculate each dTAD of chromosome separately
class paralfunc(object):
    def __init__(self,myfun,num_processer):
        self.myfun = myfun
        self.num_processer = num_processer

        chrlist= list(range(1,23)); chrlist.append("X")
        chrolist = ["chr"+str(a) for a in chrlist]
        self.chrolist = chrolist

    def run(self,pathName,pathControl,resolution):
        resultlist=[]
        p = Pool(self.num_processer)
        for r in self.chrolist:
            result = p.apply_async(self.myfun, args=(r,pathName,pathControl,resolution,))
            resultlist.append(result)
        p.close()
        p.join()

        output_left = pd.DataFrame()
        output_right = pd.DataFrame()
        for i in resultlist:
            output_single = i.get().copy()
            output_left = output_left.append(output_single["leftTAD"])
            output_right = output_right.append(output_single["rightTAD"])
        return(output_left,output_right)

def call_dTAD(chrom,pathName,pathControl,resolution):
    filename = pathName+"/observed.KR."+chrom+".matrix.gz"
    controlfilename = pathControl + "/observed.KR."+chrom+".matrix.gz"

    dTAD = DirectionalTAD(filename,controlfilename, \
                      resolution,chr=chrom,startDRF=500000,sizeDRF=1000000,\
                      sizeIS=150000)
    leftTAD,rightTAD,_ = dTAD.extractRegion()
    return({"leftTAD":leftTAD,"rightTAD":rightTAD})

def alldTAD(pathName,pathControl,resolution,outname="twoSample"):
    ltad,rtad = paralfunc(call_dTAD,30).run(pathName,pathControl,resolution)
    ltad.to_csv(outname+"_leftTAD.csv",sep="\t",index=False)
    rtad.to_csv(outname+"_rightTAD.csv",sep="\t",index=False)

#alldTAD("/Users/wangjiankang/figureServer/Nov2020/Rad21KD1_HiCmatrix",
#        "/Users/wangjiankang/figureServer/Nov2020/Control1_HiCmatrix",50000)

#=====================================#
#simply call all TAD

class paralfuncOneSample(object):
    def __init__(self,myfun,num_processer):
        self.myfun = myfun
        self.num_processer = num_processer

        chrlist= list(range(1,23)); chrlist.append("X")
        chrolist = ["chr"+str(a) for a in chrlist]
        self.chrolist = chrolist

    def run(self,pathName,resolution):
        resultlist=[]
        p = Pool(self.num_processer)
        for r in self.chrolist:
            result = p.apply_async(self.myfun, args=(r,pathName,resolution,))
            resultlist.append(result)
        p.close()
        p.join()

        output_all = pd.DataFrame()
        for i in resultlist:
            output_single = i.get().copy()
            output_all = output_all.append(output_single)
        return(output_all)

def TAD1sample(chrom,pathName,resolution):
    filename = pathName+"/observed.KR."+chrom+".matrix.gz"
    tad = TADcallIS(filename,resolution,chrom,squareSize=150000)
    return(tad)

def runTAD1sample(pathName,resolution,outname="oneSample"):
    tad = paralfuncOneSample(TAD1sample,30).run(pathName,resolution)
    tad.to_csv(outname+"_TAD.csv",sep="\t",index=False)

#runTAD1sample("/Users/wangjiankang/figureServer/Nov2020/Rad21KD1_HiCmatrix",50000)
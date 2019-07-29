def cut(Value, CutPoints = [1,2,3], FloatPoints = False):
# Version: 1.0 (15/7/2019) 
# Converts a continuous variable into an categorical one 
# Example: PandasSeries.apply(cut, CutPoints = [18.5,25,30,35,40], FloatPoints = 1)
    if FloatPoints == False: 
        if Value < CutPoints[0]:
            return "<%s" %CutPoints[0]
        for x in range(1,len(CutPoints)):
            if Value <= CutPoints[x]:
                return ">{} & <={}".format(CutPoints[x-1],CutPoints[x])
        if Value > CutPoints[-1]:
            return ">%s" %CutPoints[x]
    else: 
        Value = round(Value, FloatPoints)
        if Value < CutPoints[0]:
            return "<%s" %CutPoints[0]
        for x in range(1,len(CutPoints)):
            if Value < CutPoints[x]:
                return "{} - {}".format(CutPoints[x-1],CutPoints[x]-10**-FloatPoints)
        if Value >= CutPoints[-1]:
              return ">%s" %CutPoints[x]

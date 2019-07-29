def cut(Value, CutPoints = [1,2,3], FloatPoints = False):
# Version: 1.0 (15/7/2019) 
# Aim: convert a continuous variable into an categorical one 
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

def BMI_Calculator (DataFrame, Height = "Height", Weight =  'Weight', Unit = 'cm', Continuous=True):
# Version: 1.0 (15/7/2019) 
# Aim: calculate the body mass index 
    if Continuous == True:
        if Unit == 'cm':
            return (DataFrame[Weight] / DataFrame[Height]**2 * 10000)
        elif Unit == 'm':
            return (DataFrame[Weight] / DataFrame[Height]**2)
    else: 
        if Unit == 'cm':
            ContinuousBMI  = DataFrame[Weight] / DataFrame[Height]**2 * 10000
            return (ContinuousBMI.apply(cut, CutPoints = [18.5,25,30,35,40], FloatPoints = 1))
        elif Unit == 'm':
            ContinuousBMI = DataFrame[Weight] / DataFrame[Height]**2
            return (ContinuousBMI.apply(cut, CutPoints = [18.5,25,30,35,40], FloatPoints = 1))
        
def IBW_Calculator (DataFrame, Height = "Height", Sex =  'Sex', Unit = 'cm'):
# Version: 1.0 (15/7/2019) 
# Aim: calculate the ideal body weight
# Method:
## Ideal body weight (IBW) (men) = 50 kg + 2.3 kg x (height, in - 60)
## Ideal body weight (IBW) (women) = 45.5 kg + 2.3 kg x  (height, in - 60)
    if Unit == 'cm':
        Height = DataFrame[Height] * 0.393701
    elif Unit == 'm': 
        Height = DataFrame[Height] * 39.3701
    elif Unit == 'in':
        Height = DataFrame[Height]  
    
    Sex = DataFrame[Sex] == "Male"
    return (45.5 + 4.5 * Sex +  (2.3 * (Height - 60) ))

df['Ideal_Weight'] = IBW_Calculator(df) 
def ABW_Calculator (DataFrame, IBW = "Ideal_Weight", Weight =  'Weight'):
# Version: 1.0 (15/7/2019) 
# Aim: calculate the adjusted body weight
# Method: ABW = IBW + 0.4 x (actual body weight - IBW)
    IBW = DataFrame[IBW] 
    Weight = DataFrame[Weight] 
    return (IBW + 0.4 * (Weight - IBW))

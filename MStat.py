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
# Example: df['Ideal_Weight'] = IBW_Calculator(df) 
    if Unit == 'cm':
        Height = DataFrame[Height] * 0.393701
    elif Unit == 'm': 
        Height = DataFrame[Height] * 39.3701
    elif Unit == 'in':
        Height = DataFrame[Height]  
    
    Sex = DataFrame[Sex] == "Male"
    return (45.5 + 4.5 * Sex +  (2.3 * (Height - 60) ))

def ABW_Calculator (DataFrame, IBW = "Ideal_Weight", Weight =  'Weight'):
# Version: 1.0 (15/7/2019) 
# Aim: calculate the adjusted body weight
# Method: ABW = IBW + 0.4 x (actual body weight - IBW)
    IBW = DataFrame[IBW] 
    Weight = DataFrame[Weight] 
    return (IBW + 0.4 * (Weight - IBW))

def Corrected_Weight_Calculator (DataFrame, Weight =  'Weight', IBW = "Ideal_Weight", ABW = 'Adjusted_Weight', BMI = 'BMI' ):
# Version: 1.0 (31/7/2019) 
# Aim: return actual weight for underweight patients, ideal weight for normal-weight patients 
## and adjusted weight for overweight patients 
    Weight = DataFrame[Weight] 
    IBW = DataFrame[IBW] 
    BMI = DataFrame[BMI]
    Corrected_Weight = DataFrame[ABW].copy()
    for x in range(len(Corrected_Weight)):
        if BMI.iloc[x] == '<18.5':
            Corrected_Weight.iloc[x] = Weight.iloc[x]
        elif BMI.iloc[x] == '18.5 - 24.9':
            Corrected_Weight.iloc[x] = IBW.iloc[x]  
    return (Corrected_Weight)

def GFR_Calculator (DataFrame, Creatinine='Creatinine', Sex =  'Sex', Age='Age', Weight = 'Weight', Equation='MDRD'): 
# Version: 2.0 (31/7/2019) 
# Assumption: No Black Patients 
# Method: 
## GFR by the MDRD Equation = 186 × Serum Cr^-1.154 * age^-0.203 × 1.212 (if patient is black) × 0.742 (if female)
## CrCl by the Cockcroft-Gault Equation == (140 – age) × (weight, kg) × (0.85 if female) / (72 × Cr)
## GFR by CKD-EPI Equation = A × (Scr/B)^C × 0.993^age × (1.159 if black) where A, B, and C change (See bellow)
    IsFemale = DataFrame[Sex] == "Female"
    Sex = DataFrame[Sex]
    Creatinine = DataFrame[Creatinine]
    Age = DataFrame[Age]
    Weight = DataFrame[Weight]
    if Equation == 'MDRD': 
        return (186 * (Creatinine**-1.154) * (Age**-0.203) * (0.742*IsFemale) + 
               186 * (Creatinine**-1.154) * (Age**-0.203) * (~IsFemale))
    elif Equation == 'Cockcroft-Gault':
        return ((140 - Age) * (Weight) * (0.85 * IsFemale) / (72 * Creatinine) + 
               (140 - Age) * (Weight) * (1 * ~IsFemale) / (72 * Creatinine))
    elif Equation == 'CKD-EPI':
        DataFrame['CKD-EPI Equation'] = np.NaN 
        CKD = DataFrame['CKD-EPI Equation']
        for x in range(len(CKD)):
            if Sex.iloc[x] == 'Male':
                A = 141
                B = 0.9
                if Creatinine.iloc[x] <= 0.9:
                    C = -0.411
                else: 
                    C = -1.209
                CKD.iloc[x] = A * ((Creatinine.iloc[x]/B)** C) * (0.993 ** Age.iloc[x])
            elif Sex.iloc[x] == 'Female':
                A = 144
                B = 0.7
                if Creatinine.iloc[x] <= 0.9:
                    C = -0.329
                else: 
                    C = -1.209
                CKD.iloc[x] = A * ((Creatinine.iloc[x]/B)** C) * (0.993 ** Age.iloc[x])
        return (CKD)

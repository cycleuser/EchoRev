gender_type = 'boy'
person_name = 'Mecury'
person_age = 3
person_hight = 1
person_weight = 16
def BMI(weight = 16, hight = 1.0):
    bmi = float(weight) /(float(hight)**2)
    return(bmi)
print(BMI(90,1.8))


print(BMI(person_weight,person_hight))
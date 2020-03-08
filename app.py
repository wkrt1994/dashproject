
import pandas as pd
import numpy as np
import random
import sys 

#Parámetros del modelo y lectura excel. 
n=10000                                                                         #Simulaciones
m=1                                                                             #Tipo de método
datos='IMP.xlsx'                                                                #DASH

#LECTURA PARA IMP Y FREC
#Lectura hoja de Impacto 
Imp=pd.read_excel(datos, sheet_name='Imp')
Imp[['L Inferior', 'L Superior']] = Imp[['L Inferior', 'L Superior']].astype(int)
Imp=Imp.fillna(value=0)
Imp=Imp[Imp['Probabilidad'] != 0]

#Lectura información de frecuencia
Frec=pd.read_excel(datos, sheet_name='Frec')


#VALIDACIONES IMPACTO
#Validación que los datos son número
#Que el LS y LI del impacto coincidan. 
for i in range (1, Imp.shape[0]):
    riact=Imp.iloc[i,1]
    rsant=Imp.iloc[i-1,2]
    if riact != rsant:
        sys.exit("En el impacto, el límite superior no coincide con Limite inferior siguiente")

#Probabilidad Impacto sume 100%
prob= Imp['Probabilidad'].sum()
if prob != 1: 
    sys.exit("Las probabilidades de impacto no suman el 100%") 

#Probabilidades del Impacto entre 0 y 1
for i in range (0, Imp.shape[0]):
    prob2Imp = Imp['Probabilidad'][i]
    if float(prob2Imp) > 1 : 
        sys.exit("La probabilidad debe ser un número entre 0 y 1")
    elif float(prob2Imp) < 0 :
        sys.exit("La probabilidad debe ser un número entre 0 y 1")



#LECTURA Y VALIDACIONES PARA FRECUENCIA
#PARA MÉTODO 1:
if m ==1:
    #Lectura datos frecuencia met1
    met1=Frec.iloc[0:10,0:4]
    met1=met1.fillna(value=0)
    met1[['L Inferior','L Superior']]=met1[['L Inferior','L Superior']].astype(int)
    met1=met1[met1['Probabilidad'] != 0]
    
    #Validación que los datos son número
#    for i in range(0,9):
#        for j in range(0,3):
#            if (type(Imp.iloc[i,j]) != 'numpy.float64' and type(Imp.iloc[i,j]) != 'numpy.int32' and type(Imp.iloc[i,j]) != 'numpy.int64'):
#                sys.exit("En la frecuencia, existen caracteres no numéricos")
                
    #Validacion Ls(actual) = Li(anterior) +1 coincidan
    for i in range (1, met1.shape[0]):
        riact=met1.iloc[i,1]
        rsant=met1.iloc[i-1,2]+1
        if riact != rsant:
            sys.exit("En la frecuencia, el límite superior no coincide con Limite inferior") 

    #Suma de prob sea 1
    probM1=(met1['Probabilidad'].astype(float)).sum()
    if probM1 !=1:
        sys.exit("En la frecuencia, las probabilidades de frecuencia no suman el 100%") 

    #Probabilidades de la Fq entre 0 y 1
    for i in range (0, met1.shape[0]):
        prob2Fq = met1['Probabilidad'][i]
        if float(prob2Fq) > 1 : 
            sys.exit("En la frecuencia, la probabilidad debe ser un número entre 0 y 1")             #DASH
        elif float(prob2Fq) < 0 :
            sys.exit("En la frecuencia, la probabilidad debe ser un número entre 0 y 1")
        
#PARA MÉTODO 2:
if m==2:
    #Lectura datos frecuencia met2
    met2=Frec.iloc[0:1,5:7]
    met2=met2.astype(int)
    #validar que se ingresa un número
#    for i in range(0,1):
#        if type(met2.iloc[0,i]) == 'numpy.int32' and type(met2.iloc[0,i]) == 'numpy.int32':
#            sys.exit("Debe ingresar un caracter numérico")

#PARA MÉTODO 3:
if m==3:
    #Lectura datos frecuencia met3
    met3=Frec.iloc[0:1,8:10]
    met3.columns=['Poblacion','Prob de un evento']
    met3['Poblacion']=met3['Poblacion'].astype(int)
    #Validar que se ingresa un número 
#    for i in range(0,1):
#        if type(met3.iloc[0,i])== 'numpy.int32' or type(met3.iloc[0,i]) == 'numpy.float64':
#            sys.exit("Debe ingresar un caracter numérico")

    #Probabilidad del evento entre 0 y 1
    if met3.iloc[0,1] > 1:
        sys.exit("La probabilidad de un evento debe ser un número entre 0 y 1")
    elif met3.iloc[0,1] < 0: 
        sys.exit("La probabilidad de un evento debe ser un número entre 0 y 1")


#SIMULACIÓN DE IMPACTO, FRECUENCIA Y AGREGACIÓN ALEATORIA
#Definición de vectores donde se alojarán los resultados
rIn = np.zeros(n, dtype=np.int64)
ma95=np.zeros(30, dtype=np.int64)       #P95 Matriz agregada
ma50=np.zeros(30, dtype=np.int64)       #P50 Matriz agregada
ma99=np.zeros(30, dtype=np.int64)       #P99 Matriz agregada
mamedia=np.zeros(30, dtype=np.int64)    #Media Matriz agregada
fq95 = np.zeros(30, dtype=np.int64)       #P95 Vector Frecuencia
fq50 = np.zeros(30, dtype=np.int64)       #P50 Vector Frecuencia
fq99 = np.zeros(30, dtype=np.int64)       #P99 Vector Frecuencia
fqmedia = np.zeros(30, dtype=np.int64)    #Media Vector Frecuencia

              

for k in range (0,30):
    
    #Simulación vector impacto
    vectorIm=[]
    for i in range (0, len(Imp)):
        n2=(n*Imp.iloc[i,3]).round(0).astype(int)
        aux = np.random.uniform(low=Imp.iloc[i,1], high=Imp.iloc[i,2], size=(n2))
        vectorIm=np.append(vectorIm,aux)
    vectorIm=vectorIm.astype(int)
    vectorIm=list(vectorIm)

    #Simulación vector frecuencia
    VectorFq=[]
    
    #Método1
    if m==1:
        for i in range(0,len(met1)):
            nf=np.float32(n*met1.iloc[i,3]).round(0).astype(int)
            auxf=np.random.uniform(low=met1.iloc[i,1], high=met1.iloc[i,2], size=nf).round(0).astype(int)
  
            VectorFq=np.append(VectorFq,auxf)
        VectorFq=VectorFq.astype(int)
    
    #Método2
    if m==2:
        lamb = met2.iloc[0,0]/met2.iloc[0,1]
        VectorFq= np.random.poisson(lam= lamb, size=n)

    #Método3
    if m==3:
        pob=met3.iloc[0,0]
        prob=met3.iloc[0,1]
        VectorFq= np.random.binomial(pob, prob, n) 
    
     
    #Agregación aleatoria
    for i in range(0, len(VectorFq)):
        rIn[i]=sum(random.sample(vectorIm,VectorFq[i]))
    
    #Resultados matriz agregada de pérdidas
    ma95[k]=np.quantile(rIn,0.95)
    ma50[k]=np.quantile(rIn,0.5)
    ma99[k]=np.quantile(rIn, 0.99)
    mamedia[k]=rIn.mean()
    
    #Resultados vector Frecuencia
    fq50[k]=np.quantile(VectorFq,0.5)
    fq95[k]=np.quantile(VectorFq,0.95)
    fq99[k]=np.quantile(VectorFq, 0.99)
    fqmedia[k] = VectorFq.mean()

# Resultados
expo50=ma50.mean()
expo95=ma95.mean()
expo99=ma99.mean()
expome=mamedia.mean()

freq50=fq50.mean().round(0)
freq95=fq95.mean().round(0)
freq99=fq99.mean().round(0)
frecmedia= fqmedia.mean().round(0)

impactoP95 = expo95/freq95
impactoP95 = impactoP95.astype(int)


# Para exportar resultados a excel. 
rIn=pd.DataFrame(rIn)
rIn

# Importar matriz conjunta
ruta = "D:\wrivera\Documents\MatrizConjunta.csv"
archivo=rIn.to_csv(ruta)

#dataFrame con resultados finales 
Resultados=pd.DataFrame({'Media Matriz Conjunta':[mediarIn],'P95 Matriz Conjunta':[expo95],'Expo50':[expo50],
                         'Expo99':[expo99],'Media Frec':[mediaFq],'Freq50':[freq50],'Freq95':[freq95],'Freq99':[freq99],
                         'Impacto':[Impacto]})
Resultados[['Media Matriz Conjunta', 'P95 Matriz Conjunta','Expo50','Expo99','Media Frec','Freq50','Freq95','Freq99',
           'Impacto']] = Resultados[['Media Matriz Conjunta', 'P95 Matriz Conjunta','Expo50','Expo99','Media Frec','Freq50','Freq95','Freq99',
           'Impacto']]
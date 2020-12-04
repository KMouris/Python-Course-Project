import numpy as np
import pandas as pd
import os
import glob
import sys
import time
start_time = time.time()

#----Check Function 1: Checks if folder path exists-----#
def CheckPath(path):
    if os.path.exists(path) == True:
        pass
    else:
        sys.exit("ERROR: The file directory doesn't exist")

#----Check Function 2: Checks if there are an equal number of precipitation and temperature rasters
def CheckNumberFiles(filenames_precip, filenames_temp):
     if len(filenames_precip) == len(filenames_temp):
         pass
     else:
         if len(filenames_precip) > len(filenames_temp):
            sys.exit("ERROR: There are more precipitation raster files than temperature raster files. Check user input!")
         else:
             sys.exit("ERROR: There are more temperature raster files than precipitation raster files. Check user input!")

#----Function 1: Get Storm Date#
###Funciton recieves file name (which is the storm date) and saves each value [year, month, day, hour, minute, second] in an array
def GetDate(name):
    date=np.zeros(6) #Initialize an array with 6 values, will be a float array
    date[0]=float(name[0:4]) #year
    date[1]=float(name[4:6]) #month
    date[2]=float(name[6:8]) #day
    date[3]=float(name[10:12]) #hour
    date[4]=00        #minute (not in name)
    date[5]=00        #second (not in name)
    # print(date)
    return date

#----Function 2: Value Matrix ----#
###Funtion Receives matrix from original .txt file and saves the values >-9999 (cells with data) in a new 2D matrix
###Additionally, it saves the original row and column position of each value, for later use and to identify the cell (station)
def ValueMatrix(storm_array):
    s=np.array(storm_array.shape)  #-get number of rows and columns, s[0]=rows, s[1]=columns
    nz=storm_array[storm_array> -9999].size  #-total number of cells with non zero or zero values (different that -9999). This is the size of new matrix
    value=np.zeros((int(nz),3)) #-Initialize a new matrix to save the original row, column and value for each cell
    n=0 #-counter to fill each row in the new matrix "value", changes value in every "if"
    for i in range(0,s[0]):  #-go through every row
        for j in range(0,s[1]):  #-goes through every column in original matrix
            if storm_array[i,j]>-9999:  #-if value in cell is a value cell (different to -9999)
                value[n,0]=i       #-save in first column the original row value, represented by "i"
                value[n,1]=j       #-save in second column the original column value, represented by "j"
                value[n,2]=storm_array[i,j]  #-save value in
                # print("Saved value: ",storm_array[i,j] )
                n+=1 #-increase the counter to fill a new row in each iteration, only when value fits the criteria in the IF
    return value

#----Function 3: Fill 3D array with preciptiation values----#
###Function Recieves date, precipitation value matrix, 3D matrix and iteration number as inputs to fill array of arrays (3D matrix)
def ThreeDArray_Precipitation(date, value, tdm, n): #date array, value array, 3D array, iteration number=row to fill
    nz=int(value.size/3) #Number of rows in Value Matrix. ###Must change if matrix has more than 3 values!!!####, #Number of 2D arrays in 3D array
    for k in range(0,nz): #-To fill each array one at a time
        tdm[k,n,0:6]=date #fill columns 1 to 5, from row n (number of file) and array "k" with the date
        tdm[k,n,6]=value[k,2] #fill column 6 with rain value (in mm)
        tdm[k, n, 7] = 9999 #fills the temperature column with 9999 values for now. If a temperature raster is inputed, this value will be replaced later
        tdm[k,n,8]=value[k,0] #fill column 7 with original row value, in original raster
        tdm[k, n, 9] = value[k, 1]  # fill column 7 with original row value, in original raster
    return tdm

#----Function 4: Fills 3D array with temperature values----#
###Function fills the 3D matrix with the temperature values. First, it must match the dates and the cell location for each file
def ThreeDArray_Temperature(date_t, value, tdm,n):
    nz = int(value.size / 3)  # Number of rows in Value Matrix. ###Must change if matrix has more than 3 values!!!####, #Number of 2D arrays in 3D array
    for k in range(0,nz):
        p_date = tdm[k,n,0:6] #gets the date for the nth precipitation value in each array
        p_location = tdm[k,n,8:10] #gets the row and column number of original precipitation value
        # print("Precipitation date: ", p_date, "\n Temperature date: ", date_t)
        # print("Are the dates the same? ", np.array_equal(p_date, date_t))
        # print("Are the locations the same? ", np.array_equal(p_location, value[k,0:2] ))
        if np.array_equal(p_date, date_t) == True and np.array_equal(p_location, value[k,0:2] ) == True: #if the cell location AND date coincide
            tdm[k,n,7] = value[k,2]
        else:
            if np.array_equal(p_date, date_t)== False: #if the dates are different, there is an error
                sys.exit("ERROR: The temperature file dates do not coincide with the Precipitation raster dates. Please check user input")
            else:
                sys.exit("ERROR: Check the precipitation and/or temperature files for any errors.")
    return tdm

#----MAIN Function 1: Precipitation data files----#
###Function recieves the data from the original precipitation files (storm array) and gets the date (from name) - File name must be in the format YYYYMMDD_HH
###Also receives the 3D matrix (tdm) where the data from the storm_array is saved in the needed format. "i" correpsonds to the
### file iteration number, which corresponds to the row in each array in the 3D array being filled
def Precipitation(name, storm_array, tdm, i): #recieves name of file (to get date), the storm array from the .txt file, the 3D matrix, the file iteration number
    date = GetDate(name)  # send file name to function to get the date and time of the file values
    value = ValueMatrix(storm_array)  # Send original matrix to function, to get new matrix with only value cells, with original row, column and value
    # print("Value matrix: \n",new)
    tdm = ThreeDArray_Precipitation(date, value, tdm, i)  # Get 3D arrays, every array is a different cell, or station. Each row is a certian date (file)
    return tdm

#----MAIN Function 2: Temperature data files----#
###Function recieves the file  (name) and data matrix from original temperature matrix (temp_array), if the user defines one.
###There should be the same number of files (dates) and the same number of cells (stations) as in the precipitation rasters
###It also receives the previously filled 3D matrix with precipitation values (tdm), and the iteration number
def Temperature(name, temp_array, tdm, i):
    date_t=GetDate(name)
    value = ValueMatrix(temp_array)
    # print("Temperature value matrix: \n", value)
    tdm= ThreeDArray_Temperature(date_t, value, tdm, i)
    return tdm

#----Main Function 3: Saves Data in .csv files----#
###Function saves each array in a different file to check your work and for later use in EI30 program----#
def SaveFiles(tdm, path): #Receives: 3D matrix
    nz=int(tdm.shape[0]) #number of cells or "stations" (number of arrays in 3D array)
    for k in range(0,nz): #For each "station" or cell
        name=path+"\\"+str(tdm[k,0,8])+"_"+str(tdm[k,0,9])+".csv" #File name, to save each array with different name
        m= tdm[k,:,:] #Save current array "k" as a single 2D matrix
        m=np.reshape(m,(int(tdm.shape[1]),int(tdm.shape[2]))) #reshape m as 2D matrix, since we already removed all other arrays that made it a 3D array
        df_station = pd.DataFrame(data=m, columns=["Year", "Month", "Day", "Hour", "Minute", "Second", "Precipitation (mm)", "Temperature", "Original Row", "Original Column"])
        print("Saving file: ", name)
        df_station.to_csv(name, sep=',', index=False)

###--------MAIN CODE-------###

##----USER INPUT----##:

#Folder Path where the precipitation files to open are
path_precip=r'P:\aktiv\2018_DLR_DIRT-X\300 Modelling\310 Models\01_Erosion_model\08_Snow\Test_Spring_2018\01_18\Prec'  #Precipitation data
path_temp=r'P:\aktiv\2018_DLR_DIRT-X\300 Modelling\310 Models\01_Erosion_model\08_Snow\Test_Spring_2018\01_18\Temp'  #Temperature data
savepath= r'P:\aktiv\2018_DLR_DIRT-X\300 Modelling\310 Models\01_Erosion_model\08_Snow\Test_Spring_2018\01_18\CSVperCell'  #Folder to save results (.CSV files for with all time data, per cell (station)

#User determines if they will input temperature files, if True, then also input a folder path where the temperature raster files are (in .txt format)
temp=True

##----CODE----##

#Check for input mistakes and get list of file names for Temperature and Precipitation:
CheckPath(path_precip)
filenames_precip=sorted(glob.glob(path_precip + "\*.txt")) #Get all txt files in the path directory, and save them in a list
if temp == True:
    CheckPath(path_temp)
    filenames_temp = sorted(glob.glob(path_temp + "\*.txt"))  # Get all txt temperature files in the path directory, and save them in a list
    CheckNumberFiles(filenames_precip,
                     filenames_temp)  # Check if there are same number of precipitation and temperature files

#INITIATE 3D MATRIX WHERE ALL THE FILES WILL BE SAVED
na=2897 #number of arrays, which are the number of value cells in each raster (MUST BE MODIFIED IF RASTER SIZE CHANGES)
nr=int(len(filenames_precip)) #number of rows equals number of files in folder
# print("Number of files: ", nr)
nc=10 #There are 10 columns in each row: year, month, day, hour, minute, second, rain, temperature, original row, original column
tdm=np.empty(((na, nr, nc)), dtype=np.dtype('f4')) #Initiate the 3D matrix, fill it with 0s
print(tdm.shape)

#print(filenames)
i=0 #counter for number of filenames, to iterate in "for file" loop

#-----MAIN PRECIPITATION LOOP: Iterates through every  precipitation file in the given folder-----#
for file in filenames_precip: #temperature and precipitaton values must have same name
    name=os.path.basename(filenames_precip[i]) #gets name of file being read
    print("File: ", name)
    storm_array=np.array(pd.read_csv(file, delimiter='\t', header=None, skiprows=6))
    tdm = Precipitation(name, storm_array, tdm, i)
    i+=1 #increases counter

#-----Main TEMPERATURE Loop: Iterates through every temperature file in temperature folder, if the user inputs one
if temp == True: #Fills temperature data only if user inputs such data
    print('START TEMPERATURE READING')
    i=0 #restars counter for temperature files
    for file in filenames_temp:
        name = os.path.basename(filenames_temp[i])  # gets name of file being read
        temp_array=np.array(pd.read_csv(file, delimiter='\t', header=None, skiprows=6))
        tdm= Temperature(name, temp_array, tdm, i)
        i+=1

#SAVE RESULTING FILES:
SaveFiles(tdm, savepath)
print('My program took ', time.time()-start_time, "s to run.")








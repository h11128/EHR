import sys
import os
import xlrd
import datetime 
import xlwt
from xlwt import Workbook 
import math 
from xlutils.copy import copy
import csv

f = 'EHRdataSample.xlsx'
data = xlrd.open_workbook(f)
table = data.sheet_by_index(0)
m = table.nrows
n = table.ncols
#wb = Workbook() 
#sheet1 = wb.add_sheet('Sheet 3')     
# gender, age_group, date_of_injury, PRE_max_days, POST_max_days, and Symptom frequency
def normallize_categorical(X):
  total = len(set(X))
  category = {}
  newArray = []
  count = 1
  for i in X:
    if i not in category:
      category[i] = count
      count +=1
      newArray.append(count/total)
    else:
      newArray.append(category[i]/total)
  return newArray

def normallize_continuous(X):
  maxValue = max(X)
  minValue = min(X)
  ranging = maxValue - minValue
  newArray = []
  for i in X:
    newArray.append(abs(i)/ranging)
  return newArray

def normallize_sequence(X, duration_range):
  for i in range(len(X)):
    if i == 0:
      pass
    elif X[i] != "k":
      X[i] = (X[i]-duration_range[0])/duration_range[2]
    else:
      X[i] = 0
  return X[1:]

patient_id = table.col_values(0, 1)
gender = table.col_values(1, 1)
age_group = table.col_values(3,1)
encounter_date = table.col_values(9, 1)
pre_max_days = table.col_values(16, 1)
post_max_days = table.col_values(17, 1)
date_injury = table.col_values(6, 1)


#initialize dictionary for second type of data
second_data = {}
patient_group = list(set(patient_id))
for i in range(len(patient_group)):
  second_data[patient_group[i]] = ["k" for _ in range(17, 34)]

patient_normalize = normallize_categorical(patient_id)
gender = normallize_categorical(gender)
age_group = normallize_categorical(age_group)
pre_max_days = normallize_continuous(pre_max_days)
post_max_days = normallize_continuous(post_max_days)

injury_time = []
frequency = []
min_Date = 999999999
max_Date = 0
for i in range(0, m-1):
  duration = encounter_date[i] - encounter_date[0]
  injury_time.append(duration)
  current_id = table.cell(i+1, 0).value
  current_gender = gender[i]
  value = 0
  for k in range(17, 34):
    if k != 17:
      value += table.cell(i+1, k).value
      sympton_value = table.cell(i+1, k).value
      current_occurence = second_data[current_id][k-17]
      if int(sympton_value == 1):
        occurence_duration = encounter_date[i] - date_injury[i]
        # fill the occurence
        if current_occurence == "k" or current_occurence <= occurence_duration:
          
          second_data[current_id][k-17] = occurence_duration
          # occurence duration
          if min_Date> occurence_duration:
            min_Date = occurence_duration
          if max_Date< occurence_duration:
            max_Date = occurence_duration
      
    else:
      save_gender = second_data[current_id][0]
      if save_gender != current_gender:
        second_data[current_id][0] = current_gender
  frequency.append(value)

encounter_date = normallize_continuous(encounter_date)
frequency = normallize_continuous(frequency)
injury_time = normallize_continuous(injury_time)
# data for first type of data
the_data = [patient_id, frequency, gender, age_group, encounter_date, pre_max_days, post_max_days, patient_normalize, injury_time]


duration_range = [min_Date, max_Date, max_Date - min_Date]
for k in second_data:
  
  second_data[k] = normallize_sequence(second_data[k], duration_range)
  print(k, end = ",")
  
  for j in range(len(second_data[k])):
    if j!=len(second_data[k])-1:
      print(second_data[k][j], end=',')
    else:
      print(second_data[k][j])


# csv_file = open('csv_file.csv', 'w')
# wr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
# for rownum in range(6):
#     wr.writecol(the_data[i])

# csv_file.close()
"""
for i in range(len(gender)):
  for j in range(len(the_data)):
    if j!=len(the_data)-1:
      print(the_data[j][i], end=',')
    else:
      print(the_data[j][i])
"""

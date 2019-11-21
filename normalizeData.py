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
  count = 0
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


patient_id = table.col_values(0, 1)
gender = table.col_values(1, 1)
age_group = table.col_values(3,1)
date_injury = table.col_values(9, 1)
pre_max_days = table.col_values(16, 1)
post_max_days = table.col_values(17, 1)
injury_time = []
frequency = []


for i in range(0, m-1):
  duration = date_injury[i] - date_injury[0]
  injury_time.append(duration)

  value = 0
  for k in range(18, 33):
    value += table.cell(i+1, k).value
  frequency.append(value)

patient_normalize = normallize_categorical(patient_id)
gender = normallize_categorical(gender)
age_group = normallize_categorical(age_group)
date_injury = normallize_continuous(injury_time)
pre_max_days = normallize_continuous(pre_max_days)
post_max_days = normallize_continuous(post_max_days)
frequency = normallize_continuous(frequency)
the_data = [patient_id, frequency, gender, age_group, date_injury, pre_max_days, post_max_days, patient_normalize, injury_time]

# csv_file = open('csv_file.csv', 'w')
# wr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
# for rownum in range(6):
#     wr.writecol(the_data[i])

# csv_file.close()
for i in range(len(gender)):
  for j in range(len(the_data)):
    if j!=len(the_data)-1:
      print(the_data[j][i], end=',')
    else:
      print(the_data[j][i])


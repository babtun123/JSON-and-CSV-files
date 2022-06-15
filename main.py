
######################################################
# Project: 3
# UIN: 669794692
# repl.it URL: https://replit.com/@UICCS111HayesSpring2022/Project-3-SamuelShodiya#main.py
 
######################################################
# imports
import csv
import requests
import json
import matplotlib.pyplot as plt

# function definitions
def get_data_from_file(fn, format = ""):
  """Function to get data from file either as a csv file or a json file."""

  # if format is an empty string, check for csv and json in filename(fn)
  if format == "":
   if "csv" in fn:
     format = "csv"
   if "json" in fn:
     format = "json"
    
  data = []
  # open file as a csv reader
  if (format == "csv"):
    with open(fn) as csv_file:
      return_data = csv.reader(csv_file, delimiter=',')

      next (return_data)
      for row in return_data:
        data.append(row)

    return data
  # open file as a json
  elif (format == "json"):
    j = open(fn)

    text = j.read()

    json_format = json.loads(text)

    for row in json_format:
      data.append(row)

    return data
    
def get_data_from_internet (fn, format = ""):
  """converts data from the internet into a csv file or a json file"""
  if format == "":
   if "csv" in fn:
     format = "csv"
   if "json" in fn:
     format = "json"
     
  data_2 = []
  if (format == "json"):
    r = requests.get(fn)

    content = r.json()
    for row in content:
      data_2.append(row)
    return data_2

  elif (format == "csv"):
    with requests.Session() as s:
      download = s.get(fn)

      csv_content = download.content.decode('utf-8')

      csv_reader = csv.reader(csv_content.splitlines(), delimiter=',')
      my_list = list(csv_reader)
      for row in my_list:
        data_2.append(row)
      return data_2

# main
def main():
  """Main function"""
  local_file_data = get_data_from_file("ChicagoWeather_Mar2022.csv")

  internet_data = get_data_from_internet("https://data.cityofchicago.org/resource/ygr5-vcbg.json?$WHERE=tow_date%20BETWEEN%20%222022-03-01%22%20and%20%222022-03-31%22&$LIMIT=1500")

# Question 1: How many blue cars (color: BLU)  were towed in March 2022?  (an integer)
  BLU_count = 0
  tow_day_dict = {}
  sum_of_towed_cars = 0
  for item in internet_data:
    # print(item)
    car_color = item.get("color", "none")
    if car_color == "BLU":
      BLU_count += 1
  # print(BLU_count)

# Question 2: Which day had the most towed cars?  (format as YYYY-MM-DD)
    split_tow_date = item["tow_date"].split("T")[0]
  
    if split_tow_date in tow_day_dict:
      tow_day_dict[split_tow_date] += 1
    else:
      tow_day_dict[split_tow_date] = 1
  print(tow_day_dict)
  tow_day_tuple = tow_day_dict.items()
  sorted_list_of_tuple = sorted(tow_day_tuple, key = lambda x:x[1])
  most_towed_cars = sorted_list_of_tuple[-1][0]

  # Question 3: What is the average number of cars towed per day? (format to one decimal place)
  for value in tow_day_dict:
    dict_value = tow_day_dict[value]
    sum_of_towed_cars += dict_value

  ave_towed_cars = sum_of_towed_cars / len(tow_day_dict)
  ave_towed_cars_rounded = "{:.1f}".format(ave_towed_cars)
  
  # print(ave_towed_cars)
  # print(ave_towed_cars_rounded)
  # print(sum_of_towed_cars)

# Question 4: Which day had the highest temperature?  (format as YYYY-MM-DD)
  max_temp = ""
  max_temp_day = ""
  for line in local_file_data:
    if (line[2] > max_temp):
      max_temp = line[2]
      max_temp_day = line[0]
  max_temp_date = "2022-3-" + max_temp_day
  # print(max_temp_date)
  # print(max_temp_day, max_temp)
    
# Question 5: What was the average max temperature for the month?  (format to one decimal place)
  total_max_temp = 0
  for max_temp in local_file_data:
    # print (max_temp[1])
    total_max_temp += int(max_temp[1])
  # print(total_max_temp)
  average_max_temp = total_max_temp / 31
  average_max_temp_rounded = "{:.1f}".format(average_max_temp)
  # print(average_max_temp_rounded)
  # print(average_max_temp)

# Question 6: How many FORD cars were towed on the day with the most precipitation? (an integer)
  max_preci = ""
  # max_preci_day = ""
  for preci in local_file_data:
    if preci[-1] > max_preci:
      max_preci = preci[-1]
      # max_preci_day = line[0]
  # print(max_preci)

  ford_counter = 0
  for date in internet_data:
    if (date["tow_date"] == "2022-03-19T00:00:00.000"):
      car_make = date.get("make", "none")
      if (car_make == "FORD"):
        ford_counter += 1
      # print(date)
  # print(ford_counter)   


  # write answers as text files
  file = open('Answers.txt', 'w')
  file.write(str(BLU_count))
  file.write("\n") 
  file.write(str(most_towed_cars))
  file.write("\n")
  file.write(str(ave_towed_cars_rounded))
  file.write("\n")
  file.write(str(max_temp_date))
  file.write("\n")
  file.write(str(average_max_temp_rounded))
  file.write("\n")
  file.write(str(ford_counter))
  file.close()

  
                         # Visualization
  
  # y-axis
  num_of_car_towed = [ tow_day_dict[elem] for elem in tow_day_dict]
  # print(num_of_car_towed)
  # x-axis
  lst_of_car_towed_day = [ elem for elem in tow_day_dict]
  # print(lst_of_car_towed_day)
  date_list = []
  for split in lst_of_car_towed_day:
    date_split = split[-2: ]
    date_list.append(int(date_split))
    # print(date_split)
  # print(date_list)
    
  # y-axis
  precipitation_list = []
  for precip in local_file_data:
    precipitation_list.append(float(precip[-1]))
  # print(precipitation_list)
  fig, ax1 = plt.subplots()
  color = 'tab:red'
  ax1.set_xlabel('Day')
  ax1.set_ylabel('No. of car towed', color=color)
  ax1.plot(date_list, num_of_car_towed, color=color)
  ax1.tick_params(axis='y', labelcolor=color)
  
  ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
  
  color = 'tab:blue'
  ax2.set_ylabel('Precipitation', color=color)  # we already handled the x-label with ax1
  ax2.plot(date_list, precipitation_list, color=color)
  ax2.tick_params(axis='y', labelcolor=color)
  
  fig.tight_layout() # otherwise the right y-label is slightly clipped
  plt.title("Line Chart")
  plt.savefig("line_chart.png")
  # plt.show()


  # Piechart
  car_make_piechart_dict = {}
  for date in internet_data:
    car_make_piechart = date.get("make", "none")
    if car_make_piechart in car_make_piechart_dict:
      car_make_piechart_dict[car_make_piechart] += 1
    else:
      car_make_piechart_dict[car_make_piechart] = 1
  sorted_car_make = sorted(car_make_piechart_dict.items(), key = lambda car_make:car_make[1])
  
  # print(car_make_piechart_dict)
  # print(sorted_car_make)

  size = [x[1] for x in sorted_car_make]
  labels = [x[0] for x in sorted_car_make]

  fig, ax1 = plt.subplots()
  ax1.pie(size, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
  ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
  plt.title("Car Chart")
  plt.savefig("pie_chart.png")
  # plt.show()
  
  # print(size)
  # print(labels)
  # print(BLU_count)

main()

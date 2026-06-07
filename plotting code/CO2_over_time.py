#The packages you will need
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

#Load in your data
#k30 = pd.read_csv('Your CSV here') #The K30 data file
#office = pd.read_csv('Your CSV name here') #Refrance data
k30 = pd.read_csv('your csv here')          # Time_UTC, CO2_ppm
office = pd.read_csv('your csv here')

#Read the datetime column 
#Both of the files are set to UTC time. If your timestamp format is different these might need to chagne
k30["datetime"] = pd.to_datetime(k30["Time_UTC"], format="%H:%M:%S")
office["datetime"] = pd.to_datetime(office["TIME"], format="%H:%M:%S")

#Define the start and end time that will be plotted on the graphs and that you want to compare between
#Can comment out if you want to use the whole time of both data sets
start = pd.to_datetime("23:00:00", format="%H:%M:%S")
end   = pd.to_datetime("23:16:00", format="%H:%M:%S")

#Filter the datasets down to the specifc timeframe 
k30_f = k30[(k30["datetime"] >= start) & (k30["datetime"] <= end)]
office_f = office[(office["datetime"] >= start) & (office["datetime"] <= end)]


#To match the time values
# Adjustable tolerance (in seconds)
tolerance_seconds = 3
tolerance = pd.Timedelta(seconds=tolerance_seconds)
#Sort the dataframes
k30_f = k30_f.sort_values("datetime")
office_f = office_f.sort_values("datetime")
#Actual matching of the timestamps
matched = pd.merge_asof(
    k30_f,
    office_f,
    on="datetime",
    direction="nearest",
    tolerance=tolerance
)
#remove rows with no matchs
#Fills with NaN
matched = matched.dropna(subset=["12CO2"])



#Plot of K30 and Reference over time
fig, ax = plt.subplots(figsize=(12,5))
fig.canvas.manager.set_window_title("K30 and Office Over Time")
ax.plot(matched["datetime"], matched["CO2_ppm"], label="K30 CO₂")
ax.plot(matched["datetime"], matched["12CO2"], label="Office CO₂")

# This format only shows time and not date 
#Comment out these two lines if you want the date to show before the timestamp 
ax.xaxis.set_major_locator(mdates.AutoDateLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))

#Figure formating 
plt.xlabel("Time (HH:MM:SS)")
plt.ylabel("CO₂ (ppm)")
plt.legend()
plt.tight_layout()
#plt.savefig('K30_Office over time.jpg')
plt.show()



#The packages you will need
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

#Load in your data
k30 = pd.read_csv('Your CSV here') #The K30 data file
office = pd.read_csv('Your CSV name here') #Refrance data


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

# Set up for regression
x = matched["12CO2"].values
y = matched["CO2_ppm"].values

# Linear regression
slope, intercept = np.polyfit(x, y, 1)
y_pred = slope * x + intercept

# R² calculation
ss_res = np.sum((y - y_pred)**2)
ss_tot = np.sum((y - np.mean(y))**2)
r2 = 1 - ss_res/ss_tot

print("Regression line:")
print(f"K30_CO2 = {slope:.3f} * Office_CO2 + {intercept:.3f}")
print(f"R² = {r2:.4f}")


fig2 = plt.figure(figsize=(7,7))
fig2.canvas.manager.set_window_title("K30 vs Office Scatter + Regression")
ax2 = fig2.add_subplot(111)

# --- Scatter plot for fig2 ---
ax2.scatter(x, y, alpha=0.7, label="Matched data")

# Regression line
x_line = np.linspace(min(x), max(x), 100)
y_line = slope * x_line + intercept
ax2.plot(x_line, y_line, color="red", label="Regression line")

# Labels and title
ax2.set_xlabel("Office CO₂ (ppm)")
ax2.set_ylabel("K30 CO₂ (ppm)")
ax2.set_title("K30 vs Office CO₂ (Nearest Timestamp Match)")

# Regression equation text
eq_text = f"K30 = {slope:.3f} × Office + {intercept:.3f}\nR² = {r2:.4f}"
ax2.text(
    0.05, 0.95,
    eq_text,
    transform=ax2.transAxes,
    fontsize=12,
    verticalalignment='top',
    bbox=dict(facecolor='white', alpha=0.7, edgecolor='none')
)

ax2.legend()
fig2.tight_layout()
plt.show()

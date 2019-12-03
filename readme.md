# Background

This project is to visualize the EHR data using star coordinates in 3D space.

# Dataset

EHR.csv

# Running Command

python3 chart.py EHR.csv

# Interaction
mouse interaction: left click on a selected point, only show the middle point and trajectory, closest point of selected point

slider interaction: 
	record: from 0-7. 0-1 means nothing, 1-2 means only show final point for all points, 2-3 means final point and trajectory, 3-4 means final point and trajectory and middlepoints, 4-5 means final point and middlepoints, 5-6 means final points, 6-7 means show nothing	
	person: from 0-max_person. Means how many closest point one wants when click on the selcted point
	point Size: change the point size of final point, middle point will change accordingly
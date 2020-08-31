# Background

This project is to visualize the EHR data using star coordinates in 3D space.

EHR data: https://drive.google.com/drive/folders/1pb0CCT6Pnp0WZagkqrKtTHVpDsGsokEf
star coordinate: https://en.wikipedia.org/wiki/Celestial_coordinate_system
report: report.pdf 


# Data normallization (Just in case needed, but you don't have to do this. EHR.csv already exist)
python normalizeData.py > EHR.csv

# Dataset
EHR.csv

# Running Command
python3 chart.py EHR.csv mode_number

# mode_number, the mode of how the feature vector form in the 3 dimension Cartesian Coordinate systme
possible mode:0,1,2,3,4
  rho_x = pearsonr(x axis, features[i])
  similar to rho_y and rho_z
  #angle mode, use two angle with x axis and z axis
   angle calculate from       
	  angle1 = (abs(rho_x) + 1) / (rho_x+1+rho_y+1) * math.pi
      angle2 = (abs(rho_z) +1)/ 2 * math.pi
  if mode == 0:
    vector = [math.cos(angle1), math.sin(angle1), math.cos(angle2)]
  #disimilarity mode, the more disimilar to one (x, y, z) axis the closer to them
  elif mode == 1:
    vector = [-rho_x, -rho_y, -rho_z]
  #similarity mode,  the more similar to one (x, y, z) axis the closer to them
  elif mode ==2:
    vector = [rho_x, rho_y, rho_z]
  #generative mode: where the distribution of vector will try to equally divide the space in a generative manner
  elif mode == 3:
	vector = [1,0,0], [0,1,0], [0,0,1], [-1,0,0].......[-1/(3)^0.5, 1/(3)^0.5, 1/(3)^0.5]........[1/(2)^0.5, 1/(2)^0.5,0].....
	6 possible generation from vector [1,0,0]
	8 possible generation from vector [1/(3^0.5), 1/(3^0.5),1/(3^0.5)]
    12 possible generation from vector [1/(2^0.5) , 1/(2^0.5,0]
	
  # 2d mode: no z axis, only x and y axis, all the feature vector equally divide the space
  elif mode == 4:
    angle = 2 * math.pi * vector_number /rho_x
    base1 = [math.sin(angle), math.cos(angle), 0]
    vector = base1
  # unfinished future mode:
  First thought: project from 2d mode's vector to 3d, keep the angle in the 2d but project 1/3 of the vector to the z>0 space and 1/3 to the z<0 space, and the angle between z axis would be 45.
  
  Second thought: only initiallize two vector as x axis [1,0,0]  and y axis [0,0,1]. And then for all the vector calculate the angle between x, and y, and then find a vector that satisfy the two angle constraint. Similar for the later on vector
  
  Third thought:initiallize one vector as x axis [1,0,0]. For the first vector calculate the angle between x, and then randomly select the vector in all the possible selection. For the second vector calculate the two angle and select. For the third vector calculate the three angle and select one vector that satisfy the selection. For the rest vector only consider three angle constraint.
  
  
# Interaction
mouse interaction: left click on a selected point, only show the middle point and trajectory, (person) number of closest point of selected point

slider interaction: 
	record: from 0-7. 0-1 means nothing, 1-2 means only show final point for all points, 2-3 means final point and trajectory, 3-4 means final point and trajectory and middlepoints, 4-5 means final point and middlepoints, 5-6 means final points, 6-7 means show nothing	
	person: from 0-max_person. Means how many closest point one wants when click on the selcted point
	point Size: change the point size of final point, middle point will change accordingly

# Summary Report on "Where do we find missing data in a commercial real-time location system? Evidence from 2 dairy froms"

## Introduction

- The objective of this study was to investigate whether there
are any major obstacles, or sections, inside open freestall barns
that would interfere with data captured from a UWB-based RTLS.
- They explored the extent to which missing data in the CowView automatic monitoring system could be attributed to the cows’ locations within 2 dairy barns.
- Investigated variation in missing data between cows.

## Materials and Methods

- Data were collected from two commercial farms using RTLS to monitor individual cow positions.
- Farm A in Sweden housed a mix of Holstein Friesian and Swedish Red cows; Farm B in the Netherlands had Holstein Friesian cows.
- The study used cleaned RTLS data to analyze cubicle occupancy over a 6-days evenly distributed throughout a 3-mo period.

## Methods and Challenges

- A challenge in the analysis of missing data was separating individual cow effects from spatial effects.
- To encounter this challenge linear mixed model was fitted with response variable, involving cow and day as fixed effects and grid square as random effect with a threshold of 5s as a time gap.
- Logit-transformation was applied to the data to improve its fit to a normal distribution.
- A conditional autoregressive (CAR) model was used for spatial effects using the hglm package in R.

## Statistical Analysis

- A larger amount of data was missing along one wall of the barn, right hand side, of both farms. 
- Farm 2 experienced higher levels of missing data at the entrance to one of the automatic milking machines.
- Large variation was detected between the proportion of lost positions of different cows in the raw data. 

## Discussion

- Fitted proportions of lost positions were evenly distributed within both barns, RTLS inside the barns operated effectively.
- Data missing along the RHS of wall on both farms was attributed to the signal truncation outside the floorplan in the CowView system, rather than interference from physical objects.
- Farm 2 missing data was due to the presence of significant metal components that disrupted the signal, as well as the machine's location in the corner of the barn, resulting in poor signal reception within that grid square.
- Individual differences could be due to battery malfunction or could be the position of the tag on the
neck collars.

## Conclusion

- Study shows no major obstacles were found to interfere with the RTLS except for an automatic milking machine in one of the barns.
-  Although very few sections in the investigated barns had high levels of missing data, variations between individual tags must be considered when analyzing social behavior among dairy cows, especially in areas with a high proportion of missing data.
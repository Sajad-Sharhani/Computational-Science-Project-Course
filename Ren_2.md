## Summary Report on "Interpolation Methods to Improve Data Quality of Indoor Positioning Data for Dairy Cattle"

### Introduction

- RTLS using UWB technology enable continuous monitoring of cow's behavior and social interactions in dairy barns. Previous studies have reported missing data issues in UWB systems, varying from 2% to as high as 58%, with significant variation among individual cows and areas within the barn.
- Interpolation methods are useful for fitting in missing data for precise spatial analysis of cow interactions.
- Median filters, image analysis, Kalman filters, and different interpolation approaches, have been used in previous studies to refine UWB-based behavior classification and improve accuracy in positioning data.
- The current study aims to investigate missing data patterns and evaluate multiple interpolation methods to identify the most accurate method for predicting missing positions.

### Materials and Methods

- The study was conducted at a Swedish dairy farm housing about 200 milking cows, including Holstein Friesian, Swedish Red, and crossbreds in a non-insulated free-stall barn.
- The barn, measuring 74 × 33 m, had feeding alleys on both sides, and cows were divided into two groups, each with access to a feeding alley.
- RTLS consisted of eight ceiling-mounted anchors, forming a coordinate system to cover the entire barn.
- 6 days data sampled across 3-months, each day covering continuous 24-hour periods was used for analysis.

### Statistical Analysis

 #### Missing data pattern :
- Missing data patterns were assessed of 69 cows over a 6-day period in a dairy barn.
- Different categories of missing data were identified: 1 second, 5 consecutive seconds, and 10 consecutive minutes, accounting for an average of 31.29%, 18%, and 4% of the study duration, respectively.
- A 20 x 17 grid superimposed on the barn's floorplan for studing missing data.
- Linear mixed models with spatial smoothing were applied, treating missing data duration as a Gamma-distributed response variable.
- The hierarchical generalized linear mixed model (HGLM) with spatial smoothing was employed using the hglm package in R to perform these analyses, referred to as the "duration of missing data model."

#### Missing data simulation :
- 20 tags were chosen for a comparative assessment of interpolation methods,tags experienced less than 25% missing data for 1 second or more and less than 13% missing data for 5 consecutive seconds or more.
- Missing data was simulated by estimating probabilities of missing data streaks based on cow positions.
- Simulation process was repeated 10 times for each cow for 6 days. Models were established to predict missing data proportions and durations, using cow-specific fixed effects and grid-specific fixed effects.
- Estimated model parameters were used to generate missing data instances and lengths, allowing for a total of 24,158,870 observations of simulated missing data.
- The missing data pattern and simulation procedures were executed in R, generating a heat map of the simulated missing data positions, which provided a basis for assessing interpolation errors.

#### Interpolation method :

4 Interpolation methods were used: 
- Previous Position: Utilizes the last known position of the cow when data is missing.
- Linear Interpolation: Connects missing data points with a straight line between the last known positions.
- Cubic Spline Interpolation: Utilizes cubic interpolation to create smooth, continuous second-order derivative polynomials.
- Modified Akima (Makima): An adaptation of the Akima algorithm employing cubic interpolation with continuous first-order derivatives. This modified version gives more weight to slopes closer to zero, avoiding overshooting and maintaining a balance between flat regions.
- Datasets were interpolated to 1 Hz temporal resolution. For gaps in cow position data, the nearest non-missing value was interpolated. The Euclidean distance between the interpolated and observed positions was used to calculate error distances.
- CowView translates raw position data into clustered positions and maps these to the barn layout to determine cow activities like resting, feeding, standing, and walking. These activities are identified with over 95% accuracy and were used to assess interpolation errors for the different activities.

### Results


#### Missing Data Patterns :
- Duration Distribution: Simulated missing data duration follows a Gamma distribution, with some periods lasting up to 1 hour and 20 minutes.
- Locations of Missing Data: Concentration of simulated missing data primarily observed around the cubicle area and near feeding tables.

#### Interpolation Performance in the Barn :
- Error Distribution on the Floorplan: Larger error distances observed in pathways where cows walk, notably between cubicles.

#### Overall Interpolation Performance :
- Mean Error Distances: Ranged from around 55 cm for the "previous position" method to about 17 cm for the modified Akima interpolation when compared to observed CowView data.

#### Effect of Missing Data Duration :
- Error Distance Changes with Duration: Error distances significantly increased for data missing up to 1 minute, but stabilized as duration increased beyond 1 minute, with higher variance.
- Stabilization: Modified Akima interpolation showed a lower stable error level compared to other methods.

#### Performance for Different Activities :
- Activities and Interpolation: Modified Akima interpolation consistently showed the lowest error distances across various activities, exhibiting the most improvement compared to using the last observed position.

#### Error Distance vs. Data Duration :
- Sharp increase in error distance from zero to 1 minute of missing data.
- Beyond 1 minute, error distances stabilized with increased variance.
- Modified Akima method maintained a lower, stable error level compared to other methods.

#### Comparison for Different Activities (Linear vs. Modified Akima) :
- Under 5 minutes of missing data: Modified Akima demonstrated better performance. It consistently exhibited the lowest error distance and was substantially superior to linear interpolation for all 4 activities, with mean error distances stabilizing
at lower levels.


### Discussion
- Investigated cow activities: 57% resting, 20% feeding, 10% standing, and 13% walking, showing the highest error in tracking individuals walking.
- Error distances stabilized after 1 minute of missing data, possibly due to limited cow movement within the barn.
- Larger errors observed where cows walked (corners around the feeding area and across cubicles), suggesting potential for refining interpolation methods based on the barn's structure.
- Acknowledged that despite enhanced methods, system noise and specific cow movements create limitations in improving data interpolation.

### Conclusion
- Demonstrated the effectiveness of Modified Akima interpolation in significantly improving accuracy compared to simple extrapolation across various barn areas.
Identified Modified Akima as the most accurate method for resting, feeding, standing, and walking activities.
- Emphasized that reliable position data through interpolation could significantly enhance further analyses of indoor cow behavior and social interactions.

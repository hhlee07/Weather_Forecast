# Weather_Forecast
## Forecasting abonormal climate for each region in Korea with AWS table data
### AWS data
<img width="80%" src="https://user-images.githubusercontent.com/81947384/180928852-56b37d49-cd31-445a-95de-49bca478ba96.PNG"/>
### Meta data
<img width="80%" src="https://user-images.githubusercontent.com/81947384/180928852-56b37d49-cd31-445a-95de-49bca478ba96.PNG"/>
### Label
#### dry / frozen / heat-wave / h-rain / h-snow / nsw / sand / sea-wave / strom-wave / typoon / wind
### Preprocessing
#### - Use Reverse Geocoding to convert region address
#### - Concatenate meta data with AWS data to use additional information
#### - Fill all missing value using linear interpolation, normalize values with minmax scaling
### Model structure
<img width="80%" src="https://user-images.githubusercontent.com/81947384/180928852-56b37d49-cd31-445a-95de-49bca478ba96.PNG"/>
### Result
#### - MSE: 0.0046
#### - F1-score: 0.7479
#### - Inference Time: 0.0007231235504150391
#### - Model Size: 162kb

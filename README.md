# Weather_Forecast
## Forecasting abonormal climate for each region in Korea with AWS table data
### AWS data

### Meta data

### Label
### Preprocessing
#### - Use Reverse Geocoding to convert region address
#### - Concatenate meta data with AWS data to use additional information
#### - Fill all missing value using linear interpolation, normalize values with minmax scaling
### Model structure

### Result
#### - MSE: 0.0046
#### - F1-score: 0.7479
#### - Inference Time: 0.0007231235504150391
#### - Model Size: 162kb

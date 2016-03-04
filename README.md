# findat
Easily retrieve, store, and analyze financial data

#This package is still being developed

Currently, there are two modules: 'finret' and 'finstat'.
To use this package, you will need to have numpy, scipy, and pandas packages installed as well.

finret makes retrieving data from web sources like Yahoo, The St. Louis FED Database FRED, and Robert Shiller's database easy to do. All data is returned as a pandas dataframe.

findat contains a linear regression class ('lin_reg') that makes regressing data in pandas DataFrames or Series easy to do. Moreover, the lin_reg class has simulation methods that allow you to model the uncertainty in the regression errors and predictors. See Chapter 7 of "Data Analysis Using Regression and Multilevel/Hierarchical Models" by Gelman and Hill. 


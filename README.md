# Analyzing A Facebook Ad Campaign in Dash

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Features](#features)
* [Results](#results)
* [Status](#status)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)

## General info
This data is from a Facebook ad campaign. The campaign is focused on customer acquisition versus brand awareness. The primary goal is “Website Registrations Completed” and the secondary goal is “Website Leads.” The target acquisition cost for the primary goal was $50 or less. 

In this project, I will create a tool in plotly's dash to explore the data set and different visualizations.

## Technologies
* Python 3.7

## Setup
Use requirements.txt file to install required packages, or install packages and versions listed below:

* pandas==1.0.1
* numpy==1.18.1
* catboost==0.23
* matplotlib==3.1.3
* scikit_learn==0.23.1
* xgboost==1.1.1

Data can be found on [Kaggle](https://www.kaggle.com/blastchar/telco-customer-churn)

## Features
The following three Machine Learning models are included:

* CatBoost
* XGBoost
* Random Forest

## Results
Overall the CatBoost model outperformed the Random Forest and XGBoost models in recall. Recall is the chosen metric because the cost of false positives is low in this case and we want to capture all positives. The full metrics for each model is included below: 
### Random Forest Results:
| Metric | Train | Test |
| ------ | ----- | ----- |
| AUC | 0.746 | 0.896 |
| Accuracy | 0.766 | 0.873 |
| F1 | 0.614 | 0.797 |
| Recall | 0.703 | 0.945 |
| Precision | 0.546 | 0.690 |
### XGBoost Results:
| Metric | Train | Test |
| ------ | ----- | ----- |
| AUC | 0.759 |  0.789 |
| Accuracy | 0.746 | 0.769 |
| F1 | .622 | 0.656 |
| Recall | 0.786 |  0.831 |
| Precision | 0.514 | 0.542 |

### CatBoost Results:
| Metric | Train | Test |
| ------ | ----- | ----- |
| AUC | 0.753 |  0.753 |
| Accuracy | 0.714 | 0.712 |
| F1 | 0.608 |  0.608 |
| Recall | 0.836 | 0.840 |
| Precision | 0.478 |  0.476 |

## Status
Project is: _In Progress_

## Contact
Created by [Gabrielle Nyirjesy](https://www.linkedin.com/in/gabrielle-nyirjesy) - feel free to contact me!

## Acknowledgements
* Data pulled from [Kaggle](https://www.kaggle.com/blastchar/telco-customer-churn)

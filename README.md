# Overview

This is a project on predicting if a client will subscribe to a term deposit at a bank. 
The data is taken from the [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/Bank+Marketing)!
This is done as part of the Machine Learning Engineering course held by Alexey Grigorev.

## Problem description

If we think about how banks earn money, one of such methods is to aggressively grow their money with investments.

They are able to have a large amount of capital as there are people who subscribe to term deposits. 

With this, the bank is able to give them the interest rate that they have offered, and take the rest of the profit from these investments as a way to earn money.

With this model, it will predict the customers that are more likely to subscribe to a term deposit. 

This allows the bank to better convert these customers to subscribe to a term deposit. 

## Contents of the folder

The data folder consists of the original dataset that I have used myself, as well as the new dataset added with a few feaatured engineered from the original dataset.

The code folder consists of: 
- notebook - where all the EDA, cleaning, and model training happens
- predict - to load the model and serve it via a web service
- predict-test - to test the output of the model 
- pipenv and pipenv.lock for the virtual environment using pipenv
- Dockerfile for using a Docker container


## Data 

The data can be found here in the [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/Bank+Marketing)

As mentioned on the website, there are four datasets. 

I am primarily using dataset number 1, which is very close to the data analyzed in [Moro et al., 2014] as there are more inputs to analyze. 

The Kaggle version of it consists of the old dataset (dataset 3) and one additional input that is not in this current dataset called 'balance'.

The 'balance' is the amount of money that the person has in their bank account. 

However, since there is no ID that I I can use to join the two datasets, I will not be using balance.

Instead, the additional metrics in the updated dataset should do well! 

For the rest of the inputs/columns, please refer to the 'bank-additional-names' document or refer to the UCI website. 

To load the dataset, do add in ';' in the 'sep' parameter.

## Deployment of model

I am currently using Windows, therefore waitress is the way I deploy the model. 
To deploy the model with waitress, please use: `waitress-serve --listen=0.0.0.0:9696 predict:app`

If you can't use that, you can use `python3 -m waitress --listen=0.0.0.0:9696 predict:app` instead.

If you want to use gunicorn, you can do so by doing gunicorn `--bind 0.0.0.0:9696 predict:app`

## Virtual Environment/venv 

I used pipenv for the virtual environment. In order to use the same venv as me, do use pip install pipenv.

To replicate the environment, on your command line, use `pipenv install numpy scikit-learn==0.24.2 xgboost==1.4.2 pandas flask gunicorn waitress`

You can run the environment using pipenv shell, and deploy the model as normal.

To deploy the model, refer to the "Depolyment of model" part of the README.

## Docker

I have built the model and pushed it to [kwangyy/bank-prediction:3.8.12-slim](https://hub.docker.com/r/kwangyy/bank-prediction) for easy use!

To take the model from the docker container I built, just replace
`FROM python:3.8.12-slim` with 
`FROM kwangyy/bank-prediction:3.8.12` in the dockerfile.

If you choose to build a docker file locally instead, here are the steps to do so:

1. In your command line, run: `docker run -it --rm --entrypoint=bash python:3.8.12-slim` to create a docker image.

2. Create a Dockerfile as such:

~~~~
FROM python:3.8.12-slim

RUN pip install pipenv

WORKDIR /app

COPY ["Pipfile", "Pipfile.lock", "./"]

RUN pipenv install --system --deploy

COPY ["predict.py", "xgbclassifier.bin", "./"]

EXPOSE 9696

ENTRYPOINT ["waitress-serve", "--listen=0.0.0.0:9696", "predict:app"]
~~~~

This allows us to install python, run pipenv and its dependencies, run our predict script and our model itself and deploys our model using waitress.
Similarly, you can just use the dockerfile in this repository.

3. Build the docker container with `Docker build -t bank-prediction . `

4. Run the docker container with `Docker run -it -p 9696:9696 bank-prediction:latest` so that we can use our model!


## Deploying onto AWS Elastic Beanstalk
To deploy this into the cloud using AWS Elastic Beanstalk: 
1. Use `pipenv install --dev awsebcli` to install the command line for AWS Elastic Beanstalk. This is because we only need Elastic Beanstalk for deploying to the cloud and not actually for the model itself. 
2. Use `eb local run --port 9696`, allowing EB to build the Docker container.
3. Use `eb create bank-serving-env` to create the environment for the container itself 
4. AWS will start creating the environment, so do give it a few minutes. Once it is done, there will be a line that says 'Application available at ....'. Copy and paste the link - that is your new host. 
5. If you happen to use a .py file for a request, do change your host to the link, and your url to a f-string.
e.g. If your host = `kwangyy.importantletters.us-east-2.elasticbeanstalk.com`, then your url = `f'http://{host}/predict'`
6. To terminate, use `eb terminate bank-serving-env` to not waste your EC2 hours (you need to pay for your instance hours once it hits a certain limit, you know that right?) 

## If you like the project, it would be appreciated if you star this repo. Please feel free to fork the content as well!
[Kaggle](https://www.kaggle.com/kwangyangchia)

[Linkedin](https://www.linkedin.com/in/kwang-yang-chia/)

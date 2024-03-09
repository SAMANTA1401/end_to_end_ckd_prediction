### CKD prediction using classification  model

#### STEP-1: Clone the repository   
```bash
https://github.com/SAMANTA1401/ckd_prediction
```
#### STEP-2: Create a conda environment after opening the repository
```bash
conda create -p venv python==3.10 -y
```
```bash
conda activate venv
```
#### STEP-3: Install the requirements
```bash
pip install -r requirements.txt
pip freeze
pip freeze > requirements.txt
```
####  STEP-4: RUN : For data ingestion, data transformation, preproccessing and model training
```bash
python -m src.components.data_ingestion
```
or
```bash
dvc init
dvc repro
```
#### STEP-5: RUN: For prediction
```bash
python app.py
```

### AWS-CICD-Deployment-with-Github-Actions

#### 1. Login to AWS console.
#### 2. Create IAM user for deployment

```bash
#with specific access

1. EC2 access : It is virtual machine

2. ECR: Elastic Container registry to save your docker image in aws


#Description: About the deployment

1. Build docker image of the source code

2. Push your docker image to ECR

3. Launch Your EC2 

4. Pull Your image from ECR in EC2

5. Lauch your docker image in EC2

#Policy:

1. AmazonEC2ContainerRegistryFullAccess

2. AmazonEC2FullAccess
```
#### 3. Create ECR repo to store/save docker image
```bash
Save the URI: 987001014426.dkr.ecr.eu-north-1.amazonaws.com/kidney
```
#### 4. Create EC2 machine (Ubuntu)
#### 5. Open EC2 and Install docker in EC2 Machine:
```bash
#optinal

sudo apt-get update -y

sudo apt-get upgrade

#required

curl -fsSL https://get.docker.com -o get-docker.sh

sudo sh get-docker.sh

sudo usermod -aG docker ubuntu

newgrp docker
```

#### 6. Configure EC2 as self-hosted runner:
```bash
setting>actions>runner>new self hosted runner> choose os> then run command one by one
```
#### 7. Setup github secrets:
```bash
AWS_ACCESS_KEY_ID=

AWS_SECRET_ACCESS_KEY=

AWS_REGION = eu-north-1

AWS_ECR_LOGIN_URI = demo>>  987001014426.dkr.ecr.eu-north-1.amazonaws.com

ECR_REPOSITORY_NAME = kidney

```


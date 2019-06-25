# Cloud Run Image Demo

## First let's make sure you have a project name set and the us-central1 region

```
gcloud config set project <your project>
gcloud config set compute/region us-central1
```

## We will then install beta components and Cloud Run for gcloud
```
gcloud components install beta
gcloud components update
```

## Let's make sure we have Docker Setup Locally
```
gcloud auth configure-docker
gcloud components install docker-credential-gcr
```


## We will also need to setup some environment variable. PROJECT_ID will be the project you set above. THE _IMAGE_ variable will be the name of the Docker image you create. You can use anything for image name. _SERVICE_ will be the name of the service you launch. This too can be anything you want. 

```
export PROJECT_ID='<your project>'
export PROJ_NUMBER=$(gcloud projects list --filter="$PROJECT_ID" --format="value(PROJECT_NUMBER)")
export _IMAGE_='<your image name>'
export _SERVICE_='<your service name>'


```

## Let's enable APIs for Container Engine, Cloud Run, Container Registry, Cloud Build and Vision API

```
gcloud services enable container.googleapis.com containerregistry.googleapis.com cloudbuild.googleapis.com run.googleapis.com cloudapis.googleapis.com
```

## Let's give Cloud Build access to Cloud Run 

```
gcloud projects add-iam-policy-binding $PROJECT_ID \
--member serviceAccount:$PROJ_NUMBER@cloudbuild.gserviceaccount.com \
--role roles/container.developer

gcloud projects add-iam-policy-binding $PROJECT_ID \
--member serviceAccount:$PROJ_NUMBER@cloudbuild.gserviceaccount.com \
--role roles/run.admin

gcloud projects add-iam-policy-binding $PROJECT_ID \
--member serviceAccount:$PROJ_NUMBER@cloudbuild.gserviceaccount.com \
--role roles/iam.serviceAccountUser

gcloud iam service-accounts add-iam-policy-binding \
      $PROJ_NUMBER@cloudbuild.gserviceaccount.com \
      --member=serviceAccount:$PROJ_NUMBER-compute@developer.gserviceaccount.com \
      --role='roles/iam.serviceAccountUser'

```


## Now let's pull down our repository and enter the directory

```
git clone git@github.com:TheJaySmith/cr-img-demo.git \
 && cd cr-img-demo
```


Take a look at cloudbuild.yaml. Each step of the build process is shown here. Step 1 turns the code into a Docker container. Step 2 pushes the container to GCR. Step 3 deploys the container to Cloud Run named "ml-vision-cr".

### Let's go ahead and deploy 


```

gcloud builds submit --config cloudbuild.yaml . --substitutions=_IMAGE_="$_IMAGE_",_SERVICE_="$_SERVICE_"
```

In The Cloud Console, go to Cloud Run and choose your new application. Click the URL . 


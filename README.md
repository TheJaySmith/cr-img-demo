# Cloud Run Image Demo

## First let's declare some variable

```
export PROJECT='<your project>'
export IMAGE='<your image name>'
```

## Let's enable APIs for Cloud Run and Container Registry and Cloud Build

```
gcloud services enable container.googleapis.com containerregistry.googleapis.com cloudbuild.googleapis.com
```


## Now let's pull down our repository and enter the directory

```
git clone git@github.com:TheJaySmith/cr-img-demo.git \
 && cd cr-img-demo
```


### take a look at cloudbuild.yaml. Each step of the build process is shown here. Step 1 turns the code into a Docker container. Step 2 pushes the container to GCR. Step 3 deploys the container to Cloud Run named "ml-vision-cr".

### Let's go ahead and deploy 


```
gcloud builds submit --config cloudbuild.yaml .
```
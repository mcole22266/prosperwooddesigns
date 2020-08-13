# Website for Prosper Wood Designs

_still in development_

---

## How to Run

1) Create the file `prosperwooddesigns.secrets.env` in the root of the project
2) Add the following parameters to this file:
    - **AWS_ACCESS_KEY_ID**
    - **AWS_SECRET_ACCESS_KEY**
    - **POSTGRES_USER**
    - **POSTGRES_PASSWORD**
3) Run the app as follows depending on whether you want to run in dev or prod modes:
    - **Development Mode**: `docker-compose up --build`
        - _Note_: In `./prosperwooddesigns/config.py`, set **AWS_DOWNLOAD_IMAGES** to `True` in 
            ConfigDev in order to download all images from the S3 bucket to local
    - **Production Mode**: `docker-compose -f docker-compose.prod.yml up --build`
4) Navigate to `localhost:5000` to visit the app

## Configuration

The following configuration options are available in `./prosperwooddesigns/config.py`:

- **AWS_DOWNLOAD_IMAGES**: Set to True in order to automatically download all images from S3 into local environment.
    - True by default in production
    - False by default in development
- **SECRET_KEY**: Pass your own custom secret key or modify the default randomly generated key
    - Set to `os.urandom(16)` by default

## Developer Information

- Project Owner & Developer
    - Michael Cole
    - mcole042891.prof.dev@gmail.com

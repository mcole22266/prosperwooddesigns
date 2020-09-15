# Website for Prosper Wood Designs

_still in development_

---

## How to Run

1) Create the file `prosperwooddesigns.secrets.env` in the root of the project
2) Add the following parameters to this file:
    - AWS Credentials:
        - You can get these from your AWS Console: https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html#access-keys-and-secret-access-keys
        - _**AWS_ACCESS_KEY_ID**_
        - _**AWS_SECRET_ACCESS_KEY**_
    - Postgres Credentials:
        - This is the username and password that will be used in the Postgres container
        - _**POSTGRES_USER**_
        - _**POSTGRES_PASSWORD**_
    - Other Credentials:
        - _**ADMIN_FORM_SECRET_CODE**_
            - Define the Secret Code that will be used on the Admin Create Page
3) Run the app as follows depending on whether you want to run in dev or prod modes:
    - **Development Mode**: `docker-compose up --build`
        - _Note_: In `./prosperwooddesigns/config.py`, set **AWS_DOWNLOAD_IMAGES** to `True` in ConfigDev in order to download all images from the S3 bucket to local
    - **Production Mode**: `docker-compose -f docker-compose.prod.yml up --build`
4) To visit the app, navigate to:
   - **Development Mode**: `localhost:5000`
   - **Production Mode**: `localhost`

## Configuration

The following configuration options are available in `./prosperwooddesigns/config.py`:

_Note: You'll find these options under the ConfigDev and ConfigProd classes_

- General Config
    - _**GENERATE_FAKE_DATA**_
        - Set this to `True` in order for the app to automatically generate fake data for all tables in the db
    - _**DB_CREATE_ADMIN_USER**_
        - Set this to `True` in order for the app to automatically generate a default admin user defined by the following parameters in `prosperwoodesigns.env`:
            - DB_TEST_ADMIN_USERNAME
            - DB_TEST_ADMIN_PASSWORD
            - DB_TEST_ADMIN_FIRSTNAME
            - DB_TEST_ADMIN_LASTNAME
    - _**LOG_TO_STDOUT**_
        - Set this to `True` in order for all logs to be written to stdout _(can be used in conjunction with `LOG_TO_FILE`)_
    - _**LOG_TO_FILE**_
        - Set this to `True` in order for all logs to be written to logfiles _(can be used in conjunction with `LOG_TO_STDOUT`)_
    - _**ADMIN_AUTO_LOGIN**_
        - Set this to `True` in order to automatically be logged in as Admin upon arriving at index page
- SQLAlchemy Config
    - _**SQLALCHEMY_ECHO**_
        - From the [source](https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/): _"If set to True SQLAlchemy will log all the statements issued to stderr which can be useful for debugging."_
- AWS Config
    - _**AWS_DOWNLOAD_IMAGES**_
        - Set this to `True` in order for the app to download all images from the S3 bucket upon initialization. S3 Bucket information is defined by:
            - AWS_PROJECT_BUCKET
            - AWS_PROJECT_BUCKET_IMAGE_DIR

## Developer Information

- Project Owner & Developer
    - Michael Cole
    - mcole042891.prof.dev@gmail.com

# Introduction

This repo provides general scripts to automate data processing for IPA research projects. In particular, we provide modules to:

* Download data using SurveyCTO API
* Clean and transform data
* Push data to Box using Box API
* Push data to AWS S3 Buckets

In order to run this modules in the correct order, this repo provides `.sh` template files (referred to as pipelines) that call the different modules according to projects needs. `.sh` are also simple to schedule in a server machine so that they run periodically.

## Setting up your pipeline

Run `projects_pipelines\template_pipeline\template_pipeline.sh` to run a pipeline for your project. If you need to modify it, create a copy of the `template_pipeline` folder and edit the `.sh` file according to your needs. For example of other pipelines used in the past, you can check pipelines under the `projects_pipelines` folder.

### Setup needed

Surveycto server must be shared with `ipa_box_service_account@poverty-action.org`, and box folders IDS where data will be kept must be shared with `ipa_box_service_account@poverty-action.org`. You must also share box files IDs for other input files.

### Inputs needed to run your pipeline

* server name
* form ID(s)
* list of form fields that have media files (ex: text_audit, audio_audit, etc.). If there are multiple forms, specify fields for each form ID
* Box folder ID of the Box folder where the raw csv of survey responses should be sent
* Box folder ID where media files should be sent
* Box file ID of the SurveyCTO encryption key saved in Box
* Box file ID of xlsform
* start date of data collection
* frequency/time of data downloads

### Set up your ec2 instance

1. Launch ubuntu instance from aws console

2. Log into instance

`ssh -i /path_to_ec2_pem_key.pem ubuntu@your_instance_public_dns`

3. Clone repo

`git clone url_to_data_pipeline_repo`

4. Inside data_pipeline folder, install dependencies in a virtual environment

Install python3-venv [Only once]
`sudo apt-get install python3-venv`

Create virtual env [Only once]
`python3 -m venv venv`

Activate virtual env
`source venv/bin/activate`

Install dependencies
`pip install -r requirements.txt`

<!--
ADD this once task DM-116 https://ipa-grds.atlassian.net/jira/software/c/projects/DM/boards/10/roadmap?selectedIssue=DM-116 is ready

5. Copy surveycto server key to pipeline folder in ec2 instance

`scp -i /path_to_ec2_pem_key.pem /path/to/key/key.pem ubuntu@your_instance_public_dns:~/data_pipeline/projects_pipeline/template_pipeline/.` -->


5. Set up crontab to run pipeline every night, according to user inputs in the form when they signed in to run the pipeline


### How to schedule the pipeline

Setup [cron](https://opensource.com/article/17/11/how-use-cron-linux) to run your `.sh` pipeline as periodically as you want.

For example, run

```
crontab -e

#Write down in the end of the crontab file the following line:
0 0 * * * source venv/bin/activate; \
/home/ubuntu/data_pipeline/projects_pipelines/IPA_COL_iso2_midline/./iso2_midline.sh \
--server yourserver \
--download_wide_csv False \
--download_wide_json True \
--transform_json_to_csv True \
--form_id yourformid \
--start_timestamp 0 \
--username "username@poverty-action.org" \
--password "password_here" \
--box_folder_id 1111111111 \
--columns_with_attachments "text_audit,pre_survey_audio" \
--media_box_folder_id 2222222222222 >> /home/ubuntu/data-pipeline/projects-pipeline/your_project/your_project_pipeline_log.txt
```

The "0 0 * * *" indicates that the script should be run by crontab every night. Check https://crontab.guru/ for examples.

Remember that crontab works with absolute routes for files.

You can check what crontab has run with:
```
tail /var/log/syslog
```

### A note on .sh pipeline files created in windows

If you are creating the `.sh` files on Windows, run the command `dos2unix your_pipeline.sh` to transform them so they can run on Linux machines.

Also remember running `chmod +x pipeline.sh` to be able to run it as an executable.

## Why use a .sh file instead of a python file?

Importantly, you will notice that our pipeline uses the `curl` command to download data. This is preferred over other options that download data using `python`, `stata` or others, given that if data is too big, these programs will run out of memory.

## Encryption

The pipeline pushes unencrypted data to Box and AWS. It is project teams responsibility to later encrypt the files.

For that, we recommend the following step-by-step:

1. Encrypt the empty folder where files will be saved using Boxcryptor.
2. Every day, after files have been pushed to Box and synced to your computer using Box Drive, select those files that are unencrypted and encrypt them using Boxcryptor. Repeat this step however frequently you want, ideally daily. It's important you encrypt the files, not the folder (which should have already been encrypted in step 1)

### Possible extension of pipeline: Automatic encryption

Set up an AWS Lightsail VM to encrypt files once they are pushed to Box. The VM must hence have Box Drive and Boxcryptor installed. You can use Boxcryptor command line (run with bc.cmd) to encrypt the files (use the `encryption --files path_to_file` command to encrypt). The VM could be set up to run every night, get the list of unencrypted files in the given Box Drive folder, and encrypt them.

Setup:

1. Install boxcryptor

Invoke-WebRequest -Uri https://www.boxcryptor.com/l/download-windows -OutFile Boxcryptor.msi

2. Install box drive

Invoke-WebRequest -Uri https://e3.boxcdn.net/box-installers/desktop/releases/win/Box-x64.msi -OutFile Box-x64.msi

3. Log in to both with credentials that have access to data and encryption permissions (probably ipa_box_service_account@poverty-action.org)

4. Create a script that encrypts every file in the folder

5. Schedule the script to run every night

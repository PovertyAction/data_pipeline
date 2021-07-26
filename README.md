# Introduction

This repo provides general scripts to automatize data processing. In particular, we provide modules to:

* Download data using SurveyCTO API
* Cleaning and transforming data
* Push data to Box using Box API
* Push data to AWS S3 Buckets

In order to run this modules in the correct order, this repo also provides `.sh` template files (reffered to as pipelines) that call the different modules according to projects needs. `.sh` are also simple to schedule in a server machine so that they run periodically.

## Setting up your pipeline

Check out `projects_pipelines\template_pipeline\template_pipeline.sh` to start your new pipeline and decide what to include. You can also check other pipelines under the `projects_pipelines` to look for other examples.

### Setup needed

Surveycto server must be shared with `researchsupport@poverty-action.org`, and box folders where data will be kept must be shared with `ipa_box_service_account@poverty-action.org`

### Inputs needed to run your pipeline

* server name
* form(s) name(s)
* surveycto username and password
* destiny where to save files (either box drive path, box folder id, and/or aws bucket)
* column names that have attachments (case we want to download attachments too)
* server key box file id

### How to run periodically

Setup [cron](https://opensource.com/article/17/11/how-use-cron-linux) to run your `.sh` pipeline as periodically as you want.

For example, run

```
crontab -e

#Write down in the end of the crontab file the following line:
0 0 * * * /home/ubuntu/data-pipeline/projects-pipeline/your_project/your_project_pipeline.sh >> /home/ubuntu/data-pipeline/projects-pipeline/your_project/your_project_pipeline_log.txt
```
You can check what has crontab run with:
```
tail /var/log/syslog
```
Remember to use absolute routes

### A note on .sh pipeline files created in windows

After creating `.sh` files in windows, run the command `dos2unix your_pipeline.sh` to transform them so they run on linux machines.

Also remember running `chmod +x pipeline.sh` to be able to run it as an executable.

## A note on encryption

If you are pushing data to Box directly or AWS, the data will not pass through Boxcryptor and hence will not be encrypted. It is research teams responsibility to later encrypt data.

## A note on size of data download

Importantly, you will notice that our pipeline uses the `curl` command to download data. This is preferred over other options that download data using `python`, `stata` or others, given that if data is too big, these programs will run out of memory.




<!-- # Setting up Lightsail VM

An alternative is to set up pipelines that download data directly to boxcryptor folders. For that, you might want to set up a Lightsail VM. More on ## Lightsail section

1. Launch AWS Lightsail VM
2. Install boxcryptor

Invoke-WebRequest -Uri https://www.boxcryptor.com/l/download-windows -OutFile Boxcryptor.msi

3. Install box drive

Invoke-WebRequest -Uri https://e3.boxcdn.net/box-installers/desktop/releases/win/Box-x64.msi -OutFile Box-x64.msi

4. Install python

Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.9.4/python-3.9.4-amd64.exe -OutFile python-3.9.4-amd64.exe

5. Install git

Invoke-WebRequest -Uri https://github.com/git-for-windows/git/releases/download/v2.31.1.windows.1/Git-2.31.1-64-bit.exe -OutFile Git-2.31.1-64-bit.exe

6. Clone this repo

git clone https://github.com/PovertyAction/surveycto_data_download.git

7. Install dependencies (requirements.txt) -->

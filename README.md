# Introduction

This repo provides general scripts to automatize data processing. In particular, we provide modules to:

* Download data using SurveyCTO API
* Cleaning and transforming data
* Push data to Box using Box API
* Push data to AWS S3 Buckets

## Setting up your pipeline

Check out `projects_pipelines` directory for examples.
In particular, `template_pipeline\template_pipeline.sh` has all possibilities inclueded.

### Inputs needed to run your pipeline

*server name
*form(s) name(s)
*column names of files with attachments
*destiny where to save files (either box drive path, box folder id, and/or aws bucket)
*surveycto username and password

If you want to save files in box, you must share the folder with ipa_box_service_account@poverty-action.org

## A note on encryption

If you are pushing data to Box or AWS, the data will not pass through Boxcryptor and hence will not be encrypted. It is research teams responsibility to later encrypt data.

## A not on size of data download

Importantly, you will notice that our pipeline uses the `curl` command to download data. This is preffered over other options that download data using `python`, `stata` or others, given that if data is too big, these programs will run out of memory.

## A note on .sh files created in windows

After creating `.sh` files in windows, run the command `dos2unix your_pipeline.sh` to transform them so they run on linux machines.

Remember running `chmod +x pipeline.sh` to be able to run it as an executable.



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

# Introduction

This repo provides general scripts to automatize data processing. In particular, we provide modules to:

* Download data using SurveyCTO API
* Cleaning and merging data
* Push data to Box using Box API
* Push data to AWS S3 Buckets

## Setting up your pipeline

Check out `projects_pipelines` directory for examples

## A note on encryption

If you are pushing data to Box or AWS, the data will not pass through Boxcryptor and hence will not be encrypted. It is research teams responsibility to later encrypt data.

An alternative is to set up pipelines that download data directly to boxcryptor folders. For that, you might want to set up a Lightsail VM. More on ## Lightsail section

## A not on size of data download

Importantly, you might want to consider the size of files you are downloading from SurveyCTO. If they are too big, you might want to use `curl` to download them rather than doing so from `python` scripts.

## A note on .sh files created in windows

After creating `.sh` files in windows, run the command `dos2unix your_pipeline.sh` to transform them so they run on linux machines.




<!-- # Setting up Lightsail VM

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

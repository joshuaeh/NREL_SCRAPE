# NRELASI

The EKO ASI-16 camera at NREL takes images every minute but only saves the image every 10 minutes. Higher frequency images may assist studies using the sky camera. Here we enable scraping and saving the image each minute.

Images are published by NREL at the url: `https://midcdmz.nrel.gov/data/rt/srrlasi.jpg`

## docker

to build the image:

```bash
docker build --tag <tag> .
```

to run the image with a volume:

```bash

```

for example:

```bash
docker build --tag simple .
docker run -v "C:\Users\jhamm\OneDrive - The University of Texas at Austin\business\UTexas\projects\NRELASI\data:/data/" simple
```

# Snow Profile Avalance Hazard Prediction

## Datasets

Download the SAIS snow profile datasets from here: https://www.sais.gov.uk/snow-profiles

Copy the CSV to `./profiles`

Format the CSV (inside VIM only) using the following search/replace

Remove commas within quotes

%s/".\{-}"/\=substitute(submatch(0), ',', '' , 'g')/g

Remove = signs

%s/=//g

## Usage

Run `ruby csv_formatter.rb` to convert CSV to Neral Network format.

Run `python train_cnn.py` to fit the model to the downloaded dataset.

## Docker

```bash
docker build -t snow-profile-nn .
docker run snow-profile-nn python train_nn.py
```

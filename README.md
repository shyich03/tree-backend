# TreeCertificates
## Installation:

You nee to download AVITABILE map from 
http://lucid.wur.nl/storage/downloads/high-carbon-ecosystems/Avitabile_AGB_Map.zip
and put Avitabile_AGB_Map.tif file to into src folder.

pip install requirement.txt

download gdal
https://github.com/domlysz/BlenderGIS/wiki/How-to-install-GDAL

create a key folder under the project root folder<br />
download your google service account json file<br /><br />
create a util.py file under the server folder<br />
add variables path and path_key, representing path to CertificateInterface.py file and path to the service account json file<br /><br />
python manage.py makemigrations<br />
python manage.py migrate<br />
python manage.py createsuperuser<br />
python manage.py runserver <br /><br />

create to Alan Marko for certicates and earth engine files integration
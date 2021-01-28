# TreeCertificates
A significant problem with forest conservation and tree planting efforts is that there is currently no way to guarantee that a conserved forest or tree planted
would continue to be in existence at some future time. Yet, credit is given at the time of tree planting or when a forest conservation action is taken. 
This sets up a perverse incentive for a tree planter to make no effort to conserve trees after payment has been received.

This project implements interface that creates blockchain-based certificates linked to the existence of
trees, so that, if a tree is damaged or cut down, the certificate is declared void. Specifically,
it links satellite data to per-tree certificates on a blockchain. If a satellite image discovers that a tree is no longer present, then this would be
certified by an independent third-party, such as WCMC and placed on the blockchain, as well. This could trigger either penalty payments or a reduction in the number of carbon
credits available to the tree planter.

The application in its current form allows the user to specify the area of a forest(e.g. Gola Rainforest National Park). The application then downloads data from Hansen dataset
decribing the state of the forest, calculates the amount of carbon stored inside of the area and also checks whether there are no other certificates already in this area.
If not, the application creates new certificate for the forest storing both area information and the amount of carbon. It is then possible to modify the certificate or recalculate
it in case that the amount of carbon stored has changed(for example because some trees were cut).


You nee to download AVITABILE map from 
*http://lucid.wur.nl/storage/downloads/high-carbon-ecosystems/Avitabile_AGB_Map.zip
and put Avitabile_AGB_Map.tif file to into src folder.

pip install requirement.txt

change path to treeinterface in server/app/api/view.py

download gdal
https://github.com/domlysz/BlenderGIS/wiki/How-to-install-GDAL

create a key folder under the project root folder
download your google service account json file
create a util.py file under the server folder
add variables path and path_key, representing path to CertificateInterface.py file and path to the service account json file
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 

create to Alan Marko for certicates and earth engine files integration
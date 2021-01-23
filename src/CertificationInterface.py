"""
CertificationInterface.py

CertificationInterface.py implements core methods for log-in to Google Earth Engine, receiving user input,
and calculating requested properties of selected forest such as the total amount of carbon stored and

In order to log-in to the Google Earth Engine it is necessary to create an account at console.developers.google and change client_secrets.json file

In order to see an example usage, please see CertificationDemo.py
"""

from google import resumable_media
import datetime
import ee
import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from PIL import Image
from osgeo import gdal
import numpy as np
import datetime

import json
import time
import base64
from algosdk import algod
from algosdk import mnemonic
from algosdk import transaction
import hashlib
import Algorand
import Editor
import sys
from time import sleep
import ProgressBar
from DataReader import DataReader
from CertificateMaker import CertificateMaker
from CertificateIndexer import CertificateIndexer
from CertificateIndexer import SavedHash
import pickle
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.cloud import storage

from constants import cell_size
from  constants import real_cell_size


class CertificationInterface:
    def __init__(self): 
        # print("Please log in to your google earth engine account.")
        # ee.Authenticate()
        # ee.Initialize()
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/shyic/Projects/TreeCertificates/key/woven-grail-248317-4b9659d1c442.json"

        service_account = 'trees-385@woven-grail-248317.iam.gserviceaccount.com'
        credentials = ee.ServiceAccountCredentials(service_account, '../key/woven-grail-248317-4b9659d1c442.json')
        ee.Initialize(credentials)
        self.mapa=ee.Image("UMD/hansen/global_forest_change_2019_v1_7").select(['treecover2000'])
        self.loss=ee.Image("UMD/hansen/global_forest_change_2019_v1_7").select(['loss'])
        
        self.storage_client = storage.Client()
        self.bucket = self.storage_client.get_bucket('earth_engine_forest')
        

    def downloadFromDrive(self, file_name):
        print("start download from bucket")

        blob = self.bucket.get_blob(file_name + '.tif')
        print("1")
        uri = "files/"+file_name + '.tif'
        print("2", blob, uri)
        if not os.path.exists("files/"):
            os.mkdir('files/')
            print("folder created", )
        try:
            blob.download_to_filename(uri)
        except FileNotFoundError  as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print (message, ex.filename)
        print("4")
        self.bucket.delete_blob(blob.name)
        options_list = [
            '-ot Byte',
            '-of JPEG',
            '-b 1',
            '-scale'
        ]
        print("45")
        options_string = " ".join(options_list)
        gdal.Translate("files/"+file_name + '.png',
                       "files/"+file_name + '.tif',
                       options=options_string)

        # im = Image.open("files/"+file_name + '.png')
        # im.show()
        print("fin download from bucket")

    def uploadToDrive(self,population,File_Name,x1,y1,x2,y2):
        geometry = ee.Geometry.Rectangle( [x1,y1,x2,y2])
        print(File_Name)
        task_config = {
            'region': geometry.coordinates().getInfo(),
            'scale': 50,
            'description': File_Name,
            'bucket': 'earth_engine_forest',
        }

        task = ee.batch.Export.image.toCloudStorage(population, **task_config)
        task.start()
        task.status()
        print(task, task.status())
        counter=0
        pb=ProgressBar.ProgressBar()
        while task.status()['state'] in ['READY', 'RUNNING']:
            print(task.status())
            pb.printProgress(min(counter,66),66)
            time.sleep(1)
            print(task, task.status())
            counter+=1
            print(task.status())
        pb.printProgress(100,100)
        print("finish download to bucket")
        return


    def readSelectedArea(self,file_name,x1,y1,x2,y2):
        print()
        print("Please mark your forest.", file_name)
        e=Editor.Editor(file_name)

        im = Image.open("files/"+file_name+"bitmask" + '.png')
        imarray = np.array(im)
        height=imarray.shape[0]
        width=imarray.shape[1]
        #print(height)
        #print(width)
        bitmask=np.zeros((height//cell_size,width//cell_size),np.int)
        print("Reading bitmask:")
        pb=ProgressBar.ProgressBar()
        for i in range(5,bitmask.shape[0]*cell_size,cell_size):
            for j in range(5,bitmask.shape[1]*cell_size,cell_size):
                y=i//cell_size
                x=j//cell_size
                if (imarray[i][j] == [255,0,0]).all():
                    bitmask[y][x]=1
                elif (imarray[i][j] == [255,255,0]).all():
                    bitmask[y][x]=2
                elif (imarray[i][j] == [0,128,0]).all():
                    bitmask[y][x]=3
                else:
                    bitmask[y][x]=0
            pb.printProgress(i,height//cell_size)
        pb.printProgress(100,100)
        print()
        for i in range(0, bitmask.shape[0]):
            for j in range(0, bitmask.shape[1]):
                if bitmask[i][j] == 1:
                    print("R", end=" ")
                elif bitmask[i][j] == 2:
                    print("Y", end=" ")
                elif bitmask[i][j] == 3:
                    print("G", end=" ")
                else:
                    print(".", end=" ")
            print()

        total_carbon=self.calculateCarbon(file_name,bitmask,x1,y1,x2,y2,width, height)
        return (bitmask,total_carbon,x1,y1,datetime.datetime.now())

    def calculateCarbon(self,file_name,bitmask,x1,y1,x2,y2,width,height):
        imLoss = Image.open("files/"+file_name + "loss" + '.png')
        imarrayLoss = np.array(imLoss)
        total_loss = 0
        total_carbon = 0
        dr = DataReader("Avitabile_AGB_Map")
        print("Calculating the total amount of carbon:")
        pb = ProgressBar.ProgressBar()
        for i in range(0, bitmask.shape[0]):
            for j in range(0, bitmask.shape[1]):
                if not bitmask[i][j] > 0:
                    continue
                lossSum = 0
                cellCarbon = 0
                for k in range(0, cell_size):
                    for l in range(0, cell_size):
                        y = i * cell_size + k
                        x = j * cell_size + l
                        lossSum += (imarrayLoss[y][x] // 255)
                        longtitude = (x2 - x1) * (x / width) + x1
                        latitude = (y2 - y1) * (y / height) + y1

                        carbonValue = dr.getValue(latitude, longtitude) * (1 - (imarrayLoss[y][x] // 255))

                        if carbonValue < 0:
                            carbonValue = 0

                        cellCarbon += carbonValue

                cellCarbon /= cell_size * cell_size

                aliveCells = cell_size * cell_size - lossSum
                total_loss += lossSum
                total_carbon += cellCarbon
            pb.printProgress(i, bitmask.shape[0])
        pb.printProgress(100, 100)
        total_carbon *= 900
        return total_carbon

    def tidyCoordinate(self,x):
        count=int(round(x/real_cell_size))
        res=count*real_cell_size
        return res

    def getArea(self, x1, x2, y1, y2):
        print( x1, x2, y1, y2)
        # print("Please enter the bounding rectangle of your forest.")
        # print("Gola Rainforest National Park has coordinates (7.997,-11.535,7.2,-10.387).")
        self.y1 = y1 #float(input("Top-Left latitude:"))
        self.x1 = x1 #float(input("Top-Left longtitude:"))
        self.y2 = y2 #float(input("Bottom-Right latitude:"))
        self.x2 = x2 #float(input("Bottom-Right longtitude:"))

        self.y1= self.tidyCoordinate(self.y1)
        self.x1 = self.tidyCoordinate(self.x1)
        self.y2 = self.tidyCoordinate(self.y2)
        self.x2 = self.tidyCoordinate(self.x2)

        print()
        self.file_name="img"+str(self.y1)+str(self.x1)
        if not os.path.exists("files/"+self.file_name + '.png'):
            print("Downloading tree cover data to bucket:")
            self.uploadToDrive(self.mapa,self.file_name,self.x1,self.y1,self.x2,self.y2)
            print("download cover from bucket")
            self.downloadFromDrive(self.file_name)
        else:
            print("already exist")
        if not os.path.exists("files/"+self.file_name + 'loss.png'):
            print("Downloading forest loss data:")
            self.uploadToDrive(self.loss,self.file_name+"loss",self.x1,self.y1,self.x2,self.y2)
            self.downloadFromDrive(self.file_name+"loss")
        else:
            print("loss already exist")

        #input("Please select area to work with")
        # print(self.readSelectedArea(self.file_name,self.x1,self.y1,self.x2,self.y2))
        return self.file_name




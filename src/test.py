from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from CertificationInterface import CertificationInterface

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

def main():
    # 
    c = CertificationInterface()
    c.downloadFromDrive('img4.997964.99796')

if __name__ == '__main__':
    main()
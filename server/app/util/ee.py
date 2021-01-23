import ee


service_account = ' trees-385@woven-grail-248317.iam.gserviceaccount.com'
credentials = ee.ServiceAccountCredentials(service_account, '../../../key/woven-grail-248317-4b9659d1c442.json')
ee.Initialize(credentials)
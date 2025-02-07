from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import math

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']

class VIEWIDError(Exception):pass

def get_credentials(KEY_FILE_LOCATION):
    """Initializes an Analytics Reporting API V4 service object.
    Returns:
      An authorized Analytics Reporting API V4 service object.
    """
    # get token
    credentials = ServiceAccountCredentials.from_json_keyfile_name(KEY_FILE_LOCATION, SCOPES)

    # build the service object.
    analytics = build('analyticsreporting', 'v4', credentials=credentials)
    return analytics

def report_prettifier(report,is_df = True):

	columnHeader = report.get('columnHeader', {})
	data = {}
	dimensions = []
	metrics = []

	for dimension in columnHeader.get('dimensions',[]):
	    name = dimension.split(':')[1]
	    dimensions.append(name)
	    data[name] = []
	for metric in columnHeader['metricHeader']['metricHeaderEntries']:
	    name = metric['name'].split(':')[1]
	    metrics.append(name)
	    data[name] = []

	# dimensions may not be, they are not required in request
	if dimensions:
	    for row in report['data']['rows']:
	        for i,value in enumerate(row['dimensions']):
	            data[dimensions[i]].append(value)
	        for i,value in enumerate(row['metrics'][0]['values']):
	            data[metrics[i]].append(value)
	else:
	    for row in report['data']['rows']:
	        for i,value in enumerate(row['metrics'][0]['values']):
	            data[metrics[i]].append(value)
	if is_df:
		return pd.DataFrame().from_dict(data)
	else:
		return data

def responce_to_list_reports(body,VIEW_ID,anal_cred,size=10000,list_reports=None):
    """
    Returns a list of data objects from responce
    or appends to list you have set
    """
    if  not list_reports:
        list_reports=[]
    if VIEW_ID is None:
    	raise VIEWIDError('in functioon {0}'.format(whoami()))
    page_token=0
    body['reportRequests'][0]['pageSize']=size
    body['reportRequests'][0]['pageToken']=str(page_token)
    
    responce=anal_cred.reports().batchGet(body=body).execute()
    report=responce['reports'][0]

    num_pages = math.ceil(report['data']['rowCount'] / size)
    list_reports.append(report_prettifier(report))

    for i in range(1,num_pages):
        body['reportRequests'][0]['pageToken']=str(i*size)
        responce=anal_cred.reports().batchGet(body=body).execute()
        report=responce['reports'][0]
        list_reports.append(report_prettifier(report))
    return list_reports

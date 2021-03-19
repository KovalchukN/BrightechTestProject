from googleapiclient import discovery
import httplib2
from settings import CREDENTIALS_FILE, SPREADSHEET_ID
from oauth2client.service_account import ServiceAccountCredentials


credentials = ServiceAccountCredentials.from_json_keyfile_name(
	CREDENTIALS_FILE,
	['https://www.googleapis.com/auth/spreadsheets',
	 'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
SERVISE = discovery.build('sheets', 'v4', http = httpAuth)

def uload_to_spreadsheet(start_sheet: str, cars, end_sheet = 1):
	col = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	ROW = len(cars)

	if end_sheet:
		end_sheet = str(col[len(cars[0])]+str(ROW))
	else:
		end_sheet = "H5"

	values = SERVISE.spreadsheets().values().batchUpdate(
		spreadsheetId=SPREADSHEET_ID,
		body={
			"valueInputOption": "USER_ENTERED",
			"data":[
				{
					"range": start_sheet +"1:"+ end_sheet,
				 	"majorDimension": "ROWS",
				 	"values": cars
				}
				]
		}).execute()







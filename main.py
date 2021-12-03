from datetime import datetime
from pywebio.output import *
from pywebio import *
from pywebio.input import *
import sweetviz as sv
import pandas as pd
import json
import file_manipulation
import Data_database

def saveFiles(data):
    # Puts data in the /database folder
    data["date"] = datetime.now().strftime("%m_%d_%y")
    filename = f'database/{data["uuid"]}_{data["date"]}.json'
    with open(filename, 'w') as fp:
        json.dump(data, fp, indent=4)
    #df = pd.DataFrame.from_dict(data)

    # Unpacking data
    data2=data.values()
    data3=[]
    for value in data2:
        print(value)
        data3.append(value)
    name, date, uuid, serial_number, firmware_version, BT_reads, fob_reads, jumper, failure, *notes = data3
    print(notes[0])

    # Log in database
    Data_database.log_data(name, date, uuid, serial_number, firmware_version, BT_reads, fob_reads, jumper, failure, notes[0])

def showAnalytics():
    # Finds all .json files in /database folder, returns them as df
    df = file_manipulation.mergeJsonToDf('database')

    # Builds a report from df
    my_report = sv.analyze(df)

    #print('here is the error')
    my_report.show_html()  # Default arguments will generate to "SWEETVIZ_REPORT.html"
    # File Output
    put_html('SWEETVIZ_REPORT.html')

def main():
    # For automatic reconnection
    session.run_js('WebIO._state.CurrentSession.on_session_close(()=>{setTimeout(()=>location.reload(), 4000})')

    # Widgets are set here
    data = {'submit': False}

    # Put a label on top of window
    put_text("For help visit www.helpmeout.com")

    # Create a info dictionary that will be empty until you click something
    info = input_group('Add data',[
        input("Approved by:", placeholder='Your name', name='name'),
        input("UUID:", placeholder='4-digits', name='uuid'),
        input("Serial Number:", placeholder='6-digits', name='serial_number'),
        input("Firmware Version:", placeholder='From read', name='firmware_version'),
        input("BT reads :", placeholder='100', name='BT_reads'),
        input("Fob reads:", placeholder='100', name='fob_reads'),
    ])

    # Create a info dictionary that will be empty until you click something
    info2 = input_group('Add data:', [
        radio("Jumper on?", options=['Yes', 'No'], name= 'jumper'),
        radio("Test result:", options=['Locked nfc', 'No power', 'No fob read', 'Looped buzzer', 'No bt', 'All good'], name= "failure"),
        textarea('notes', rows=3, placeholder='Anything weird?', name='notes'),
        actions('', [
            {'label': 'Save', 'value': 'save'},
        ], name='buttons'),
    ])

    # Create a info dictionary that will be empty until you click something
    info3 = input_group('If you want to check the database, else refresh to re-test', [
        actions('', [
            {'label': 'Show database', 'value': 'confirm'},
        ], name='buttons'),
    ])

    # Merge both dictionaries
    infoAll = {**info, **info2}
    print(infoAll)

    # Button selection logic
    if info2['buttons'] == 'save':
        saveFiles(infoAll)
        #print (f'THIS:{info}')
        #THIS:{'buttons': 'save'}

    if info3['buttons'] == 'confirm':
        showAnalytics()
    start_server(main, port=8986)

if __name__ == '__main__':
    start_server(main, port=8986) #http://localhost:8986/

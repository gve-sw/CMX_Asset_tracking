# Asset_tracking_POV
This prototype is a mockup interface to CMX that can take in the notifications data using CMX REST APIs to locate assets by the mac address on a floor map, The prototype is built using a python Flask server and CISCO UI toolkit and cisco NeXt UI toolkit
the GUI allows the user to orgnise assets into groups and allows the user to reqest the location of an asset or group of assets

## Usage:
Clone the repo :
```
$ git clone https://github.com/Abdellbar/Asset_tracking_POV
```

Install dependencies :
```
$ pip install flask
$ pip install WTForms
```
update the mac address of the devices to be tracked, in the GroupTag_Form,Select_Form classes in server.py and js/nodes.js files 

Launch the server by issueing 
```
$ python server.py
```

In a web browser open :
http://127.0.0.1:5000/start

## Integrate to CMX:

Add the url 'http://127.0.0.1:5000/webhook' into CMX to post the location data directly to the app


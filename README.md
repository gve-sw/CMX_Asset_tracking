# Asset_tracking_POV
This is a prototype for asset tracking using CMX

## Usage:
Clone the repo :
```
$ git clone hhttps://github.com/Abdellbar/Asset_tracking_POV
```

Install dependencies :
```
$ pip install flask
$ pip install WTForms
```

Lunch the server by issueing 
```
$ python server.py
```

In a web browser open :
http://127.0.0.1:5000/start

## Integrate to CMX:

Add the url 'http://127.0.0.1:5000/webhook' into CMX to post the location data directly to the app


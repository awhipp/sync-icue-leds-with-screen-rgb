# iCUE SDK Application

Changes all iCUE devices based on main screen's average pixel color. Color updates at roughly 24fps.

## Installation

* Clone this repository
* Install Python 3.7+
* Install dependencies `pip install -r requirements.txt`
* Enable SDK mode on iCUE application
* Run the python application `python app.py`
* To run the application in the background: `pythonw app.py`
* Execute this application on startup through a bash script or otherwise to have it run. This application should take ownership of the iCUE LEDs as long as it is running before any other applications take ownership.

## Testing

Visit [this color changing site](https://www.webfx.com/web-design/random-color-picker) once runnning to view the changes live.
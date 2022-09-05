# iCUE SDK Application

Changes all iCUE devices based on main screen's average pixel color. Color updates at roughly 24fps.

## Installation

* Clone this repository
* Install Python 3.7+
* Install dependencies `pip install -r requirements.txt`
* Enable SDK mode on iCUE application
* Run the python application `python app.py`
* To run the application in the background: `pythonw app.py`
* Run either of the above at startup

## Parameters

Since most iCUE systems are peripherals under the screen, this app parameterizes the percentage of the screen used for color determination:
`pythonw app.py 40` means 40% of the bottom half of the screen's real estate will be used for color averaging

## Testing

Visit [this color changing site](https://www.webfx.com/web-design/random-color-picker) once runnning to view the changes live.
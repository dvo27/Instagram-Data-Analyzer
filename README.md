# Instagram-Data-Analyzer
Get an insight into your Instagram data with this app!

## Needed Installations
### Downloading Instagram Data:

Head over to your Instagram account and follow the following steps:

- Click the hamburger menu in the top left, then click Your Activity
- Click Download your information at the bottom, and press request a download
- Select complete copy and enter the email where you want to receive the data
- **For the format option, select JSON**
- You can select the date range of your own preference, for default settings, select "All Time"
- Enter your Instagram account password and click Request download.
- You'll soon receive an email titled Your Instagram Data with a link to your data. Click Download data and follow the instructions to finish downloading your information.
- Extract the data from the zip file to a known location as you will need to know the file location to correctly run the project


### Installing Needed Python Libraries:

Use the [pip installer](https://pip.pypa.io/en/stable/getting-started/) in the terminal to install all the needed libraries:
```
pip install pandas
pip install seaborn
pip install matplotlib
```

## Features
```
Please choose an option below!:
[1] : Get DMs With Specific User Data
[2] : Get Follow Data
[Q] : Quit Program
-------------------------------------
```

### DMs Menu

```
Welcome To The Message Data Section!
------------------------------------
To return to the main menu please type "return"

Please enter the path to a file in /messages/inbox/ ending in .json: 
```

### Follow Up
```
Welcome To The Follow Data Section!
------------------------------------

Please choose an option below!:
[1] : Get Following Data
[2] : Check Who Isn't Following You Back

[return] : Return to main menu
-------------------------------------
```

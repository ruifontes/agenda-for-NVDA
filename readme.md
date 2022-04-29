#Agenda

<br>
## Informations
* Authors: Abel Passos, Ângelo Abrantes and Rui Fontes
* Updated: April 16, 2022
* Download [stable version][1]
* Compatibility: NVDA version 2019.3 and later

<br>
## Presentation
This add-on allows you to write down appointments and activities with or without alarms.
You can use two different agendas.
To switch between them, go to the NVDA menu, Preferences, Settings, agenda section and choose from the combobox the agenda you want to use.
If the second line is empty, use the \"Select or add a directory\" button to create a second agenda.
If you use this button with a path selected, the agenda 	will be moved to the new path, if there is no agenda in it. If it does, only the path will be changed, and both agendas will be preserved, with the new path being used.
At NVDA startup you will be reminded of the appointments for the current day and the next. This reminder can be a window with a list of all appointments or a reminder with a dialog and an audible alarm for appointments with a set alarm.
This option can be configured in the add-on's settings.

<br>
## Command
The command to invoke the add-on is NVDA+F4.
You can change it in the Input gestures dialog, in the agenda section.

<br>
## How it works:
* When you open the program, the current day's appointments will be displayed.
* In the main window there are the fields to change the date, the appointments for the selected date, and some program control buttons that will be described later.
The date fields can be changed using the vertical arrows or by typing the desired value. When changing the date, the day's appointments will be automatically displayed.


### Hotkeys for the main window:


* Alt + 1-9: Advances the number of days for the value pressed;
* Alt+0: Returns to the current date;
* Alt+left arrow: Goes back one day in the date;
* Alt+right arrow: Advance one day in the date;
* Alt+Up Arrow: Advance one week;
* Alt+Down arrow: Goes back one week;
* Alt+PageUp: Advance one month;
* Alt+PageDown: Goes back one month;
* Enter: If an appointment is selected, it opens the editing window. Otherwise, it opens the window for creating a new appointment;
* Delete: Deletes the selected record. Same function as the Remove button;
* Control+f: Opens the "Search" window. Equal to activate the "Search" button.

### Functions of the buttons in the main window and their respective accelerator keys:
* Add (Alt+A): Opens a window for registering appointments on the selected date;
* Edit (Alt+E): Opens a window for editing the selected appointment;
* Remove (Alt+R): Deletes the selected appointment;
* Search (Alt+S): Opens a window for searching for information in the agenda
* exit (Alt+S): Closes the window.

<br>
### The adding and editing functions are quite similar, and for this reason the window that will be described serves both functions.
The main difference is that in order to edit, you need to have previously selected an appointment to be changed.
Also, in the Edit function, the selected appointment data is displayed in the window for modification. In the Add option, the window opens with the selected date and the other fields blank

<br>
### Add and Edit window fields
* day/month/year: date fields that can be changed with the vertical arrows or by typing the desired value
* hour/minutes: time fields that can be changed with the vertical arrows or by typing the desired value
* Description: field to fill in the information about the commitment ;
* Alarms: check boxes that should be checked as needed. By default, when any alarm is selected in advance of the appointment date and time, the exact time alarm is automatically activated
* OK button (Alt+O): enters the appointment information into the calendar
* Cancel button (Alt+C): does not save the information filled in this window
* The Add/Edit window has the shortcut keystroke Ctrl+Enter to save the filled in information. This is equivalent to the function of the OK button

<br>
### Search window fields
* Search type: you must select from the following options:
<br>
	* text search: an edit field will open for you to type what you want to search for. It is not necessary to type the entire phrase, the search can be done with parts of words;
	* Next 7 days: displays the appointments for the next 7 days, not including the current day;
	* Next 30 days: displays the appointments for the next 30 days, not including the current day;
	* Date range: displays the start and end date fields for searching;
<br>
* Search button (Alt+S): Executes the selected search and returns the information found;
* Add button (Alt+A): The same add function as in the main window. The difference is that if you have selected an appointment, the add window will be on the date of the selected appointment. If no appointment is selected, it displays the window on the current date;
* Edit button (Alt+E): The same edit function as in the main window. Needs an appointment to be selected;
* Remove button (Alt+R): Remove the selected appointment;
* Remove all (Alt+L): Deletes all displayed appointments;
* Cancel button (Alt+C): closes the search window and returns to the main window.


# Electronic Intern

An electronic intern for [PhillyASAP](http://phillyasap.org/) using Twilio's voice API. A Work in progress, more details soon!  

Imagine an electronic intern that has a computer. In this case, the intern's computer is a Flask app on Heroku. The intern makes a REST API request to the computer for each phone call that he or she wants to make.  

Yes, I know it doesn't make sense that the computer has its own computer but let's roll with it.
## Installation

### Setup your environment

1. Copy the `.setenv.template` file to `.setenv`.
2. Fill in the values provided:
  * `INTERN_ACCT`: your Twilio AccountSID
  * `INTERN_TOKEN`: your Twilio Token
  * `INTERN_FROM`: The phone number your calls will come from without delimiters
  * `PHILLYASAP_FORWARD_NO`: PhillyASAP's phone number to forward calls to from within the app http:// [your Heroku app name].herokuapp.com/intro
  * `INTERN_URL`: The URL that the server-side app is running from, for example, 
 
### Install the requirements

Make sure you have Python, and pip installed.

1. Install the Python requirements:  
    `pip install -r requirements.txt`. (You'll probably want to do this in a [virtualenv](http://www.dabapps.com/blog/introduction-to-pip-and-virtualenv-python))

### Run the intern's computer locally
1. Do this:  `python run.py`
2. Set `INTERN_URL` to `http://localhost:8000`
3. You're ready to run the intern

### Intern: go!

Start the intern with:  
  `python run.py [numbers_to_call.csv]`  

Your CSV file should have the phone numbers to call. The intern doesn't need headers!

### Install the intern's computer on Heroku

1. Create a new app on Heroku
2. Push the code to Heroku:  
`git push heroku master`
3. Set the `PHILLYASAP_FORWARD_NO` to Heroku with:  
`heroku config:set PHILLYASAP_FORWARD_NO`
3. Try http:// [your Heroku app name].herokuapp.com/intro and confirm that you get XML back
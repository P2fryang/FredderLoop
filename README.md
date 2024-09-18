Building:

Every push to the main branch will trigger a Github Action that rebuilds the discord bot on that server


Architecture Proposal:

schedule python scripts to run periodically with crontab -e on ubuntu server

(github stores the crontab file that schedules the scripts and the various scripts to run)
(setup ubuntu server to listen to github actions to update code and run crontabs)
(set up google service account to create and manage forms so that users cannot edit / view them easily)

createForm.py
runs at the beginning of every month
creates a google form with a sharable link in a specified folder
everyone with the link can edit the google form
enable something so cannot submit responses to google form yet (google forms API currently doesn't support this)
boot up discord bot to share link for form in letter loop channel

collectResponses.py
runs 3 weeks after form is created, monthly
changes permission so that form is not editable
allows responses to google form
toggle setting to allow users to edit their responses after submitting
boot up discord bot to notify channel to submit responses

shareResponses.py
runs 4 weeks after form is created, monthly
several options here
creates a google doc with all the responses
creates and hosts a website with all the responses
doesn’t do anything really just share the google form response link
have to make sure pictures are nicely displayed
would be nice to be able to comment and sort responses by question / person
boot up discord bot to notify responses are available

(optional)
reminders.py
runs a day before shareResponses run
boot up discord bot to remind people who haven’t submitted
this means bot will have to maintain a set of people who are in letterloop and a set of people who have submitted the form
this could mean maybe give bot access to user and roles in the server
this could mean have a field in form to specify discord username or email

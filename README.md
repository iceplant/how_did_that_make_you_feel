## Django Commands ##


`python3 manage.py makemigrations`
`python3 manage.py migrate`
`python3 manage.py runserver`


## References

1. setting up django API + react crud app https://www.geeksforgeeks.org/integrating-django-with-reactjs-using-django-rest-framework/
2. Create-react-app not generating template => delete all instances of create-react-app EVERYWHERE on machine and retry. Will require a bash global search
3. css not importing? Try adding .module.css to filename. 

top emotions: anger/annoyance, sadness, optimism, gratitude, joy
don't make things red and green

check csrf stuff in settings.py         'rest_framework.authentication.BasicAuthentication', vs session auth in REST_FRAMEWORK

remove CORS allow all origins before going to prod!!!

CSRF issue: 
1. check whether you're using localhost or 127.0.0.1 for everything
2. check whether you're using HTTP or HTTPS for everything
3. check that the cookies are getting fetching from the cache on each new request. There doesn't seem to be a way to watch for cookie changes, so you just need to fetch them each time. 
4. try in firefox? idk if that actually helped
# Rekognition workflow
1. API -> admin perms
2. Starts workflow with specific payload
3. Starts rekognition
4. Waits for the analysis
5. Sends results to lambda in order to compare
6. Receives response from lambda
7. Sends response back to the API

## Admin perms
1. User receives JWT with role
2. When the login POST request is made, the server also sends the admin dashboard

2. a. If the user is not an admin then the server sends the normal application

This means that the pages are served by django since accessing S3 to do it would increase the overhead
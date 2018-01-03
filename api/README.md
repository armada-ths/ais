The API app is responsible for providing Armada mobile applications with access to information from and to the server.

It has no models itself, however it does have serializers for models of objects that the API can work with.

An example of the usage of this app is our matching:
- At first the mobile application creats a GET request to ais.armada.nu/api/questions and receives all dynamic data associated with the exhibitor questions.
- Then, after the user provided their input, a PUT request is sent to the same ais.armada.nu/api/questions with user's answer data. This also starts the matching process on the server.
- Finally the application polls a GET request to ais.armada.nu/api/results until it receives an answer, which it then displays as matching result to the user.

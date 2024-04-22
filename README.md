# URL-Container
To quick start with docker:

   1. Clone this repository:
       ```bash
      git clone https://github.com/karina-kavaleuskaya/TestProject.git
      ```

   

Without docker:
  1. Create database with name **test**
  2. Go to the project folder
       ```bash
        cd testproject
        ```
  3. Apply migrations
      ```bash
       python manage.py makemigrations
       python manage.py migrate
      ```
  4. Run the app
      ```bash
      python manage.py runserver
      ```
     

You can test this app with postman requests collection (it is in **_/testproject_** folder)

# SchoolsApi-Django-
* This project creates simple backend restful apis
    * CRUD endpoints are created for courses, administrators, teachers and students
    * GET /api/schools/:schoolId:/stats returns the following:
        ```
        {
            id: <schoolId>,
            courses: <# of courses>,
            admins: <# of admins>,
            teachers: <# of teachers>,
            students: <# of students>
        }
        ```
    * POST /api/transfer moves a student from one class to another
        ```
        # Request body
        {
            studentId: <studentId>,
            fromCourseId: <current course ID>,
            toCourseId: <target course ID>
        }
        ```

* There are five models: administrators, courses, schools, teachers and students
    * administrators, courses, teachers and students are related to 1 school
    * A course can have 0 to 1 teachers and 0 to many students

* To start this site, run "docker-compose up -d"
* Then run "docker exec -it schoolsapi-django--web-1 /bin/bash" to enter the container
* Then update the database by making migrations
* Executes following commands in the container as needed:
    ```
    # To make update changes to database (make migrations)
    python project/manage.py makemigrations
    python project/manage.py migrate

    # To create superuser
    python project/manage.py createsuperuser

    # To exit the container
    exit
    ```
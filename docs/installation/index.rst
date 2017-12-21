Installation Guide
==================

1. Install Python (version 3.4 or higher)

2. Install Flask

We used Flask framework for web developement.

.. code-block:: console

   pip3 install -U flask

3. Install Psycopg2

Our project needs Psycopg2 as a PostgreSQL adapter.

.. code-block:: console

   pip3 install -U psycopg2

4. Install flask_login

We used flask-login for login/session management.

.. code-block:: console

   pip3 install flask-login

5. Install passlib

We used passlib for hashing users' passwords.

.. code-block:: console

   pip3 install passlib

6. After installing requirements, clone repository to your preffered location.

7. Use vagrant in order to use database system and wait until it finishes.

.. code-block:: console

   vagrant up

8. Run the server file in order to use in localhost

.. code-block:: console

   python server.py


As long as "server.py" is running, you can connect to "localhost:5000" to view our site.
# Set up

1. Clone the repo:
    ```shell
    git clone https://github.com/phaishuk/inforce_test_task.git
    ```
2. Navigate to the project directory (don't forget to check the directory where you clone the project):

    ```shell
    cd inforce_test_task
    ```

3. Create a virtual environment:
    ```shell
    python -m venv venv
    ```

4. Activate the virtual environment:

   - For Windows:
   ```shell
   venv\Scripts\activate
   ```
   - For MacOS, Unix, Linux:
   ```shell
   source venv/bin/activate
   ```
   
5. Install the required dependencies:
   ```shell
   pip install -r requirements.txt
   ```
6. In this project sensitive data moved to `.env.sample` file. \
   Please rename it `.env.sample -> .env` before running server.
   It is necessary for docker and server start!

7. For this app you need to have docker installed. Run command to start infrastructure stuff available.
   ```shell
   docker-compose up --build
   ```


# Short description

The main idea in this task that we have two types of employees that are 
have an opportunity to vote or to upload their menu. After voting admin can close voting.

All the documentation described endpoint `api/doc/swagger/`.

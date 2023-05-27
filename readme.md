# Sports Management Backend

This is the backend component of a sports management website. It is built using FastAPI, SQLAlchemy, MySQL, and PyMySQL.

## Features

- User management: Create and manage user accounts.
- Student management: Manage student information.
- Game management: Create and manage different games.
- Organizer management: Manage organizers and their information.
- Tournament management: Create and manage tournaments for different games.
- Team management: Create and manage teams for tournaments.
- Registration: Allow teams to register for tournaments.
- Match management: Manage matches between teams.
- Score management: Record and manage scores for matches.
- Knockout management: Manage knockout stages in tournaments.

## Installation

1. Clone the repository:
   git clone <repository-url>

2. Change into the project directory:
   cd sports-management-backend

3. Install the required dependencies:
   pip install -r requirements.txt

4. Configure the database:

- Update the database connection details in the `config/db.py` file.
- Create a MySQL database and ensure the connection details are correct.

5. Run the application:
   uvicorn index:app --reload

The backend server should now be running on `http://localhost:8000`.

## API Documentation

The API documentation is automatically generated and available at `http://localhost:8000/docs`. It provides detailed information about the available endpoints, request/response formats, and authentication requirements.

## Database Schema

The database schema for the application can be found in the `models/index.py` file. It defines the tables and relationships used by SQLAlchemy to interact with the database.

## Contributing

Contributions to the project are welcome! If you find any issues or would like to add new features, please submit a pull request.

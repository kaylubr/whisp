# Whisp

#### Description:

Whisp is a web application that allows users to register, log in, and send messages anonymously in a secure environment. The application uses SQLite as its database and implements basic user authentication features, such as password hashing and session management. 

The core functionality of the app revolves around two key entities: **Users** and **Messages**. Users can create an account with a unique username and password, and once logged in, they can send generate link for other users. The application also provides users with the ability to view messages that sent to them on their dashboard.

### Key Features:
- **User Registration**: Users can create an account by providing a unique username and a password. The password is securely hashed before storing it in the database.
- **Login**: Users can log in using their registered username and password. If credentials are incorrect, an error message is displayed.
- **Messaging**: Users can send messages using unique links associated with their profiles. When a message is sent, it is stored in the database and associated with the recipient.
- **User Profile**: Each user has a profile page containing a unique link that others can use to send them messages.
- **Message Viewing**: When logged in, users can view messages they have received from others.

### Project Structure:

This project contains the following files and directories:

- `app.py`: The main application file that defines all routes, models, and logic for the Flask app. It also includes the necessary setup for the SQLite database and the creation of tables.
- `hash.py`: A utility module that contains two functions, `encode_id` and `decode_id`, used for encoding and decoding user IDs for secure messaging.
- `templates/`: This folder contains the HTML templates used to render the app's pages. These include:
  - `index.html`: The main page where users see messages sent to them.
  - `register.html`: The registration page for creating a new account.
  - `login.html`: The login page where users enter their credentials.
  - `profile.html`: Displays the user's profile along with a unique link to send them messages.
  - `message.html`: The page for composing and sending a message to another user.
  - `error.html`: Displays error messages for various operations like registration or login failures.
  - `success.html`: Displays a success message when a message is successfully sent.

### Database Models:

This application uses two primary models defined in `app.py`:

1. **Users**:
   - `id`: A unique integer identifier for each user.
   - `username`: A unique string representing the user's chosen username.
   - `password`: A securely hashed password for authentication.
   - `hashed_id`: A unique, encoded identifier for each user used for secure messaging links.
   
2. **Messages**:
   - `id`: A unique integer identifier for each message.
   - `recipient_id`: A foreign key linking the message to the recipient user.
   - `message`: The content of the message sent.

### Design Choices:

While implementing this project, there were several design choices made that I believe are important to note:

1. **Password Hashing**: 
   The application uses `werkzeug.security`'s `generate_password_hash` function to securely hash passwords before storing them in the database. This ensures that even if the database is compromised, user passwords remain secure.

2. **Session Management**:
   Flask's built-in session management system is used to track the logged-in user. The `SECRET_KEY` configuration ensures the session cookies are signed and protected against tampering.

3. **Database Choice**:
   SQLite was chosen for simplicity and ease of use, given that this is a basic application. It requires no separate server setup and is perfect for small to medium-sized applications. If this app were to scale, a more robust solution like PostgreSQL or MySQL could be used.

4. **Encoded User IDs**:
   The `encode_id` and `decode_id` functions are used to provide an additional layer of security for user identification. This approach prevents users from directly guessing other users' IDs in URLs.

5. **Flask’s Simplicity**:
   Flask was chosen for its simplicity and flexibility, which allowed me to quickly prototype and build this application. Flask's minimalistic design helped focus on the core functionality without much overhead.

### Setup Instructions:

To run this project locally, follow these steps:

1. Clone the repository:

```bash
git clone <repository_url>
cd <repository_directory>

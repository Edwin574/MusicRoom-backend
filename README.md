# Music Room
### Introduction

Music Room is a collaborative music application that allows users to create and join rooms where they can collaboratively play and control music using Spotify. The application leverages Spotify's API to manage music playback and implements a voting system for skipping tracks, ensuring a democratic and engaging listening experience.

## Features

- Create a room with a unique room code.
- Join a room using a room code.
- Vote to skip the current song.
- Control music playback (play, pause, skip).
- Authenticate with Spotify.

## Features Description

### 1. Room Creation and Management
**Room Creation**: The host creates a room by sending a POST request to the `/createroom` endpoint. This generates a unique room code that can be shared with other users. The room details are stored in the database, and the room code is used to identify the room in subsequent operations.

**Joining a Room**: Users can join a room using the unique room code by sending a POST request to the `/join-room` endpoint. This adds the user to the room, allowing them to participate in music playback control and voting.

**Leaving a Room:** Users can leave a room by sending a POST request to the `/leave-room` endpoint. This removes the user from the room and updates the room's participant list.

**Updating Room Settings**: The host can update room settings (such as the number of votes required to skip a song) by sending a PATCH request to the `/update-room` endpoint.

### 2. Music Playback Control
**Playing and Pausing Songs**: Users can play and pause songs in the room by sending PUT requests to the `/play-song` and `/pause-song` endpoints, respectively. These actions are controlled through Spotify's API.

**Skipping Songs**: To skip a song, users vote by sending a POST request to the `/skip-song` endpoint. The song is skipped only if the number of votes meets the threshold defined by the room settings.

### 3. Spotify Integration and Authentication
**Authentication**: Users authenticate with Spotify by first getting the Spotify authentication URL through the `/get-auth-url` endpoint. After the user authenticates, Spotify redirects them to a specified redirect URI, which is handled by the `/redirect` endpoint. The `/is-authenticated` endpoint checks if the user is authenticated.

**Current Song Information**: The `/current-song` endpoint retrieves the currently playing song's details using Spotify's API.

## API Endpoints

### Room Management

- **Create Room**
  - **Endpoint**: `/createroom`
  - **Method**: POST
  - **Description**: Creates a new room with a unique room code.
  
- **Get Room**
  - **Endpoint**: `/get-room`
  - **Method**: GET
  - **Description**: Retrieves details of a room by room code.
  
- **Join Room**
  - **Endpoint**: `/join-room`
  - **Method**: POST
  - **Description**: Allows a user to join a room using a room code.
  
- **User in Room**
  - **Endpoint**: `/user-in-room`
  - **Method**: GET
  - **Description**: Checks if a user is in a room.
  
- **Leave Room**
  - **Endpoint**: `/leave-room`
  - **Method**: POST
  - **Description**: Allows a user to leave a room.
  
- **Update Room**
  - **Endpoint**: `/update-room`
  - **Method**: PATCH
  - **Description**: Updates room settings.

### Spotify Authentication

- **Get Auth URL**
  - **Endpoint**: `/get-auth-url`
  - **Method**: GET
  - **Description**: Retrieves the Spotify authentication URL.
  
- **Redirect URI**
  - **Endpoint**: `/redirect`
  - **Method**: GET
  - **Description**: Handles Spotify's authentication callback.
  
- **Check Authentication**
  - **Endpoint**: `/is-authenticated`
  - **Method**: GET
  - **Description**: Checks if the user is authenticated with Spotify.

### Music Control

- **Current Song**
  - **Endpoint**: `/current-song`
  - **Method**: GET
  - **Description**: Retrieves the currently playing song.
  
- **Pause Song**
  - **Endpoint**: `/pause-song`
  - **Method**: PUT
  - **Description**: Pauses the current song.
  
- **Play Song**
  - **Endpoint**: `/play-song`
  - **Method**: PUT
  - **Description**: Plays the current song.
  
- **Skip Song**
  - **Endpoint**: `/skip-song`
  - **Method**: POST
  - **Description**: Votes to skip the current song. Requires a certain number of votes to skip.

## Project Setup

### Prerequisites

- Python 3.10+
- Django 3.2+
- Spotify Developer Account

### Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/Edwin574/Music-Room.git
    cd music-room
    ```

2. **Create a virtual environment and activate it**:

Make sure you have `pipenv` installed you can use ```sh pip install pipenv```
    ```sh
    pipenv shell
    ```

3. **Install the required dependencies**:
    ```sh
    pipenv install
    ```

4. **Set up environment variables**:
   Create a `.env` file in the project root and add your Spotify API credentials:
    ```
    SPOTIFY_CLIENT_ID=your_spotify_client_id
    SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
    SPOTIFY_REDIRECT_URI=your_spotify_redirect_uri
    ```

5. **Apply database migrations**:
    ```sh
    python manage.py migrate
    ```

6. **Run the server**:
    ```sh
    python manage.py runserver
    ```

### Usage
An Easy way of holding an intresting music jam by allowing anyone in a house party to control music.

### Example Requests

- **Create Room**:
  ```sh
  curl -X POST http://127.0.0.1:8000/createroom


# Playlist migrator
A simple client-server app that transfers music playlists between Spotify and YouTube Music.

The app uses Python with Flask for the server and React with TypeScript for the front end.

# Features
`The app is still in development. For now these features are present:`
- Logging in using a Spotify account
- Displaying your Spotify playlists
- Display the tracks of a Spotify playlist

# How to run
Make sure you have installed:
- Python 3.13.2 (or above)
- pip 24.3.1 (or above)
- node.js 20.8.1 (or above)

## Packages

After you clone the project, navigate to the client folder and run "npm install" to get the needed packages
```
\Playlist-migrator> cd client
\Playlist-migrator\client> npm install
```
Then, go inside the server folder and install the python dependencies
```
\Playlist-migrator\client> cd ../server
\Playlist-migrator\server> pip install -r requirements.txt
```

## Spotify program
Currently, I haven't hosted the server anywhere so the only way of getting the app to work is to run the server yourself.

To be able to call the Spotify API, you will need to set up a program on the Spotify developers page. More info at: https://developer.spotify.com/

After the program setup, you will receive `client id` and `client secret` keys.

## Environment variables
For security reasons, the `client id` and the `client secret` are kept inside the environment variables of the operating system. You will need to add 2 variables with names `SPOTIPY_CLIENT_ID` and `SPOTIPY_CLIENT_SECRET` with their values being your keys from Spotify
> [!IMPORTANT]
> Notice that the variable names start with SPOTIPY instead of SPOTIFY

## Running the servers
After everything is set up, you can navigate to the server's folder and run the `main.py`. Your server should start on localhost with port `8080`.

Then, navigate to the client folder and run the frontend server by calling
```
\Playlist-migrator\client> npm run
```
The server should run on port `5173`

# Planned features
- Log in using YouTube
- Editing and creating playlists for both platforms
- Migrating playlists from both platforms
- Change the communication between the servers to HTTPS
- Add authentication tokens when calling the server API

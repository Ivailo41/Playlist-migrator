import './App.css'
import React from 'react'

function App() {
  return (
    <div className="page-wrapper">
      <Header />
      <PlaylistContainer />
    </div>
  )
}

function Header() {

  return (
    <header>
      <LoginButton />
      <LoginYoutubeButton />
      <LogOutButton />
    </header>
  )
}

function LoginButton() {
  const handleClick = () => {
    window.location.href = 'http://127.0.0.1:8080/login';  // Open in the same tab
  }

  return (
    <button onClick={handleClick}>Login</button>
  )
}

function LoginYoutubeButton() {
  const handleClick = () => {
    window.location.href = 'http://127.0.0.1:8080/api/youtube/login';  // Open in the same tab
  }

  return (
    <button onClick={handleClick}>Login</button>
  )
}

function LogOutButton() {
  const handleClick = () => {
    window.location.href = 'http://127.0.0.1:8080/logout';
  }

  return (
    <button onClick={handleClick}>Logout</button>
  )
}

function PlaylistContainer() {

  let initialList: any[] = [];
  const [list, setList] = React.useState(initialList);

  // Later add variable to send request based on the platform
  const fetchPlaylists = async () => {
    const response = await fetch('http://127.0.0.1:8080/getUserPlaylists', {
      method: 'GET',
      credentials: 'include',  // Include cookies in the request
    });

    const data = await response.json();
    return data;
  };

  const handleClick = () => {
    fetchPlaylists()
      .then((data) => {
        if (data['error']) {
          console.log(data['error']);
          return;
        }
        setList(data['items']);
        console.log(data['items']);
    }).catch((error) => {
      console.error('Error:', error);
    });
  };

  return (
    <div className="playlist-wrapper">
      <ul className="playlist-container">
        <button onClick={handleClick}>Print Playlists</button>
        {list.map((item) => (
          <PlaylistItem playlist={item}/>
        ))}
      </ul>
    </div>
  )
}

function PlaylistItem({ playlist }: { playlist: any }) {

  let trackList: any[] = [];
  const [tracks, setTracks] = React.useState(trackList);
  
  const totalTracks = playlist.tracks['total'];

  const imageSrc = (): string =>
  {
    if (playlist.images) {
      return playlist.images[0].url;
    }
    else {
      return 'song_cover.png';
    }
  }

  const fetchPlaylistTracks = async (id: string) => {
    const response = await fetch(`http://127.0.0.1:8080/getPlaylistTracks?playlistId=${id}&totalTracks=${totalTracks}`, 
    {
      method: 'GET',
      credentials: 'include',
      headers: 
      {
        'Content-Type': 'application/json'
      }
      });
    
    const data = await response.json();
    return data;
  }


  const handleClick = async (id: string) => 
  {
    fetchPlaylistTracks(id)
      .then((data) => {
        if (data['error']) {
          console.log(data['error']);
          return;
        }
        setTracks(data['items']);
        console.log(data['items']);
    }).catch((error) => {
      console.error('Error:', error);
    });
  }

  return (
    <div className="playlist-item">
      <img src={imageSrc()} width={100} height={100} alt="playlist" />
      <div>
        <a target="_blank" href={playlist.external_urls['spotify']}>{playlist.name}</a>
        <p>{playlist.tracks['total']} tracks</p>
      </div>
      <button onClick={() => handleClick(playlist.id)}>Get tracks</button>
      <ul>
        {tracks.map((track) => (
          <li key={track.track.id}>{track.track.name}</li>
        ))}
      </ul>
    </div>
  )
}

export default App;

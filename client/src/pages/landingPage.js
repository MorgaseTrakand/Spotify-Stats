import '../App.css';


function LandingPage() {

  async function handleClick() {
    fetch('http://127.0.0.1:5000/auth/login', {
      credentials: "include"
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      // Handle the parsed JSON data
      console.log(data);  
      window.location.href = data.authUrl;
      
    })
    .catch(error => {
      console.error('Fetch error:', error);
    });
  }



  return (
    <div className="hero">
      <button onClick={handleClick}>Login to Spotify</button>
    </div>
  );
}

export default LandingPage;
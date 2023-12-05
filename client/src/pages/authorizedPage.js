import '../App.css';
import './dashboard.css'
import React, { useContext } from 'react';
import MyContext from '../myContext';

function AuthorizedPage() {
  const queryString = window.location.search; // Gets the query string (?param1=value1&param2=value2)
  const params = new URLSearchParams(queryString);
  const code = params.get('access_token');
  const state = params.get('state')

  function Top() {
    fetch(`http://127.0.0.1:5000/auth/top?accessToken=${code}`)
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      console.log(data);        
    })
    .catch(error => {
      console.error('Fetch error:', error);
    });
  }
  

  return (
    <div>
        <button onClick={Top}>Get Data</button>
        <div className='hero'>
          <div className='main-container'>
            <div className='artist-container'></div>
            <div className='track-container'>
              <div className='slider-container'></div>
            </div>
          </div>
        </div>
    </div>
  );
}

export default AuthorizedPage;
import { useState } from 'react';
import './LoginSignup.css'
import chart from './assets/stockchart.png'
import icon from './assets/icon.png'

function LoginSignUp({ onLoginSuccess }) {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState(''); 

  const handleSubmit = async (e) => {
    e.preventDefault();
    const endpoint = isLogin ? 'login' : 'signup';

    const response = await fetch(`http://localhost:5002/${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(isLogin ? { email, password } : { name, email, password }),
    });

    const result = await response.json();
    
    if (result.success) {
      onLoginSuccess({
        userId: result.userId,
        name: result.name
      });
    } else {
      alert(result.message);
    }
  };

  const toggleForm = () => {
    setIsLogin(!isLogin);
    setEmail('');
    setPassword('');
    setName('');
  };

  return (
    <div className="wrapper">
      <div className="nicetext">
        <h1 id="home"><img src={icon}></img>NITWSE</h1>
        <p id="fullform">National Institute of Technology Warangal Stock Exchange </p>
        <h2 id="subtext">Do you have what it takes?</h2>
        <div className="container"><img src={chart} id="chart"></img></div>
      </div>
      <div className="cardwrapper">
        <div className="auth-card">
          <h2 id="head">{isLogin ? 'Login' : 'Sign Up'}</h2>
          <form onSubmit={handleSubmit}>
            {!isLogin && (
              <input
                type="text"
                placeholder="Name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
              />
            )}

            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />

            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />

            <button type="submit">{isLogin ? 'Login' : 'Sign Up'}</button>
          </form>

          <p onClick={toggleForm}>
            {isLogin ? "Don't have an account? Sign Up" : "Already have an account? Login"}
          </p>
        </div>
      </div>
    </div>
  );
}

export default LoginSignUp;

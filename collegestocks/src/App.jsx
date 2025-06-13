import './App.css'
import {useState} from 'react'
import LoginSignUp from './LoginSignup'
import StockDashboard from './DashBoard'

function App() {
  const [isLogin, setLogin] = useState(true);
  const [userData, setUserData] = useState(null);

  const handleLoginSuccess = (data) => {
    setUserData(data);
    setLogin(false);
  };

  return (
    <>   
    {isLogin ? 
      <LoginSignUp onLoginSuccess={handleLoginSuccess}/> : 
      <StockDashboard userId={userData?.userId} userName={userData?.name}/>
    }
    </>
  );
}

export default App

import { useState } from "react";
import "./App.css";
import About from  "./components/Nav/About";
import Services from  "./components/Nav/Services";
import Contact from  "./components/Nav/Contacts";
import Dashboard from "./components/Dashboard";
import StockContext from "./context/StockContext";
import ThemeContext from "./context/ThemeContext";
import {BrowserRouter as  Router, Route, Routes} from 'react-router-dom';
import Navbar from "./components/Navbar";
import Login from "./components/Login"

function App() {
  const [darkMode, setDarkMode] = useState(false);
  const [stockSymbol, setStockSymbol] = useState("API");

  return (

    <Router>
    <ThemeContext.Provider value={{ darkMode, setDarkMode }}>
      <StockContext.Provider value={{ stockSymbol, setStockSymbol }}>
        <Navbar/>
        <Routes>
            <Route path="/" element= {<Dashboard/>} exact/>
            <Route path="/about" element={<About/>} />
            <Route path="/services" element={<Services/>} />
            <Route path="/contact" element={<Contact/>} /> 

        </Routes>
      </StockContext.Provider>
    </ThemeContext.Provider>

    </Router>


  );
}


export default App;



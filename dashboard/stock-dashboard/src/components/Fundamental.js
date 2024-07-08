
import React, { useContext } from "react";
import Card from "./Card";
import ThemeContext from "../context/ThemeContext";
import Title from "./Title";

const Fundamental = ({quotes}) => {
  console.log(quotes)
  const { darkMode } = useContext(ThemeContext);
  const detailsList = {
    net_profit : "NET PROFIT",
    net_margin : "NET_MARGIN",
    ROE : "ROE",
    ROA : "ROA",
    book_value  : "BOOK VALUE"
    
  };

return (
  <>
  
<Title title={"Fundamental Performance"}/>
<Card>
  
  <ul
    className={`w-auto h-auto flex ${
      // Use flex-row for large devices and flex-col for small devices
      darkMode ? "divide-gray-800" : null
    }`}
    style={{
      // Adjust flex direction based on screen size
      flexDirection: "row", // Default to column
      // For large devices, switch to row
      "@media (minWidth: 768px)": {
        flexDirection: "row",
        flexWrap: "wrap", // Allow items to wrap to the next line
      },
    }}
  >
    {Object.keys(detailsList).map((item) => (
      <li
        key={item}
        className={`flex-1 ${
          // Adjust item alignment based on screen size
          darkMode ? "divide-gray-800" : null
        }`}
        style={{
          // Add spacing and width for each item
          // Style the KPI appearance
          backgroundColor: darkMode ? "#1f2937" : "#f3f4f6",
          borderRadius: "0.5rem",
          boxShadow: "0 0 10px rgba(0, 0, 0, 0.1)",
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        <span style={{ fontSize: "2rem", fontWeight: "bold", color:"green" }}>
          {detailsList[item]}
        </span>
        <span style={{fontWeight:"bold", fontSize:"1rem"}}>{quotes[item]}</span>
      </li>
    ))}
  </ul>
</Card>
  
  </>
)}
;

export default Fundamental 
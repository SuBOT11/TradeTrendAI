import React, { useContext } from "react";
import Card from "./Card";
import ThemeContext from "../context/ThemeContext";
import Title from "./Title";
import StockContext from "../context/StockContext";

const Recommend = ({ recom }) => {
  const { darkMode } = useContext(ThemeContext);
  console.log(recom[0])

 const {stockSymbol}  = useContext(StockContext)
  
  return (
    <>
    <Title title={`Stocks similar to ${stockSymbol}`}/>
    
    {recom.map(com => (
    <div className="px-4 py-2 max-h-auto overflow-hidden">
    <Card>
      <ul
        className={` ${
          darkMode ? "divide-gray-800" : null
        }`}
      >
               <span>{com['symbol']}</span>
        {

            Object.keys(com['similarFields']).map(item =>( 
            <li key={com.symbol} className="py-4 flex justify-between items-center">
              <span className="px-2">{item}</span>
              <span className="font-bold">
                   {(com['similarFields'][item]).toFixed(2)}
              </span>
            </li>
            ))
        }
      </ul>
    </Card>
</div>
    ))
    } 
    </>
  );
};

export default Recommend;

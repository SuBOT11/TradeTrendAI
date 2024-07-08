import React, { useContext, useEffect, useState } from "react";
import ThemeContext from "../context/ThemeContext";
import Overview from "./Overview";
import Details from "./Details";
import Chart from "./Chart";
import Header from "./Header";
import StockContext from "../context/StockContext";
import { fetchStockDetails, fetchQuote, fetchRecommendedStocks } from "../utils/api/stock-api";
import Technical from "./Technical";
import Recommend from "./Recommend";
import Navbar from "./Navbar";
import Fundamental from "./Fundamental";

const Dashboard = () => {
  const { darkMode } = useContext(ThemeContext);

  const { stockSymbol } = useContext(StockContext);

  const [stockDetails, setStockDetails] = useState({});

  const [quote, setQuote] = useState({});

  const [recommended , setRecommended]  = useState([]);

  useEffect(() => {
    const updateStockDetails = async () => {
      try {
        const result = await fetchStockDetails(stockSymbol);
        setStockDetails(result);
      } catch (error) {
        setStockDetails({});
        console.log(error);
      }
      
    };

    const updateStockOverview = async () => {
      try {
        const result = await fetchQuote(stockSymbol);
        console.log(result)
        setQuote(result);
      } catch (error) {
        setQuote({});
        console.log(error);
      }
    };


    const updateRecommendedView = async () => {
      try {
        const result = await fetchRecommendedStocks(stockSymbol);
        console.log(result)
        setRecommended(result);
      } catch (error) {
        setRecommended({});
        console.log(error);
      }
    };


    updateStockDetails();
    updateStockOverview();
    updateRecommendedView();
  }, [stockSymbol]);

  return (
    <div className={`grid grid-cols-1 md:grid-cols-2 
    xl:grid-cols-3 grid-rows-8 md:grid-rows-9 xl:grid-rows-8 auto-rows-fr gap-6 p-10 font-quicksand
     ${darkMode ? "bg-gray-900 text-gray-300" : "bg-neutral-100"}`}>
   
      <div className="col-span-1 md:col-span-2 xl:col-span-3 row-span-1 flex justify-start items-center">
        <Header name={stockDetails.description} />
      </div>
      <div className="col-span-1 md:col-span-2 xl:col-span-3 xl:row-span-1 flex justify-start items-center">
        <Technical quotes={quote}/>


      </div>
      <div className="md:col-span-2 row-span-3">
        <Chart />
      </div>
      <div>
        <Overview
          symbol={stockSymbol}
          price={quote.close}
          change={quote.change}
          changePercent={quote.pc_change}
          currency='NPR'
        />
      </div>
      <div className="row-span-3 xl:row-span-2">
        <Details details={stockDetails} />
      </div>
      <div className="col-span-1 md:col-span-2 xl:col-span-3 xl:row-span-1 flex justify-start items-center">

          <Fundamental quotes={stockDetails}/>

      </div>

      <div className="xl:col-span-3 xl:row-span-5 flex flex-wrap justify-start items-center">
        <Recommend recom={recommended} />
      </div>    

          


     
    </div>
  );
};

export default Dashboard;

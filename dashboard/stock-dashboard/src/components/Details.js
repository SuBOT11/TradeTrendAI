import React, { useContext } from "react";
import Card from "./Card";
import ThemeContext from "../context/ThemeContext";

const Details = ({ details }) => {
  const { darkMode } = useContext(ThemeContext);
  console.log(details)
  console.log("this ran fooker")
  const detailsList = {
    symbol : "Symbol",
    description : "Name",
    sector : "Sector",
    market_capitalization: "Market Capitalization",
    size : "Company Size",
    pe_ratio : "PE Ratio",
    dividend_yield: "Dividend Yield",
    net_profit: "NET Profit",
    eps : "Earning Per Share"
  };

  const convertMillionToBillion = (number) => {
    return (number / 1000).toFixed(2);
  };

  return (
    <Card>
      <ul
        className={`w-full flex flex-col justify-between divide-y-1 ${
          darkMode ? "divide-gray-800" : null
        }`}
      >
        {Object.keys(detailsList).map((item) => {
          return (
            <li key={item} className="flex-1 flex justify-between items-center">
              <span>{detailsList[item]}</span>
              <span className="font-bold">
                {item === "market_capitalization"
                  ? `${convertMillionToBillion(details[item])}B`
                  : details[item]}
              </span>
            </li>
          );
        })}
      </ul>
    </Card>
  );
};

export default Details;

import React, { useContext, useEffect, useState } from "react";
import ChartFilter from "./ChartFilter";
import Card from "./Card";
import {
  Area,
  XAxis,
  YAxis,
  ResponsiveContainer,
  AreaChart,
  Tooltip,
} from "recharts";
import ThemeContext from "../context/ThemeContext";
import StockContext from "../context/StockContext";
import { fetchHistoricalData } from "../utils/api/stock-api";
import {fetchPredictedData} from "../utils/api/stock-api";
import {
  createDate,
  convertDateToUnixTimestamp,
  convertUnixTimestampToDate,
} from "../utils/helpers/date-helper";
import { chartConfig } from "../constants/config";

const Chart = () => {
  const [filter, setFilter] = useState("1W");

  const { darkMode } = useContext(ThemeContext);

  const { stockSymbol } = useContext(StockContext);
  
  const [data, setData] = useState([]);
  const [predictedData, setPredictedData] = useState([]);

  const formatData = (data,pred_data) => {
    console.log(data,"hist data");
    console.log(pred_data,"pred data")
    const hist_arr = data.c.map((item, index) => {
      return {
        history : item.toFixed(2),
        date: convertUnixTimestampToDate(data.t[index]),
        type: "history"
      };
    });
      const pred_arr = pred_data.c.map((item, index) => {
        return { 
          predicted : parseFloat(item).toFixed(2),
          date : convertUnixTimestampToDate(pred_data.t[index]),
          type : "predicted"
        }
      })


      console.log(hist_arr.concat(pred_arr));
      return hist_arr.concat(pred_arr);
  };

  useEffect(() => {
    const getDateRange = () => {
      const { days, weeks, months, years } = chartConfig[filter];

      const endDate = new Date();
      const startDate = createDate(endDate, -days, -weeks, -months, -years);

      const startTimestampUnix = convertDateToUnixTimestamp(startDate);
      const endTimestampUnix = convertDateToUnixTimestamp(endDate);
      return { startTimestampUnix, endTimestampUnix };
    };

    const updateChartData = async () => {
      try {
        const { startTimestampUnix, endTimestampUnix } = getDateRange();
        const resolution = chartConfig[filter].resolution;
        const result = await fetchHistoricalData(
          stockSymbol,
          resolution,
          startTimestampUnix,
          endTimestampUnix
        );


        const predictedResult = await fetchPredictedData(stockSymbol);
        setPredictedData(predictedResult);
        setData(formatData(result,predictedResult));
        
      } catch (error) {
        setData([]);
        setPredictedData([]);
        console.log(error);
      }
    };

    updateChartData();
  }, [stockSymbol, filter]);

  return (
    <Card>
      <ul className="flex absolute top-2 right-2 z-40">
        {Object.keys(chartConfig).map((item) => (
          <li key={item}>
            <ChartFilter
              text={item}
              active={filter === item}
              onClick={() => {
                setFilter(item);
              }}
            />
          </li>
        ))}
      </ul>
      <ResponsiveContainer>
        <AreaChart data={data}>
          {console.log(data[0])}
          <defs>
            <linearGradient id="chartColor" x1="0" y1="0" x2="0" y2="1">
              <stop
                offset="5%"
                stopColor={darkMode ? "#312e81" : "rgb(199 210 254)"}
                stopOpacity={0.8}
              />
              <stop
                offset="95%"
                stopColor={darkMode ? "#312e81" : "rgb(199 210 254)"}
                stopOpacity={0}
              />
            </linearGradient>
            <linearGradient id="chartColor1" x1="0" y1="0" x2="0" y2="1">
              <stop
                offset="5%"
                stopColor={darkMode ? "#E4080A" : "rgb(256 136 137)"}
                stopOpacity={0.8}
              />
              <stop
                offset="95%"
                stopColor={darkMode ? "#E4080A" : "rgb(256 136 137)"}
                stopOpacity={0}
              />
            </linearGradient>
          </defs>
          <Tooltip
            contentStyle={darkMode ? { backgroundColor: "#111827" } : null}
            itemStyle={darkMode ? { color: "#818cf8" } : null}
          />
            <Area
              type="monotone"
              dataKey="history"
              stroke="#312e81"
              fill="url(#chartColor)"
              //fill={
            //(data) => data.type === 'history' ? '#8884d8' : '#82ca9d'
              //}
              fillOpacity={1}
              strokeWidth={0.5}
            />
            <Area
              type="monotone"
              dataKey="predicted"
              stroke="#312e81"
              fill="url(#chartColor1"
              //fill={
            //(data) => data.type === 'history' ? '#8884d8' : '#82ca9d'
              //}
              fillOpacity={1}
              strokeWidth={0.5}
            />
          <XAxis dataKey="date" />
          <YAxis domain={["dataMin", "dataMax"]} />
        </AreaChart>
      </ResponsiveContainer>
    </Card>
  );
};

export default Chart;

import React, { useContext, useEffect, useState } from "react";
import ThemeContext from "../context/ThemeContext";

const Title = ({title}) =>  {

    const { darkMode } = useContext(ThemeContext);
    const bgColor = darkMode ? "bg-stone-600" : "bg-stone-200";
    const textColor = darkMode ? "text-white" : "text-gray-800";


  // Alternatively, you can use RGB values

  return (
    <div className={`${bgColor} ${textColor} py-4 px-6 rounded-t-lg`}>
      <h2 className="text-xl font-semibold uppercase">{title}</h2>
    </div>
  );


}

export default Title
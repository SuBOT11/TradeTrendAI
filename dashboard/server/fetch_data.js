
url = 'https://merolagani.com/handlers/TechnicalChartHandler.ashx?type=get_advanced_chart&symbol=AHL&resolution=1W&rangeStartDate=1677347332&rangeEndDate=1711561792&from=&isAdjust=1&currencyCode=NPR'
fetch(url)
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => {
    console.log(data); // Process the JSON data here
  })
  .catch(error => {
    console.error('There was a problem with the fetch operation:', error);
  });

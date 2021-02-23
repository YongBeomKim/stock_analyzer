import CardStockMarket from './components/inquiry/card/cardStockMarket';
import './App.css';
import React, { Component } from 'react';
import axios from 'axios';

class App extends Component{
  constructor(props){
    super(props);
  }

  render(){
    axios({
      method : "get",
      url : "http://127.0.0.1:8000/rest_api/market/"
    })
    .then(response => {
      console.log(response);
      let stockMarkets = {};
      response.data.forEach(element => {
        console.log(element["id"]);
        console.log(element["stock_market_name"]);
      });
    })
    .catch(error => {
      console.log("error", error);
    })
    return (
      // <div className="App" style={style}>
      <div id="grid">
        <ul className="stockMarkets">
          <CardStockMarket></CardStockMarket>
          <CardStockMarket></CardStockMarket>
          <CardStockMarket></CardStockMarket>
          <CardStockMarket></CardStockMarket>
          <CardStockMarket></CardStockMarket>
        </ul>
      </div>
    );
  }
}

export default App;

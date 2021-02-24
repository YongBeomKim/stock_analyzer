import CardStockMarket from './components/inquiry/card/cardStockMarket';
import './App.css';
import React, { Component } from 'react';
import axios from 'axios';

class App extends Component{
  constructor(props){
    console.log('constructor')
    super(props);
    this.markets = [];
    fetch("http://127.0.0.1:8000/rest_api/market/",{
      method:"GET"
    })
    .then(response => response.json())
    .then(response => console.log('success', JSON.stringify(response)))


    // console.log('after', this.market)
    
    // axios({
    //   method : "get",
    //   // url : "http://175.116.181.151:4040/siqms/rest_api/getAllLayerIdNameList"
    //   url : "http://127.0.0.1:8000/rest_api/market/"
    // })
    // .then(response => {
    //   console.log(response);
    //   response.data.forEach(element => {
    //     // debugger;
    //     let _id = element["id"];
    //     let _name = element["stock_market_name"];
    //     let market = <CardStockMarket name={_name}/>
    //     this.markets.push(market);
    //     console.log('here is ', this.markets);
    //   });
    // })
    // .catch(error => {
    //   console.log("error", error);
    // })
    this.state = {
      markets: [
        // {id: 1, title: 'KOSPI'}
      ]
    }
  }

  render(){
    return (
      // <div className="App" style={style}>
      <div id="grid">
        <ul className="stockMarkets">
          {/* {this.state.markets} */}
          {this.markets}
        </ul>
      </div>
    );
  }
}

export default App;

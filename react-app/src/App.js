import CardStockMarket from './components/inquiry/card/cardStockMarket';
import './App.css';
import React, { Component } from 'react';
import axios from 'axios';

class App extends Component{

  state = {
    view: 'market',
    markets: []
  }

  constructor(props){
    super(props);
  }

  shouldComponentUpdate(){
    
  }

  render(){
    console.log('im render!', this.state.markets);

    return (
      // <div className="App" style={style}>
      <div id="grid">
        <ul className="stockMarkets">
          {this.state.markets}
        </ul>
      </div>
    );
  }

  componentDidMount(){
    console.log('im didmount!');
    axios({
      method : "get",
      url : "http://127.0.0.1:8000/rest_api/market/"
    })
    .then(response => {
      console.log(response);
      let _markets = [];
      response.data.forEach(element => {
        let _id = element["id"];
        let _name = element["stock_market_name"];
        let market = <CardStockMarket name={_name}/>
        _markets = _markets.concat(market);
      });
      console.log('hello', _markets);
      this.setState({markets: _markets});
    })
    .catch(error => {
      console.log("error", error);
    })
  }
}

export default App;

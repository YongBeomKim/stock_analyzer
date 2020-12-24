import React, { Component } from 'react'
import CardStockMarket from '../card/cardStockMarket'

class ListStockMarket extends Component {
    render() {
        var markets = [];
        var marketDatas = this.props.data;
        var i = 0;

        for (i = 0; i < marketDatas.length; i++){
            marketData = marketDatas[i]
            markets.push(
            <li key = {marketData.id}>
                <CardStockMarket name={marketData.name}></CardStockMarket>
            </li>
            );
        }

        return (
        <nav>
            <ul>
            {markets}
            </ul>
        </nav>
        );
    }
  }

  export default ListStockMarket;

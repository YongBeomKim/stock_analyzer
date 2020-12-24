import React, { Component } from 'react'

// 2020.12.24 : 테이블로 대체할 수 있음.
class ListStockItem extends Component {
    render() {
        var items = [];
        var itemDatas = this.props.data;
        var i = 0;

        for (i = 0; i < itemDatas.length; i++){
            itemData = itemDatas[i]
            items.push(
            <li key = {itemData.id}>
                {/* <CardStockMarket name={itemData.name}></CardStockMarket> */}
            </li>
            );
        }

        return (
        <nav>
            <ul>
            {items}
            </ul>
        </nav>
        );
    }
  }

  export default ListStockItem;

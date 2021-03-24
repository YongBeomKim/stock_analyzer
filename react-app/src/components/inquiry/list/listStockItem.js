import React, { Component } from 'react'
import CardStockItem from '../card/cardStockItem'
import axios from 'axios';

// 2020.12.24 : 테이블로 대체할 수 있음.
class ListStockItem extends Component {
    state = {
        items: []
    }

    constructor(props){
        super(props);
    }

    render() {
        return (
            <div id="grid">
                <ul className="stockItems">
                    {this.state.items}
                </ul>
            </div>
        );
    }

    componentDidMount(){
        axios({
            method : "get",
            url : "http://127.0.0.1:8000/rest_api/item_list/"
        })
        .then(response => {
            console.log(response);
            let _item_name;
            let _item_code;
            let _items = [];
            response.data.forEach((element, idx) =>{
                if(idx == 10) return;
                _item_name = element["stock_item_name"];
                _item_code = element["stock_item_code"];
                let item = <CardStockItem name={_item_name} code={_item_code} />
                _items = _items.concat(item);
            });
            this.setState({items:_items});
        })
        .catch(error => {
            console.log("error", error);
        })
        }
  }

  export default ListStockItem;

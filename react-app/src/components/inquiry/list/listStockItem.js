import React, { Component } from 'react'

// 2020.12.24 : 테이블로 대체할 수 있음.
class ListStockItem extends Component {
    render() {
        return (
        <nav>
            <ul>
            
            </ul>
        </nav>
        );
    }

    componentDidMount(){
        axios({
            method : "get",
            url : "http://127.0.0.1:8000/rest_api/item/"
        })
        .then(response => {
            console.log(response);
        })
        .catch(error => {
            console.log("error", error);
        })
        }
  }

  export default ListStockItem;

import ListStockMarket from './components/inquiry/list/listStockMarket';
import './App.css';
import React, { Component } from 'react';


class App extends Component{

  state = {
    view_mode: 'market',
  }

  constructor(props){
    super(props);
  }

  // shouldComponentUpdate(){
  // }

  render(){
    let template = null;
    if (this.state.view_mode == 'market') {
      template = <ListStockMarket/>;
    }

    return (
      <div className="App">
        {template}
      </div>
    );
  }
}

export default App;

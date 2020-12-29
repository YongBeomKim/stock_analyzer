import CardStockMarket from './components/inquiry/card/cardStockMarket';
import './App.css';

function App() {
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

export default App;

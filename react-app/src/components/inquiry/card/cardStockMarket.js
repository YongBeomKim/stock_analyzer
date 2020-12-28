import React, { Component } from 'react'
import {Card, CardHeader, CardContent, CardActions} from '@material-ui/core'

class CardStockMarket extends Component {
    render() {
        var marketName = this.props.name;
        
        return (
            <Card>
                <CardHeader></CardHeader>
                <CardContent></CardContent>
                <CardActions></CardActions>
            </Card>
        );
    }
  }

  export default CardStockMarkets;

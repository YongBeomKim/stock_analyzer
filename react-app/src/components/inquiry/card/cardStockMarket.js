import React, { Component } from 'react'

import './cardStockMarket.css'

import {Card, CardHeader, CardContent, CardActions, CardMedia} from '@material-ui/core'
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button'

class CardStockMarket extends Component {
    render() {
        var marketName = this.props.name;
        
        return (
            <Card className="root">
                <CardHeader>
                    
                </CardHeader>
                <CardContent>
                    <Typography className="content">I'm {marketName}. </Typography>
                </CardContent>
                <CardActions>
                    <Button size="small">GO TO</Button>
                </CardActions>
            </Card>
        );
    }
  }

  export default CardStockMarket;



















/* Simple card */
//   import React from 'react';
//   import { makeStyles } from '@material-ui/core/styles';
//   import Card from '@material-ui/core/Card';
//   import CardActions from '@material-ui/core/CardActions';
//   import CardContent from '@material-ui/core/CardContent';
//   import Button from '@material-ui/core/Button';
//   import Typography from '@material-ui/core/Typography';
  
//   const useStyles = makeStyles({
//     root: {
//       minWidth: 275,
//     },
//     bullet: {
//       display: 'inline-block',
//       margin: '0 2px',
//       transform: 'scale(0.8)',
//     },
//     title: {
//       fontSize: 14,
//     },
//     pos: {
//       marginBottom: 12,
//     },
//   });
  
//   export default function SimpleCard() {
//     const classes = useStyles();
//     const bull = <span className={classes.bullet}>•</span>;
  
//     return (
//       <Card className={classes.root}>
//         <CardContent>
//           <Typography className={classes.title} color="textSecondary" gutterBottom>
//             Word of the Day
//           </Typography>
//           <Typography variant="h5" component="h2">
//             be{bull}nev{bull}o{bull}lent
//           </Typography>
//           <Typography className={classes.pos} color="textSecondary">
//             adjective
//           </Typography>
//           <Typography variant="body2" component="p">
//             well meaning and kindly.
//             <br />
//             {'"a benevolent smile"'}
//           </Typography>
//         </CardContent>
//         <CardActions>
//           <Button size="small">Learn More</Button>
//         </CardActions>
//       </Card>
//     );
//   }
  
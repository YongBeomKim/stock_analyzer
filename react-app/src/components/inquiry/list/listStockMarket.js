import React, { Component } from 'react'
import CardStockMarket from '../card/cardStockMarket'
import axios from 'axios';

class ListStockMarket extends Component {
    state = {
        markets: []
      }
    
    constructor(props){
    super(props);
    }

    render(){
        return (
          <div id="grid">
            <ul className="stockMarkets">
              {this.state.markets}
            </ul>
          </div>
        );
      }
    
    componentDidMount(){
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
        this.setState({markets: _markets});
    })
    .catch(error => {
        console.log("error", error);
    })
    }
}

export default ListStockMarket;





  /* Spacing */
//   import React from 'react';
//   import { makeStyles } from '@material-ui/core/styles';
//   import Grid from '@material-ui/core/Grid';
//   import FormLabel from '@material-ui/core/FormLabel';
//   import FormControlLabel from '@material-ui/core/FormControlLabel';
//   import RadioGroup from '@material-ui/core/RadioGroup';
//   import Radio from '@material-ui/core/Radio';
//   import Paper from '@material-ui/core/Paper';
  
//   const useStyles = makeStyles((theme) => ({
//     root: {
//       flexGrow: 1,
//     },
//     paper: {
//       height: 140,
//       width: 100,
//     },
//     control: {
//       padding: theme.spacing(2),
//     },
//   }));
  
//   export default function SpacingGrid() {
//     const [spacing, setSpacing] = React.useState(2);
//     const classes = useStyles();
  
//     const handleChange = (event) => {
//       setSpacing(Number(event.target.value));
//     };
  
//     return (
//       <Grid container className={classes.root} spacing={2}>
//         <Grid item xs={12}>
//           <Grid container justify="center" spacing={spacing}>
//             {[0, 1, 2].map((value) => (
//               <Grid key={value} item>
//                 <Paper className={classes.paper} />
//               </Grid>
//             ))}
//           </Grid>
//         </Grid>
//         <Grid item xs={12}>
//           <Paper className={classes.control}>
//             <Grid container>
//               <Grid item>
//                 <FormLabel>spacing</FormLabel>
//                 <RadioGroup
//                   name="spacing"
//                   aria-label="spacing"
//                   value={spacing.toString()}
//                   onChange={handleChange}
//                   row
//                 >
//                   {[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((value) => (
//                     <FormControlLabel
//                       key={value}
//                       value={value.toString()}
//                       control={<Radio />}
//                       label={value.toString()}
//                     />
//                   ))}
//                 </RadioGroup>
//               </Grid>
//             </Grid>
//           </Paper>
//         </Grid>
//       </Grid>
//     );
//   }
  
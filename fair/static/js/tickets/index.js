import React, {Component, Fragment} from 'react';
import ReactDOM from 'react-dom';
import JssProvider from 'react-jss/lib/JssProvider';
import {createGenerateClassName, withStyles} from '@material-ui/core/styles';
import CssBaseline from "@material-ui/core/CssBaseline/CssBaseline";
import MuiThemeProvider from "@material-ui/core/es/styles/MuiThemeProvider";
import armadaTheme from 'armada/theme';
import Typography from "@material-ui/core/Typography/Typography";
import Ticket from "./Ticket";

const generateClassName = createGenerateClassName({
  dangerouslyUseGlobalCSS: false,
  productionPrefix: 'c'
});

const styles = theme => ({
  root: {
    fontSize: '16px'
  },
});

class App extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    const {classes} = this.props;

    const {lunch_tickets} = window.reactProps;
    console.log(lunch_tickets);

    return (
        <JssProvider generateClassName={generateClassName}>
          <Fragment>
            <CssBaseline/>
            <MuiThemeProvider theme={armadaTheme}>
              <Typography variant="h4" gutterBottom>Tickets for this years fair</Typography>
              {lunch_tickets.map(ticket => <Ticket key={ticket.id} token={ticket.token} title={`Lunch Ticket - ${ticket.date}`}/>)}
            </MuiThemeProvider>
          </Fragment>
        </JssProvider>
    )
  }
}

const AppWithStyles = withStyles(styles)(App);

ReactDOM.render(
    <AppWithStyles/>,
    document.getElementById('react')
);

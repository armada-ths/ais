import React, {Component, Fragment} from 'react';
import ReactDOM from 'react-dom';
import CssBaseline from "@material-ui/core/CssBaseline/CssBaseline";
import {createMuiTheme, withStyles} from '@material-ui/core/styles';
import MuiThemeProvider from "@material-ui/core/es/styles/MuiThemeProvider";
import SignupForm from "./SignupForm";
import Manage from './Manage';
import Header from "./Header";
import Paper from "@material-ui/core/es/Paper/Paper";

const theme = createMuiTheme({
  palette: {
    primary: {
      main: "#01d690",
      contrastText: "#ffffff"
    },
  }
});

const styles = theme => ({
  root: {
    maxWidth: 960,
    margin: 'auto',
    padding: theme.spacing.unit * 2,
    [theme.breakpoints.down('xs')]: {
      padding: 0
    }
  },
  paper: {
    padding: theme.spacing.unit * 4,
  },
});

class App extends Component {
  render() {
    const {classes} = this.props;
    const {
        event,
        payment_url,
        signup_url,
        user,
        teams,
        stripe_publishable
    } = window.reactProps;

    return (
        <Fragment>
          <CssBaseline/>
          <MuiThemeProvider theme={theme}>
            <div className={classes.root}>
              <Paper className={classes.paper}>
                <Header event={event}/>
                {user.signup_complete ? (
                    <Manage event={event} teams={teams}/>
                ) : (
                    <SignupForm
                        event={event}
                        feePayed={user.fee_payed}
                        paymentUrl={payment_url}
                        signupUrl={signup_url}
                        stripe_publishable={stripe_publishable}
                    />
                )}
              </Paper>
            </div>
          </MuiThemeProvider>
        </Fragment>
    )
  }
}

const AppWithStyles = withStyles(styles)(App);

ReactDOM.render(
    <AppWithStyles/>,
    document.getElementById('react')
);

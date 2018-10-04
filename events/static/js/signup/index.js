import React, {Component, Fragment} from 'react';
import ReactDOM from 'react-dom';
import CssBaseline from "@material-ui/core/CssBaseline/CssBaseline";
import {createMuiTheme, withStyles} from '@material-ui/core/styles';
import MuiThemeProvider from "@material-ui/core/es/styles/MuiThemeProvider";
import SignupForm from "./SignupForm";
import Manage from './Manage';
import Header from "./Header";
import reducer from './reducer';
import Paper from "@material-ui/core/es/Paper/Paper";
import * as ACTIONS from './actions';
import keyBy from 'lodash/keyBy';

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
  constructor(props) {
    super(props);
    const {
      participant,
      teams
    } = window.reactProps;

    this.state = reducer({}, {
      type: ACTIONS.INIT,
      payload: {
        participant,
        teams: keyBy(teams, 'id')
      }
    });

    this.dispatcher = this.dispatcher.bind(this);
  }

  dispatcher(action) {
    this.setState(state => reducer(state, action));
  }

  render() {
    const {classes} = this.props;
    const {participant, teams} = this.state;
    const {
      event,
      payment_url,
      signup_url,
      stripe_publishable
    } = window.reactProps;

    return (
        <Fragment>
          <CssBaseline/>
          <MuiThemeProvider theme={theme}>
            <div className={classes.root}>
              <Paper className={classes.paper}>
                <Header event={event}/>
                {participant.signup_complete ? (
                    <Manage
                        event={event}
                        teams={teams}
                        dispatcher={this.dispatcher}
                    />
                ) : (
                    <SignupForm
                        event={event}
                        feePayed={participant.fee_payed}
                        paymentUrl={payment_url}
                        signupUrl={signup_url}
                        stripe_publishable={stripe_publishable}
                        dispatcher={this.dispatcher}
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

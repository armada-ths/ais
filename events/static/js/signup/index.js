import React, {Component, Fragment} from 'react';
import ReactDOM from 'react-dom';
import CssBaseline from "@material-ui/core/CssBaseline/CssBaseline";
import {withStyles} from '@material-ui/core/styles';
import theme from '../theme';
import MuiThemeProvider from "@material-ui/core/es/styles/MuiThemeProvider";
import SignupForm from "./components/SignupForm";
import Manage from './components/Manage';
import Header from "./components/Header";
import reducer from './reducer';
import compose from 'recompose/compose';
import {init} from './actions';
import keyBy from 'lodash/keyBy';
import withWidth from "@material-ui/core/es/withWidth/withWidth";

const styles = theme => ({
  root: {
    maxWidth: 960,
    margin: `${theme.spacing.unit * 2}px auto`,
    padding: theme.spacing.unit * 3,
    [theme.breakpoints.down('sm')]: {
      margin: 0,
      height: '100vh'
    }
  },
});

class App extends Component {
  constructor(props) {
    super(props);
    const {
      participant,
      teams
    } = window.reactProps;

    this.state = reducer({}, init(participant, keyBy(teams, 'id')));

    this.dispatcher = this.dispatcher.bind(this);
  }

  dispatcher(action) {
    this.setState(state => reducer(state, action));
  }

  render() {
    const {classes, width} = this.props;
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
            <div
                className={classes.root}
            >
              <Header event={event}/>
              {participant.signup_complete ? (
                  <Manage
                      checkInToken={participant.check_in_token}
                      currentTeamId={participant.team_id}
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
            </div>
          </MuiThemeProvider>
        </Fragment>
    )
  }
}

const AppWithStyles = compose(
    withStyles(styles),
    withWidth()
)(App);

ReactDOM.render(
    <AppWithStyles/>,
    document.getElementById('react')
);

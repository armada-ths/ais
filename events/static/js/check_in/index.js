import React, {Component, Fragment} from 'react';
import JssProvider from 'react-jss/lib/JssProvider';
import {createGenerateClassName, withStyles} from '@material-ui/core/styles';
import armadaTheme from '../theme';
import ReactDOM from 'react-dom';
import QrCodeIcon from 'mdi-material-ui/Qrcode';
import ChecklistIcon from 'mdi-material-ui/FormatListCheckbox';
import MuiThemeProvider from "@material-ui/core/es/styles/MuiThemeProvider";
import CssBaseline from "@material-ui/core/es/CssBaseline/CssBaseline";
import ParticipantList from './ParticipantList';
import BottomNavigation from "@material-ui/core/es/BottomNavigation/BottomNavigation";
import BottomNavigationAction from "@material-ui/core/es/BottomNavigationAction/BottomNavigationAction";
import Grid from "@material-ui/core/es/Grid/Grid";
import QRSCanner from "./QRScanner";
import * as API from './api';
import CounterLine from "./CounterLine";
import sortBy from 'lodash/sortBy';
import filter from 'lodash/filter';
import find from 'lodash/findIndex';

const generateClassName = createGenerateClassName({
  dangerouslyUseGlobalCSS: false,
  productionPrefix: 'c'
});

const styles = theme => ({
  root: {
    height: '100%'
  },
  content: {
    margin: '0 auto',
    maxWidth: 500,
    height: '100%',
  }
});

class App extends Component {
  constructor(props) {
    super(props);

    const sortedParticipants = sortBy(window.reactProps.participants, 'name');

    this.state = {
      navigationIndex: 1,
      participants: sortedParticipants,
    };

    this.handleNavigation = this.handleNavigation.bind(this);
    this.handleCheckIn = this.handleCheckIn.bind(this);
    this.handleCheckOut = this.handleCheckOut.bind(this);
  }

  handleNavigation(event, value) {
    this.setState({navigationIndex: value})
  }

  handleCheckIn(id) {
    const {event_id} = window.reactProps;

    this.setState(prevState => {
      const participants = [...prevState.participants];
      const index = find(prevState.participants, {'id': id});
      participants[index].has_checked_in = true;

      return {
        ...prevState,
        participants
      }
    });

    API.checkIn(event_id, id);
  }

  handleCheckOut(id) {
    const {event_id} = window.reactProps;

    this.setState(prevState => {
      const participants = [...prevState.participants];
      const index = find(prevState.participants, {'id': id});
      participants[index].has_checked_in = false;

      return {
        ...prevState,
        participants
      }
    });

    API.checkOut(event_id, id);
  }

  render() {
    const {classes} = this.props;
    const {navigationIndex, participants} = this.state;
    const {event_id} = window.reactProps;

    const total = participants.length;
    const current = filter(participants, 'has_checked_in').length;

    return (
        <JssProvider generateClassName={generateClassName}>
          <Fragment>
            <CssBaseline/>
            <MuiThemeProvider theme={armadaTheme}>
              <Grid container direction="column" wrap="nowrap" className={classes.root}>
                {navigationIndex === 0 && (
                    <QRSCanner
                        eventId={event_id}
                        handleCheckIn={this.handleCheckIn}
                    />
                )}
                {navigationIndex === 1 && (
                    <ParticipantList
                        handleCheckIn={this.handleCheckIn}
                        handleCheckOut={this.handleCheckOut}
                        participants={participants}
                    />
                )}
                <CounterLine current={current} total={total}/>
                <BottomNavigation
                    value={navigationIndex}
                    onChange={this.handleNavigation}
                    showLabels
                >
                  <BottomNavigationAction label="QR Scan" icon={<QrCodeIcon/>}/>
                  <BottomNavigationAction label="List" icon={<ChecklistIcon/>}/>
                </BottomNavigation>
              </Grid>
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

import React, {Component, Fragment} from 'react';
import {withStyles} from '@material-ui/core/styles';
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
import QRSCanner from "./QRSCanner";
import CounterLine from "./CounterLine";
import sortBy from 'lodash/sortBy';
import filter from 'lodash/filter';
import find from 'lodash/findIndex';

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
  }

  handleNavigation(event, value) {
    this.setState({navigationIndex: value})
  }

  handleCheckIn(id) {
    // TODO Send API call to backend

    this.setState(prevState => {
      const participants = [...prevState.participants];
      const index = find(prevState.participants, {'id': id});
      participants[index].has_checked_in = true;

      return {
        ...prevState,
        participants
      }
    });
  }

  render() {
    const {classes} = this.props;
    const {navigationIndex, participants} = this.state;

    const total = participants.length;
    const current = filter(participants, 'has_checked_in').length;

    return (
        <Fragment>
          <CssBaseline/>
          <MuiThemeProvider theme={armadaTheme}>
            <Grid container direction="column" wrap="nowrap" className={classes.root}>
              {navigationIndex === 0 && (
                  <QRSCanner/>
              )}
              {navigationIndex === 1 && (
                  <ParticipantList
                      handleCheckIn={this.handleCheckIn}
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
    )
  }
}

const AppWithStyles = withStyles(styles)(App);

ReactDOM.render(
    <AppWithStyles/>,
    document.getElementById('react')
);

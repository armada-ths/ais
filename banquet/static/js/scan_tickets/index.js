import React, {Component, Fragment} from 'react';
import ReactDOM from 'react-dom';
import JssProvider from 'react-jss/lib/JssProvider';
import {createGenerateClassName, withStyles} from '@material-ui/core/styles';
import CssBaseline from "@material-ui/core/CssBaseline/CssBaseline";
import QrCodeIcon from 'mdi-material-ui/Qrcode';
import ChecklistIcon from 'mdi-material-ui/FormatListCheckbox';
import MuiThemeProvider from "@material-ui/core/es/styles/MuiThemeProvider";
import armadaTheme from 'armada/theme';
import {createErrorMessage, createSuccessMessage, createWarningMessage} from 'armada/Notification/util';
import TicketList from './TicketList';
import * as API from './api';
import QRScanner from 'armada/QRScanner';
import Grid from "@material-ui/core/Grid/Grid";
import BottomNavigation from "@material-ui/core/BottomNavigation/BottomNavigation";
import BottomNavigationAction from "@material-ui/core/BottomNavigationAction/BottomNavigationAction";

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

    this.state = {
      navigationIndex: 1
    };

    this.handleNavigation = this.handleNavigation.bind(this);
    this.handleScannedToken = this.handleScannedToken.bind(this);
  }

  handleNavigation(event, value) {
    this.setState({navigationIndex: value})
  }

  handleScannedToken(data) {
    return API.checkInByToken(data)
        .then(response => {
          const ticket = response.data.ticket;

          return createSuccessMessage(`${ticket.name} (${ticket.table} - ${ticket.seat})`);
        })
        .catch(reason => {
          if (reason.response.status === 403) {
            return createWarningMessage(reason.response.data.message);
          } else {
            return createErrorMessage(reason.response.data.message);
          }
        });
  }

  render() {
    const {classes} = this.props;
    const {navigationIndex} = this.state;

    return (
        <JssProvider generateClassName={generateClassName}>
          <Fragment>
            <CssBaseline/>
            <MuiThemeProvider theme={armadaTheme}>
              <Grid container direction="column" wrap="nowrap" className={classes.root}>
                {navigationIndex === 0 && (
                    <QRScanner handleData={this.handleScannedToken}/>
                )}
                {navigationIndex === 1 && (
                    <TicketList/>
                )}
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

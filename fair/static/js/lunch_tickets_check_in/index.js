import React, {Component, Fragment} from 'react';
import ReactDOM from 'react-dom';
import JssProvider from 'react-jss/lib/JssProvider';
import {createGenerateClassName, withStyles} from '@material-ui/core/styles';
import CssBaseline from "@material-ui/core/CssBaseline/CssBaseline";
import QrCodeIcon from 'mdi-material-ui/Qrcode';
import ChecklistIcon from 'mdi-material-ui/FormatListCheckbox';
import MuiThemeProvider from "@material-ui/core/es/styles/MuiThemeProvider";
import armadaTheme from 'armada/theme';
import List from './TicketList';
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
  }

  handleNavigation(event, value) {
    this.setState({navigationIndex: value})
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
                {navigationIndex === 1 && (
                    <List/>
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
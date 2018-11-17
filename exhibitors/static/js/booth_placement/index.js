import React, {Component, Fragment} from 'react';
import JssProvider from 'react-jss/lib/JssProvider';
import ReactDOM from 'react-dom';
import {createGenerateClassName, withStyles} from '@material-ui/core/styles';
import CssBaseline from "@material-ui/core/CssBaseline/CssBaseline";
import MuiThemeProvider from "@material-ui/core/es/styles/MuiThemeProvider";
import armadaTheme from 'armada/theme';
import Typography from "@material-ui/core/Typography/Typography";

const generateClassName = createGenerateClassName({
  dangerouslyUseGlobalCSS: false,
  productionPrefix: 'c'
});

const styles = theme => ({});

class App extends Component {
  render() {
    return (
        <JssProvider generateClassName={generateClassName}>
          <Fragment>
            <CssBaseline/>
            <MuiThemeProvider theme={armadaTheme}>
              <Typography color="primary">Placement</Typography>
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

import React, {Component, Fragment} from 'react';
import ReactDOM from 'react-dom';
import Typography from "@material-ui/core/es/Typography/Typography";
import CssBaseline from "@material-ui/core/CssBaseline/CssBaseline";
import {createMuiTheme} from '@material-ui/core/styles';
import MuiThemeProvider from "@material-ui/core/es/styles/MuiThemeProvider";
import Card from "@material-ui/core/es/Card/Card";
import CardContent from "@material-ui/core/es/CardContent/CardContent";

const theme = createMuiTheme({
  palette: {
    primary: {
      main: "#01d690",
      contrastText: "#ffffff"
    },
  }
});

class App extends Component {
  render() {

    return (
        <Fragment>
          <CssBaseline/>
          <MuiThemeProvider theme={theme}>
            <Card>
              <CardContent>
                <Typography variant="title" color="inherit">
                  Armada Runners Again?
                </Typography>
              </CardContent>
            </Card>
          </MuiThemeProvider>
        </Fragment>
    )
  }
}

ReactDOM.render(
    <App/>,
    document.getElementById('react')
);

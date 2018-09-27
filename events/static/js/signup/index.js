import React, {Component, Fragment} from 'react';
import ReactDOM from 'react-dom';
import CssBaseline from "@material-ui/core/CssBaseline/CssBaseline";
import {createMuiTheme} from '@material-ui/core/styles';
import MuiThemeProvider from "@material-ui/core/es/styles/MuiThemeProvider";
import Form from "./Form";

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

    const {event, payment_url, signup_url, fee_payed} = window.reactProps;

    return (
        <Fragment>
          <CssBaseline/>
          <MuiThemeProvider theme={theme}>
            <Form event={event} paymentUrl={payment_url} signupUrl={signup_url} feePayed={fee_payed}/>
          </MuiThemeProvider>
        </Fragment>
    )
  }
}

ReactDOM.render(
    <App/>,
    document.getElementById('react')
);

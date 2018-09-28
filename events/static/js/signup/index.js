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

    const {event, payment_url, signup_url, user} = window.reactProps;

    return (
        <Fragment>
          <CssBaseline/>
          <MuiThemeProvider theme={theme}>
            <span>{user.signup_complete ? 'Yes' : 'No'}</span>
            <Form
                event={event}
                feePayed={user.fee_payed}
                paymentUrl={payment_url}
                signupUrl={signup_url}
            />
          </MuiThemeProvider>
        </Fragment>
    )
  }
}

ReactDOM.render(
    <App/>,
    document.getElementById('react')
);

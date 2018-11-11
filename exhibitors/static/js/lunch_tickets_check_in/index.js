import React, {Component, Fragment} from 'react';
import ReactDOM from 'react-dom';
import JssProvider from 'react-jss/lib/JssProvider';
import {createGenerateClassName} from '@material-ui/core/styles';
import CssBaseline from "@material-ui/core/CssBaseline/CssBaseline";
import Typography from "@material-ui/core/Typography/Typography";
import MuiThemeProvider from "@material-ui/core/es/styles/MuiThemeProvider";
import armadaTheme from 'armada/theme';

const generateClassName = createGenerateClassName({
  dangerouslyUseGlobalCSS: false,
  productionPrefix: 'c'
});

class App extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    const tickets = window.reactProps.lunch_tickets;

    return (
        <JssProvider generateClassName={generateClassName}>
          <Fragment>
            <CssBaseline/>
            <MuiThemeProvider theme={armadaTheme}>
              <Typography color="primary">Hello lunch!</Typography>
              <ul>
                {tickets.map(ticket => (
                    <li key={ticket.id}>
                      {ticket.company}
                    </li>
                ))}
              </ul>
            </MuiThemeProvider>
          </Fragment>
        </JssProvider>
    )
  }
}

ReactDOM.render(
    <App/>,
    document.getElementById('react')
);
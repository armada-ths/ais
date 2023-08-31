import React, {Component, Fragment} from 'react';
import ReactDOM from 'react-dom';
import JssProvider from 'react-jss/lib/JssProvider';
import {createGenerateClassName, withStyles} from '@material-ui/core/styles';
import CssBaseline from "@material-ui/core/CssBaseline/CssBaseline";
import MuiThemeProvider from "@material-ui/core/es/styles/MuiThemeProvider";
import armadaTheme from 'armada/theme';
import Typography from "@material-ui/core/Typography/Typography";
import Ticket from "./Ticket";

const generateClassName = createGenerateClassName({
  dangerouslyUseGlobalCSS: false,
  productionPrefix: 'c'
});

const styles = theme => ({
  root: {
    fontSize: '16px'
  },
});

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      expanded: null
    };

    this.handleChange = this.handleChange.bind(this);
  }

  handleChange(panel) {
    this.setState(prevState => {
      const {expanded} = prevState;
      return {
        expanded: expanded !== panel ? panel : false,
      }
    });
  }

  render() {
    const {classes} = this.props;
    const {expanded} = this.state;
    const {lunch_tickets, banquet_participant} = window.reactProps;

    const hasTickets = lunch_tickets.length > 0 || banquet_participant;

    return (
        <JssProvider generateClassName={generateClassName}>
          <Fragment>
            <CssBaseline/>
            <MuiThemeProvider theme={armadaTheme}>
              <Typography variant="h4" gutterBottom>Tickets</Typography>
              {hasTickets ? (
                  <Fragment>
                    {lunch_tickets.map(ticket =>
                        <Ticket
                            key={ticket.id}
                            id={ticket.id}
                            expanded={expanded === ticket.id}
                            openPanel={this.handleChange}
                            token={ticket.token}
                            title={`Lunch ticket - ${ticket.date}`}
														dietary_restrictions={ticket.dietary_restrictions}
														other_dietary_restrictions={ticket.other_dietary_restrictions}
                        />
                    )}
                    {banquet_participant && (
                        <Ticket
                            id={banquet_participant.id}
                            expanded={expanded === banquet_participant.id}
                            openPanel={this.handleChange}
                            token={banquet_participant.token}
                            title={banquet_participant.title}
														dietary_restrictions={banquet_participant.dietary_restrictions}
														other_dietary_restrictions={banquet_participant.other_dietary_restrictions}
                        />
                    )}
                  </Fragment>
              ) : (
                  <Typography>You have no tickets.</Typography>
              )}
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

import React, {Component} from 'react';
import TextField from "@material-ui/core/TextField/TextField";
import Grid from "@material-ui/core/Grid/Grid";
import * as API from '../api';
import Table from "@material-ui/core/Table/Table";
import TableHead from "@material-ui/core/TableHead/TableHead";
import TableRow from "@material-ui/core/TableRow/TableRow";
import TableCell from "@material-ui/core/TableCell/TableCell";
import TableBody from "@material-ui/core/TableBody/TableBody";
import withStyles from "@material-ui/core/es/styles/withStyles";
import Checkbox from "@material-ui/core/Checkbox/Checkbox";
import CircularProgress from "@material-ui/core/es/CircularProgress/CircularProgress";
import sortBy from 'lodash/sortBy';
import findIndex from 'lodash/findIndex';

const styles = theme => ({
  root: {
    flexGrow: 1,
    margin: '0 auto',
    paddingLeft: theme.spacing.unit * 2,
    paddingRight: theme.spacing.unit * 2,
    height: 0 // Why this works, I do not know
  },
  search: {
    height: 50,
    paddingTop: theme.spacing.unit * 2,
    width: '100%',
  },
  loading: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    height: '100%',
    width: '100%',
  },
  table: {
    overflow: 'scroll'
  },
  nowrap: {
    whiteSpace: 'nowrap'
  }
});

class TicketList extends Component {
  constructor(props) {
    super(props);

    this.state = {
      searchQuery: '',
      tickets: [],
      loading: false
    };

    this.timeoutId = null;

    this.handleSearchQueryChange = this.handleSearchQueryChange.bind(this);
    this.handleCheckboxChange = this.handleCheckboxChange.bind(this);
    this.performSearch = this.performSearch.bind(this);
  }

  componentWillUnmount() {
    if (this.timeoutId) clearTimeout(this.timeoutId);
  }

  handleSearchQueryChange(event) {
    const {value} = event.target;

    if (this.timeoutId) clearTimeout(this.timeoutId);
    this.timeoutId = setTimeout(this.performSearch, 2000);

    this.setState({
      searchQuery: value,
    })
  }

  performSearch() {
    const {searchQuery} = this.state;

    if (searchQuery.trim() !== '') {
      this.setState({loading: true});

      API.search(searchQuery)
          .then(response => {
            const sortedTickets = sortBy(response.data.result, 'date');
            this.setState({
              tickets: sortedTickets,
              loading: false
            })
          });
    }
  }

  handleCheckboxChange(ticketId) {
    const {tickets} = this.state;
    const index = findIndex(tickets, {'id': ticketId});
    const ticketIsUsed = tickets[index].used;

    this.setState(prevState => {
      const tickets = [...prevState.tickets];
      tickets[index].used = !ticketIsUsed;

      return {
        ...prevState,
        tickets
      }
    });

    if (ticketIsUsed) {
      API.checkOut(ticketId);
    } else {
      API.checkIn(ticketId);
    }
  }

  render() {
    const {classes} = this.props;
    const {searchQuery, tickets, loading} = this.state;

    return (
        <Grid container direction="column" wrap="nowrap" className={classes.root}>
          <Grid item className={classes.search}>
            <TextField
                value={searchQuery}
                onChange={this.handleSearchQueryChange}
                placeholder="Search..."
                type="search"
                fullWidth
            />
          </Grid>
          {loading ? (
              <div className={classes.loading}>
                <CircularProgress/>
              </div>
          ) : (
              <Grid item className={classes.table}>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Name</TableCell>
                      <TableCell>Email</TableCell>
                      <TableCell>Day</TableCell>
                      <TableCell>Comment</TableCell>
                      <TableCell>Used</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {tickets.map(ticket => (
                        <TableRow hover key={ticket.id}>
                          <TableCell className={classes.nowrap}>{ticket.name}</TableCell>
                          <TableCell>{ticket.email_address}</TableCell>
                          <TableCell className={classes.nowrap}>{ticket.date}</TableCell>
                          <TableCell>{ticket.comment}</TableCell>
                          <TableCell padding="checkbox">
                            <Checkbox
                                color="primary"
                                checked={ticket.used}
                                onChange={() => this.handleCheckboxChange(ticket.id)}
                            />
                          </TableCell>
                        </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </Grid>
          )}
        </Grid>
    )
  }
}

export default withStyles(styles)(TicketList);

import React, {Component} from 'react';
import TextField from "@material-ui/core/TextField/TextField";
import Grid from "@material-ui/core/Grid/Grid";
import * as API from '../api';
import withStyles from "@material-ui/core/es/styles/withStyles";
import Checkbox from "@material-ui/core/Checkbox/Checkbox";
import CircularProgress from "@material-ui/core/es/CircularProgress/CircularProgress";
import findIndex from 'lodash/findIndex';
import List from "@material-ui/core/List/List";
import ListItem from "@material-ui/core/ListItem/ListItem";
import ListItemText from "@material-ui/core/ListItemText/ListItemText";
import ListItemSecondaryAction from "@material-ui/core/ListItemSecondaryAction/ListItemSecondaryAction";

const styles = theme => ({
  root: {
    flexGrow: 1,
    margin: '0 auto',
    maxWidth: 500,
    height: 0 // Why this works, I do not know
  },
  search: {
    position: 'relative',
    height: 50,
    paddingTop: theme.spacing.unit * 2,
    width: '100%',
  },
  loading: {
    position: 'absolute',
    bottom: 12,
    right: 24
  },
  list: {
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

  componentDidMount() {
    this.performSearch();
  }

  handleSearchQueryChange(event) {
    const {value} = event.target;

    if (this.timeoutId) clearTimeout(this.timeoutId);
    this.timeoutId = setTimeout(this.performSearch, 200);

    this.setState({
      searchQuery: value,
    })
  }

  performSearch() {
    const {searchQuery} = this.state;

    this.setState({loading: true});
    API.search(searchQuery)
      .then(response => {
        this.setState({
          tickets: response.data.result,
          loading: false
        })
      });
  }

  handleCheckboxChange(ticketId) {
    const {tickets} = this.state;
    const index = findIndex(tickets, {'id': ticketId});
    const ticketIsScanned = tickets[index].ticket_scanned;

    this.setState(prevState => {
      const tickets = [...prevState.tickets];
      tickets[index].ticket_scanned = !ticketIsScanned;

      return {
        ...prevState,
        tickets
      }
    });

    if (ticketIsScanned) {
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
            {loading && (
                <CircularProgress
                    size={20}
                    className={classes.loading}
                />
            )}
          </Grid>
          <Grid item className={classes.list}>
            <List>
              {tickets.map(ticket => (
                  <ListItem key={ticket.id} disableGutters>
                    <ListItemText primary={ticket.name} secondary={`${ticket.table} - ${ticket.seat}`}/>
                    <ListItemSecondaryAction>
                      <Checkbox
                          color="primary"
                          checked={ticket.ticket_scanned}
                          onChange={() => this.handleCheckboxChange(ticket.id)}
                      />
                    </ListItemSecondaryAction>
                  </ListItem>
              ))}
            </List>
          </Grid>
        </Grid>
    )
  }
}

export default withStyles(styles)(TicketList);

import React, {Component} from 'react';
import withStyles from "@material-ui/core/es/styles/withStyles";
import TextField from "@material-ui/core/TextField/TextField";
import Grid from "@material-ui/core/Grid/Grid";
import * as API from '../api';
import ListItem from "@material-ui/core/ListItem/ListItem";
import ListItemText from "@material-ui/core/ListItemText/ListItemText";
import ListItemSecondaryAction from "@material-ui/core/ListItemSecondaryAction/ListItemSecondaryAction";
import Checkbox from "@material-ui/core/Checkbox/Checkbox";
import List from "@material-ui/core/List/List";

const styles = theme => ({
  root: {
    flexGrow: 1,
    maxWidth: 500,
    margin: '0 auto',
    height: 0 // Why this works, I do not know
  },
  search: {
    height: 50,
    padding: theme.spacing.unit * 2,
    width: '100%',
  },
  list: {
    overflow: 'scroll'
  },
  listItem: {
    paddingTop: 13,
    paddingBottom: 13
  },
});

class TicketList extends Component {
  constructor(props) {
    super(props);

    this.state = {
      searchQuery: '',
      tickets: []
    };

    this.timeoutId = null;

    this.handleSearchQueryChange = this.handleSearchQueryChange.bind(this);
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
      API.search(searchQuery)
          .then(response => {
            this.setState({tickets: response.data.result})
          });
    }

  }

  render() {
    const {classes} = this.props;
    const {searchQuery, tickets} = this.state;

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
          <Grid item className={classes.list}>
            <List>
              {tickets.map(ticket => (
                  <ListItem className={classes.listItem} key={ticket.id}>
                    <ListItemText primary={ticket.company} secondary={ticket.email_address}/>
                    <ListItemSecondaryAction>
                      <Checkbox
                          color="primary"
                          checked={ticket.used}
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

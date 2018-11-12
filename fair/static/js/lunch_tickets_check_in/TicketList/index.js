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

const styles = theme => ({
  root: {
    flexGrow: 1,
    maxWidth: 900,
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
  nowrap: {
    whiteSpace: 'nowrap'
  }
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
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Company</TableCell>
                  <TableCell>Email</TableCell>
                  <TableCell>Day</TableCell>
                  <TableCell>Comment</TableCell>
                  <TableCell>Used</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {tickets.map(ticket => (
                    <TableRow key={ticket.id}>
                      <TableCell className={classes.nowrap}>{ticket.company}</TableCell>
                      <TableCell>{ticket.email_address}</TableCell>
                      <TableCell className={classes.nowrap}>{ticket.day}</TableCell>
                      <TableCell>{ticket.comment}</TableCell>
                      <TableCell>
                        <Checkbox
                            color="primary"
                            checked={ticket.used}
                        />
                      </TableCell>
                    </TableRow>
                ))}

              </TableBody>
            </Table>
          </Grid>
        </Grid>
    )
  }
}

export default withStyles(styles)(TicketList);

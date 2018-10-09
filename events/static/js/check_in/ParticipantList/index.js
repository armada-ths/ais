import React, {Component} from 'react';
import {withStyles} from '@material-ui/core/styles';
import List from "@material-ui/core/es/List/List";
import ListItem from "@material-ui/core/es/ListItem/ListItem";

import ListItemText from "@material-ui/core/es/ListItemText/ListItemText";
import Grid from "@material-ui/core/es/Grid/Grid";
import ListItemSecondaryAction from "@material-ui/core/es/ListItemSecondaryAction/ListItemSecondaryAction";
import Checkbox from "@material-ui/core/es/Checkbox/Checkbox";
import TextField from "@material-ui/core/es/TextField/TextField";
import includes from 'lodash/includes';
import filter from 'lodash/filter';

const styles = theme => ({
  root: {
    flexGrow: 1,
    maxWidth: 500,
    margin: '0 auto',
    height: 0 // Why this works, I do not know
  },
  list: {
    overflow: 'scroll'
  },
  search: {
    height: 50,
    padding: theme.spacing.unit * 2,
    width: '100%',
  }
});

class ParticipantList extends Component {
  constructor(props) {
    super(props);

    this.state = {
      filterString: '',
      openDialog: false,
    };

    this.handleChange = this.handleChange.bind(this);
    this.handleCheckboxChange = this.handleCheckboxChange.bind(this);
  }

  handleChange(event) {
    const {name, value} = event.target;

    this.setState({
      [name]: value
    })
  }

  handleCheckboxChange(event, id) {
    const {handleCheckIn} = this.props;
    const {checked} = event.target;

    // TODO Show dialog confirming we want to undo a check-in

    if (checked) {
      handleCheckIn(id);
    } else {
      this.setState({
        openDialog: true
      })
    }
  }

  render() {
    const {filterString} = this.state;
    const {classes, participants} = this.props;

    const filteredParticipants = filter(participants, participant => includes(participant.name.toLowerCase(), filterString.toLowerCase()));

    return (
        <Grid container direction="column" wrap="nowrap" className={classes.root}>
          <Grid item className={classes.search}>
            <TextField
                value={filterString}
                name='filterString'
                onChange={this.handleChange}
                placeholder="Filter participants..."
                type="search"
                fullWidth
                autoFocus
            />
          </Grid>
          <Grid item className={classes.list}>
            <List>
              {filteredParticipants.map(participant => (
                  <ListItem key={participant.id}>
                    <ListItemText primary={participant.name}/>
                    <ListItemSecondaryAction>
                      <Checkbox
                          onChange={(event) => this.handleCheckboxChange(event, participant.id)}
                          color="primary"
                          checked={participant.has_checked_in}
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

export default withStyles(styles)(ParticipantList);
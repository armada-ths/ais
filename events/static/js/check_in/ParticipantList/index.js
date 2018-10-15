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
import Dialog from "@material-ui/core/Dialog/Dialog";
import DialogContent from "@material-ui/core/DialogContent/DialogContent";
import DialogContentText from "@material-ui/core/DialogContentText/DialogContentText";
import DialogActions from "@material-ui/core/DialogActions/DialogActions";
import Button from "@material-ui/core/Button/Button";

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
  listItem: {
    paddingTop: 13,
    paddingBottom: 13
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
      dialogOpen: false,
      clickedParticipantName: null,
      clickedParticipantId: null,
    };

    this.handleChange = this.handleChange.bind(this);
    this.handleDialogClose = this.handleDialogClose.bind(this);
    this.handleDialogClosed = this.handleDialogClosed.bind(this);
    this.handleCheckOutConfirmed = this.handleCheckOutConfirmed.bind(this);
    this.handleCheckboxChange = this.handleCheckboxChange.bind(this);
  }

  handleChange(event) {
    const {name, value} = event.target;

    this.setState({
      [name]: value
    })
  }

  handleDialogClose() {
    this.setState({
      dialogOpen: false,
    })
  }

  handleDialogClosed() {
    this.setState({
      clickedParticipantName: null,
      clickedParticipantId: null
    })
  }

  handleCheckOutConfirmed() {
    const {handleCheckOut} = this.props;
    const {clickedParticipantId} = this.state;

    this.setState({
      dialogOpen: false
    });

    handleCheckOut(clickedParticipantId);
  }

  handleCheckboxChange(event, id, name) {
    const {handleCheckIn} = this.props;
    const {checked} = event.target;

    if (checked) {
      handleCheckIn(id);
      this.setState({
        filterString: ''
      });
    } else {
      this.setState({
        dialogOpen: true,
        clickedParticipantName: name,
        clickedParticipantId: id
      })
    }
  }

  render() {
    const {filterString, dialogOpen, clickedParticipantName} = this.state;
    const {classes, participants} = this.props;

    const filteredParticipants = filter(participants, participant =>
        includes(participant.name.toLowerCase(), filterString.toLowerCase())
    );

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
            />
          </Grid>
          <Grid item className={classes.list}>
            <List>
              {filteredParticipants.map(participant => (
                  <ListItem className={classes.listItem} key={participant.id}>
                    <ListItemText primary={participant.name}/>
                    <ListItemSecondaryAction>
                      <Checkbox
                          color="primary"
                          checked={participant.has_checked_in}
                          onChange={event => this.handleCheckboxChange(event, participant.id, participant.name)}
                      />
                    </ListItemSecondaryAction>
                  </ListItem>
              ))}
            </List>
            <Dialog
                open={dialogOpen}
                onClose={this.handleDialogClose}
                onExited={this.handleDialogClosed}
            >
              <DialogContent>
                <DialogContentText>
                  Undo check in of {clickedParticipantName}?
                </DialogContentText>
              </DialogContent>
              <DialogActions>
                <Button onClick={this.handleDialogClose} color="primary">
                  Cancel
                </Button>
                <Button onClick={this.handleCheckOutConfirmed} color="primary" autoFocus>
                  Undo
                </Button>
              </DialogActions>
            </Dialog>
          </Grid>
        </Grid>
    )
  }
}

export default withStyles(styles)(ParticipantList);
import React, {Component, Fragment} from 'react';
import {withStyles} from '@material-ui/core/styles';
import Grid from "@material-ui/core/es/Grid/Grid";
import {createTeam, joinTeam} from "./api";
import * as ACTIONS from './actions';
import Typography from "@material-ui/core/es/Typography/Typography";

const styles = theme => ({
  formControl: {
    margin: theme.spacing.unit,
    minWidth: 120,
  },
  signupText: {
    marginTop: theme.spacing.unit * 2
  }
});

class Manage extends Component {
  constructor(props) {
    super(props);

    this.state = {
      selectedTeamId: null,
      dialogOpen: false
    };

    this.handleSelectTeam = this.handleSelectTeam.bind(this);
    this.handleJoinTeam = this.handleJoinTeam.bind(this);
    this.handleCreateTeam = this.handleCreateTeam.bind(this);
    this.handleDialogOpen = this.handleDialogOpen.bind(this);
    this.handleDialogClose = this.handleDialogClose.bind(this);
  }

  handleSelectTeam(event) {
    const id = event.target.value;

    this.setState({
      selectedTeamId: id
    })
  }

  handleJoinTeam() {
    const {event} = this.props;
    const {selectedTeamId} = this.state;

    joinTeam(event.id, selectedTeamId);
  }

  handleCreateTeam(teamName) {
    const {event, dispatcher} = this.props;

    createTeam(event.id, teamName)
        .then(response => dispatcher({
          type: ACTIONS.UPDATE_TEAM,
          payload: response.data
        }));
  }

  handleDialogOpen() {
    this.setState({dialogOpen: true})
  }

  handleDialogClose() {
    this.setState({dialogOpen: false})
  }

  render() {
    const {teams, classes} = this.props;
    const {selectedTeamId, dialogOpen} = this.state;

    const selectedTeam = teams[selectedTeamId];

    return (
        <Fragment>
          <Grid container spacing={16}>
            <Grid container item xs={12} justify="center">
              <Typography className={classes.signupText} color="primary" variant="display1">
                🎉 You have signed up to this event! 🎉
              </Typography>
            </Grid>

            {/*
            <Grid item sm={6}>
              <Button color="primary" onClick={this.handleDialogOpen}>Create new team</Button>
              <CreateTeamDialog
                  open={dialogOpen}
                  handleClose={this.handleDialogClose}
                  handleCreate={this.handleCreateTeam}
              />
              <Typography variant="caption">
                Open Teams
              </Typography>
              <TextField
                  placeholder="Filter teams"
                  type="search"
                  margin="normal"
              />
              <FormControl className={classes.formControl}>
                <InputLabel htmlFor="open-teams">Open Teams</InputLabel>
                <Select
                    value={selectedTeam ? selectedTeam.id : ''}
                    onChange={this.handleSelectTeam}
                    inputProps={{
                      name: 'open-teams',
                      id: 'open-teams',
                    }}
                >
                  {teams.map(team =>
                      <MenuItem
                          key={team.id}
                          value={team.id}
                      >
                        {team.name} ({team.number_of_members}/{team.capacity})
                      </MenuItem>)}
                </Select>
              </FormControl>
            </Grid>
            <Grid item sm={6}>
              {selectedTeam && (
                  <Team
                      name={selectedTeam.name}
                      leader={selectedTeam.leader}
                      members={selectedTeam.members}
                      canJoin={selectedTeam.number_of_members < selectedTeam.capacity}
                      handleJoinTeam={this.handleJoinTeam}
                  />
              )}
            </Grid>
              */}
          </Grid>
        </Fragment>
    )
  }
}

export default withStyles(styles)(Manage);

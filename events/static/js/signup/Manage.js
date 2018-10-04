import React, {Component, Fragment} from 'react';
import {withStyles} from '@material-ui/core/styles';
import Grid from "@material-ui/core/es/Grid/Grid";
import Team from "./Team";
import CreateTeamDialog from "./CreateTeamDialog";
import {createTeam, joinTeam} from "./api";
import Button from "@material-ui/core/es/Button/Button";
import TextField from "@material-ui/core/es/TextField/TextField";
import Typography from "@material-ui/core/es/Typography/Typography";

const styles = theme => ({
  formControl: {
    margin: theme.spacing.unit,
    minWidth: 120,
  },
});

class Manage extends Component {
  constructor(props) {
    super(props);

    this.state = {
      selectedTeam: null,
      dialogOpen: false
    };

    this.handleSelectTeam = this.handleSelectTeam.bind(this);
    this.handleJoinTeam = this.handleJoinTeam.bind(this);
    this.handleCreateTeam = this.handleCreateTeam.bind(this);
    this.handleDialogOpen = this.handleDialogOpen.bind(this);
    this.handleDialogClose = this.handleDialogClose.bind(this);
  }

  handleSelectTeam(event) {
    const {teams} = this.props;
    const id = event.target.value;

    this.setState({
      selectedTeam: teams.find(team => team.id === id)
    })
  }

  handleJoinTeam() {
    const {event} = this.props;
    const {selectedTeam} = this.state;

    joinTeam(event.id, selectedTeam.id);
  }

  handleCreateTeam(teamName) {
    const {event} = this.props;

    createTeam(event.id, teamName);

  }

  handleDialogOpen() {
    this.setState({dialogOpen: true})
  }

  handleDialogClose() {
    this.setState({dialogOpen: false})
  }

  render() {
    const {teams, classes} = this.props;
    const {selectedTeam, dialogOpen} = this.state;

    return (
        <Fragment>
          <Grid container spacing={16}>
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
              {/*
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
              */}
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
          </Grid>
        </Fragment>
    )
  }
}

export default withStyles(styles)(Manage);

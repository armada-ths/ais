import React, {Component} from 'react';
import {withStyles} from '@material-ui/core/styles';
import Grid from "@material-ui/core/es/Grid/Grid";
import Button from "@material-ui/core/es/Button/Button";
import CreateTeamDialog from "./CreateTeamDialog";
import TeamInformation from "./TeamInformation";
import TeamList from "./TeamList";

const styles = theme => ({
  root: {
    marginTop: theme.spacing.unit * 2,
    paddingTop: theme.spacing.unit * 2,
  },
});

class Teams extends Component {
  constructor(props) {
    super(props);

    this.state = {
      dialogOpen: false,
    };

    this.handleDialogOpen = this.handleDialogOpen.bind(this);
    this.handleDialogClose = this.handleDialogClose.bind(this);
  }

  handleDialogOpen() {
    this.setState({dialogOpen: true})
  }

  handleDialogClose() {
    this.setState({dialogOpen: false})
  }

  render() {
    const {dialogOpen} = this.state;
    const {
      classes,
      teams,
      selectedTeam,
      currentTeam,
      participantId,
      handleCreateTeam,
      handleSelectTeam,
      handleJoinTeam,
      handleLeaveTeam
    } = this.props;

    const isMemberOfSelectedTeam = selectedTeam.id === currentTeam.id;

    const leaderOfSelectedTeam = selectedTeam.members.find(member => member.leader);

    const isLeaderOfSelectedTeam = isMemberOfSelectedTeam && leaderOfSelectedTeam && leaderOfSelectedTeam.participant_id === participantId;

    console.log(isLeaderOfSelectedTeam);

    return (
        <div className={classes.root}>
          <Grid container spacing={16}>
            <Grid
                item
                container
                spacing={16}
                direction="column"
                alignItems="center"
                sm={6}
                xs={12}>
              <Grid item>
                <Button color="primary" variant="outlined" onClick={this.handleDialogOpen}>Create new team</Button>
              </Grid>
              <CreateTeamDialog
                  open={dialogOpen}
                  handleClose={this.handleDialogClose}
                  handleCreate={handleCreateTeam}
              />
              <Grid item>
                <TeamList
                    handleSelectTeam={handleSelectTeam}
                    teams={teams}
                />
              </Grid>
            </Grid>
            <Grid item sm={6} xs={12}>
              {selectedTeam && (
                  <TeamInformation
                      team={selectedTeam}
                      canJoin={selectedTeam.number_of_members < selectedTeam.capacity && selectedTeam.id !== currentTeam.id}
                      canLeave={selectedTeam.id === currentTeam.id}
                      isLeader={isLeaderOfSelectedTeam}
                      handleJoinTeam={handleJoinTeam}
                      handleLeaveTeam={handleLeaveTeam}
                  />
              )}
            </Grid>
          </Grid>
        </div>
    )
  }
}

export default withStyles(styles)(Teams);

import React, {Component} from 'react';
import Grid from "@material-ui/core/es/Grid/Grid";
import Button from "@material-ui/core/es/Button/Button";
import CreateTeamDialog from "./CreateTeamDialog";
import TeamInformation from "./TeamInformation";
import TeamList from "./TeamList";

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
    const {teams, selectedTeam, handleCreateTeam, handleSelectTeam, handleJoinTeam} = this.props;

    return (
        <Grid container spacing={16}>
          <Grid item sm={6} xs={12}>
            <Button color="primary" onClick={this.handleDialogOpen}>Create new team</Button>
            <CreateTeamDialog
                open={dialogOpen}
                handleClose={this.handleDialogClose}
                handleCreate={handleCreateTeam}
            />
            <TeamList
                handleSelectTeam={handleSelectTeam}
                teams={teams}
            />
          </Grid>
          <Grid item sm={6} xs={12}>
            {selectedTeam && (
                <TeamInformation
                    name={selectedTeam.name}
                    leader={selectedTeam.leader}
                    members={selectedTeam.members}
                    canJoin={selectedTeam.number_of_members < selectedTeam.capacity}
                    handleJoinTeam={handleJoinTeam}
                />
            )}
          </Grid>
        </Grid>
    )
  }
}

export default Teams;

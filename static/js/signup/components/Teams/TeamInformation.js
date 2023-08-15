import React, {Component} from 'react';
import {withStyles} from '@material-ui/core/styles';
import List from "@material-ui/core/es/List/List";
import ListItem from "@material-ui/core/es/ListItem/ListItem";
import ListItemText from "@material-ui/core/es/ListItemText/ListItemText";
import ListItemSecondaryAction from "@material-ui/core/es/ListItemSecondaryAction/ListItemSecondaryAction";
import Divider from "@material-ui/core/es/Divider/Divider";
import ListItemIcon from "@material-ui/core/es/ListItemIcon/ListItemIcon";
import AddPeopleIcon from 'mdi-material-ui/AccountPlus';
import RemovePeopleIcon from 'mdi-material-ui/AccountRemove';
import CloseIcon from 'mdi-material-ui/Close';
import EditIcon from 'mdi-material-ui/Pencil';
import CheckIcon from 'mdi-material-ui/Check';
import Typography from "@material-ui/core/Typography/Typography";
import IconButton from "@material-ui/core/IconButton/IconButton";
import Input from "@material-ui/core/Input/Input";
import InputAdornment from "@material-ui/core/InputAdornment/InputAdornment";
import reject from 'lodash/reject';

const styles = theme => ({
  input: {
    color: theme.palette.text.primary
  }
});

class TeamInformation extends Component {
  constructor(props) {
    super(props);

    this.state = {
      editing: false,
      name: props.team.name
    };

    this.handleInputButton = this.handleInputButton.bind(this);
    this.handleRemoveMember = this.handleRemoveMember.bind(this);
    this.handleChange = this.handleChange.bind(this);
  }

  handleInputButton() {
    const {handleUpdateTeam, team} = this.props;

    this.setState(prevState => {
      if (prevState.editing) {

        if (prevState.name !== team.name) {
          handleUpdateTeam(team.id, {
            name: prevState.name,
            members: team.members
          });
        }

        return {
          editing: false
        }
      }

      return {
        editing: true
      }
    })
  }

  handleRemoveMember(teamMemberId) {
    const {handleUpdateTeam, team} = this.props;

    const updatedTeamMembers = reject(team.members, {'id': teamMemberId});

    handleUpdateTeam(team.id, {
      name: team.name,
      members: updatedTeamMembers
    });
  }

  handleChange(event) {
    const {name, value} = event.target;
    this.setState({
      [name]: value
    })
  }

  render() {
    const {editing, name} = this.state;
    const {
      classes,
      team,
      canJoin,
      isCurrentTeam,
      isLeader,
      participantId,
      handleJoinTeam,
      handleLeaveTeam
    } = this.props;

    const inputError = name.trim().length === 0;

    return (
        <div className={classes.root}>
          {isLeader ? (
              <Input
                  type="text"
                  name="name"
                  onChange={this.handleChange}
                  classes={{disabled: classes.input}}
                  error={inputError}
                  value={name}
                  disabled={!editing}
                  disableUnderline={!editing}
                  fullWidth
                  endAdornment={
                    <InputAdornment position="end">
                      <IconButton disabled={editing && inputError} onClick={this.handleInputButton} aria-label="Delete">
                        {editing ? <CheckIcon/> : <EditIcon/>}
                      </IconButton>
                    </InputAdornment>
                  }
              />
          ) : (
              <Typography gutterBottom variant="subtitle1">{team.name}</Typography>
          )}
          <List disablePadding>
            {team.members.map(({id, name, leader, participant_id}) =>
                <ListItem disableGutters key={id}>
                  <ListItemText primary={name} secondary={leader ? 'Leader' : ''}/>
                  {isLeader && participantId !== participant_id && (
                      <ListItemSecondaryAction>
                        <IconButton onClick={() => this.handleRemoveMember(id)}>
                          <CloseIcon/>
                        </IconButton>
                      </ListItemSecondaryAction>
                  )}
                </ListItem>
            )}
            <Divider/>
            {canJoin && (
                <ListItem disableGutters button onClick={handleJoinTeam}>
                  <ListItemIcon>
                    <AddPeopleIcon/>
                  </ListItemIcon>
                  <ListItemText primary="Join team"/>
                </ListItem>
            )}
            {isCurrentTeam && (
                <ListItem disableGutters button onClick={handleLeaveTeam}>
                  <ListItemIcon>
                    <RemovePeopleIcon/>
                  </ListItemIcon>
                  <ListItemText primary="Leave team"/>
                </ListItem>
            )}
          </List>
        </div>
    )
  }
}

export default withStyles(styles)(TeamInformation);
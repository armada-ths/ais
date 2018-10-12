import React, {Component} from 'react';
import {withStyles} from '@material-ui/core/styles';
import List from "@material-ui/core/es/List/List";
import ListItem from "@material-ui/core/es/ListItem/ListItem";
import ListItemText from "@material-ui/core/es/ListItemText/ListItemText";
import Divider from "@material-ui/core/es/Divider/Divider";
import ListItemIcon from "@material-ui/core/es/ListItemIcon/ListItemIcon";
import AddPeopleIcon from 'mdi-material-ui/AccountPlus';
import RemovePeopleIcon from 'mdi-material-ui/AccountRemove';
import Typography from "@material-ui/core/Typography/Typography";
import TextField from "@material-ui/core/TextField/TextField";

const styles = theme => ({
  root: {
    paddingLeft: theme.spacing.unit * 2,
    paddingRight: theme.spacing.unit * 2,
  },
});

class TeamInformation extends Component {
  render() {
    const {
      classes,
      team,
      canJoin,
      canLeave,
      isLeader,
      handleJoinTeam,
      handleLeaveTeam
    } = this.props;

    return (
        <div className={classes.root}>
          {isLeader ? (
              <TextField
                  value={team.name}
                  fullWidth
              />
          ) : (
              <Typography gutterBottom variant="subtitle1">{team.name}</Typography>
          )}
          <Divider/>
          <List disablePadding>
            {team.members.map(({name, leader}) =>
                <ListItem disableGutters key={name}>
                  <ListItemText primary={name} secondary={leader ? 'Leader' : ''}/>
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
            {canLeave && (
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
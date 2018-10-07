import React, {Component, Fragment} from 'react';
import List from "@material-ui/core/es/List/List";
import ListItem from "@material-ui/core/es/ListItem/ListItem";
import ListItemText from "@material-ui/core/es/ListItemText/ListItemText";
import Divider from "@material-ui/core/es/Divider/Divider";
import ListSubheader from "@material-ui/core/es/ListSubheader/ListSubheader";
import ListItemIcon from "@material-ui/core/es/ListItemIcon/ListItemIcon";
import AddPeopleIcon from 'mdi-material-ui/AccountPlus';
import RemovePeopleIcon from 'mdi-material-ui/AccountRemove';


class TeamInformation extends Component {
  render() {
    const {name, members, canJoin, handleJoinTeam, handleLeaveTeam} = this.props;

    return (
        <Fragment>
          <List disablePadding subheader={<ListSubheader disableGutters>Members of {name}</ListSubheader>}>
            {members.map(({name, leader}) =>
                <ListItem key={name}>
                  <ListItemText primary={name} secondary={leader ? 'Leader' : ''}/>
                </ListItem>
            )}
            <Fragment>
              <Divider/>
              <ListItem button disabled={!canJoin} onClick={handleJoinTeam}>
                <ListItemIcon>
                  <AddPeopleIcon/>
                </ListItemIcon>
                <ListItemText primary="Join team"/>
              </ListItem>
              <ListItem button disabled={!canJoin} onClick={handleLeaveTeam}>
                <ListItemIcon>
                  <RemovePeopleIcon/>
                </ListItemIcon>
                <ListItemText primary="Leave team"/>
              </ListItem>
            </Fragment>
          </List>
        </Fragment>
    )
  }
}

export default TeamInformation;
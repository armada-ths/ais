import React, {Component, Fragment} from 'react';
import List from "@material-ui/core/es/List/List";
import ListItem from "@material-ui/core/es/ListItem/ListItem";
import ListItemText from "@material-ui/core/es/ListItemText/ListItemText";
import Divider from "@material-ui/core/es/Divider/Divider";
import ListSubheader from "@material-ui/core/es/ListSubheader/ListSubheader";


class Team extends Component {
  render() {
    const {name, leader, members, canJoin, handleJoinTeam} = this.props;

    return (
        <Fragment>
          <List disablePadding subheader={<ListSubheader disableGutters>Members of {name}</ListSubheader>}>
            {leader && (
                <ListItem>
                  <ListItemText primary={leader} secondary="Leader"/>
                </ListItem>
            )}
            {members.map(member =>
                <ListItem key={member}>
                  <ListItemText primary={member}/>
                </ListItem>
            )}
            <Fragment>
              <Divider/>
              <ListItem button disabled={!canJoin} onClick={handleJoinTeam}>
                <ListItemText primary="Join team"/>
              </ListItem>
            </Fragment>
          </List>
        </Fragment>
    )
  }
}

export default Team;
import React, {Component, Fragment} from 'react';
import {withStyles} from '@material-ui/core/styles';
import TextField from "@material-ui/core/es/TextField/TextField";
import List from "@material-ui/core/es/List/List";
import map from 'lodash/map';
import filter from 'lodash/filter';
import includes from 'lodash/includes';
import sortBy from 'lodash/sortBy';
import size from 'lodash/size';
import ListItem from "@material-ui/core/es/ListItem/ListItem";
import ListItemText from "@material-ui/core/es/ListItemText/ListItemText";
import Typography from "@material-ui/core/es/Typography/Typography";

const styles = theme => ({
  list: {
    maxHeight: 300,
    overflow: 'scroll'
  },
});

class TeamList extends Component {
  constructor(props) {
    super(props);

    this.state = {
      search: ''
    };

    this.handleChange = this.handleChange.bind(this);
  };

  handleChange(event) {
    const {name, value} = event.target;

    this.setState({
      [name]: value,
    })
  }

  render() {
    const {search} = this.state;
    const {classes, teams, handleSelectTeam} = this.props;

    const filteredTeams = filter(teams, team => includes(team.name.toLowerCase(), search.toLowerCase()));

    const sortedTeams = sortBy(filteredTeams, 'name');

    return (
        <Fragment>
          {size(teams) > 0 ? (
              <Fragment>
                <TextField
                    name="search"
                    value={search}
                    onChange={this.handleChange}
                    fullWidth
                    placeholder="Teams..."
                />
                <List className={classes.list}>
                  {map(sortedTeams, team => (
                      <ListItem key={team.id} button onClick={() => handleSelectTeam(team.id)}>
                        <ListItemText
                            primary={team.name}
                        />
                        <ListItemText
                            primaryTypographyProps={{
                              align: 'right',
                              variant: 'body1',
                              color: 'textSecondary'
                            }}
                            primary={`${team.number_of_members} / ${team.capacity}`}
                        />
                      </ListItem>
                  ))}
                </List>
              </Fragment>
          ) : (
              <Typography align="center" variant="body1">
                No teams exist yet!
              </Typography>
          )}


        </Fragment>
    )
  }
}

export default withStyles(styles)(TeamList);
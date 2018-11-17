import React, {Component, Fragment} from 'react';
import JssProvider from 'react-jss/lib/JssProvider';
import ReactDOM from 'react-dom';
import {createGenerateClassName, withStyles} from '@material-ui/core/styles';
import CssBaseline from "@material-ui/core/CssBaseline/CssBaseline";
import MuiThemeProvider from "@material-ui/core/es/styles/MuiThemeProvider";
import armadaTheme from 'armada/theme';
import Select from "@material-ui/core/Select/Select";
import FormControl from "@material-ui/core/FormControl/FormControl";
import MenuItem from "@material-ui/core/MenuItem/MenuItem";
import InputLabel from "@material-ui/core/InputLabel/InputLabel";
import keyBy from 'lodash/keyBy';
import map from 'lodash/map';
import PlaceBooth from "./PlaceBooth";
import Grid from "@material-ui/core/Grid/Grid";

const generateClassName = createGenerateClassName({
  dangerouslyUseGlobalCSS: false,
  productionPrefix: 'c'
});

const styles = theme => ({
  formControl: {
    margin: theme.spacing.unit,
    minWidth: 120,
  },
});

class App extends Component {
  constructor(props) {
    super(props);

    const {locations} = window.reactProps;

    this.state = {
      locations: keyBy(locations, 'id'),
      selectedLocationId: ""
    };
    this.handleChange = this.handleChange.bind(this);
  }

  handleChange(event) {
    this.setState({[event.target.name]: event.target.value});
  };

  render() {
    const {classes} = this.props;
    const {selectedLocationId, locations} = this.state;

    const selectedLocation = selectedLocationId !== "" ? locations[selectedLocationId] : null;

    return (
        <JssProvider generateClassName={generateClassName}>
          <Fragment>
            <CssBaseline/>
            <MuiThemeProvider theme={armadaTheme}>
              <Grid container direction="column">
                <Grid item>
                  <FormControl className={classes.formControl}>
                    <InputLabel htmlFor="location">Location</InputLabel>
                    <Select
                        value={selectedLocationId}
                        onChange={this.handleChange}
                        inputProps={{
                          name: 'selectedLocationId',
                          id: 'selectedLocationId',
                        }}
                    >
                      {map(locations, location => (
                          <MenuItem
                              key={location.id}
                              value={location.id}
                          >
                            {location.name}
                          </MenuItem>
                      ))}
                    </Select>
                  </FormControl>
                </Grid>
                <Grid item>
                  {selectedLocation && (
                      <PlaceBooth map={selectedLocation.map}/>
                  )}
                </Grid>
              </Grid>
            </MuiThemeProvider>
          </Fragment>
        </JssProvider>
    )
  }
}

const AppWithStyles = withStyles(styles)(App);

ReactDOM.render(
    <AppWithStyles/>,
    document.getElementById('react')
);

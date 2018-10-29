import React, {Component, Fragment} from 'react';
import Typography from "@material-ui/core/es/Typography/Typography";
import Grid from "@material-ui/core/es/Grid/Grid";

class Header extends Component {
  render() {
    const {event} = this.props;

    return (
        <Fragment>
          <Typography variant="display2" color="primary" gutterBottom>
            {event.name}
          </Typography>
          <Typography paragraph>
            {event.description}
          </Typography>
          <Grid container spacing={16}>
            {event.location && (
                <Grid item sm={6}>
                  <Typography variant="caption" gutterBottom>
                    Location
                  </Typography>
                  <Typography>
                    {event.location}
                  </Typography>
                </Grid>
            )}
            {event.food && (
                <Grid item sm={6}>
                  <Typography variant="caption" gutterBottom>
                    Food
                  </Typography>
                  <Typography>
                    {event.food}
                  </Typography>
                </Grid>
            )}
            {event.external_event_link && (
                <Grid item sm={6}>
                  <Typography variant="caption" gutterBottom>
                    More information
                  </Typography>
                  <Typography component="a" target="_blank" rel="noopener noreferrer" href={event.external_event_link} color="primary"
                              gutterBottom>
                    {event.external_event_link}
                  </Typography>
                </Grid>
            )}
          </Grid>
        </Fragment>
    )
  }
}

export default Header;

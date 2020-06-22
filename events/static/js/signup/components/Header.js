import React, {Component, Fragment} from 'react';
import {withStyles} from '@material-ui/core/styles';
import Typography from "@material-ui/core/es/Typography/Typography";
import Grid from "@material-ui/core/es/Grid/Grid";

const styles = theme => ({
  description: {
    whiteSpace: 'pre-line'
  }
});

class Header extends Component {
  render() {
    const {event, classes} = this.props;

    return (
        <Fragment>
          <Typography variant="display2" color="primary" gutterBottom>
            {event.name}
          </Typography>
          <Typography className={classes.description} paragraph>
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
						{event.event_start_string && (
								<Grid item sm={6}>
									<Typography variant="caption" gutterBottom>
										Time
									</Typography>
									<Typography>
										{event.event_start_string} 
									</Typography>
								</Grid>
						)}
            {event.contact_email && (
              <Grid item sm={6}>
                <Typography variant="caption" gutterBottom>
                  Contact e-mail
                </Typography>
                <Typography component="a" target="_blank" href={"mailto:"+event.contact_email} color="primary">
                  {event.contact_email}
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

export default withStyles(styles)(Header);

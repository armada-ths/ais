import React, {Component} from 'react';
import {withStyles} from '@material-ui/core/styles';
import Button from "@material-ui/core/es/Button/Button";
import Grid from "@material-ui/core/es/Grid/Grid";
import Typography from "@material-ui/core/es/Typography/Typography";

const styles = theme => ({
  root: {
    marginTop: theme.spacing.unit * 2,
    paddingTop: theme.spacing.unit * 6,
    paddingBottom: theme.spacing.unit * 6,
  },
});

class Deregister extends Component {

  handleClick() {
    
  };

  render() {
    const {event, classes} = this.props;
    

  
    return (
        <div className={classes.root}>
          <Grid container justify="center" alignItems="center" direction="column" spacing={24}>
          <Button
	                
	                onClick={this.handleClick}
	                variant="contained"
	                color="primary"
									style={{marginTop: 10}}
	            >
	              {"Deregister"}
	            </Button>
            <Grid item>
              <Typography variant="subtitle1">
                Click on this button to deregister from this event. Be aware that you will not be able to reverse the decision!
              </Typography>
            </Grid>
          </Grid>
        </div>
    )
  }
}



export default withStyles(styles)(Deregister);
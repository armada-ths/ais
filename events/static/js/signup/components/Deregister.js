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

  constructor(props) {
    super(props);

    this.state = {
      search: ''
    };

  };
  

 
  render() {
    const {search} = this.state;
    const {event, classes, handleDeregister} = this.props;
    

  
    return (
        <div className={classes.root}>
          <Grid container justify="center" alignItems="center" direction="column" spacing={30}>
            <Grid item>
              <Button
	                
	                onClick={() => handleDeregister()}
	                variant="contained"
	                color="primary"
									style={{marginTop: 10}}
	            >
	              {"Deregister"}
	            </Button>
            </Grid>
            <Grid item style={{ marginTop: 15 }}>
              <Typography variant="subtitle1" align="center" topmargin >
                Click to deregister from this event. <br></br>
                This action is permanent and cannot be undone. You will lose your spot in the event. 
              </Typography>
            </Grid>
          </Grid>
        </div>
    )
  }
}



export default withStyles(styles)(Deregister);
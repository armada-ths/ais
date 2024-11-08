import React, {Component, Fragment} from 'react';
import Typography from "@material-ui/core/es/Typography/Typography";
import Button from "@material-ui/core/es/Button/Button";
import Grid from "@material-ui/core/es/Grid/Grid";


class WaitingListPage extends Component {
  constructor(props) {
    super(props);  
  }


  render() {
    const {event} = this.props;
    
   
    return (
        <Grid container spacing={16}>
        <div className='image-section' >
          {
            event.image_url && (
              <img alt='Event image' src={event.image_url} style={{"max-width":"100%",}}/>
            )
          }
        </div>
    
            
        <Grid item sm={12}>
                    <Typography style={{marginTop: 8}}>By signing up you agree to THS Armada's <a href="https://docs.google.com/document/d/14_dUZHTL6QUNF9UeL7fghJXO1wZimbi_aKG5ttcGd1s/edit#heading=h.hpqg0xn5jl2q" target="_blank" rel="noopener noreferrer" style={{ color: "#00d790" }}>Privacy Notice</a>.</Typography>
        
        <Typography style={{marginTop: 16, color: "#d73030", fontSize: 18 }}>
        {'You have already joined the waiting list for this event.'}
        </Typography>
        <Typography style={{marginTop: 16, fontSize: 18 }}>
        {'If a spot opens up for you, you will automatically be added to the event. Even if you do not get a spot, you can still come to the physical location of the event on the day of: if registered attendees do not show up, you (and all other people on the waiting list) will be given a spot on a first-come first-served basis.'}
        </Typography>
        
        <Button
            disabled="true"
            variant="contained"
            color="primary"
            style={{marginTop: 10}}
        >
            {"Not open for sign up"}
        </Button>
        
        <Button
            disabled="true"
            variant="contained"
            color="secondary"
            style={{marginTop: 10, marginLeft: 20}}
        >
            {"Join Waiting List"}
        </Button>
            
        </Grid>
			
        </Grid>
    )
  }
}

export default WaitingListPage;
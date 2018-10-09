import React, {Component} from 'react';
import {withStyles} from '@material-ui/core/styles';
import jsQR from 'jsqr';
import CameraIcon from 'mdi-material-ui/Camera';
import CameraOffIcon from 'mdi-material-ui/CameraOff';
import Button from "@material-ui/core/es/Button/Button";
import Grid from "@material-ui/core/es/Grid/Grid";

const styles = theme => ({
  root: {
    position: 'relative',
    flexGrow: 1,
    maxWidth: 500,
    margin: '0 auto',
    height: 0 // Why this works, I do not know
  },
  video: {
    height: '100%',
    width: '100%',
    objectFit: 'cover'
  }
});

class QRSCanner extends Component {
  constructor(props) {
    super(props);

    this.state = {
      ready: false,
      paused: false,
      data: 'No data'
    };

    this.videoRef = React.createRef();
    this.canvasRef = React.createRef();

    this.tick = this.tick.bind(this);
    this.handlePause = this.handlePause.bind(this);
  }

  componentDidMount() {
    this.canvasCtx = this.canvasRef.current.getContext('2d');

    navigator.mediaDevices.getUserMedia({
      video: {
        facingMode: 'environment',
        width: {
          ideal: 1280
        },
        height: {
          ideal: 720
        }
      }
    }).then(stream => {
      this.videoRef.current.srcObject = stream;
      this.videoRef.current.onloadedmetadata = () => {
        this.setState({ready: true, paused: false});
        this.videoRef.current.play();
        // requestAnimationFrame(this.tick);
      };
    }).catch(reason => console.dir(reason));
  }

  tick() {
    const canvasElement = this.canvasRef.current;
    const video = this.videoRef.current;

    console.log("Tick!");
    canvasElement.height = video.videoHeight;
    canvasElement.width = video.videoWidth;

    this.canvasCtx.drawImage(video, 0, 0, canvasElement.width, canvasElement.height);
    const imageData = this.canvasCtx.getImageData(0, 0, canvasElement.width, canvasElement.height);

    const code = jsQR(imageData.data, imageData.width, imageData.height, {
      inversionAttempts: "dontInvert",
    });

    if (code && code.data !== "") {
      this.setState({data: code.data});
    } else {
      requestAnimationFrame(this.tick)
    }
  }

  handlePause() {
    this.videoRef.current.srcObject.getTracks()[0].enabled = this.state.paused;
    this.setState(prevState => ({
      paused: !prevState.paused
    }));
  }

  render() {
    const {classes} = this.props;
    const {ready, paused, data} = this.state;

    return (
        <Grid container direction="column" wrap="nowrap" className={classes.root}>
          <video
              className={classes.video}
              playsInline
              ref={this.videoRef}
          />
          <canvas style={{display: 'none'}} ref={this.canvasRef}/>
          <Button style={{position: 'absolute', bottom: '16px', right: '16px'}} variant="fab" color="primary" onClick={this.handlePause}>
            {paused ? (
                <CameraIcon/>
            ) : (
                <CameraOffIcon/>
            )}
          </Button>
        </Grid>
    )
  }
}

export default withStyles(styles)(QRSCanner);

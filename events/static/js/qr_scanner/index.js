import React, {Component, Fragment} from 'react';
import jsQR from 'jsqr';
import {withStyles} from '@material-ui/core/styles';
import theme from '../theme';
import ReactDOM from 'react-dom';
import MuiThemeProvider from "@material-ui/core/es/styles/MuiThemeProvider";
import CssBaseline from "@material-ui/core/es/CssBaseline/CssBaseline";
import Typography from "@material-ui/core/es/Typography/Typography";
import Button from "@material-ui/core/es/Button/Button";

const styles = theme => ({
  video: {
    backgroundColor: theme.palette.primary.main,
    height: 400,
    width: '100%'
  },
});

class App extends Component {
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
    this.drawLine = this.drawLine.bind(this);
  }

  componentDidMount() {
    this.canvasCtx = this.canvasRef.current.getContext('2d');

    console.log(this.canvasCtx);

    navigator.mediaDevices.getUserMedia({
      video: {
        facingMode: 'environment', width: {ideal: 1280},
        height: {ideal: 720}
      }
    })
        .then(stream => {
          this.videoRef.current.srcObject = stream;
          this.videoRef.current.onloadedmetadata = () => {
            this.setState({ready: true, paused: false});
            this.videoRef.current.play();
            requestAnimationFrame(this.tick);
          };
        })
        .catch(reason => console.dir(reason));
  }

  drawLine(begin, end, color) {
    this.canvasCtx.beginPath();
    this.canvasCtx.moveTo(begin.x, begin.y);
    this.canvasCtx.lineTo(end.x, end.y);
    this.canvasCtx.lineWidth = 6;
    this.canvasCtx.strokeStyle = color;
    this.canvasCtx.stroke();
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
      this.drawLine(code.location.topLeftCorner, code.location.topRightCorner, "#FF3B58");
      this.drawLine(code.location.topRightCorner, code.location.bottomRightCorner, "#FF3B58");
      this.drawLine(code.location.bottomRightCorner, code.location.bottomLeftCorner, "#FF3B58");
      this.drawLine(code.location.bottomLeftCorner, code.location.topLeftCorner, "#FF3B58");
    } else {
      if (!this.state.paused)
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
        <Fragment>
          <CssBaseline/>
          <MuiThemeProvider theme={theme}>
            <video
                playsInline
                ref={this.videoRef}
                className={classes.video}
            />
            <canvas style={{display: 'none'}} ref={this.canvasRef}/>
            <Typography variant="headline">{ready ? 'Ready!' : 'Not ready...'}</Typography>
            <Typography variant="headline">{data}</Typography>
            <Button disabled={!ready} onClick={this.handlePause}>{paused ? 'Play' : 'Pause'}</Button>
          </MuiThemeProvider>
        </Fragment>
    )
  }
}

const AppWithStyles = withStyles(styles)(App);

ReactDOM.render(
    <AppWithStyles/>,
    document.getElementById('react')
);

import React, {Component} from 'react';
import {withStyles} from '@material-ui/core/styles';
import * as API from '../api';
import CameraIcon from 'mdi-material-ui/Camera';
import CameraOffIcon from 'mdi-material-ui/CameraOff';
import Button from "@material-ui/core/es/Button/Button";
import Grid from "@material-ui/core/es/Grid/Grid";
import classNames from 'classnames';
import Notification from "./Notification";
import CircularProgress from "@material-ui/core/es/CircularProgress/CircularProgress";
import jsQR from "jsqr";

const styles = theme => ({
  root: {
    position: 'relative',
    flexGrow: 1,
    maxWidth: 500,
    margin: '0 auto',
    height: 0 // Why this works, I do not know
  },
  loading: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    height: '100%',
    width: '100%',
  },
  video: {
    height: '100%',
    width: '100%',
    objectFit: 'cover'
  },
  hidden: {
    display: 'none'
  }
});

class Index extends Component {
  constructor(props) {
    super(props);

    this.notificationQueue = [];

    this.state = {
      ready: false,
      paused: false,
      notificationOpen: false,
      notificationInfo: {}
    };

    this.videoRef = React.createRef();
    this.canvasRef = React.createRef();

    this.timeoutId = null;

    this.tick = this.tick.bind(this);
    this.handleTogglePause = this.handleTogglePause.bind(this);
    this.handleFoundData = this.handleFoundData.bind(this);
    this.queueNotification = this.queueNotification.bind(this);
    this.processQueue = this.processQueue.bind(this);
    this.handleNotificationClose = this.handleNotificationClose.bind(this);
    this.handleNotificationClosed = this.handleNotificationClosed.bind(this);
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
        this.setState({
          ready: true,
          paused: false
        });
        this.videoRef.current.play();

        this.tick();
      };
    }).catch(reason => {
      this.queueNotification({
        text: `Error when starting camera: ${reason.message}`,
        type: "error"
      });
    });
  }

  componentWillUnmount() {
    this.videoRef.current.onloadedmetadata = null;
    clearTimeout(this.timeoutId);
  }

  tick() {
    const canvasElement = this.canvasRef.current;
    const video = this.videoRef.current;

    canvasElement.height = video.videoHeight;
    canvasElement.width = video.videoWidth;

    this.canvasCtx.drawImage(video, 0, 0, canvasElement.width, canvasElement.height);
    const imageData = this.canvasCtx.getImageData(0, 0, canvasElement.width, canvasElement.height);

    const code = jsQR(imageData.data, imageData.width, imageData.height, {
      inversionAttempts: "dontInvert",
    });

    if (code && code.data !== "") {
      this.handleFoundData(code.data);
    } else {
      this.timeoutId = setTimeout(this.tick, 100);
    }
  }

  handleFoundData(data) {
    const {eventId} = this.props;

    API.getByCheckInToken(eventId, data)
        .then(response => {
          this.props.handleCheckIn(response.data.participant.id);

          this.queueNotification({
            text: `${response.data.participant.name} checked in!`,
            type: "success"
          });
        })
        .catch(reason => {
          this.queueNotification({
            text: `${data} is not a valid code.`,
            type: "error"
          });
        })
        .then(() => {
          this.timeoutId = setTimeout(this.tick, 2000);
        });
  }

  queueNotification(message) {
    const {notificationOpen} = this.state;

    this.notificationQueue.push({
      ...message,
      key: new Date().getTime()
    });

    if (notificationOpen) {
      this.setState({
        notificationOpen: false
      });
    } else {
      this.processQueue();
    }
  }

  processQueue() {
    if (this.notificationQueue.length > 0) {
      this.setState({
        notificationInfo: this.notificationQueue.shift(),
        notificationOpen: true,
      })
    }
  }

  handleNotificationClose(event, reason) {
    if (reason === 'clickaway') return;

    this.setState({
      notificationOpen: false,
    });
  }

  handleNotificationClosed() {
    this.processQueue();
  }

  handleTogglePause() {
    this.setState(prevState => {
      if (prevState.paused) {
        this.videoRef.current.srcObject.getTracks()[0].enabled = true;

        this.tick();

        return {
          paused: false
        }
      } else {
        this.videoRef.current.srcObject.getTracks()[0].enabled = false;

        clearTimeout(this.timeoutId);

        return {
          paused: true
        }
      }
    });
  }

  render() {
    const {classes} = this.props;
    const {ready, paused, notificationInfo, notificationOpen} = this.state;

    return (
        <Grid container direction="column" wrap="nowrap" className={classes.root}>
          {!ready && (
              <div className={classes.loading}>
                <CircularProgress/>
              </div>
          )}
          <video
              className={classNames(classes.video, {[classes.hidden]: !ready})}
              playsInline
              ref={this.videoRef}
          />
          <canvas style={{display: 'none'}} ref={this.canvasRef}/>
          {ready && (
              <Button
                  variant="fab"
                  color="primary"
                  style={{position: 'absolute', bottom: '16px', right: '16px'}}
                  onClick={this.handleTogglePause}
              >
                {paused ? <CameraIcon/> : <CameraOffIcon/>}
              </Button>
          )}
          <Notification
              open={notificationOpen}
              message={notificationInfo}
              onClose={this.handleNotificationClose}
              onExited={this.handleNotificationClosed}
          />
        </Grid>
    )
  }
}

export default withStyles(styles)(Index);

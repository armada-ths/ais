import React, {Component} from 'react';
import {withStyles} from '@material-ui/core/styles';

const styles = theme => ({
  canvas: {
    border: 'solid 1px #CCC',
    cursor: 'crosshair'
  },
});

const EPS = 18; // How many pixels away we want to snap to start of path
const TARGET_WIDTH = 900;

const addToPath = (path, x, y) => {
  const [first, ...rest] = path;

  if (first) {
    const xDist = Math.abs(first[0] - x);
    const yDist = Math.abs(first[1] - y);

    if (xDist < EPS && yDist < EPS) {
      return [...path, first];
    }
  }

  return [...path, [x, y]];
};

const drawPath = (ctx, path, color = 'black') => {
  if (path.length < 2) new Error("Path length is < 2");

  const [first, ...rest] = path;

  ctx.strokeStyle = color;
  ctx.beginPath();
  ctx.moveTo(first[0], first[1]);
  for (let point of rest) {
    ctx.lineTo(point[0], point[1]);
  }
  ctx.stroke();

  ctx.strokeStyle = 'black';
};

class PlaceBooth extends Component {
  constructor(props) {
    super(props);

    this.canvasRef = React.createRef();

    this.state = {
      currentPath: []
    };

    this.handleCanvasClick = this.handleCanvasClick.bind(this);
  }

  componentDidMount() {
    const {map} = this.props;

    const scaledWidth = TARGET_WIDTH;

    const ratio = scaledWidth * 1.0 / map.width;

    const scaledHeight = map.height * ratio;

    this.canvasRef.current.width = scaledWidth;
    this.canvasRef.current.height = scaledHeight;

    this.backgroundImage = new Image(scaledWidth, scaledHeight);

    this.backgroundImage.onload = () => {
      console.log(this.backgroundImage.width, this.backgroundImage.height);
      this.drawCanvas();
    };

    this.backgroundImage.src = map.url;
  }

  drawCanvas() {
    const {currentPath} = this.state;

    const ctx = this.canvasRef.current.getContext('2d');

    // Reset map
    ctx.clearRect(0, 0, this.canvasRef.current.width, this.canvasRef.current.height);
    ctx.drawImage(this.backgroundImage, 0, 0, this.backgroundImage.width, this.backgroundImage.height);

    if (currentPath.length > 1) {
      drawPath(ctx, currentPath, 'red');
    }
  }

  handleCanvasClick(event) {
    const elemLeft = this.canvasRef.current.offsetLeft;
    const elemTop = this.canvasRef.current.offsetTop;

    const x = event.pageX - elemLeft;
    const y = event.pageY - elemTop;

    this.setState(prevState => ({
      currentPath: addToPath(prevState.currentPath, x, y),
    }), this.drawCanvas);
  }

  render() {
    const {classes} = this.props;

    return (
        <canvas
            className={classes.canvas}
            onClick={this.handleCanvasClick}
            ref={this.canvasRef}
        >

        </canvas>
    )
  }
}

export default withStyles(styles)(PlaceBooth);
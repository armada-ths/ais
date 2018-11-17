import React, {Component, Fragment} from 'react';
import {withStyles} from '@material-ui/core/styles';
import Button from "@material-ui/core/Button/Button";

const styles = theme => ({
  canvas: {
    border: 'solid 1px #CCC',
    cursor: 'crosshair'
  },
});

const EPS = 18; // How many pixels away we want to snap to start of path
const TARGET_WIDTH = 900;

const scalePath = (path, xScale, yScale) => path.map(([x, y]) => [x * xScale, y * yScale]);

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
      currentPath: [],
    };

    this.handleCanvasClick = this.handleCanvasClick.bind(this);
    this.handleUndo = this.handleUndo.bind(this);
  }

  componentDidMount() {
    const {map} = this.props;

    const scaleFactor = TARGET_WIDTH * 1.0 / map.width;

    const scaledWidth = map.width * scaleFactor;
    const scaledHeight = map.height * scaleFactor;

    this.canvasRef.current.width = scaledWidth;
    this.canvasRef.current.height = scaledHeight;

    this.backgroundImage = new Image(scaledWidth, scaledHeight);

    this.backgroundImage.onload = () => {
      this.drawCanvas();
    };

    this.backgroundImage.src = map.url;
  }

  drawCanvas() {
    const {booths} = this.props;
    const {currentPath} = this.state;

    const ctx = this.canvasRef.current.getContext('2d');
    ctx.strokeWidth = 3;

    // Reset map
    ctx.clearRect(0, 0, this.canvasRef.current.width, this.canvasRef.current.height);
    ctx.drawImage(this.backgroundImage, 0, 0, this.backgroundImage.width, this.backgroundImage.height);

    if (currentPath.length > 1) {
      drawPath(ctx, currentPath, 'red');
    }

    for (let booth of booths) {
      drawPath(ctx, scalePath(booth.boundaries, this.canvasRef.current.width, this.canvasRef.current.height), 'yellow');
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

  handleUndo() {
    this.setState(prevState => ({
      currentPath: prevState.currentPath.slice(0, prevState.currentPath.length - 1),
    }), this.drawCanvas);
  }

  render() {
    const {currentPath} = this.state;
    const {classes} = this.props;

    return (
        <Fragment>
          <canvas
              className={classes.canvas}
              onClick={this.handleCanvasClick}
              ref={this.canvasRef}
          />
          <div>
            <Button
                onClick={this.handleUndo}
                variant="contained"
                disabled={currentPath.length === 0}
            >
              Undo
            </Button>
          </div>
        </Fragment>
    )
  }
}

export default withStyles(styles)(PlaceBooth);
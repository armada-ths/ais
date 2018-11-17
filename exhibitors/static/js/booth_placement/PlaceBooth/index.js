import React, {Component, Fragment} from 'react';
import {withStyles} from '@material-ui/core/styles';
import Button from "@material-ui/core/Button/Button";
import TextField from "@material-ui/core/TextField/TextField";
import Grid from "@material-ui/core/Grid/Grid";

const styles = theme => ({
  canvas: {
    border: 'solid 1px #CCC',
    cursor: 'crosshair',
    marginTop: theme.spacing.unit,
    marginBottom: theme.spacing.unit
  },
  saveButton: {
    marginLeft: theme.spacing.unit * 2
  }
});

const EPS = 18; // How many pixels away we want to snap to start of path
const TARGET_WIDTH = 900;

const pathHasCycle = (path) => {
  const first = path[0];
  const last = path[path.length - 1];

  return path.length > 1 && first[0] === last[0] && first[1] === last[1];
};

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
  const [first, ...rest] = path;

  ctx.strokeStyle = color;

  if (rest.length > 0) {
    ctx.beginPath();
    ctx.moveTo(first[0], first[1]);
    for (let point of rest) {
      ctx.lineTo(point[0], point[1]);
    }
    ctx.stroke();

  } else {
    ctx.beginPath();
    ctx.arc(first[0], first[1], 1, 0, 2 * Math.PI);
    ctx.fill();
  }

  ctx.strokeStyle = 'black';
};

class PlaceBooth extends Component {
  constructor(props) {
    super(props);

    this.canvasRef = React.createRef();

    this.state = {
      currentPath: [],
      currentPathFinished: false,
      boothName: ""
    };

    this.handleCanvasClick = this.handleCanvasClick.bind(this);
    this.handleUndo = this.handleUndo.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.handleSave = this.handleSave.bind(this);
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

    // Reset map
    ctx.clearRect(0, 0, this.canvasRef.current.width, this.canvasRef.current.height);
    ctx.drawImage(this.backgroundImage, 0, 0, this.backgroundImage.width, this.backgroundImage.height);

    if (currentPath.length > 0) {
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

    this.setState(prevState => {
      const updatedPath = addToPath(prevState.currentPath, x, y);
      return {
        currentPath: updatedPath,
        currentPathFinished: pathHasCycle(updatedPath)
      }
    }, this.drawCanvas);
  }

  handleChange(event) {
    this.setState({[event.target.name]: event.target.value});
  };

  handleUndo() {
    this.setState(prevState => {
      const updatedPath = prevState.currentPath.slice(0, prevState.currentPath.length - 1);

      return {
        currentPath: updatedPath,
        currentPathFinished: pathHasCycle(updatedPath)
      };
    }, this.drawCanvas);
  }

  handleSave() {
    this.setState(prevState => {
      console.log(prevState.currentPath);
      console.log(scalePath(prevState.currentPath, 1.0 / this.canvasRef.current.width, 1.0 / this.canvasRef.current.height));

      return {
        currentPath: [],
        currentPathFinished: false,
        boothName: ""
      };
    }, this.drawCanvas);
  }

  render() {
    const {currentPath, currentPathFinished, boothName} = this.state;
    const {classes} = this.props;

    const boothPlacementFinished = currentPathFinished && boothName.trim().length > 0;

    return (
        <Fragment>
          <canvas
              className={classes.canvas}
              onClick={this.handleCanvasClick}
              ref={this.canvasRef}
          />
          <Grid container spacing={8} direction="row" justify="space-between">
            <Grid item>
              <Button
                  onClick={this.handleUndo}
                  variant="contained"
                  disabled={currentPath.length === 0}
              >
                Undo
              </Button>
            </Grid>
            <Grid item>
              <TextField
                  onChange={this.handleChange}
                  name="boothName"
                  value={boothName}
                  placeholder="Booth name"
                  margin="none"
              />
              <Button
                  disabled={!boothPlacementFinished}
                  onClick={this.handleSave}
                  className={classes.saveButton}
                  variant="contained"
                  color="primary"
              >
                Save
              </Button>
            </Grid>
          </Grid>
        </Fragment>
    )
  }
}

export default withStyles(styles)(PlaceBooth);
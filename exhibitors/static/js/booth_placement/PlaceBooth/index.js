import React, {Component} from 'react';
import {withStyles} from '@material-ui/core/styles';

const styles = theme => ({
  canvas: {
    border: 'solid 1px #CCC'
  },
});

const drawPath = (ctx, path, color = 'black') => {
  if (path.length < 2) new Error("Path length is < 2");

  const [first, ...rest] = path;

  ctx.strokeStyle = color;
  ctx.beginPath();
  ctx.moveTo(first.x, first.y);
  for (let point of rest) {
    ctx.lineTo(point.x, point.y);
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

    this.canvasRef.current.height = map.height;
    this.canvasRef.current.width = map.width;

    this.backgroundImage = new Image(map.width, map.height);

    this.backgroundImage.onload = () => {
      this.drawCanvas();
    };

    this.backgroundImage.src = map.url;
  }

  drawCanvas() {
    const {currentPath} = this.state;

    const ctx = this.canvasRef.current.getContext('2d');

    ctx.clearRect(0, 0, this.canvasRef.current.width, this.canvasRef.current.height);
    ctx.drawImage(this.backgroundImage, 0, 0);

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
      currentPath: [
        ...prevState.currentPath,
        {x, y}
      ]
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
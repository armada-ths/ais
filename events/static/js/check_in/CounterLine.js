import React, {PureComponent} from 'react';
import {withStyles} from '@material-ui/core/styles';
import Typography from "@material-ui/core/es/Typography/Typography";

const styles = theme => ({
  root: {
    backgroundColor: theme.palette.background.paper,
    paddingTop: 4
  }
});

class CounterLine extends PureComponent {
  render() {
    const {classes, current, total} = this.props;

    const isDone = current === total;

    return (
        <div className={classes.root}>
          <Typography align="center" color={isDone ? 'primary' : 'textPrimary'} variant="body2">
            {current} / {total}
          </Typography>
        </div>
    )
  }
}

export default withStyles(styles)(CounterLine);

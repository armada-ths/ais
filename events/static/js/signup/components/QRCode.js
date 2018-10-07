import React, {Component} from 'react';
import {withStyles} from '@material-ui/core/styles';
import QRCodeReact from 'qrcode.react';
import Grid from "@material-ui/core/es/Grid/Grid";
import Typography from "@material-ui/core/es/Typography/Typography";

const styles = theme => ({
  root: {
    marginTop: theme.spacing.unit * 2,
    paddingTop: theme.spacing.unit * 2,
  },
});

class QRCode extends Component {
  render() {
    const {theme, classes, value} = this.props;

    return (
        <div className={classes.root}>
          <Grid container justify="center" alignItems="center" direction="column" spacing={24}>
            <Grid item>
              <QRCodeReact
                  size={256}
                  fgColor={theme.palette.primary.main}
                  value={value}
              />
            </Grid>
            <Grid item>
              <Typography variant="subheading">
                Show this code when checking in to the event! 🤳
              </Typography>
            </Grid>
          </Grid>
        </div>
    )
  }
}

export default withStyles(styles, {withTheme: true})(QRCode);

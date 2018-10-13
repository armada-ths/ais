import React, {Component} from 'react';
import Snackbar from "@material-ui/core/Snackbar/Snackbar";
import SnackbarContent from "@material-ui/core/SnackbarContent/SnackbarContent";
import CheckIcon from 'mdi-material-ui/CheckCircleOutline';
import AlertIcon from 'mdi-material-ui/AlertOutline';
import AlertCircleIcon from 'mdi-material-ui/AlertCircleOutline';
import withStyles from "@material-ui/core/es/styles/withStyles";
import classNames from 'classnames';
import green from "@material-ui/core/es/colors/green";
import amber from "@material-ui/core/es/colors/amber";

const variantIcon = {
  success: CheckIcon,
  warning: AlertIcon,
  error: AlertCircleIcon,
};

const styles = theme => ({
  contentRoot: {
    backgroundColor: theme.palette.background.paper,
    color: theme.palette.text.primary
  },
  content: {
    display: 'flex',
    alignItems: 'center'
  },
  icon: {
    marginRight: theme.spacing.unit
  },
  error: {
    fill: theme.palette.error.main
  },
  success: {
    fill: green[400]
  },
  warning: {
    fill: amber[500]
  }
});

class Notification extends Component {
  render() {
    const {classes, message: {key, text, type}, ...rest} = this.props;
    const Icon = type ? variantIcon[type] : null;

    return (
        <Snackbar
            key={key}
            open={open}
            anchorOrigin={{
              vertical: 'top',
              horizontal: 'center',
            }}
            autoHideDuration={6000}
            {...rest}
        >
          <SnackbarContent
              className={classes.contentRoot}
              message={
                <span className={classes.content}>
                  {Icon && <Icon className={classNames(classes.icon, classes[type])}/>}
                  {text}
                </span>
              }
          />
        </Snackbar>
    )
  }
}

export default withStyles(styles)(Notification);
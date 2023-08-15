import React, {Component} from 'react';
import Dialog from "@material-ui/core/es/Dialog/Dialog";
import DialogTitle from "@material-ui/core/es/DialogTitle/DialogTitle";
import DialogContent from "@material-ui/core/es/DialogContent/DialogContent";
import DialogContentText from "@material-ui/core/es/DialogContentText/DialogContentText";
import TextField from "@material-ui/core/es/TextField/TextField";
import DialogActions from "@material-ui/core/es/DialogActions/DialogActions";
import Button from "@material-ui/core/es/Button/Button";

class CreateTeamDialog extends Component {
  constructor(props) {
    super(props);

    this.state = {
      teamName: '',
    };

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    const {name, value} = event.target;

    this.setState({
      [name]: value
    });
  }

  handleSubmit() {
    const {teamName} = this.state;
    const {handleCreate, handleClose} = this.props;

    handleCreate(teamName);
    handleClose();
  }

  render() {
    const {open, handleClose} = this.props;
    const {teamName} = this.state;

    return (
        <Dialog
            open={open}
            onClose={handleClose}
        >
          <DialogTitle>Create New Team</DialogTitle>
          <DialogContent>
            <DialogContentText>
              Note that creating a new team will cause you to leave your current team.
            </DialogContentText>
            <TextField
                name="teamName"
                value={teamName}
                onChange={this.handleChange}
                autoComplete="off"
                autoFocus
                margin="dense"
                label="Team Name"
                type="text"
                fullWidth
            />
          </DialogContent>
          <DialogActions>
            <Button onClick={handleClose} color="primary">
              Cancel
            </Button>
            <Button onClick={this.handleSubmit} disabled={teamName === ''} color="primary">
              Create
            </Button>
          </DialogActions>
        </Dialog>
    )
  }
}

export default CreateTeamDialog;

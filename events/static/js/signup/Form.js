import React, {Component} from 'react';
import {withStyles} from '@material-ui/core/styles';
import Paper from "@material-ui/core/es/Paper/Paper";
import Typography from "@material-ui/core/es/Typography/Typography";
import Question from "./Question";
import Button from "@material-ui/core/es/Button/Button";
import Grid from "@material-ui/core/es/Grid/Grid";
import axios from 'axios';

import forEach from 'lodash/forEach';
import isEmpty from 'lodash/isEmpty';
import find from 'lodash/find';

const styles = theme => ({
  root: {
    maxWidth: 960,
    margin: 'auto',
    marginTop: theme.spacing.unit * 2,
    padding: theme.spacing.unit * 2,
  },
  paper: {
    padding: theme.spacing.unit * 4,
  },
  signup: {
    marginTop: theme.spacing.unit * 2,
  }
});

class Form extends Component {
  constructor(props) {
    super(props);

    let answers = {};

    props.event.signup_questions.forEach(({id, type}) => {
      if (type === 'multiple_choice') {
        answers[id] = []
      } else {
        answers[id] = ''
      }
    });

    this.state = {
      payed: false,
      errors: {},
      answers
    };

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.validate = this.validate.bind(this);
  }

  handleChange(id, value) {

    this.setState(prevState => ({
      answers: {
        ...prevState.answers,
        [id]: value
      }
    }));
  }

  validate() {
    const {answers} = this.state;
    const {signup_questions} = this.props.event;
    let errors = {};

    forEach(answers, (answer, id) => {
      const question = find(signup_questions, {id: parseInt(id)});

      if (question.required && isEmpty(answer)) {
        errors[id] = true;
      }
    });

    return errors;
  }

  handleSubmit() {
    const errors = this.validate();
    this.setState({
      errors
    });

    if (isEmpty(errors)) {
      axios.post('')
    }
  }

  render() {
    const {classes, event} = this.props;
    const {answers, errors} = this.state;

    return (
        <div className={classes.root}>
          <Paper className={classes.paper}>
            <Grid container spacing={16}>
              <Grid item>
                <Typography variant="display2" color="primary" gutterBottom>
                  {event.name}
                </Typography>
                <Typography paragraph>
                  {event.description}
                </Typography>
                <Grid container spacing={16}>
                  <Grid item>
                    <Typography variant="caption" gutterBottom>
                      Location
                    </Typography>
                    <Typography>
                      {event.location}
                    </Typography>
                  </Grid>
                  <Grid item>
                    <Typography variant="caption" gutterBottom>
                      More info
                    </Typography>
                    <Typography component="a" target="_blank" rel="noopener noreferrer" href={event.external_event_link} color="primary">
                      {event.external_event_link}
                    </Typography>
                  </Grid>
                </Grid>

                <Grid container spacing={16}>
                  {event.signup_questions.map(question => <Question
                      key={question.id}
                      handleChange={this.handleChange}
                      value={answers[question.id]}
                      error={errors[question.id]}
                      {...question}/>)}
                </Grid>
              </Grid>
              <Grid item>
                <Button onClick={this.handleSubmit} className={classes.signup} variant="contained" color="primary">Signup</Button>
              </Grid>
            </Grid>
          </Paper>
        </div>
    )
  }
}

export default withStyles(styles)(Form);
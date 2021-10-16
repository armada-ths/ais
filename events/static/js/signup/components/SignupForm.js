import React, {Component, Fragment} from 'react';
import Typography from "@material-ui/core/es/Typography/Typography";
import Button from "@material-ui/core/es/Button/Button";
import Grid from "@material-ui/core/es/Grid/Grid";
import axios from 'axios';
import Cookie from 'js-cookie';
import forEach from 'lodash/forEach';
import isEmpty from 'lodash/isEmpty';
import find from 'lodash/find';
import mapValues from 'lodash/mapValues';
import {updateParticipant} from '../actions';
import {Elements, StripeProvider} from 'react-stripe-elements';

import Question from "./Question";
import Stripe from "./Stripe";

import "../../../../../static/events.css"

class SignupForm extends Component {
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
      payed: props.feePayed,
      errors: {},
      answers
    };

    this.handleChange = this.handleChange.bind(this);
		this.handleClick = this.handleClick.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.validate = this.validate.bind(this);
		this.showErrors = this.showErrors.bind(this);

  }

  handleChange(id, value) {

    this.setState(prevState => ({
      answers: {
        ...prevState.answers,
        [id]: value
      }
    }));
  }

	handleClick() {
		this.handleSubmit("");
	}

  handleSubmit(intent_id) {
    const errors = this.validate();
    const {signupUrl, dispatcher} = this.props;

    const answers = mapValues(this.state.answers, answer => Array.isArray(answer) ? answer.join(',') : answer);

    this.setState({
      errors: errors
    });

    if (isEmpty(errors)) {
      axios.post(signupUrl, {answers, intent_id}, {
        headers: {
          "X-CSRFToken": Cookie.get('csrftoken')
        }
      }).then(response => {
            dispatcher(updateParticipant(response.data.participant));
          }
      )
    }
  }

  validate() {
		const {answers, payed}=this.state;
    const {signup_questions, fee} = this.props.event;
    let errors = {};

    forEach(answers, (answer, id) => {
      const question = find(signup_questions, {id: parseInt(id)});

      if (question.required && isEmpty(answer)) {
        errors[id] = true;
      }
    });

    return errors;
  }

	showErrors(errors) {
		this.setState({
			errors: errors
		})
	}

  render() {
    const {event, stripe_publishable, payment_url} = this.props;
    const {answers, errors, payed} = this.state;

    return (
        <Grid container spacing={16}>
          {/* TODO Image have no restriction */}
        <div className='image-section' >
          <img alt='' src={event.image_url}/>
        </div>
          <Grid item>
						<Grid container spacing={16}>
							{event.signup_questions.map(question => <Question
									key={question.id}
									handleChange={this.handleChange}
									value={answers[question.id]}
									error={errors[question.id]}
									{...question}/>)}
						</Grid>
            <Grid container spacing={16}>
              {event.fee > 0 && (
                  <Grid item sm={12}>
                    <Typography variant="caption" color={errors['payment'] && 'error'} gutterBottom>
                      Payment
                    </Typography>
                    <Typography>
                      {payed ? (
                          'The event fee has been paid!  🎉'
                      ) : (
                          <Fragment>
														<Typography style={{marginTop: 8, marginBottom: 8}}>This event has a fee of {event.fee} SEK to sign up. By signing up you agree to THS Armada's <a href="https://docs.google.com/document/d/14_dUZHTL6QUNF9UeL7fghJXO1wZimbi_aKG5ttcGd1s/edit#heading=h.hpqg0xn5jl2q" target="_blank" rel="noopener noreferrer" style={{ color: "#00d790" }}>Privacy Notice</a>.</Typography>
															<StripeProvider apiKey={this.props.stripe_publishable}>
															<Elements locale='en'>
                                <Stripe
                                    stripe_publishable={stripe_publishable}
																		paymentUrl={this.props.paymentUrl}
																		openForSignup={event.open_for_signup}
																		handleSubmit={this.handleSubmit}
																		validator={this.validate}
																		showErrors={this.showErrors}
                                />
															</Elements>
															</StripeProvider>
                          </Fragment>
                      )}
                    </Typography>
                  </Grid>
								)}
            </Grid>
          </Grid>
					{event.fee == 0 && (
	          <Grid item sm={12}>
							<Typography style={{marginTop: 8}}>By signing up you agree to THS Armada's <a href="https://docs.google.com/document/d/14_dUZHTL6QUNF9UeL7fghJXO1wZimbi_aKG5ttcGd1s/edit#heading=h.hpqg0xn5jl2q" target="_blank" rel="noopener noreferrer" style={{ color: "#00d790" }}>Privacy Notice</a>.</Typography>
	            <Button
	                disabled={!event.open_for_signup}
	                onClick={this.handleClick}
	                variant="contained"
	                color="primary"
									style={{marginTop: 10}}
	            >
	              {event.open_for_signup ? "Sign Up" : "Not open for sign up"}
	            </Button>
	          </Grid>
					)}
        </Grid>
    )
  }
}

export default SignupForm;

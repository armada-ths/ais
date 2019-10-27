import React, {Component} from 'react';
import Button from "@material-ui/core/es/Button/Button";
import {CardElement, injectStripe} from 'react-stripe-elements';
import axios from 'axios';
import Cookie from 'js-cookie';
import isEmpty from 'lodash/isEmpty';

class Stripe extends Component {
  constructor(props) {
    super(props);

		this.nameInput = React.createRef();
		this.cardElement = React.createRef();

		this.state = {
			processingPayment: false,
			error: null,
			payed: false
		}

    this.handleClick = this.handleClick.bind(this);
		this.fetch_payment_intent = this.fetch_payment_intent.bind(this);
		this.handle_stripe_payment = this.handle_stripe_payment.bind(this);
		this.setState = this.setState.bind(this);
  }

  handleClick(event) {
		const errors = this.props.validator();
		if (!isEmpty(errors)) {
			this.props.showErrors(errors);
			return;
		}

		this.setState({
			processingPayment: true,
			error: null
		})

		const {paymentUrl} = this.props;

		this.fetch_payment_intent(paymentUrl)

    event.preventDefault();
  }

	fetch_payment_intent (paymentUrl) {
		axios.post(paymentUrl, {
		}, {
			headers: {
				"X-CSRFToken": Cookie.get('csrftoken')
			}
		}).then((response) => {
			response=response.data;
			if (response['error']) {
				this.setState({
					processingPayment: false,
					error: response.error
				})
			} else if (response['client_secret']) {
				this.handle_stripe_payment(response['client_secret'], response['intent_id'])
			}
		});
	}

	handle_stripe_payment (client_secret, intent_id) {
		this.props.stripe.handleCardPayment(
			client_secret,
			this.cardElement.current
		).then((result) => {
			if (result.error) {
				this.setState({
					processingPayment: false,
					error: result.error
				})
			} else {
				this.props.handleSubmit(intent_id)
			}
		});
	}

  render() {
    return (
			<div>
				<CardElement onReady={this.cardElement}/>
				<div style={{marginTop: 10, color: 'red'}}>{this.state.error ? this.state.error.message : ""}</div>
				<Button
						disabled={!this.props.openForSignup || this.state.processingPayment}
						onClick={this.handleClick}
						variant="contained"
						color="primary"
						style={{marginTop: 10}}
				>
					{this.props.openForSignup ? "Pay and Sign Up" : "Not open for sign up"}
				</Button>
				<div style={{marginTop: 10, }}>{this.state.processingPayment ? <em>Processing payment - almost done... </em> : ""}</div>
			</div>
		)
  }
}

export default injectStripe(Stripe);

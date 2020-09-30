import React, { Component } from 'react';
import Button from "@material-ui/core/es/Button/Button";
import { CardElement, injectStripe } from 'react-stripe-elements';
import axios from 'axios';
import Cookie from 'js-cookie';
import isEmpty from 'lodash/isEmpty';

class Stripe extends Component {
	constructor(props) {
		super(props);

		this.nameInput = React.createRef();
		this.cardElement = React.createRef();

		this.state = {
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

		this.props.updateProcessingPayment('stripe', true);

		const { paymentUrl } = this.props;
		this.fetch_payment_intent(paymentUrl)

		event.preventDefault();
	}

	fetch_payment_intent(paymentUrl) {
		axios.post(paymentUrl, {
		}, {
			headers: {
				"X-CSRFToken": Cookie.get('csrftoken')
			}
		}).then((response) => {
			response = response.data;
			if (response['error']) {
				this.props.updateProcessingPayment('stripe', false, response.error)
			} else if (response['client_secret']) {
				this.handle_stripe_payment(response['client_secret'], response['intent_id'])
			}
		});
	}

	handle_stripe_payment(client_secret, intent_id) {
		this.props.stripe.handleCardPayment(
			client_secret,
			this.cardElement.current
		).then((result) => {
			if (result.error) {
				this.props.updateProcessingPayment('stripe', false, result.error)
			} else {
				this.props.handleSubmit(intent_id)
			}
		});
	}

	render() {
		return (
			<div>
				<CardElement onReady={this.cardElement} options={{ disabled: this.props.disabled }} />
				<Button
					disabled={!this.props.openForSignup || this.props.disabled}
					onClick={this.handleClick}
					variant="contained"
					color="primary"
					style={{ marginTop: 10 }}
				>
					{this.props.openForSignup ? "Pay and Sign Up" : "Not open for sign up"}
				</Button>
			</div>
		)
	}
}

export default injectStripe(Stripe);

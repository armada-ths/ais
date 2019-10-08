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
				this.handle_stripe_payment(response['client_secret'])
			}
		});
	}

	handle_stripe_payment (client_secret) {
		const name = this.nameInput.current.value;
		debugger;
		this.props.stripe.handleCardPayment(
			client_secret,
			this.cardElement.current,
			{
				payment_method_data: {
					billing_details: {name: name}
				}
			}
		).then((result) => {
			if (result.error) {
				this.setState({
					processingPayment: false,
					error: result.error
				})
			} else {
				this.props.handleSubmit()
			}
		});
	}

  render() {
    return (
			<div>
				<input ref={this.nameInput} type="text" className="form-control" />
				<CardElement onReady={this.cardElement}/>
				<div>{this.state.error ? this.state.error.message : ""}</div>
				{ this.state.processingPayment ? "processing payment" : <Button color="primary" onClick={this.handleClick}>Pay</Button> }
			</div>
		)
  }
}

export default injectStripe(Stripe);

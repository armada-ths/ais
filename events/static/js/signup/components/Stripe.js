import React, {Component} from 'react';
import Button from "@material-ui/core/es/Button/Button";
import {CardElement, injectStripe} from 'react-stripe-elements';

class Stripe extends Component {
  constructor(props) {
    super(props);

		this.nameInput = React.createRef();
		this.cardElement = React.createRef();

		this.state = {
			processingPayment: false,
			error: null
		}

    this.handleClick = this.handleClick.bind(this);
  }

  handleClick(event) {

		// const {description, amount} = this.props;

		this.setState({
			processingPayment: true,
			error: null
		})

		const {paymentUrl} = this.props;

		axios.post(paymentUrl, {
			// token: token['id']
		}, {
			headers: {
				"X-CSRFToken": Cookie.get('csrftoken')
			}
		}).then((response) => {
			if (response['error']) {
				// Show errors
			} else if (response['client_secret']) {
				stripe.handleCardPayment(
		    response['client_secret'], this.cardElement, {
		      payment_method_data: {
		        billing_details: {name: this.nameInput}
		      }
		    }
		  ).then(function(result) {
		    if (result.error) {
					this.setState({
						processingPayment: false,
						error: result.error
					})
		      // Display error.message in your UI.
		    } else {
		      // The payment has succeeded. Display a success message.
		    }
		  });
			}
		})


		// this.props.stripe.createToken({name: this.nameInput.current.value})
		// 	.then((result) => {
		// 		if (result.error) {
		// 			this.setState({
		// 				processingPayment: false,
		// 				error: result.error
		// 			})
		// 		} else {
		// 			this.props.handleToken(result.token, (error) => {
		// 				this.setState({
		// 					processingPayment: false,
		// 					error: error
		// 				})
		// 			});
		// 		}
		// 	})


		this.props.createPaymentIntent((error) => {
				this.setState({
					processingPayment: false,
					error: error
				})
		}).then ((result) => {

		}


    event.preventDefault();
  }

  render() {
    return (
			<div>
				<input ref={this.nameInput} type="text" className="form-control" />
				<CardElement ref={this.cardElement}/>
				<div>{this.state.error ? this.state.error.message : ""}</div>
				{ this.state.processingPayment ? "processing payment" : <Button color="primary" onClick={this.handleClick}>Pay</Button> }
			</div>
		)
  }
}

export default injectStripe(Stripe);

import React, {Component} from 'react';
import Button from "@material-ui/core/es/Button/Button";
import {CardElement, injectStripe} from 'react-stripe-elements';

class Stripe extends Component {
  constructor(props) {
    super(props);

		this.nameInput = React.createRef();

		this.state = {
			processingPayment: false,
			error: null
		}

    this.handleClick = this.handleClick.bind(this);
  }

  handleClick(event) {
    const {description, amount} = this.props;

		this.setState({
			processingPayment: true,
			error: null
		})

		this.props.stripe.createToken({name: this.nameInput.current.value})
			.then((result) => {
				if (result.error) {
					this.setState({
						processingPayment: false,
						error: result.error
					})
				} else {
					this.props.handleToken(result.token, (error) => {
						this.setState({
							processingPayment: false,
							error: error
						})
					});
				}
			})
    event.preventDefault();
  }

  render() {
    return (
			<div>
				<input ref={this.nameInput} type="text" className="form-control" />
				<CardElement />
				<div>{this.state.error ? this.state.error.message : ""}</div>
				{ this.state.processingPayment ? "processing payment" : <Button color="primary" onClick={this.handleClick}>Pay</Button> }
			</div>
		)
  }
}

export default injectStripe(Stripe);

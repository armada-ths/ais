import React, { Component } from 'react';
import Button from "@material-ui/core/es/Button/Button";

import axios from 'axios';
import Cookie from 'js-cookie';
import isEmpty from 'lodash/isEmpty';

class Swish extends Component {
	constructor(props) {
		super(props);

		this.state = {
			paymentId: null,
			swishOptions: false,
			payerAlias: '',
			qrCode: null
		}

		this.handleClick = this.handleClick.bind(this);
		this.handleOptionClick = this.handleOptionClick.bind(this);
		this.handleChangePayerAlias = this.handleChangePayerAlias.bind(this);
		this.createSwishPayment = this.createSwishPayment.bind(this);
		this.generateQRCode = this.generateQRCode.bind(this);
		this.setState = this.setState.bind(this);
	}

	// Handle Swish button click
	handleClick(event) {
		this.setState({
			swishOptions: true // Show pop-up with options
		})

		event.preventDefault();
	}

	// Handle Swish payment mode selection
	handleOptionClick(event, option) {
		if (!isEmpty(this.state.error))
			return;

		const errors = this.props.validator();
		if (!isEmpty(errors)) {
			this.props.showErrors(errors);
			return;
		}

		this.props.updateProcessingPayment('swish', true);

		if (option === 'qr-code') {
			// Show up QR Code
			const generateQRCodeUrl = this.props.paymentUrl + "/qr-code";
			this.generateQRCode(generateQRCodeUrl);
		} else {
			// Create payment for Payer Alias
			this.createSwishPayment(this.props.paymentUrl, this.state.payerAlias);
		}
	}

	// Create Swish payment
	createSwishPayment(paymentUrl, payerAlias) {
		this.setState({
			paymentId: null,
			qrCode: null
		})

		if (!/^46\d{8,15}$/.test(payerAlias)) { // Must be Swedish number with length of 8-15
			this.props.updateProcessingPayment('swish', false, { message: 'Payer alias is not valid' });
			return;
		}

		axios.post(paymentUrl, {
			swish_payer_alias: payerAlias
		}, {
			headers: {
				"X-CSRFToken": Cookie.get('csrftoken')
			}
		}).then((response) => {
			response = response.data;
			if (response['error']) {
				console.log(response.error)
				this.props.updateProcessingPayment('swish', false, { message: response.error });
			} else {
				if (response.status == "PAID") {
					this.props.handleSubmit(paymentId)
				} else {
					if (response.payment_id) {
						this.setState({
							paymentId: response.payment_id
						})
						this.checkPayment(this.props.paymentUrl + '/' + this.state.paymentId);
					} else {
						this.props.updateProcessingPayment('swish', false, { message: "Something went wrong. Please, try again." });
					}
				}
			}
		});
	}

	// Generate QR Code
	generateQRCode(generateQRCodeUrl) {
		axios.get(generateQRCodeUrl, {}, {
			headers: {
				"X-CSRFToken": Cookie.get('csrftoken')
			}
		}).then((response) => {
			response = response.data;
			if (response['error']) {
				this.props.updateProcessingPayment('swish', false, { message: response.error })
			} else {
				this.setState({
					qrCode: 'data:image/png;base64,' + response.qr_code,
					paymentId: response.payment_id
				});

				this.checkPayment(this.props.paymentUrl + '/' + this.state.paymentId);
			}
		});
	}

	// Check payment.
	checkPayment(getPaymentUrl) {

		// Retry each 5 seconds
		setTimeout(function (getPaymentUrl, paymentId, props, checkPayment) {
			console.log('Checking payment...') // TODO: Remove console.log
			axios.get(getPaymentUrl, {}, {
				headers: {
					"X-CSRFToken": Cookie.get('csrftoken')
				}
			}).then((response) => {
				response = response.data;
				if (response['error']) {
					if (response['status']) {
						props.updateProcessingPayment('swish', false, { message: response.error });
					} else {
						checkPayment(getPaymentUrl); // try again in 5 secs
					}
				} else {
					if (response.status == "PAID") {
						props.handleSubmit(paymentId)
					} else {
						props.updateProcessingPayment('swish', false, { message: "Something went wrong. Please, try again." });
					}
				}
			});
		}, 5000, getPaymentUrl, this.state.paymentId, this.props, this.checkPayment);
	}

	handleChangePayerAlias(event) {
		this.setState({
			payerAlias: event.target.value
		})
	}

	render() {
		return (
			<div>
				<Button
					disabled={!this.props.openForSignup || this.props.disabled}
					onClick={this.handleClick}
					variant="contained"
					color="primary"
					style={{ marginTop: 10 }}>
					Pay with Swish
					{/* <img src='/static/images/swish_payment_button.png' alt='Swish payment' onClick={this.handleClick} /> */}
				</Button>
				{this.state.swishOptions ? (
					<div>
						<div>
							<Button
								onClick={(e) => this.handleOptionClick(e, 'qr-code')}
								disabled={this.props.disabled}>
								QR-Code
							</Button>
							{this.state.qrCode ? (
								<img src={this.state.qrCode} style={{ width: '30%' }} />
							) : null}
						</div>
						<div>
							<input
								name="payerAlias"
								type="number"
								value={this.state.payerAlias}
								onChange={this.handleChangePayerAlias}
								disabled={this.props.disabled} />
							<Button
								onClick={(e) => this.handleOptionClick(e, 'payer-alias')}
								disabled={this.props.disabled}>
								Payer alias
						</Button>
						</div>
					</div>) : null
				}
			</div>
		)
	}
}

export default Swish;
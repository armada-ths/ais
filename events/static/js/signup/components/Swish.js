import React, { Component } from 'react';
import Button from "@material-ui/core/es/Button/Button";
import Input from "@material-ui/core/Input/Input";

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
			payerAliasError: null,
			qrCode: null
		}

		this.handleClick = this.handleClick.bind(this);
		this.handleOptionClick = this.handleOptionClick.bind(this);
		this.handleChangePayerAlias = this.handleChangePayerAlias.bind(this);
		this.createSwishPayment = this.createSwishPayment.bind(this);
		this.generateQRCode = this.generateQRCode.bind(this);
		this.resetOptions = this.resetOptions.bind(this);
		this.setState = this.setState.bind(this);

		if (!isEmpty(this.props.swishChargeId)) {
			this.checkPayment()
		}
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

		// Validate payer alias
		if (!/^46\d{8,15}$/.test(this.state.payerAlias)) { // Must be Swedish number with length of 8-15
			this.props.updateProcessingPayment('swish', false, { message: 'The Swish number must be a Swedish number of 8-15 length' });
			this.setState({
				payerAliasError: 'Payer alias not valid'
			})
			return;
		} else {
			this.setState({
				payerAliasError: null
			})
		}

		// update processing state
		this.props.updateProcessingPayment('swish', true, {});

		// Create Swish payment
		axios.post(paymentUrl, {
			swish_payer_alias: payerAlias
		}, {
			headers: {
				"X-CSRFToken": Cookie.get('csrftoken')
			}
		}).then((response) => {
			response = response.data;
			if (response['error']) {
				this.props.updateProcessingPayment('swish', false, { message: response.error });
			} else {
				if (response.status == "PAID") {
					this.props.handleSubmit(paymentId)
				} else {
					if (response.payment_id) {
						this.props.updateProcessingPayment('swish', true, 'A payment has been created in your Swish app. Waiting until the payment is done...');
						this.setState({
							paymentId: response.payment_id
						})
						// Check the state of the payment periodically
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
		// update processing state
		this.props.updateProcessingPayment('swish', true, {});

		// Generate qr code
		axios.get(generateQRCodeUrl, {}, {
			headers: {
				"X-CSRFToken": Cookie.get('csrftoken')
			}
		}).then((response) => {
			response = response.data;
			if (response['error']) {
				this.props.updateProcessingPayment('swish', false, { message: response.error })
			} else {
				this.props.updateProcessingPayment('swish', true, 'Scan the QR code with your Swish app to finish the payment');
				this.setState({
					qrCode: 'data:image/png;base64,' + response.qr_code,
					paymentId: response.payment_id
				});
				// Check the state of the payment periodically
				this.checkPayment(this.props.paymentUrl + '/' + this.state.paymentId);
			}
		});
	}

	// Check payment state periodically
	checkPayment(getPaymentUrl) {
		setTimeout(function (getPaymentUrl, that) {
			console.log('Checking payment...')
			axios.get(getPaymentUrl, {}, {
				headers: {
					"X-CSRFToken": Cookie.get('csrftoken')
				}
			}).then((response) => {
				response = response.data;
				if (response['error']) {
					if (response['status']) {
						that.props.updateProcessingPayment('swish', false, { message: response.error });
					} else {
						that.checkPayment(getPaymentUrl);
					}
				} else {
					if (isEmpty(that.state.payerAlias)) {
						that.setState({
							payerAlias: response.payer_alias
						})
					}

					// Payment states: Created, Paid, Cancelled, Timeout or Error.
					// Created is a transient state
					if (response.status == "PAID") {
						that.props.handleSubmit(that.state.paymentId);
					} else {
						if (response.status == "CREATED") {
							that.checkPayment(getPaymentUrl)
						} else {
							msg = 'Something went wrong. Please, try again.'
							switch (response.status) {
								case "CANCELLED":
									msg = 'The payment was cancelled. Please, try again.'
									break;
								case "TIMEOUT":
									msg = 'Payment timeout exceeded. Please, try again.'
									break;
							}
							that.props.updateProcessingPayment('swish', false, { message: msg });
						}
					}
				}
			});
		}, 5000, getPaymentUrl, this);
	}

	handleChangePayerAlias(event) {
		// Only numbers are allowed in a payer alias
		if (/^\d+$/.test(event.target.value) || isEmpty(event.target.value)) {
			this.setState({
				payerAlias: event.target.value
			})
		}
	}

	resetOptions() {
		this.props.updateProcessingPayment('swish', false, {})
		this.setState({
			paymentId: null,
			qrCode: null,
			swishOptions: false
		})
	}

	render() {
		return [
			<div style={{ width: '45%', display: 'inline-block', textAlign: 'right', verticalAlign: 'bottom' }}>
				{this.state.swishOptions ? (
					<div>
						<div>
							<Input
								type="text"
								name="payerAlias"
								placeholder="Swedish phone number"
								onChange={this.handleChangePayerAlias}
								error={this.state.payerAliasError}
								value={this.state.payerAlias}
								disabled={this.props.disabled}
								disableUnderline={this.props.disabled} />
							<Button
								onClick={(e) => this.handleOptionClick(e, 'payer-alias')}
								disabled={this.props.disabled || this.state.qrCode}
								variant="contained"
								color="primary"
								style={{ marginTop: 10 }}>
								Use Swish number
							</Button>
						</div>
						<div>
							<span style={{ marginRight: 10 }}>or</span>
							<Button
								onClick={(e) => this.handleOptionClick(e, 'qr-code')}
								disabled={this.props.disabled || this.state.qrCode}
								variant="contained"
								color="primary"
								style={{ marginTop: 10 }}>
								Scan QR Code
							</Button>
						</div>
					</div>
				) : (
						<Button
							disabled={!this.props.openForSignup || this.props.disabled}
							onClick={this.handleClick}
							variant="contained"
							color="primary"
							style={{ marginTop: 10 }}>
							Pay with Swish
						</Button>
					)}
			</div>,
			this.state.qrCode ? (
				<div style={{ textAlign: 'center' }}>
					<img src={this.state.qrCode} style={{ width: '35%', marginBottom: 12 }} />
					<Button
						onClick={this.resetOptions}
						variant="contained"
						color="secondary"
						style={{ margin: '0 auto', display: 'block' }}>
						Choose another option
					</Button>
				</div>
			) : null
		]
	}
}

export default Swish;
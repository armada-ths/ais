import React, {Component} from 'react';
import Button from "@material-ui/core/es/Button/Button";

class Stripe extends Component {
  constructor(props) {
    super(props);

    this.handler = StripeCheckout.configure({
      key: props.stripe_publishable,
      image: 'https://ais.armada.nu/static/images/armadalogo.svg',
      locale: 'auto',
      token: props.handleToken,
    });

    this.handleClick = this.handleClick.bind(this);
  }

  handleClick(event) {
    const {description, amount} = this.props;

    // This is safe to do in the frontend since this is just what's presented to the user, not what will actually be withdrawn from the
    // users card
    const amountInOren = parseInt(amount) * 100;

    this.handler.open({
      name: 'THS Armada',
      description: description,
      currency: 'sek',
      amount: amountInOren
    });
    event.preventDefault();
  }

  render() {
    return <Button color="primary" onClick={this.handleClick}>Pay</Button>

  }
}

export default Stripe;

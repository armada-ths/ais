import React, {Fragment, PureComponent} from 'react';
import ExpansionPanel from "@material-ui/core/ExpansionPanel/ExpansionPanel";
import ExpansionPanelSummary from "@material-ui/core/ExpansionPanelSummary/ExpansionPanelSummary";
import Typography from "@material-ui/core/Typography/Typography";
import ExpansionPanelDetails from "@material-ui/core/ExpansionPanelDetails/ExpansionPanelDetails";
import ExpandMoreIcon from 'mdi-material-ui/ChevronDown';
import QRCodeReact from 'qrcode.react';

class Ticket extends PureComponent {
  constructor(props) {
    super(props);
  }

  render() {
    const {title, token} = this.props;
    return (
        <Fragment>
          <ExpansionPanel>
            <ExpansionPanelSummary expandIcon={<ExpandMoreIcon/>}>
              <Typography>{title}</Typography>
            </ExpansionPanelSummary>
            <ExpansionPanelDetails>
              <QRCodeReact
                  size={256}
                  value={token}
                  level="L"
              />
            </ExpansionPanelDetails>
          </ExpansionPanel>
        </Fragment>
    )
  }
}

export default Ticket;

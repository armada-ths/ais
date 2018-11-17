import React, {Fragment, PureComponent} from 'react';
import ExpansionPanel from "@material-ui/core/ExpansionPanel/ExpansionPanel";
import ExpansionPanelSummary from "@material-ui/core/ExpansionPanelSummary/ExpansionPanelSummary";
import Typography from "@material-ui/core/Typography/Typography";
import ExpansionPanelDetails from "@material-ui/core/ExpansionPanelDetails/ExpansionPanelDetails";
import ExpandMoreIcon from 'mdi-material-ui/ChevronDown';
import QRCodeReact from 'qrcode.react';
import Grid from "@material-ui/core/Grid/Grid";

class Ticket extends PureComponent {
  constructor(props) {
    super(props);
  }

  render() {
    const {title, token, expanded, id, openPanel} = this.props;
    return (
        <Fragment>
          <ExpansionPanel expanded={expanded} onChange={() => openPanel(id)}>
            <ExpansionPanelSummary expandIcon={<ExpandMoreIcon/>}>
              <Typography>{title}</Typography>
            </ExpansionPanelSummary>
            <ExpansionPanelDetails>
              <Grid container justify="center" alignItems="center" direction="row">
                <Grid item>
                  <QRCodeReact
                      size={256}
                      value={token}
                      level="L"
                  />
                </Grid>
              </Grid>
            </ExpansionPanelDetails>
          </ExpansionPanel>
        </Fragment>
    )
  }
}

export default Ticket;

import React, {Component, Fragment} from 'react';
import * as API from "../api";
import {setTeams} from '../actions';
import keyBy from 'lodash/keyBy';
import QRCode from './QRCode';
import Teams from './Teams';
import PeopleIcon from 'mdi-material-ui/AccountMultiple';
import QrCodeIcon from 'mdi-material-ui/Qrcode';
import Tabs from "@material-ui/core/es/Tabs/Tabs";
import Tab from "@material-ui/core/es/Tab/Tab";
import withWidth, {isWidthDown, isWidthUp} from "@material-ui/core/es/withWidth/withWidth";

class Manage extends Component {
  constructor(props) {
    super(props);

    this.state = {
      selectedTeamId: null,
      tabIndex: 0
    };

    this.handleSelectTeam = this.handleSelectTeam.bind(this);
    this.handleJoinTeam = this.handleJoinTeam.bind(this);
    this.handleCreateTeam = this.handleCreateTeam.bind(this);


    this.handleTabSwitch = this.handleTabSwitch.bind(this);
  }

  handleSelectTeam(id) {
    this.setState({
      selectedTeamId: id
    })
  }

  handleJoinTeam() {
    const {event, dispatcher} = this.props;
    const {selectedTeamId} = this.state;

    API.joinTeam(event.id, selectedTeamId)
        .then(response => {
          const mappedTeams = keyBy(response.data.teams, 'id');
          dispatcher(setTeams(mappedTeams));
        });
  }

  handleCreateTeam(teamName) {
    const {event, dispatcher} = this.props;

    API.createTeam(event.id, teamName)
        .then(response => {
          const mappedTeams = keyBy(response.data.teams, 'id');
          dispatcher(setTeams(mappedTeams));
        });
  }

  handleTabSwitch(event, value) {
    this.setState({tabIndex: value})
  }

  render() {
    const {teams, width} = this.props;
    const {selectedTeamId, tabIndex} = this.state;

    const selectedTeam = teams[selectedTeamId];

    return (
        <Fragment>
          <Tabs
              indicatorColor="primary"
              textColor="primary"
              centered={isWidthUp('sm', width)}
              fullWidth={isWidthDown('sm', width)}
              value={tabIndex}
              onChange={this.handleTabSwitch}
          >
            <Tab icon={<PeopleIcon/>} label="Teams"/>
            <Tab icon={<QrCodeIcon/>} label="QR Code"/>
          </Tabs>
          {tabIndex === 0 && (
              <Teams
                  teams={teams}
                  selectedTeam={selectedTeam}
                  handleCreateTeam={this.handleCreateTeam}
                  handleSelectTeam={this.handleSelectTeam}
                  handleJoinTeam={this.handleJoinTeam}
              />
          )}
          {tabIndex === 1 && (
              <QRCode value="A long value here!"/>
          )}
        </Fragment>
    )
  }
}

export default withWidth()(Manage);

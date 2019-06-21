import React, { Component, Fragment } from 'react';
import { Pane } from 'evergreen-ui';

import Introduction from './Components/Introduction';
import Footer from './Components/Footer';
import BidTable from './Components/BidTable';

class App extends Component {

  render() {
    return (
      <Fragment>
        <Introduction />
        <Pane border height="70vh" display="flex" flexGrow={0}>
          <BidTable />
        </Pane>
        <Footer />
      </Fragment >
    );
  }
}

export default App;

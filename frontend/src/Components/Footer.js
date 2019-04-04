import React from 'react';
import { Heading, Pane } from 'evergreen-ui';

class Footer extends React.Component {
    render() {
        return (
            <Pane
              display="flex"
              alignItems="center"
              justifyContent="center"
            >
              <Heading is="h5" padding={10}>
                Código e dados abertos <a href="https://github.com/anapaulagomes/licitacoes-de-feira" target="_blank" rel="noopener noreferrer">aqui</a>. :)
      
                Quer ajudar? Envie um email para: dadosabertosdefeira@gmail.com
              </Heading>
            </Pane>
          );
    }
}

export default Footer;
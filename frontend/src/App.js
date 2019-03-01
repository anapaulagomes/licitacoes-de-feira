import React, { Component } from 'react';
import { Icon, Heading, Pane, Paragraph, Table } from 'evergreen-ui';

import allBids from './bids.json'; // eslint-disable-line import/extensions


class App extends Component {
  constructor(props) {
    super(props)

    this.state = {
      bids: allBids,
    }
  }

  handleFilterChange = value => {
    this.setState({ bids: this.filterData(value) })
  }

  filterData(searchQuery) {
    return allBids.filter(bid => {
      const descriptionFound = bid.description.toLowerCase().includes(searchQuery.toLowerCase());
      const bidCodeFound = bid.modality.toLowerCase().includes(searchQuery.toLowerCase());
      if (descriptionFound || bidCodeFound) {
        return bid;
      }
      return null;
    });
  }

  render() {
    return (
      <div className="App">
        <Pane flex={1} padding={50} alignItems="center" display="flex">
          <Heading size={700}>Licitações de Feira de Santana 🏦</Heading>
        </Pane>
        <Pane>
          <Table>
            <Table.Head>
              <Table.TextHeaderCell flexBasis={160} flexShrink={0} flexGrow={0}>
                Quando
            </Table.TextHeaderCell>
              <Table.SearchHeaderCell
                placeholder="Filtrar descrição..."
                onChange={this.handleFilterChange}
                value={this.state.searchQuery}
              />
              <Table.TextHeaderCell flexBasis={80} flexShrink={0} flexGrow={0}>
                Edital
            </Table.TextHeaderCell>
              <Table.TextHeaderCell flexBasis={260} flexShrink={0} flexGrow={0}>
                Licitação/Modalidade
            </Table.TextHeaderCell>
              <Table.TextHeaderCell flexBasis={100} flexShrink={0} flexGrow={0}>
                Categoria
            </Table.TextHeaderCell>
              <Table.TextHeaderCell flexBasis={100} flexShrink={0} flexGrow={0}>
                Mês/Ano
            </Table.TextHeaderCell>
            </Table.Head>
            <Table.VirtualBody height={600} >
              {this.state.bids.map(bid => (
                <Table.Row key={bid.id} height={85}>
                  <Table.TextCell flexBasis={160} flexShrink={0} flexGrow={0}>{bid.when}</Table.TextCell>
                  <Table.Cell>
                    <Paragraph>
                      {bid.description}
                    </Paragraph>
                  </Table.Cell>
                  <Table.TextCell flexBasis={80} flexShrink={0} flexGrow={0}>
                    <a href={bid.document_url} target="_blank" rel="noopener noreferrer">
                      <Icon icon="download" color="selected" marginRight={16} />
                    </a>
                  </Table.TextCell>
                  <Table.Cell flexBasis={260} flexShrink={0} flexGrow={0}>
                    <Paragraph>{bid.modality}</Paragraph>
                  </Table.Cell>
                  <Table.TextCell flexBasis={100} flexShrink={0} flexGrow={0}>{bid.category}</Table.TextCell>
                  <Table.TextCell flexBasis={100} flexShrink={0} flexGrow={0}>{bid.month_year}</Table.TextCell>
                </Table.Row>
              ))}
            </Table.VirtualBody>
          </Table>
        </Pane>
        <Pane
          display="flex"
          alignItems="center"
          justifyContent="center"
        >
          <Heading is="h3" padding={50}>
            Código e dados abertos <a href="https://github.com/anapaulagomes/licitacoes-de-feira" target="_blank" rel="noopener noreferrer">aqui</a>. :)
          </Heading>
        </Pane>
      </div>
    );
  }
}


export default App;

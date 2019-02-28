import React, { Component } from 'react';
import { Icon, Heading, Pane, Paragraph, Table } from 'evergreen-ui';
import { filter } from 'fuzzaldrin-plus'

import bids from './bids.json'; // eslint-disable-line import/extensions

class App extends Component {
  constructor(props) {
    super(props)

    this.state = {
      searchQuery: '',
    }
  }

  handleFilterChange = value => {
    this.setState({ searchQuery: value })
  }

  filter = bids => {
    const searchQuery = this.state.searchQuery.trim()

    if (searchQuery.length === 0) return bids

    return bids.filter(bid => {
      const result = filter([bid.description], searchQuery)
      return result.length === 1
    })
  }

  render() {
    const items = this.filter(bids)

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
                Modalidade
            </Table.TextHeaderCell>
              <Table.TextHeaderCell flexBasis={100} flexShrink={0} flexGrow={0}>
                Categoria
            </Table.TextHeaderCell>
              <Table.TextHeaderCell flexBasis={100} flexShrink={0} flexGrow={0}>
                Mês/Ano
            </Table.TextHeaderCell>
            </Table.Head>
            <Table.VirtualBody height={600} >
              {items.map(bid => (
                <Table.Row key={bid.id} height="auto" paddingY={5}>
                  <Table.TextCell flexBasis={160} flexShrink={0} flexGrow={0}>{bid.when}</Table.TextCell>
                  <Table.Cell>
                    <Paragraph marginY={24}>
                      {bid.description}
                    </Paragraph>
                  </Table.Cell>
                  <Table.TextCell flexBasis={80} flexShrink={0} flexGrow={0}>
                    <a href={bid.url} target="_blank" rel="noopener noreferrer"><Icon icon="download" color="selected" marginRight={16} /></a>
                  </Table.TextCell>
                  <Table.TextCell flexBasis={260} flexShrink={0} flexGrow={0}>{bid.modality}</Table.TextCell>
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
            Código e dados abertos <a href="https://github.com/anapaulagomes/licitacoes-de-feira" target="_blank">aqui</a>. :)
          </Heading>
        </Pane>
      </div>
    );
  }
}


export default App;

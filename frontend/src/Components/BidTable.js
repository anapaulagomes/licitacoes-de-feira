import React from 'react';
import { Badge, Icon, Link, Pane, Paragraph, Strong, Table, Text } from 'evergreen-ui';
import allBids from '../bids.v5.json'; // eslint-disable-line import/extensions

const categoryColors = {
    "FHFS": {
        "label": "Fundação Hospitalar de Feira de Santana",
        "color": "orange"
    },
    "SMS": {
        "label": "Secretaria de Saúde",
        "color": "purple"
    },
    "PMFS": {
        "label": "Prefeitura",
        "color": "green"
    }
}

class BidTable extends React.Component {

    constructor(props) {
        super(props)

        this.state = {
            bids: allBids.sort((a, b) => (a.month > b.month) ? 1 : -1).sort((a, b) => (a.year < b.year) ? 1 : -1),
        }
    }

    renderHistoryItem(item) {
        return (
            <div>
                <Text color="muted">
                    {item.when} {item.event}
                    <Link href={item.url} target="_blank" rel="noopener noreferrer" alignItems="center">
                        <Icon icon="download" color="muted" marginLeft={5} />
                    </Link>
                </Text>
            </div>
        )
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

    renderHeader() {
        return (
            <Table.Head>
                <Table.TextHeaderCell width={80} flex="none">
                    Mês/Ano
            </Table.TextHeaderCell>
                <Table.SearchHeaderCell
                    placeholder="Filtrar por descrição ou número da licitação..."
                    onChange={this.handleFilterChange}
                    value={this.state.searchQuery}
                    autoFocus
                />
                <Table.TextHeaderCell width={200} flex="none">
                    Licitação/Modalidade
            </Table.TextHeaderCell>
            </Table.Head>
        )
    }

    renderRow = bid => {
        return (
            <Table.Row
                key={bid.id}
                height="auto"
            >
                <Table.Cell width={80} flex="none">
                    <Paragraph>{bid.month}/{bid.year}</Paragraph>
                </Table.Cell>
                <Table.Cell>
                    <Pane marginTop={10} marginBottom={10}>
                        <Paragraph>
                            {bid.description}
                        </Paragraph>
                        <Badge
                            isSolid
                            color={categoryColors[bid.category]["color"]}
                            marginRight={8}
                        >
                            {categoryColors[bid.category]["label"]}
                        </Badge>
                        <Link href={bid.document_url} target="_blank" rel="noopener noreferrer">
                            <Badge
                                marginRight={8}
                                color={bid.document_url === "" ? "red" : "blue"}
                            >
                                {bid.document_url === "" ? "Edital não encontrado" : "Edital disponível"}
                            </Badge>
                        </Link>
                        <Paragraph marginTop={15}>
                            <Strong>Histórico</Strong>
                            {bid.history.map(item => this.renderHistoryItem(item))}
                        </Paragraph>
                    </Pane>
                </Table.Cell>
                <Table.Cell width={200} flex="none">
                    <Paragraph>{bid.modality}</Paragraph>
                </Table.Cell>
            </Table.Row>
        )
    }

    render() {
        return (
            <Table flex={1} display="flex" flexDirection="column">
                {this.renderHeader()}
                <Table.VirtualBody
                    flex={1}
                    allowAutoHeight
                >
                    {this.state.bids.map(bid => this.renderRow(bid))}
                </Table.VirtualBody>
            </Table>
        );
    }
}

export default BidTable;
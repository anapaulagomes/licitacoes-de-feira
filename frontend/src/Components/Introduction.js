import React from 'react';
import { Link, Heading, Pane, Paragraph } from 'evergreen-ui';

class Introduction extends React.Component {
    render() {
        return (
            <Pane padding={50}>
                <Heading size={700}>Licitações de Feira de Santana 🏦</Heading>
                <Paragraph paddingTop={10}>
                    Encontre as <Link href="http://www.feiradesantana.ba.gov.br/servicos.asp?id=2&s=a&cat=PMFS&dt=01-2017&link=seadm/licitacoes.asp">licitações da  prefeitura de Feira de Santana </Link>
                    de maneira fácil e rápida.
        </Paragraph>
            </Pane>
        );
    }
}

export default Introduction;
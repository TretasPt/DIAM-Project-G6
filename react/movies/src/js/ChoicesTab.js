import TabHeader from './TabHeader';
import "../css/Tabs.css"
import { useEffect, useState } from 'react';
import axios from "axios"
import { BACKEND_PATH } from './constants'

function ChoicesTab({ tab, setTab, event, username }) {
    const tabName = "Escolhas";

    const [choiceList, setChoiceList] = useState([])

    const getChoiceList = () => {
        axios.post(BACKEND_PATH + "escolhas/", { username: username, token: localStorage.getItem("token"), evento: event })
            .then((r) => { setChoiceList(r.data) })
            .catch((e) => { console.log(e) })
    }



    function Choice({ pk, sessao, filme, votos }) {
        const onClickRemove = () => {
            axios.delete(BACKEND_PATH + "voto/", { data: { username: username, token: localStorage.getItem("token"), voto: pk } })
                .then(() => { getChoiceList() })
                .catch((e) => { console.log(e); getChoiceList() });
            getChoiceList();

        }
        const onClickAdd = () => {
            axios.post(BACKEND_PATH + "voto/", { username: username, token: localStorage.getItem("token"), voto: pk })
                .then(() => { getChoiceList() })
                .catch((e) => { console.log(e); getChoiceList() });
            ;

        }
        const duracao = Math.floor(filme.duracao / 3600) + "h:" + Math.floor((filme.duracao % 3600) / 60) + "m"
        return (
            <div className='TabElement'>
                {votos.user_voted && <>
                    <input type='checkbox' disabled checked />
                    <button onClick={onClickRemove}>Remover voto</button>
                </>
                }
                {!votos.user_voted && <>
                    <input type='checkbox' disabled />
                    <button onClick={onClickAdd}>Votar</button>
                </>
                }
                <strong>Votos: </strong>{votos.count}
                <strong>Filme: </strong>{filme.nome}
                <img src={filme.imagem} alt="Sem imagem" />
                <strong>Sessão: </strong>{sessao}
                <strong>Género: </strong>{filme.genre}
                <strong>Saga: </strong>{filme.saga}
                <strong>Duração: </strong>{duracao}
                <strong>Publicado: </strong>{filme.data_publicacao}
            </div>
        )
    }

    useEffect(() => {
        if (event !== -1) {
            getChoiceList()
        }
    },
        // eslint-disable-next-line react-hooks/exhaustive-deps
        [event, tab])

    return (
        <div>
            {tab === tabName &&

                <TabHeader tabname={tabName} extraText={""} setTab={setTab} />
            }            {
                tab === tabName &&
                <div className='TabBodyDiv TabLast'>
                    {choiceList.length === 0 && <h4>Não existem escolhas.</h4>}
                    {choiceList.map((choice) => (<Choice sessao={choice.sessao} pk={choice.pk} key={choice.pk} filme={choice.filme} votos={choice.votos} />))}
                </div>
            }
        </div>
    )
}

export default ChoicesTab
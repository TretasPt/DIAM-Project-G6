import TabHeader from './TabHeader';
import "../css/Tabs.css"
import { useEffect, useState } from 'react';
import axios from "axios"
import { BACKEND_PATH, IMAGES_PATH } from './constants'


function GroupTab({ tab, setTab, username, setGroup }) {
    const tabName = "Grupos";

    const [groupList, setGroupList] = useState([])


    function Group({ data_criacao, imagem, nome, pk }) {
        const onClick = () => {
            setTab("Eventos");
            setGroup(pk)
        }
        return (
            <div className='TabElement'>
                <strong>Nome: </strong>{nome}
                <img src={IMAGES_PATH + imagem} alt='Sem imagem' />
                <strong>Criado: </strong>{data_criacao}
                <button onClick={onClick}>Selecionar</button>
            </div>
        )
    }

    useEffect(() => {
        axios.post(BACKEND_PATH + "grupos/", { username: username, token: localStorage.getItem("token") })
            .then((r) => { setGroupList(r.data) })
            .catch((e) => { console.log(e) })
    }, [username, tab])

    return (
        <div>
            <TabHeader tabname={tabName} extraText={""} setTab={setTab} />
            {
                tab === tabName &&
                <div className='TabBodyDiv'>
                    {groupList.length === 0 && <h4>Não existem grupos.</h4>}
                    {groupList.map((group) => (<Group data_criacao={group.data_criacao} imagem={group.imagem} nome={group.nome} pk={group.pk} key={group.pk} />))}
                </div>
            }

        </div>
    )
}



export default GroupTab
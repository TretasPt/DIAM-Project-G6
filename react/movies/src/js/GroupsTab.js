import TabHeader from './TabHeader';
import "../css/Tabs.css"
import { useEffect, useState } from 'react';
import axios from "axios"
import { BACKEND_PATH } from './constants'


function GroupTab({ tab, setTab, username, setGroup }) {
    const tabName = "Grupos";

    const [groupList, setGroupList] = useState([])

    const getGroupList = () => {
        axios.post(BACKEND_PATH + "grupos/", { username: username, token: localStorage.getItem("token") })
            .then((r) => { setGroupList(r.data) })
            .catch((e) => { console.log(e) })
    }

    function Group({ data_criacao, imagem, nome, pk }) {
        const onClick = () => {
            setTab("Eventos");
            setGroup(pk)
        }
        return (
            <div>
                <h5>Nome: {nome}</h5>
                <h5>Criado: {data_criacao}</h5>
                <img src={imagem} alt='Sem imagem' width={"80%"}  />
                <button onClick={onClick}>Selecionar</button>
            </div>
        )
    }

    useEffect(() => { getGroupList() }, [username,tab])

    return (
        <div className='TabElement'>
            <TabHeader tabname={tabName} extraText={""} setTab={setTab} />
            {
                tab == tabName &&
                <div className='TabBodyDiv'>

                    {groupList.map((group) => (<Group data_criacao={group.data_criacao} imagem={group.imagem} nome={group.nome} pk={group.pk} key={group.pk} />))}
                    {/* {groupList} */}
                </div>
            }

        </div>
    )
}



export default GroupTab